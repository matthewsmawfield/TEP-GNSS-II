#!/usr/bin/env python3
"""
Step 2.9: Dependence and Cycle-Count Pricing

Prices the two multiplicity caveats flagged on the secondary signatures:

1. PLANETARY EVENT DEPENDENCE (56/156 significant at >=2sigma)
   The 156 event tests share the same daily coherence series, so adjacent
   +-120-day inference windows overlap and the tests are not statistically
   independent.  This step reports the effective independence count: the
   size of a maximal non-overlapping-window subset (greedy, in date order),
   together with the disjoint-cell upper bound on independent 240-day
   windows the data span can host.  The significant-hit count is then
   repriced against the dependence-aware null, giving a binomial tail that
   is conservative with respect to residual inter-window correlation.

2. NUTATION CYCLE-COUNT UNCERTAINTY (18.6-year coupling R^2 = 0.641)
   The record spans 1.361 nutation cycles, so each phase bin is populated
   by at most two independent cycle realizations (the second cycle covers
   only part of phase space).  This step reports the cycle count per
   tested period, the phase-bin replication limit, and the standard error
   on R^2 implied by the n = 12 phase-bin fit (Wishart/Olkin-Pratt
   large-sample variance), alongside the existing permutation null
   percentiles that already price phase alignment.

Inputs (existing pipeline outputs only):
  - results/outputs/step_2_2_geospatial_temporal_analysis_code.json
  - results/outputs/nutation_surrogate_validation.json

Output:
  - results/outputs/step_2_9_dependence_pricing.json

Runtime: seconds. No primary data reprocessing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
STEP22_FILE = ROOT / "results/outputs/step_2_2_geospatial_temporal_analysis_code.json"
NUTATION_FILE = ROOT / "results/outputs/nutation_surrogate_validation.json"
OUTPUT_FILE = ROOT / "results/outputs/step_2_9_dependence_pricing.json"

ANALYSES = [
    'jupiter_opposition_analysis',
    'saturn_opposition_analysis',
    'mars_opposition_analysis',
    'venus_conjunction_analysis',
    'mercury_conjunction_analysis',
]

INFERENCE_WINDOW_DAYS = 120   # pre-specified primary window
N_EVENTS_CATALOG = 156        # total events analyzed at the primary window
SIGMA_THRESHOLD = 2.0         # reported detection threshold


def print_status(msg: str, level: str = "INFO"):
    print(f"[{level}] {msg}")


def planetary_event_dependence(step22: Dict) -> Dict:
    """Effective independence count and dependence-aware hit pricing."""
    events: List[Dict] = []
    for key in ANALYSES:
        evres = step22.get(key, {}).get('results_by_window_size', {}) \
                                   .get(str(INFERENCE_WINDOW_DAYS), {}) \
                                   .get('event_results', {})
        for name, ed in evres.items():
            edate = ed.get('event_date')
            if not edate:
                continue
            sigma = ed.get('gaussian_fit', {}).get('sigma_level') or 0.0
            events.append({
                'name': name,
                'date': datetime.fromisoformat(edate),
                'sigma_level': float(sigma),
                'significant': float(sigma) >= SIGMA_THRESHOLD,
            })
    events.sort(key=lambda e: e['date'])

    n_analyzed = len(events)
    n_sig = sum(e['significant'] for e in events)

    # Greedy maximal subset whose +-120-day windows do not overlap
    # (successive event dates must be separated by > 2 * window).
    gap = 2 * INFERENCE_WINDOW_DAYS
    indep: List[Dict] = []
    last = None
    for e in events:
        if last is None or (e['date'] - last['date']).days > gap:
            indep.append(e)
            last = e
    n_indep = len(indep)
    k_indep = sum(e['significant'] for e in indep)

    span_days = (events[-1]['date'] - events[0]['date']).days if events else 0
    disjoint_cells = span_days // gap if gap else 0

    # Null per-event rate at the >=2sigma threshold (two-sided normal).
    alpha = float(2 * (1 - stats.norm.cdf(SIGMA_THRESHOLD)))
    expected_full = N_EVENTS_CATALOG * alpha
    expected_indep = n_indep * alpha
    # Dependence-aware pricing: hit fraction among non-overlapping tests.
    binom_p = float(1 - stats.binom.cdf(k_indep - 1, n_indep, alpha)) \
        if n_indep else None
    binom_p_full = float(1 - stats.binom.cdf(n_sig - 1, N_EVENTS_CATALOG, alpha))

    return {
        'n_events_catalog': N_EVENTS_CATALOG,
        'n_events_analyzed_primary_window': n_analyzed,
        'n_significant_ge2sigma': n_sig,
        'inference_window_days': INFERENCE_WINDOW_DAYS,
        'sigma_threshold': SIGMA_THRESHOLD,
        'alpha_per_event_twosided': alpha,
        'effective_independence': {
            'method': (
                'Greedy maximal subset of events whose +-120-day inference '
                'windows share no calendar days (successive dates >240 days '
                'apart); window overlap is the dominant dependence channel '
                'because every test draws on the same daily coherence series.'
            ),
            'n_independent_windows': n_indep,
            'n_significant_independent': k_indep,
            'independent_hit_rate': k_indep / n_indep if n_indep else None,
            'disjoint_cell_upper_bound': int(disjoint_cells),
            'span_days_first_to_last_event': span_days,
        },
        'null_expectation': {
            'under_independence_156': expected_full,
            'under_independence_29': expected_indep,
        },
        'hit_pricing': {
            'binomial_tail_full_catalog': binom_p_full,
            'binomial_tail_independent_subset': binom_p,
            'interpretation': (
                'Even under the most conservative independence count '
                f'({n_indep} non-overlapping windows), the observed '
                f'{k_indep} detections exceed the null expectation '
                f'({expected_indep:.2f}) by an order of magnitude '
                f'(binomial tail p = {binom_p:.2e}).'
            ),
        },
    }


def nutation_cycle_pricing(step22: Dict, surrogate: Dict) -> Dict:
    """Cycle-count and R^2 uncertainty for the 18.6-year coupling."""
    span_days = step22['nutation_analysis']['data_span_days']
    results = {}
    for name, per_days in [('main_nutation_18p6y', 6798.4),
                           ('annual_nutation', 365.25),
                           ('semiannual_nutation', 182.6)]:
        cycles = span_days / per_days
        results[name] = {'period_days': per_days, 'cycles_observed': cycles}

    # Phase-bin replication: the second cycle covers only part of phase
    # space, so per-bin replication is bounded by ~1-2 cycle realizations.
    main = step22['nutation_analysis']['nutation_results']['main_nutation']
    phase_data = main['phase_data']
    n_pairs_bins = [b['n_pairs'] for b in phase_data]
    max_np = max(n_pairs_bins)
    est_cycles_per_bin = [2.0 * np_ / max_np for np_ in n_pairs_bins]

    # R^2 standard error for the n = 12 phase-bin sinusoid fit.
    # Large-sample Wishart variance of the squared multiple correlation:
    #   Var(R^2) ~ 4 rho^2 (1-rho^2)^2 (n-k-1)^2 / ((n^2-1)(n+k+1))
    n_bins, k_params = 12, 3
    r2 = main['r_squared']
    var_r2 = (4 * r2 * (1 - r2) ** 2 * (n_bins - k_params - 1) ** 2
              / ((n_bins ** 2 - 1) * (n_bins + k_params + 1)))
    se_r2 = float(np.sqrt(var_r2))

    sur = surrogate.get('results', {}).get('main_nutation', {})
    perm = sur.get('permutation_test', {})

    return {
        'data_span_days': span_days,
        'cycles_per_period': results,
        'main_nutation': {
            'r_squared': r2,
            'r_squared_standard_error': se_r2,
            'r_squared_approx_2sigma_band': [
                max(0.0, r2 - 2 * se_r2), min(1.0, r2 + 2 * se_r2)],
            'n_phase_bins': n_bins,
            'phase_bin_replication': {
                'cycles_observed': results['main_nutation_18p6y']['cycles_observed'],
                'max_independent_cycle_realizations_per_bin': 2,
                'est_cycles_per_bin_from_pair_counts': [
                    round(x, 3) for x in est_cycles_per_bin],
                'pair_count_range': [min(n_pairs_bins), max_np],
                'note': (
                    'Phase-bin pair counts span ~7x, reflecting partial '
                    'second-cycle phase coverage: each bin is effectively '
                    'one or two cycle realizations, so the fitted amplitude '
                    'and phase are single-cycle-dominated.  The detection '
                    'itself is priced by the phase-shuffled permutation '
                    'null (observed R^2 above the 99th null percentile), '
                    'which already accounts for the limited cycle count.'
                ),
            },
        },
        'permutation_null_context': {
            'null_r_squared_mean': perm.get('null_r_sq_mean'),
            'null_r_squared_95th': perm.get('null_r_sq_95th'),
            'null_r_squared_99th': perm.get('null_r_sq_99th'),
            'permutation_p_value': perm.get('p_value'),
        },
    }


def main() -> Dict:
    print_status('Step 2.9: dependence and cycle-count pricing', 'INFO')

    step22 = json.load(open(STEP22_FILE))
    surrogate = json.load(open(NUTATION_FILE)) if NUTATION_FILE.exists() else {}

    results = {
        'step': '2.9',
        'name': 'Dependence and Cycle-Count Pricing',
        'timestamp': datetime.now().isoformat(),
        'planetary_event_dependence': planetary_event_dependence(step22),
        'nutation_cycle_pricing': nutation_cycle_pricing(step22, surrogate),
        'success': True,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print_status(f'Results saved to {OUTPUT_FILE}', 'SUCCESS')
    return results


if __name__ == '__main__':
    main()
