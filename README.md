# Global Time Echoes: 25-Year Analysis of CODE Precise Clock Products

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17517141.svg)](https://doi.org/10.5281/zenodo.17517141)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

![Global Time Echoes: 25-Year Analysis](site/public/header-image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.20 (Cairo)  
**First published:** 3 November 2025 · **Last updated:** 30 September 2026
**Status:** Preprint  
**DOI:** [10.5281/zenodo.17517141](https://doi.org/10.5281/zenodo.17517141)  
**Website:** [https://mlsmawfield.com/tep/gnss-ii/](https://mlsmawfield.com/tep/gnss-ii/)

## Abstract





Analysis of 25.3 years of global GNSS timing data (165.2 million station-pair observations) documents persistent velocity-dependent correlations in atomic clock networks. Critically, this work proposes that standard GNSS processing algorithms, designed to remove energetic (common-mode) errors via datum constraints, inadvertently preserve the subtle, geometry-dependent (differential) correlations that are the focus of this work. Building on the multi-centre study's validation (R²=0.92-0.97 between CODE, IGS, ESA), the extended temporal baseline confirms long-baseline recovery and enables investigation of long-period geophysical phenomena inaccessible in shorter baselines. Seven convergent signatures are identified: (1) Spatial anisotropy persists with EW>NS (global EW/NS ratio=2.16, strength=1.981 ± 0.23 resampling SE, integrated 25.3-year aggregate), (2) anisotropy ratio correlates with orbital velocity (r=-0.888; surrogate p < 2 × 10⁻⁷, 0/5M exceeded; t-test p ≈ 2.6 × 10⁻⁴ with N_eff ≈ 11) across a 25.3-year baseline with ≈ 19% annual geometric ratio modulation, (3) a full-sky multi-resolution directional search (79,330 tested directions across four grids, with 65,341 at 1°) recovers a stable preferred direction at RA=6°, Dec=+4° (r=0.746; exploratory directional-rank p < 10⁻⁵; global sky-search significance not yet evaluated) coincident with Earth's orbital velocity tangent at aphelion (~6°) and ~162° from the CMB dipole — a heliocentric-orbital-phase signature that excludes the Solar Apex template at ~16,000 ×  variance ratio (R²=55.7% vs 0.003%), (4) planetary event catalogue (56/156 ≥ 2σ under the free-centre pulse statistic reflects repeatable estimator behaviour on the seasonal curve; true event specificity is reserved for the 40-event outer-planet opposition subset validated at 5.5 ×  over random dates, p < 10⁻¹⁷, with continuous potential correlation r = +0.116, p = 0.012), (5) preliminary coupling to 18.6-year lunar nutation (R²=0.641 ± 0.10 over 1.36 cycles; permutation p=0.0016 — the point estimate sits above the 99th percentile of phase-shuffled nulls, with amplitude and phase single-cycle-dominated) and a semiannual coherence component (R²=0.904, p=2.7 × 10⁻⁵; permutation p=0.00027, with fitted phase peaked near the orbital apsides), (6) network covariance score (0.582) replicates multi-centre range, (7) null results for solar rotation (27-day) and lunar standstill are consistent with selectivity for orbital-gravitational phenomena over surface features. The 19% modulation describes changes in the geometric shape of the correlation field (ratio of spatial correlation lengths), not clock frequency variations; individual clock-rate effects remain at standard GR-modelled fractional-frequency levels. On the held-out MGEX product the distance-structured coherence replicates (λ ≈ 1,862 km), while the anisotropy and primary orbital-velocity metrics do not replicate robustly. In-sample, a free-phase annual sinusoid is preferred over the velocity template (ΔAIC = 11.2); the signature is therefore reported as an annual modulation phased near the apsides. Observed patterns are compatible with key TEP expectations: the recovered spatial correlation length (azimuth-averaged isotropic exponential λ = 3,210 ± 389 km, with cross-sector directional dispersion λ̄_T = 4,201 ± 1,967 km across eight azimuthal sectors) lies within the pre-specified 1,000–10,000 km search window (Paper 0 §10.E); across products the fitted scale is conditioned by clock-product construction and estimator settings (reported product-level values ~1.0–4.8 × 10³ km; MGEX λ = 1,862 ± 155 km, Paper 14, Step 3.5), and the same band-ordered profile is recovered in each product; the IGS-final values are consistent with the geometric saturation radius R_T(M_⊕) ≈ 4,150 km, which is itself calibrated on this scale (Paper 6), so this is a consistency statement rather than an independent test. Model discrimination is primarily established through kernel-form selection (Gaussian and squared-exponential kernels preferred by AIC/BIC with R² = 0.965, with exponential ΔAIC = 12.8 and R² = 0.945 relative to Gaussian, strongly ruling out scale-free power-law forms with ΔAIC > 30), velocity-dependent anisotropy (r = -0.888), and geometric alignment (EW/NS = 2.16). Here “kernel” denotes the parametric family fitted to the pair-correlation decay with station separation, and “anisotropy” denotes the directional dependence of correlation strength, quantified by the EW/NS amplitude ratio and its orbital modulation. The absence of GM/r² scaling is physically consistent with the datum-projection mechanism in which common-mode components are absorbed by GNSS estimation while geometric information is transmitted; this mechanism requires validation via synthetic signal injection through the actual processing chain. Raw carrier-phase analysis, separately processed per-constellation tests, synthetic end-to-end injection, and independent external replication represent the critical next steps. The empirically derived spatial correlation length λ_T (the Temporal Topology covariance scale) is a GNSS-sector covariance scale obtained after environmental projection and processing transfer. It is not the screening operator S_Σ(E) itself and should not be identified numerically with response coefficients from other TEP channels. In the near-Earth environment, this correlation length acts as the macroscopic geometric proxy for the continuous saturation of Temporal Topology, anchoring the differential clock correlations without committing to specific subatomic microphysics. The primary result is 25.3-year aggregate consistency of distance-structured covariance and EW/NS anisotropy. The in-ecliptic orbital-phase direction, planetary event response, and nutation couplings are secondary covariance-structure signatures requiring held-out replication.


## Key Findings

The 25.3-year temporal baseline reports seven convergent signatures: orbital velocity coupling (r = −0.888), an annual orbital-phase direction at RA=6°, Dec=+4° (r=0.746), semiannual nutation (R² = 0.904), 18.6-year lunar nutation (R² = 0.641), planetary event responses (56/156 significant), spatial anisotropy (EW/NS = 2.16), and network covariance score (0.582). These signatures are not statistically independent and no joint-sigma claim is made. The preferred direction lies approximately 6° from the aphelion-velocity tangent; the CMB-apex template is anti-phase and does not identify the operative frame.

---

## The TEP Research Program

| Paper | Repository | Title | DOI |
|-------|-----------|-------|-----|
| **Paper 0** | [TEP](https://github.com/matthewsmawfield/TEP) | Temporal Equivalence Principle: Dynamic Time & Emergent Light Speed | [10.5281/zenodo.16921911](https://doi.org/10.5281/zenodo.16921911) |
| **Paper 1** | [TEP-GNSS](https://github.com/matthewsmawfield/TEP-GNSS) | Global Time Echoes: Distance-Structured Correlations in GNSS Clocks | [10.5281/zenodo.17127229](https://doi.org/10.5281/zenodo.17127229) |
| **Paper 2** | **TEP-GNSS-II** (This repo) | Global Time Echoes: 25-Year Analysis of CODE Precise Clock Products | [10.5281/zenodo.17517141](https://doi.org/10.5281/zenodo.17517141) |
| **Paper 3** | [TEP-GNSS-RINEX](https://github.com/matthewsmawfield/TEP-GNSS-RINEX) | Global Time Echoes: Raw RINEX Validation of Distance-Structured Correlations in GNSS Clocks | [10.5281/zenodo.17860166](https://doi.org/10.5281/zenodo.17860166) |
| **Paper 4** | [TEP-GL](https://github.com/matthewsmawfield/TEP-GL) | Temporal-Spatial Coupling in Gravitational Lensing: A Reinterpretation of Dark Matter Observations | [10.5281/zenodo.17982540](https://doi.org/10.5281/zenodo.17982540) |
| **Paper 5** | [TEP-GTE](https://github.com/matthewsmawfield/TEP-GTE) | Global Time Echoes: Empirical Validation of the Temporal Equivalence Principle | [10.5281/zenodo.18004832](https://doi.org/10.5281/zenodo.18004832) |
| **Paper 6** | [TEP-UCD](https://github.com/matthewsmawfield/TEP-UCD) | Temporal Topology Saturation Scale: Cross-Scale Consistency of ρ_T | [10.5281/zenodo.18064365](https://doi.org/10.5281/zenodo.18064365) |
| **Paper 7** | [TEP-RBH](https://github.com/matthewsmawfield/TEP-RBH) | The Soliton Wake: Exploring RBH-1 as a Temporal Topology Candidate | [10.5281/zenodo.18059250](https://doi.org/10.5281/zenodo.18059250) |
| **Paper 8** | [TEP-SLR](https://github.com/matthewsmawfield/TEP-SLR) | Global Time Echoes: Optical-Domain Consistency Test via Satellite Laser Ranging | [10.5281/zenodo.18064581](https://doi.org/10.5281/zenodo.18064581) |
| **Paper 9** | [TEP-EXP](https://github.com/matthewsmawfield/TEP-EXP) | What Do Precision Tests of General Relativity Actually Measure? | [10.5281/zenodo.18109760](https://doi.org/10.5281/zenodo.18109760) |
| **Paper 10** | [TEP-COS](https://github.com/matthewsmawfield/TEP-COS) | The Temporal Equivalence Principle: Suppressed Density Scaling in Globular Cluster Pulsars | [10.5281/zenodo.18165798](https://doi.org/10.5281/zenodo.18165798) |
| **Paper 11** | [TEP-H0](https://github.com/matthewsmawfield/TEP-H0) | The Cepheid Bias: Resolving the Hubble Tension | [10.5281/zenodo.18209702](https://doi.org/10.5281/zenodo.18209702) |
| **Paper 12** | [TEP-JWST](https://github.com/matthewsmawfield/TEP-JWST) | The Temporal Equivalence Principle: A Unified Resolution to the JWST High-Redshift Anomalies | [10.5281/zenodo.19000827](https://doi.org/10.5281/zenodo.19000827) |
| **Paper 13** | [TEP-WB](https://github.com/matthewsmawfield/TEP-WB) | The Temporal Equivalence Principle: Temporal Shear Recovery in Gaia DR3 Wide Binaries | [10.5281/zenodo.19102061](https://doi.org/10.5281/zenodo.19102061) |
| **Paper 15** | [TEP-EFA](https://github.com/matthewsmawfield/TEP-EFA) | Temporal Equivalence Principle: Temporal Shear in the Earth Flyby Anomaly | [10.5281/zenodo.19454862](https://doi.org/10.5281/zenodo.19454862) |
| **Paper 16** | [TEP-J0437](https://github.com/matthewsmawfield/TEP-J0437) | Synchronization Holonomy in Pulsar Scintillation | [10.5281/zenodo.19454620](https://doi.org/10.5281/zenodo.19454620) |
| **Paper 17** | [TEP-LLR](https://github.com/matthewsmawfield/TEP-LLR) | Lunar Laser Ranging and the Nordtvedt Effect | [10.5281/zenodo.19446028](https://doi.org/10.5281/zenodo.19446028) |

## Key Results

### Temporal Stability
- **Long-baseline recovery:** Original signatures confirmed over 25.3-year timescale
- **Temporal Topology correlation length:** λ<sub>T</sub> = 4,201 ± 1,967 km (anisotropy mean; exponential fit λ ≈ 3,210 km), consistent with Paper 1's range (3,330–4,549 km)
- **Multi-resolution orbital-phase direction:** Stable across 65,341 tested directions at 1° resolution

### Long-Period Geophysical Signatures
- **Nutation cycle:** Clear detection of 18.6-year lunar nutation (R² = 0.641)
- **Semiannual nutation:** Strongest geophysical coupling in entire dataset (R² = 0.904)
- **Chandler wobble:** Confirmed with extended temporal baseline
- **Seasonal patterns:** Robust annual modulation effects

### Planetary Event Analysis
- **Mercury:** 34/80 detections (42.5%)
- **Jupiter:** 8/23 detections (34.8%)
- **Saturn:** 7/25 detections (28.0%)
- **Mars:** 4/12 detections (33.3%)
- **Venus:** 3/16 detections (18.8%)

### Directional Characterization
- **Best-fit location:** RA = 6°, Dec = +4° (r=0.746), approximately 6° from Earth's aphelion-velocity tangent
- **CMB control:** The directed CMB-apex template is 162° away and anti-correlates (r=-0.546)
- **Solar-Apex control:** Null correlation (r=0.006); the best-fit template explains approximately 16,000 ×  more variance
- **Scope:** The scan fixes the background-speed magnitude and measures annual phase; it does not detect a CMB rest frame or determine a physical speed scale

## Repository Structure

```
TEP-GNSS-II/
├── scripts/
│   ├── steps/                      # Analysis pipeline
│   │   ├── step_1_1_code_longspan.py
│   │   ├── step_2_0_code_longspan.py
│   │   ├── step_2_1_code_longspan.py
│   │   ├── step_2_2_code_longspan.py  # Main geospatial-temporal analysis
│   │   ├── step_2_5_dual_motion_geometry.py
│   │   ├── step_2_6_null_control.py
│   │   └── step_2_8_draconitic_falsification.py
│   └── utils/                      # Shared utilities
├── site/                           # Academic manuscript site
│   ├── components/                 # HTML section files
│   ├── public/                     # Static assets
│   └── dist/                       # Built site output
├── results/
│   ├── figures/                    # Generated plots
│   └── outputs/                    # Analysis results (JSON)
├── logs/                           # Execution logs
├── 2-TEP-GNSS-II-v{version}-{codename}.md  # Auto-generated markdown
└── VERSION.json                    # Version metadata
```

## Installation

```bash
# Clone repository
git clone https://github.com/matthewsmawfield/TEP-GNSS-II.git
cd TEP-GNSS-II

# Install dependencies
pip install -r requirements.txt
```

## Analysis Pipeline

### Core Analysis Steps

```bash
# Step 1.1: Data acquisition and provenance
python scripts/steps/step_1_1_code_longspan.py

# Step 2.0: Correlation analysis
python scripts/steps/step_2_0_code_longspan.py

# Step 2.1: Geospatial processing
python scripts/steps/step_2_1_code_longspan.py

# Step 2.2: Comprehensive geospatial-temporal analysis
python scripts/steps/step_2_2_code_longspan.py

# Step 2.5: CMB frame validation
python scripts/steps/step_2_5_dual_motion_geometry.py

# Step 2.6: Null control tests
python scripts/steps/step_2_6_null_control.py

# Step 2.8: Draconitic falsification
python scripts/steps/step_2_8_draconitic_falsification.py
```

## Data Sources

### GNSS Clock Products
- **Provider:** CODE (Center for Orbit Determination in Europe)
- **Source:** http://ftp.aiub.unibe.ch/CODE/
- **Coverage:** March 1, 2000 – June 30, 2025 (25.3 years, 9,218 days)
- **Station Pairs:** 165.2 million measurements
- **Unique Stations:** 474 physical receivers (814 total station codes)
- **Citation:** Steigenberger et al. (2021), Johnston et al. (2017)

### Planetary Ephemeris
- **Source:** NASA JPL Development Ephemeris DE432s
- **Provider:** Jet Propulsion Laboratory via Astropy
- **Coverage:** 1550-2650 CE with meter-level accuracy
- **Citation:** Folkner et al. (2014), Astropy Collaboration (2013, 2022)

## Citation

```bibtex
@article{smawfield2025globaltimeechoes25year,
  title={Global Time Echoes: 25-Year Analysis of CODE Precise Clock Products},
  author={Smawfield, Matthew Lukin},
  journal={Zenodo},
  year={2025},
  doi={10.5281/zenodo.17517141},
  url={https://doi.org/10.5281/zenodo.17517141},
  note={Preprint v0.20 (Cairo)}
}
```

### Theoretical Framework Citation

```bibtex
@article{smawfield2025tep,
  title={Temporal Equivalence Principle: Dynamic Time & Emergent Light Speed},
  author={Smawfield, Matthew Lukin},
  year={2025},
  doi={10.5281/zenodo.16921911},
  url={https://doi.org/10.5281/zenodo.16921911}
}
```

## License

This repository is distributed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**. See [LICENSE](LICENSE) for details.

## Contact

**Author:** Matthew Lukin Smawfield  
**Email:** matthew@mlsmawfield.com  
**ORCID:** [0009-0003-8219-3159](https://orcid.org/0009-0003-8219-3159)

## Related Work

- [Paper 0: TEP Theory](https://doi.org/10.5281/zenodo.16921911) - Foundational framework
- [Paper 1: Multi-Center Validation](https://doi.org/10.5281/zenodo.17127229)
- [Paper 3: Raw RINEX Validation](https://doi.org/10.5281/zenodo.17860166)
- [TEP-GTE: Synthesis Manuscript](https://doi.org/10.5281/zenodo.18004832)

---

## Open Science Statement

These are working preprints shared in the spirit of open science—all manuscripts, analysis code, and data products are openly available under Creative Commons and MIT licenses to encourage and facilitate replication. Feedback and collaboration are warmly invited and welcome.

---

**Contact:** matthew@mlsmawfield.com  
**ORCID:** [0009-0003-8219-3159](https://orcid.org/0009-0003-8219-3159)
