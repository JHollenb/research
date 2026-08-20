# Twenty-axis semantic route circuit: evidence bundle

This bundle contains the complete twenty-row circuit ledger, an independent recheck, a proof sheet, four representative axis montages, and a promptless sensitivity control. Each semantic row uses source/target/typed-transfer/route-ablation evidence; the ledger is the authority for the row-level evidence class and gate counts.

The promptless control is included to separate route activity from semantic labeling: it uses an empty-string conditioner, fixed-norm perturbations, and no semantic target. Its report is a structural sensitivity control, not an additional semantic certificate.

Run `python verify.py` from this directory. The check verifies the complete ledger counts, representative certified rows, and promptless execution metadata.
