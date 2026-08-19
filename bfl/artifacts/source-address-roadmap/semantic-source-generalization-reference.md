# Semantic source addressing across Qwen families

This experiment asks whether the source-address role survives natural-language
wrappers and family-local lowering. Prompts contain six natural-language
key/value facts followed by a query. Discovery uses `Mappings/Query`, heldout
uses unseen `Dictionary/Lookup`, and sealed fresh trials use `Glossary/Find`.

The frozen model is the microscope specimen. Only a small Saturn address policy
is optimized on cached internal states. The address key for each value row is
the native key state two token positions earlier (`key = value`); no oracle
address is available at serving time.

## Results

| Model | Boundary | Heldout native cosine | Fresh native cosine | Fresh learned selective result |
|---|---:|---:|---:|---:|
| Qwen2.5-0.5B | layer 12 / width 896 | 127/128 | 128/128 | 76.9% precision at 50.8% coverage |
| Qwen3-0.6B | layer 14 / width 1024 | 128/128 | 128/128 | 82.1% precision at 52.3% coverage |

Fixed-position retrieval reached 27/128 on fresh prompts and random retrieval
4/128. The striking result is that the semantic address circuit is already
nearly explicit in the native middle-layer geometry before policy training.
The learned policy adds a conservative, packageable abstention surface.

The same abstract source role was compiled separately into each family. Direct
Qwen2-to-Qwen3 and Qwen3-to-Qwen2 package application was rejected by the typed
model/tokenizer/width/layer ABI. Cross-family generalization here means semantic
recompilation, not pretending hidden tensors are interchangeable.

The next interface rung also admits a real autoregressive SmolLM2-360M
backend. Its family-local layer-16/width-960 address object is joined with the
Qwen2 and Qwen3 objects by a typed cross-family capability record. All three
fresh processes now include repeat-exact 32-token native
continuation. None consumes the selected address through a payload, so payload
transfer remains explicitly open.

`analyze.py` verifies every report hash, package replay, and wrong-family
rejection, then emits the combined development matrix under
`results/source-address-roadmap-matrix/`.

This closes the short, one-token natural-language rung. Contradictions,
unanswerable inputs, multi-token spans, autonomous continuations, non-Qwen
families, and multi-seed terminal confirmation remain open.
