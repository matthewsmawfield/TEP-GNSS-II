#!/usr/bin/env python3
"""
Step 2.10: Velocity-Tracking vs Calendar-Phase Discriminator
============================================================

PURPOSE: Formal model comparison between a velocity-tracking template
(A(t) ∝ |v_orb(t)|, waveform fixed by Keplerian mechanics) and a
calendar/seasonal sinusoid (A(t) ∝ sin(2πt/yr + φ)), on the identical
34-bin GLOBAL EW/NS seasonal series from Step 2.2.

MOTIVATION:
The annual modulation of the EW/NS anisotropy ratio correlates with
orbital speed at r = -0.888. A generic annual systematic (seasonal or
calendar-locked) produces a pure sinusoid in DOY; a velocity-tracking
channel produces the |v_orb(t)| waveform, which differs by the Keplerian
eccentric-orbit asymmetry (~3.4% perihelion-aphelion speed contrast and
non-sinusoidal time-weighting through Kepler's equation). This step
reports R², adjusted R², AIC/BIC, held-out prediction error, nested
incremental F-tests, and a permutation calibration of the preference.

MODELS (all linear OLS on the GLOBAL series):
  M_v      : y = a + b·v(t)                          (2 params; TEP velocity channel)
  M_v2     : y = a + b·v²(t)                         (2 params; kinetic proxy)
  M_sin    : y = a + A sin ωt + B cos ωt             (3 params; calendar annual)
  M_sin2   : M_sin + C sin 2ωt + D cos 2ωt           (5 params; seasonal baseline)
  M_v_sin2 : y = a + b·v + C sin 2ωt + D cos 2ωt     (4 params; hybrid)

DISCRIMINATING TESTS:
  - AIC/BIC and adjusted R² between M_v and M_sin on identical data.
  - Nested F-tests: v added to the annual basis, and the annual basis
    added to v (each adds 1 dof to the other's span).
  - Keplerian asymmetry probe: regression of the data residual after
    M_sin onto the non-sinusoidal component of v(t).
  - 5-fold contiguous-block held-out prediction error.
  - Circular-phase permutation calibration of ΔAIC(M_sin − M_v).

Author: TEP-GNSS Analysis Pipeline
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "outputs" / "code_longspan"
OUTPUT_FILE = RESULTS_DIR / "step_2_10_velocity_calendar_discriminator.json"

SOLAR_YEAR_DAYS = 365.25
N_PERM = 20000
RNG_SEED = 20261001


def print_status(msg, status="INFO"):
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "WORKING": "🔄"}
    print(f"{symbols.get(status, '•')} {msg}")


def design_matrix(t, v, model):
    """Return (X, k) for each model. t in days of year, v in km/s."""
    w = 2 * np.pi / SOLAR_YEAR_DAYS
    cols = [np.ones_like(t)]
    if model == "M_v":
        cols += [v]
    elif model == "M_v2":
        cols += [v ** 2]
    elif model == "M_sin":
        cols += [np.sin(w * t), np.cos(w * t)]
    elif model == "M_sin2":
        cols += [np.sin(w * t), np.cos(w * t), np.sin(2 * w * t), np.cos(2 * w * t)]
    elif model == "M_v_sin2":
        cols += [v, np.sin(2 * w * t), np.cos(2 * w * t)]
    else:
        raise ValueError(model)
    return np.column_stack(cols)


def ols(X, y, w=None):
    """OLS (optionally weighted). Returns dict with fit statistics."""
    n, k = X.shape
    if w is not None:
        sw = np.sqrt(w)
        Xw, yw = X * sw[:, None], y * sw
    else:
        Xw, yw = X, y
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    resid = y - X @ beta
    rss = float(np.sum((resid if w is None else resid * np.sqrt(w)) ** 2))
    tss = float(np.sum(((y if w is None else (y - np.average(y, weights=w)) * np.sqrt(w))) ** 2)) \
        if w is not None else float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - rss / tss if tss > 0 else np.nan
    adj_r2 = 1 - (1 - r2) * (n - 1) / max(n - k - 1, 1)
    sigma2 = rss / n
    aic = n * np.log(max(sigma2, 1e-30)) + 2 * k
    bic = n * np.log(max(sigma2, 1e-30)) + k * np.log(n)
    dw = float(np.sum(np.diff(resid) ** 2) / rss) if rss > 0 else np.nan
    return {"beta": beta, "resid": resid, "rss": rss, "r2": r2,
            "adj_r2": adj_r2, "aic": aic, "bic": bic, "k": k, "n": n,
            "durbin_watson": dw}


def block_cv_rmse(t, v, y, model, n_folds=5):
    """Held-out prediction error on contiguous blocks (time-series honest CV)."""
    n = len(y)
    idx = np.arange(n)
    folds = np.array_split(idx, n_folds)
    sq = []
    for te in folds:
        tr = np.setdiff1d(idx, te)
        X_tr = design_matrix(t[tr], v[tr], model)
        X_te = design_matrix(t[te], v[te], model)
        beta, *_ = np.linalg.lstsq(X_tr, y[tr], rcond=None)
        sq.append(np.sum((y[te] - X_te @ beta) ** 2))
    return float(np.sqrt(np.sum(sq) / n))


def nested_f_test(y, X_small, X_full):
    """F-test for the extra columns in X_full given X_small."""
    f_small = ols(X_small, y)
    f_full = ols(X_full, y)
    df1 = X_full.shape[1] - X_small.shape[1]
    df2 = len(y) - X_full.shape[1]
    if df1 <= 0 or df2 <= 0 or f_small["rss"] <= f_full["rss"]:
        return {"F": np.nan, "df1": df1, "df2": df2, "p": np.nan}
    F = ((f_small["rss"] - f_full["rss"]) / df1) / (f_full["rss"] / df2)
    from scipy.stats import f as fdist
    return {"F": float(F), "df1": df1, "df2": df2, "p": float(1 - fdist.cdf(F, df1, df2))}


def run_bucket(rows, label, rng):
    t = np.array([r["day_of_year"] for r in rows], dtype=float)
    v = np.array([r["orbital_speed_kms"] for r in rows], dtype=float)
    y = np.array([r["ew_ns_ratio"] for r in rows], dtype=float)
    w = 2 * np.pi / SOLAR_YEAR_DAYS

    models = ["M_v", "M_v2", "M_sin", "M_sin2", "M_v_sin2"]
    fits = {m: ols(design_matrix(t, v, m), y) for m in models}
    cv = {m: block_cv_rmse(t, v, y, m) for m in models}

    # Nested discriminations (each alternative adds exactly 1 dof)
    # [1, sin, cos] + v vs [1, sin, cos]
    X_sin = design_matrix(t, v, "M_sin")
    X_sin_plus_v = np.column_stack([X_sin, v])
    f_v_given_sin = nested_f_test(y, X_sin, X_sin_plus_v)
    # [1, v] + [sin, cos] vs [1, v]  -> adds 1 dof beyond v's span
    X_v = design_matrix(t, v, "M_v")
    X_v_plus_sin = np.column_stack([X_v, np.sin(w * t), np.cos(w * t)])
    f_sin_given_v = nested_f_test(y, X_v, X_v_plus_sin)

    # Keplerian asymmetry probe: non-sinusoidal component of v(t)
    v_resid = v - X_sin @ np.linalg.lstsq(X_sin, v, rcond=None)[0]
    non_sin_frac = float(np.sum(v_resid ** 2) / np.sum((v - v.mean()) ** 2))
    resid_sin = fits["M_sin"]["resid"]
    if np.sum(v_resid ** 2) > 0:
        c = float(np.sum(resid_sin * v_resid) / np.sum(v_resid ** 2))
        sigma = np.sqrt(fits["M_sin"]["rss"] / (len(y) - 3) / np.sum(v_resid ** 2))
        t_asym = c / sigma
    else:
        c, t_asym = np.nan, np.nan

    # Permutation calibration: circular phase-shift of y destroys v-alignment
    # but preserves autocorrelation; record ΔAIC(M_sin - M_v) distribution.
    daic_obs = fits["M_sin"]["aic"] - fits["M_v"]["aic"]
    perm_daic = np.empty(N_PERM)
    ypad = np.concatenate([y, y, y])
    n = len(y)
    for i in range(N_PERM):
        s = rng.integers(0, n)
        yp = ypad[s:s + n]
        fv = ols(design_matrix(t, v, "M_v"), yp)
        fs = ols(design_matrix(t, v, "M_sin"), yp)
        perm_daic[i] = fs["aic"] - fv["aic"]
    perm_p = float((np.sum(perm_daic >= daic_obs) + 1) / (N_PERM + 1))

    # Waveform asymmetry of the data itself: skewness proxy vs model predictions
    y_skew = float(np.mean(((y - y.mean()) / y.std()) ** 3))
    v_pred_skew = float(np.mean(((fits["M_v"]["beta"][0] + fits["M_v"]["beta"][1] * v
                                  - y.mean()) / y.std()) ** 3))
    sin_pred = X_sin @ fits["M_sin"]["beta"]
    sin_pred_skew = float(np.mean(((sin_pred - y.mean()) / y.std()) ** 3))

    return {
        "label": label,
        "n_bins": int(len(y)),
        "fits": {m: {kk: (float(vv) if np.isfinite(vv) else None)
                     for kk, vv in
                     [("r2", f["r2"]), ("adj_r2", f["adj_r2"]), ("aic", f["aic"]),
                      ("bic", f["bic"]), ("rss", f["rss"]),
                      ("durbin_watson", f["durbin_watson"])]}
                 for m, f in fits.items()},
        "cv_rmse_contiguous_5fold": cv,
        "delta_aic_sin_minus_v": float(daic_obs),
        "delta_bic_sin_minus_v": float(fits["M_sin"]["bic"] - fits["M_v"]["bic"]),
        "nested_f_tests": {
            "v_given_annual_basis": f_v_given_sin,
            "annual_basis_given_v": f_sin_given_v,
        },
        "keplerian_asymmetry_probe": {
            "v_non_sinusoidal_variance_fraction": non_sin_frac,
            "data_projection_coef": c,
            "t_statistic": t_asym,
        },
        "permutation_calibration": {
            "n_permutations": N_PERM,
            "method": "circular phase-shift of the seasonal series (preserves autocorrelation)",
            "delta_aic_observed": float(daic_obs),
            "perm_delta_aic_median": float(np.median(perm_daic)),
            "perm_delta_aic_95pct": float(np.quantile(perm_daic, 0.95)),
            "p_delta_aic_ge_observed": perm_p,
        },
        "waveform_skewness": {
            "data": y_skew,
            "v_model_prediction": v_pred_skew,
            "sinusoid_model_prediction": sin_pred_skew,
        },
    }


def main():
    print_status("Step 2.10: Velocity-tracking vs calendar-phase discriminator", "WORKING")
    rng = np.random.default_rng(RNG_SEED)

    src = RESULTS_DIR / "step_2_2_geospatial_temporal_analysis_code.json"
    d = json.loads(src.read_text())
    rows_all = d["temporal_orbital_tracking"]["temporal_tracking_data"]

    buckets = {"GLOBAL": [r for r in rows_all if r["bucket"] == "GLOBAL"],
               "N_HEMI": [r for r in rows_all if r["bucket"] == "N"],
               "S_HEMI": [r for r in rows_all if r["bucket"] == "S"],
               "N_QUIET": [r for r in rows_all if r["bucket"] == "N_Quiet"],
               "S_QUIET": [r for r in rows_all if r["bucket"] == "S_Quiet"]}

    out = {
        "step": "2.10",
        "title": "Velocity-tracking vs calendar-phase discriminator",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "method": {
            "estimand": "EW/NS anisotropy ratio vs orbital-phase templates",
            "models": {
                "M_v": "a + b·|v_orb(t)| (Keplerian waveform, phase/shape fixed)",
                "M_v2": "a + b·|v_orb(t)|² (kinetic proxy)",
                "M_sin": "annual sinusoid, free phase/amplitude",
                "M_sin2": "annual + semiannual sinusoids (seasonal baseline)",
                "M_v_sin2": "velocity + semiannual hybrid",
            },
            "cv": "5-fold contiguous-block held-out RMSE",
            "calibration": f"{N_PERM} circular phase-shift permutations",
        },
        "buckets": {},
    }

    for label, rows in buckets.items():
        if len(rows) < 6:
            print_status(f"{label}: only {len(rows)} bins, skipped", "WARNING")
            continue
        res = run_bucket(rows, label, rng)
        out["buckets"][label] = res
        g = res["fits"]["M_v"]
        s = res["fits"]["M_sin"]
        print_status(f"{label}: R²(v)={g['r2']:.3f} R²(sin)={s['r2']:.3f} "
                     f"ΔAIC(sin−v)={res['delta_aic_sin_minus_v']:+.2f} "
                     f"perm p={res['permutation_calibration']['p_delta_aic_ge_observed']:.4f} "
                     f"CV RMSE v={res['cv_rmse_contiguous_5fold']['M_v']:.4f} "
                     f"sin={res['cv_rmse_contiguous_5fold']['M_sin']:.4f}", "SUCCESS")

    # Headline interpretation on GLOBAL
    g = out["buckets"]["GLOBAL"]
    interp = []
    if g["delta_aic_sin_minus_v"] > 2:
        interp.append("Velocity template preferred over free-phase annual sinusoid (ΔAIC>2)")
    elif g["delta_aic_sin_minus_v"] < -2:
        interp.append("Annual sinusoid preferred over velocity template (ΔAIC>2)")
    else:
        interp.append("Velocity and sinusoid templates statistically indistinguishable at |ΔAIC|<2")
    fv = g["nested_f_tests"]["v_given_annual_basis"]
    if np.isfinite(fv.get("p", np.nan)) and fv["p"] < 0.05:
        interp.append(f"Velocity adds information beyond the annual sinusoid (F={fv['F']:.1f}, p={fv['p']:.3g})")
    fs = g["nested_f_tests"]["annual_basis_given_v"]
    if np.isfinite(fs.get("p", np.nan)) and fs["p"] < 0.05:
        interp.append(f"Annual basis adds information beyond velocity (F={fs['F']:.1f}, p={fs['p']:.3g})")
    out["headline_interpretation"] = interp

    OUTPUT_FILE.write_text(json.dumps(out, indent=2))
    print_status(f"Results written to {OUTPUT_FILE.name}", "SUCCESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
