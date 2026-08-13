# Analysis Pipeline

## Overview

The pipeline analyses 25.3 years of CODE precise clock products (2000-2025)
to detect distance-structured correlations, anisotropy, orbital velocity
coupling, CMB frame alignment, planetary event responses, and geophysical
couplings in GNSS timing data.

## Prerequisites

```bash
pip install -r requirements.txt
```

Key dependencies: numpy, scipy, pandas, matplotlib, astropy, ephem,
pyproj, statsmodels, scikit-learn, cartopy, h5py, pyarrow.

## Running the Pipeline

### Full pipeline (Steps 1.1 -> 2.2)

```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-GNSS-II"
python scripts/steps/code_longspan_steps_1_1_to_2_2.py \
    --namespace code_longspan_2000_2025 \
    --date-start 2000-03-01 \
    --date-end 2025-06-30
```

### Individual steps

All steps write outputs to `results/outputs/` and logs to `logs/`.

| Step | Script | Output |
|------|--------|--------|
| 1.1 | `step_1_1_code_longspan.py` | Data loading and preprocessing |
| 1.2 | `step_1_2_code_longspan.py` | Coordinate validation |
| 2.0 | `step_2_0_code_longspan.py` | Correlation analysis (model comparison) |
| 2.1 | `step_2_1_code_longspan.py` | Geospatial processing |
| 2.2 | `step_2_2_code_longspan.py` | Geospatial-temporal analysis (main results) |
| 2.3 | `step_2_3_code_longspan.py` | Physical interpretation |
| 2.4 | `step_2_4_code_longspan.py` | Supplementary analysis |
| 2.5 | `step_2_5_dual_motion_geometry.py` | CMB frame / dual-motion geometry |
| 2.6 | `step_2_6_null_control.py` | Null control validation |
| 2.8 | `step_2_8_draconitic_falsification.py` | Draconitic falsification test |

### Supporting scripts

- `compute_planetary_events.py` — JPL-based planetary alignment events
- `plot_step_2_2_longspan_timeseries.py` — Timeseries figure generation
- `analyze_checkpoint.py` — Checkpoint analysis for long-running steps
- `check_residual_precision.py` — Residual precision diagnostics

## Outputs

- `results/outputs/` — JSON analysis results (all manuscript numbers trace here)
- `results/figures/` — Generated plots (PNG)
- `logs/` — Execution logs

## Data Provenance

All manuscript numbers must trace to real outputs in `results/` — no
fabricated data. The canonical results are committed at the version
corresponding to the published manuscript.
