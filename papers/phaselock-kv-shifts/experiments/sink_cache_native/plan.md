# Native SinkCache rerotation comparison

## Question

Does the public `transformers-community/sink_cache` BF16 shift path exhibit the
repeated-rerotation degradation identified in the PhaseLock paper, and does a
small FP32, unit-length rerotation fix remove that degradation in the native
Hugging Face model consumer?

## Fixed inputs and arms

- Upstream source: `transformers-community/sink_cache` commit
  `ea681c770c26d245c37d49c6760eeaa07f4fc1ce`.
- Model: Qwen2.5-1.5B-Instruct snapshot
  `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, BF16 on beast CUDA,
  eager attention, frozen weights.
- Data: WikiText-2 raw train split, one fixed token stream and tokenizer.
- Cache: four sink tokens, one-token shifts, 256-token smoke followed by the
  paper's 1024-token window, 20,000-token comparison.
- `baseline`: upstream `SinkCache` exactly as pulled.
- `patched`: the same code with FP32 coefficient and key arithmetic plus
  normalization of derived shift coefficients before repeated use.
- Both caches run interleaved against one loaded native `AutoModelForCausalLM`
  through `model.forward`, with explicit bounded local `position_ids` and
  `cache_position`. The only intended code difference is the rerotation
  arithmetic. This is the same position contract as the paper and is not an
  unmodified `model.generate()` call.

The model-forward pairing avoids a manual transformer reimplementation. It
also allows an exact pre-shift equality check, since neither patch branch
runs before the cache fills. The experiment counts actual rerotation calls
and records the dtype and norm of the coefficients at the first shift.

## Measurements and interpretation

- Per-arm teacher-forced next-token NLL and perplexity, overall and after the
  window fills, with a time series of intermediate checkpoints.
- Pre-shift maximum logit difference (mechanics check; must be zero).
- Paired top-one agreement and current maximum logit difference.
- Actual rerotation-call count and coefficient norm range (instrument check).

The working prediction was that the upstream BF16 path would accumulate a
large quality loss while the patched path stayed near the paper's FP32
arithmetic control. The 2,600-token mechanics smoke instead found nearly
equal perplexity. The full 20,000-token comparison is retained even if the
effect is small or opposite. The paper's 253.918 and 8.606 came from a
different, manual consumer with a constant rounded one-step twiddle; this
repository derives a position-dependent twiddle from a BF16 RoPE table.

An isolated 64-vector key trajectory compares upstream BF16 arithmetic,
FP32 arithmetic alone, and FP32 plus unit-length normalization against a
direct, untouched-key RoPE reference after 124, 508, and 1,022 shifts.
This separates numerical key fidelity from downstream next-token quality.

## Absolute-position generation follow-up

The wrapper's `model.generate()` path in Transformers 4.52.1 advances
`cache_position` monotonically. Those absolute RoPE phases mean retained keys
should keep their original phase; rerotating them into local slots is a
coordinate mismatch. A separate paired native run uses original absolute
`position_ids` and `cache_position` after prefill. Its baseline is the exact
upstream source. Its patched arm skips retained-key rerotation for absolute
positions, while keeping the normalized FP32 rerotation for explicit bounded
local streams. It measures whether correcting the actual generation position
contract improves next-token quality. The experiment also tests a capacity
boundary correction: appending a token that exactly fills the window does not
evict one early.

The initial paired test specifies the local positions required by the paper;
the absolute-position follow-up tests the wrapper's position contract.
On the beast's installed
Transformers 5.13.1, the class no longer constructs because the base `Cache`
initialization API changed, and Qwen2/Qwen3 attention no longer passes sine
and cosine values to `Cache.update`. Therefore the native numerical test pins
Transformers 4.52.1, where the model passes those values. Compatibility with
current Transformers requires separate work and must not be inferred from this
comparison.
