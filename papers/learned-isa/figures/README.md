# Selector performance figure

[selector-performance.svg](selector-performance.svg) compares the successful 1,024-instruction counter runs from the six-model selector study. The PNG contains the same figure. Points are medians and horizontal lines show observed minimum and maximum times, rather than confidence intervals. The caption states the different native-process and warm-model timing boundaries.

[selector-performance-data.json](selector-performance-data.json) preserves the exact timing values, trial counts, source field names, run identities, and SHA-256 of `isa/outputs/ssm-native-report/report.json`. The figure does not measure the later direct-effect networks.

To render from the checked-in data, with Matplotlib installed:

```bash
python3 render.py
```

To extract the data again from a copy of the original report and then render:

```bash
python3 render.py --report path/to/ssm-native-report.json
```

The script reads reports and draws the figure. It performs no model execution.
