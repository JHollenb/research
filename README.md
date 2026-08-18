# Research

Public-facing research demos and evidence-backed experiment reports.

# Black Forest Labs

This section documents a systematic study of Black Forest Labs image generators. The work combines model forensics, controlled behavior measurements, causal route interventions, trajectory editing, component substitution, and exact replay. The goal is to understand what information the models use, where that information enters the generation process, which interventions reach the final image, and which proposed explanations fail under stronger controls.

The experiments move from broad observation to increasingly specific tests. We first characterize counting, typography, context scaffolds, model lineage, and decoder boundaries. We then map distributed routes and time-dependent carrier behavior with native targets, wrong-site controls, shams, dose sweeps, and held-out prompts. Finally, we test practical operations such as capability patches, counterfactual image edits, foreign conditioner interfaces, structured frontends, fast exact serving, and small trajectory-following students.

The resulting reports are designed to be readable on their own and to preserve both positive and negative evidence. Strong visual results are treated as hypotheses until they survive native-consumer evaluation, independent controls, exact replay, and explicit collateral or generalization tests.

See the [Black Forest Labs experiment index](bfl/index.md) for the high-level catalog and the [standalone reports](bfl/demos/) for detailed methods and proof artifacts.
