# Recipient-native capability patch: evidence bundle

This bundle contains the machine-readable gap diagnosis, the selected recipient-local patch package, pixel outputs for the target and controls, and the later held-out gate report.

The primary proof is a matched FLUX.2 Klein 4B base/distilled comparison followed by a frozen recipient-only intervention. The raw reports record the model revision, package hash, parameter count, route/time contract, dose search, independent image evaluators, fresh-process serving, and uninstall parity. `generalization-gate-results.md` is retained as a boundary artifact: the patch transfers beyond the discovery panel, but its collateral detector fails the shipping gate.

Run `python verify.py` from this directory. The check is deliberately limited to facts present in the copied receipts and does not regenerate images.

## Files

- `gap-report.json`, `gap-receipt.json`: eight-pair base-versus-distilled counting diagnosis.
- `patch-report.json`, `patch-receipt.json`: selected dose, Act contract, evaluator results, rollback ledger, and fresh-process result.
- `act-package.npz`: the 104,044-byte FP16 rank-8 package named by the receipt.
- `target-native.png`, `target-act.png`, `target-wrong-time.png`, `target-zero-dose.png`: target and controls.
- `preserved-native.png`, `preserved-with-target-act.png`: preservation control.
- `fresh-donor-free.png`: fresh process with the donor path unavailable.
- `wrong-source-native.png`, `wrong-source-with-target-act.png`: wrong-source control.
- `dose-2-grid.png`: visual dose-search evidence.
- `generalization-gate-results.md`: later paraphrase/resolution/object-family and collateral-gate report.
