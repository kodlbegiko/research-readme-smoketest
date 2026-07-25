# Figure sources

All figures are deterministic SVG files generated from CSV source data with the Python standard library.

```bash
python docs/manuscript/figures/generate_figures.py
python docs/manuscript/figures/generate_figures.py --check
```

Files:

- `static-confusion-matrix.csv` and `static-confusion-matrix.svg` - 7/0/17/14 confusion matrix.
- `static-metrics.csv` - precision, recall, specificity, accuracy, F1, and the failed 0.750 accuracy gate.
- `dynamic-outcomes.csv` and `dynamic-outcomes.svg` - final adjudicated outcomes for ten locked cases.

These figures summarize published results. They do not alter or regenerate frozen evidence files.
