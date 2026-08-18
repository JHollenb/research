# Cross-family conditioner substitution and repair: evidence bundle

This bundle contains the native and adapted FLUX.2 conditioner receipts, the scheduler-closed
repair report and images, and a separate held-out function-recovery panel for SmolLM2 and Mamba.

The evidence is intentionally split into three claims: exact suffix closure after supplying the
native conditioning tensor; a learned foreign-to-native adapter that reaches the expected tensor
shape but only partial image fidelity; and a consumer-closed repair that improves seen prompts
strongly while improving the held-out corgi prompt only modestly. The held-out report tests whether
complete late native-state replacement can rescue foreign conditioning, independent of the learned
adapter's address-selection problem.

Run `python verify.py` from this directory. The checks are bounded to the copied reports and do not
promote the result to universal cross-family semantic interchange.
