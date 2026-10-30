# Learned ISA architectures and executable programs

This research line compares several ways to execute a bounded x86 profile, then asks whether their learned computations can be inspected, edited and compiled. Its central distinction is **selecting a supplied operation versus computing architectural effects**. The later experiments learn register/flag effects, induce small automata and microcode, and test source-qualified programs through their unchanged learned consumers.

[Read the paper](paper.md) for the architecture, mathematics, experiments, failures and evidence boundaries through **October 30, 2026**. The [early PAN-ISA companion](../pan-isa/README.md) explains the preceding typed architectural executor.

Jump to the [Mamba and Hydra equations](paper.md#mamba-and-hydra-equations), [size and native hardware performance](paper.md#size-and-performance-against-native-hardware), [direct-effect learners](paper.md#direct-prediction-of-architectural-effects), [SPF automata and FieldLM programs](paper.md#address-composition-and-explicit-automata), or [recipient-local editing](paper.md#recipient-local-nn-symbols-and-their-limits).

The strongest current observations are:

- Six matched selector adapters expose a large gap between isolated accuracy and complete-program reliability; all arithmetic remains supplied in this cohort.
- Direct-effect NN, Mamba and Hydra models execute dependent counters and stdout programs, while unseen form/register combinations and long mixed programs remain harder.
- An induced SPF bit automaton and FieldLM microcode achieve stronger composition with an explicitly richer supplied structural vocabulary.
- A frozen Mamba yields both a full parameter program and a small native-response Boolean program, with different guarantees and retained exceptions.
- Recipient-only NN edits survive subsequent native computations. The October 30 constructor generates compatible value and context from recipient state and frozen weights on eight fresh experiment envelopes; it still recomputes a substantial native prefix.

The [evidence guide](evidence/README.md) maps the paper's tables to small local snapshots. [Provenance](evidence/provenance.json) records original paths, byte hashes and modification times. [Source snapshots](sources/README.md) make the architecture and induction rules inspectable without sibling repositories. Checkpoints, full trace stores and large archives are deliberately excluded; this is a self-contained research account and reading bundle, not a complete executable environment or independent rerun.
