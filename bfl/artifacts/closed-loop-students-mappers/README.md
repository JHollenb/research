# Closed-loop students and mappers: evidence bundle

This bundle preserves the mapper-complete and full-trajectory reports and execution receipts, plus the bounded performance reference used for the standalone report. The raw files distinguish teacher-forced, uncertainty-gated, dense, free-rollout, and prompt-disjoint measurements.

The verifier checks the declared parameter count, scheduler parity, rollout quality, trajectory cut trend, and measured performance range. It does not convert the bounded student into a universal native replacement.

Run `python verify.py` from this directory.
