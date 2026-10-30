# Source snapshots

These small snapshots expose the implementation behind the paper's architecture and induction claims. They preserve their original imports and are intended for reading; executing the original experiments requires the original runtime, dependencies, checkpoints, suites and sealed payloads. No checkpoint or complete runtime is included here.

| Snapshot | What to inspect |
|---|---|
| [starter_nn.py](starter_nn.py) | Two-byte embedding, before-state features, candidate labels, discovery-loss signal |
| [selector_nn.py](selector_nn.py) | Separate staged and runtime NN heads in the PAN-native comparison |
| [selector_fieldlm.py](selector_fieldlm.py) | FieldFabric records and exact route reads |
| [selector_spf.py](selector_spf.py) | Packed phase-code records and native exact-match selection |
| [ssm.py](ssm.py) | Associative selective scan; Mamba causal convolution; Hydra shifted directional scans and diagonal |
| [direct_effect_model.py](direct_effect_model.py) | Bit-sliced Executor, copy prior, aligned/raw reads, pointers, masked key, output heads and latent variant |
| [spf_datapath.py](spf_datapath.py) | Mealy-table induction, state gauge, SPF monomial execution and flag-tap vocabulary |
| [fieldlm_microcode.py](fieldlm_microcode.py) | Structural role vocabulary, field masks, code-map induction, effect fitting and fabric serving |
| [response_route.py](response_route.py) | Uniquely supported copy/invert/constant route rules, scope checks and abstention |
| [symbol_value_edit.py](symbol_value_edit.py) | Recipient-bound sign-reflection construction and typed edit binding |

The [provenance manifest](../evidence/provenance.json) records workspace-relative original paths, original SHA-256, snapshot SHA-256 and any transformation. Import paths and names describe the original source tree. They are evidence of implementation identity, not installed capabilities of this reading repository.
