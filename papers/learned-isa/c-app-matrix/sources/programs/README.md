# Freestanding C application suite

Four deterministic workloads increase from a 14-byte greeting to a small text-record aggregator. Compile each with the harness's identical ordinary static Linux x86-64 C flags. They require no libc, file input, environment variables, clock, randomness, allocation, or startup library.

| ID | Source | Work |
|---|---|---|
| tiny | `tiny_hello.c` | The existing known Hello program, preserved exactly |
| small | `small_checksum.c` | 24 C arithmetic updates of four volatile 64-bit cells |
| medium | `medium_sort.c` | Sort 32 unsigned values, then compute an order-sensitive digest |
| large | `large_records.c` | Parse 80 built-in CSV records, aggregate eight name buckets, digest totals |

“Large” is relative to this bounded suite. It does not mean a full desktop application. The intended native dynamic-instruction ceiling is approximately 50,000; that is a workload-design target, not a measured instruction count. The run harness must retain its instruction/time limit and report unsupported instructions or incomplete runs honestly. Normal compiler choices, including instructions some learned runtimes do not support, are retained.

The computational bodies are actual C. Inline assembly is limited to the supplied Linux `write` and `exit` syscall boundary. The tiny source preserves its original two inline syscalls; the other sources share `linux_syscalls.h`. This is a minimal OS contract, not full libc or Linux compatibility. The shared wrapper writes one 8-byte little-endian result and exits 0 after a complete write (1 after a short/failed write). Tiny writes `Hello, world!\n` and exits 0 as in the known source.

Volatile inputs prevent constant-only elimination. Small has a fixed straight-line 24-update body; medium and large contain loops and conditionals. They are not assembly instruction streams rendered through C. Unsigned arithmetic has defined modulo behavior. The large parser assumes its valid built-in fixture; it does not claim general malformed-CSV handling.

`reference.py` computes expected observables without compiling/running C or consulting any model. It uses Python arbitrary-precision integer arithmetic modulo 2^64, Python sorting, and Python splitting/integer parsing. Its name-bucket reference uses the independent identity `33 == 1 (mod 8)`, reducing the C recurrence to a byte sum. `manifest.json` freezes expected stdout bytes, exit codes, input descriptions, reference details, and source hashes. Native execution of the identical compiled ELF remains a separate required comparison; expected output alone cannot establish all intermediate architectural state.

Run the reference only with:

```sh
rtk proxy python3 reference.py
```

The deterministic digest is the integer-value recurrence `h = ((h xor value) * 1099511628211) mod 2^64` starting at 1469598103934665603. It is used as an order-sensitive observable, not described as a standard byte-oriented FNV hash. The sorted values or per-bucket totals are retained in the manifest to make the expected digest inspectable.
