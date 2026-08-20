# Source-address roadmap development matrix

This bounded roadmap run is complete. It is development evidence, not a terminal claim.

## Largest findings

- Pythia step512 learned source addressing: 75.0%.
- Frozen-consumer recovery: 2.3% native -> 46.1% learned (60.9% oracle).
- Fresh alphabet retained 53.1% addressing, but even oracle payload execution reached only 9.4%; payload localization, not addressing, is now the bottleneck.
- Step1000 frozen/lowered: 52.3% -> 80.5%.
- Step4000 frozen/lowered: 35.9% -> 78.1%.
- Qwen2 fresh-template native semantic addressing: 100.0%; learned selective precision 76.9% at 50.8% coverage.
- Qwen3 fresh-template native semantic addressing: 100.0%; learned selective precision 82.1% at 52.3% coverage.

## Interpretation

The source address is a distinct, learnable and often already geometrically explicit plane. It transfers partially across checkpoints and can be restored with small recipient-local feedback. The payload is a separate plane: the fresh-alphabet miss survives even with oracle addresses, localizing the failure to payload expression/consumer compatibility. Across Qwen2 and Qwen3, the same abstract key-to-value source role compiles successfully into different native widths and layers; direct artifact reuse is deliberately rejected.

## Claim boundary

Development evidence for learned and native semantic source addressing, sealed replay, checkpoint lowering, and Qwen2/Qwen3 family-local compilation. It does not certify a universal payload, multi-token span routing, a third family, or autonomous multi-token continuation.
