# Temporal Equivalence Principle: Native hi_class Conformal Implementation, Linear Perturbation Closure, and CMB Acoustic Peak Preservation
**Matthew Lukin Smawfield**
Version: v0.6 (Cambridge)
First published: 8 June 2026 · Last updated: 10 August 2026
DOI: 10.5281/zenodo.20572722

---

## Abstract


Standard cosmology explains the Cosmic Microwave Background (CMB) acoustic peaks, the pre-recombination sound horizon, and the thermal scaling relevant to Big Bang Nucleosynthesis (BBN) within an FLRW expansion history conventionally extrapolated toward a physical singularity. This paper demonstrates that the CMB acoustic-sector and conformal thermal/sound-horizon scalings are preserved with high fidelity under a static conformal temporal-transport geometry governed by the Temporal Equivalence Principle (TEP).



In the TEP framework, matter clocks and photon phases evolve in a causal matter metric defined by a conformal scalar field $\tilde{g}_{\mu\nu} = A(\phi)^2 g_{\mu\nu}$. Because this conformal transport geometry is mathematically isomorphic to the FLRW scale factor $a(t)$, standard Boltzmann solvers like `hi_class` and `CLASS` can be used as conformal-frame calculators for the background/acoustic-sector mapping tested here. The parameter traditionally identified as Dark Energy ($\Omega_\Lambda$) is operationally reinterpreted within this implementation as the homogeneous temporal-shear background contribution filling the same background budget slot, $\Omega_\phi$.



This paper implements the native TEP interpretation directly in `hi_class`. Within the broader TEP interpretation, by recognizing that the spatial metric does not stretch, the "Big Bang" is reinterpreted not as a physical density singularity, but as a TEP temporal horizon—an asymptotic boundary where the observational clock map $A_{\rm clock} \to 0$. Direct Boltzmann integration verifies this background/acoustic mathematical isomorphism, verifying the internal conformal-frame preservation of the acoustic sector — the pre-recombination sound-horizon ratio is $r_s^{\rm TEP}/r_s^{\rm \Lambda CDM}=0.999994$ (corresponding to a $<6$ ppm deviation) and the acoustic-peak morphology remains intact without invoking early-universe spatial expansion.



Beyond the background mapping, the paper closes the linear pure-conformal scalar perturbation sector by adopting the luminal EFT closure $\alpha_M=-2\alpha_A$, $\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, and $\alpha_T=0$, for which the physical no-ghost discriminant satisfies $D=\alpha_K+\frac{3}{2}\alpha_B^2=\alpha_A^2 \ge 0$. An active-perturbation `hi_class` run evolving $\delta\phi$ through the full Einstein–Boltzmann hierarchy produces posteriors statistically indistinguishable from the background-only chain, demonstrating that the implemented linear pure-conformal scalar perturbation sector is numerically stable within the adopted linear EFT closure and observationally negligible at the current homogeneous-amplitude bound.



A joint `hi_class` Cobaya MCMC (Planck 2018 low-$\ell$ TT/EE + lensing + BAO + Pantheon+) tests the finite-turnover TEP conformal background within the native hi_class implementation, while companion TEP-C0 (Paper 26) reports Pantheon+ nested-sampling evidence for the physical no-$\Lambda$ temporal-shear branch: Bayes factor approximately 4.6 for the conservative $z_{\rm los}=5$ branch, approximately 61.8 for the fixed $z_{\rm los}=100$ benchmark, and approximately 40.3 for the broad free-$z_{\rm los}$ branch. These late-time model-comparison results are not re-derived in HC; HC supplies the native `hi_class` acoustic and perturbation closure. Within the broader TEP corpus, Paper 11 interprets the Hubble tension as a late-time, environment-dependent clock-transport effect caused by the environmental screening of the scalar field, rather than through a crisis in early-universe physics. HC does not independently re-analyse the distance-ladder data; it imports the interpretation.



Keywords: cosmology theory, cosmic microwave background, static conformal geometry, scalar-tensor theories, conformal gravity, hi_class, Horndeski, temporal equivalence principle, proper time, Cobaya, Planck 2018



## 1. Introduction


### 1.1 Contextualizing the TEP Corpus


The Temporal Equivalence Principle (TEP) has been constrained across many orders of magnitude in mass density, from terrestrial laboratory scales ($\rho \sim 20$ g/cm³) to the cosmological mean ($\rho \sim 10^{-29}$ g/cm³). Previous papers in this series have established:



- *Terrestrial scales (Paper 1):* Terrestrial atomic clock networks show 4,200 km phase correlations consistent with the candidate Temporal Topology saturation scale ρ_T ≈ 20 g/cm³.

- *Galactic scales (Paper 6, UCD):* SPARC rotation curves validate the potential-dependent proper-time mapping.

- *Stellar scales (Paper 13, WB):* Gaia DR3 wide binaries exhibit the predicted environment-dependent kinematic transition.

- *Cosmological scales (Paper 12, JWST):* High-redshift anomalies align with environment-dependent time dilation.




### 1.2 The Cosmological Horizon


The Hubble tension and the JWST high-redshift galaxy anomalies represent the two most persistent challenges in modern cosmology. Standard $\Lambda$CDM relies on a stretching spatial metric, which extrapolates to a physical singularity at $a \to 0$ and tightly restricts the available proper time for early galaxy assembly.


Previous TEP work (Paper 11, H₀; Paper 12, JWST) argued that these anomalies are resolved within the TEP framework. The TEP temporal-horizon picture replaces the FLRW singularity with an asymptotic boundary, removing the finite-age assembly bottleneck, and the $H_0$ tension is addressed as a local environmental screening effect on kinematic distance probes.


### 1.3 Purpose of This Paper


To rigorously test the CMB acoustic-sector component of the Static Conformal thesis, this paper demonstrates that the acoustic-sector integrals can be reproduced by an exactly conformal temporal mapping without explicit spatial expansion. A full light-element abundance calculation is not performed in HC. TEP-TH supplies the nonsingular temporal-horizon geometry and recombination-visibility treatment, while TEP-BBN supplies the native chemical-evolution framework and local CMB-thermalization proof of concept. The present HC claim is limited to conformal thermal/sound-horizon scaling, acoustic preservation, and the native `hi_class` perturbation implementation.


Because the TEP conformal scalar field $\tilde{g}_{\mu\nu} = A(\phi)^2 g_{\mu\nu}$ is mathematically isomorphic to the FLRW scale factor $a(t)$, the TEP Static Conformal geometry can be natively evaluated by deploying the `hi_class` Boltzmann solver as a conformal-frame calculator. This requires:



- Mapping the TEP conformal geometry onto the Boltzmann framework, establishing the implementation-level correspondence between the parameter conventionally written as $\Omega_\Lambda$ and the homogeneous temporal-shear background contribution, $\Omega_\phi$, occupying the same background-budget role as $\Omega_\Lambda$.

- Native implementation in hi_class to evaluate the conformal temporal shear field directly.

- A joint MCMC parameter estimation ($H_0$, $\Omega_b h^2$, $\Omega_{\rm cdm} h^2$, $n_s$, $A_s$, $\tau$, $A_{\rm planck}$, $\epsilon_T$) against Planck 2018, BAO, and Pantheon+ data to quantitatively demonstrate that the acoustic peaks are preserved with sound-horizon ratio $r_s^{\rm TEP}/r_s^{\rm \Lambda CDM}=0.999994$ (corresponding to a $<6$ ppm deviation) in a static conformal geometry.



This work does not independently analyse Pantheon+ supernovae or derive the full nonsingular temporal-horizon closure; those are addressed in companion papers TEP-C0 (Paper 26) and TEP-TH (Paper 27).

The critical question: Can a static conformal geometry mathematically reproduce the CMB acoustic peaks?

The claim-discipline framework for the TEP corpus, including the scope limitations of canonical precision tests, is established in TEP-EXP (Paper 9).

## 2. Theoretical Architecture: The EFT Mapping

### 2.1 The Bi-Metric Action

The TEP framework posits that matter couples to a causal matter metric $\tilde{g}_{\mu\nu}$ related to the Einstein-frame metric $g_{\mu\nu}$ via a disformal transformation:

\begin{equation} \label{eq:3_theory_01}
\tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu} + B(\phi) \nabla_\mu\phi \nabla_\nu\phi
\end{equation}

where:

- $A(\phi) = \exp(\beta_A\phi/M_{\rm Pl})$ is the conformal factor, with $\beta_A = -1.0$ (the locked lab-scale convention used across the TEP corpus)

- $B(\phi)$ controls disformal deformation of the causal structure

- $\phi$ is the dynamical proper-time field

Following TEP-TH (Paper 27), two distinct projections of the temporal field are distinguished in cosmology: $A_{\rm clock}(z)$ is the exact observational clock/redshift mapping that generates the apparent distance-redshift relation, while $A_{\rm dyn}(z)$ is the physical dynamical response that modifies expansion and perturbations. In the homogeneous background limit evaluated here, the hi_class conformal-frame mapping corresponds to $A_{\rm clock}$; the dynamical response $A_{\rm dyn}$ is parameterized by $\epsilon_T$ and modifies the Hubble parameter and acoustic observables at late times without requiring early-universe thermal screening (TEP-TH, Paper 27; TEP-BBN, Paper 29).

*Metric signature convention:* $(+, -, -, -)$ throughout.

### 2.2 Formal Bellini–Sawicki Alpha Correspondence

hi_class requires the EFT property functions $\alpha_i$ that encode metric modifications at linear perturbation level.

#### 2.2.1 Planck Mass Running ($\alpha_M$)

The conformal coupling directly determines the running of the effective Planck mass:

\begin{equation} \label{eq:3_theory_02}
\alpha_M \equiv \frac{d \ln M_{\rm eff}^2}{d \ln a} = - \frac{d \ln A^2(\phi)}{d \ln a} = - \frac{2\beta_A}{M_{\rm Pl}} \frac{\phi'}{\mathcal{H}}
\end{equation}

where $\mathcal{H} = aH$ is the conformal Hubble parameter and primes denote derivatives with respect to conformal time.

#### 2.2.2 Tensor Speed Excess ($\alpha_T$)

The disformal term $B(\phi)$ alters the gravitational wave propagation speed. Multi-messenger constraints from GW170817/GRB 170817A require:

\begin{equation} \label{eq:3_theory_03}
|c_g - c_\gamma|/c \lesssim 10^{-15} \Rightarrow \alpha_T \approx 0 \text{ (today)}
\end{equation}

However, $B(\phi)$ may be non-zero at recombination ($z \approx 1100$) provided it relaxes to zero by $z \sim 0$. This statement concerns the general disformal EFT only; the production HC acoustic/perturbation branch analysed below is the pure-conformal ($\alpha_T=0$) branch.

#### 2.2.3 Braiding ($\alpha_B$) and Kineticity ($\alpha_K$)

These functions govern scalar field clustering and metric mixing. The Bellini–Sawicki braiding parameter $\alpha_B$ should not be confused with the matter-metric disformal function $B(\phi)$; in the pure-conformal HC closure, $B(\phi) = 0$ while conformal scalar–metric mixing gives $\alpha_B = 2\alpha_A$.

\begin{equation} \label{eq:3_theory_04}
\alpha_B = -\frac{\mathcal{H}'\phi'}{\mathcal{H}^2} \cdot f_B(\phi, X)
\end{equation}

\begin{equation} \label{eq:3_theory_05}
\alpha_K = \frac{\phi'^2}{\mathcal{H}^2 M_{\rm Pl}^2} \cdot f_K(\phi, X)
\end{equation}

where $X = -\nabla_\mu\phi \nabla^\mu\phi/2$ and $f_B$, $f_K$ are functions derived from the TEP action:

- $f_B(\phi, X)$ encodes the disformal coupling to the energy-momentum tensor trace.

- $f_K(\phi, X)$ encodes the kinetic term non-canonicality from the TEP proper-time field.

The explicit functional forms follow from the bi-metric action (Equation \ref{eq:3_theory_01}) and are determined by the conformal factor $A(\phi)$ and the disformal function $B(\phi)$. Their derivation is detailed in the TEP theoretical framework (Papers 1 and 11 of the TEP corpus). The schematic $f_B$, $f_K$ forms describe the general disformal EFT bookkeeping; the production perturbation run restricts to the pure-conformal branch, where these functions reduce to the closed runtime identities given in Appendix A.5.

The background-only configuration uses $\alpha_B$ and $\alpha_K$ as formal EFT bookkeeping; during native `tep_mode` background-only integration $f_B$ and $f_K$ evaluate identically to zero, verifying that this is a strict geometric mapping at the background level. The active-perturbation closure configuration (Section 4.5) passes `gravity_model = tep` and `M2_evolution = yes` to hi_class, which evolves the implemented linear pure-conformal scalar fluctuation sector $\delta\phi$ through the adopted Bellini–Sawicki EFT closure ($\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, $c_s^2=1$), with no-ghost discriminant $D = \alpha_A^2 \ge 0$. The background conformal mapping is geometrically derived from the bi-metric action (Appendix A.3a); the perturbative completion is adopted as the pure-conformal branch of the Horndeski EFT.

### 2.3 The Static Conformal Isomorphism

The defining feature of the TEP framework is that it recasts the role normally played by a physically expanding spatial metric in the background/acoustic sector. In standard $\Lambda$CDM cosmology, the proper distance between co-moving galaxies physically increases over time, parameterized by the scale factor $a(t)$.

In the static conformal interpretation tested here, intergalactic separations are not treated as primitively expanding; the apparent expansion is reconstructed through temporal transport. The causal matter metric $\tilde{g}_{\mu\nu}$ is modulated by the conformal clock-rate field $A(\phi)$. The Temporal Equivalence Principle relies on this distinct, dynamical proper-time field and is fundamentally separate from the standard Einstein Equivalence Principle (EEP), which concerns the universality of free fall and local Lorentz invariance in metric theories of gravity. Photons propagating through this gradient experience a shift in phase and frequency, leading to the exact HC conformal-frame mapping:

\begin{equation} \label{eq:3_theory_06}
1+z = \frac{A_0}{A_{\text{em}}} = A_{\text{clock}}^{-1}(z)
\end{equation}

The exact observational clock map $A_{\text{clock}}(z)=(1+z)^{-1}$ defines the redshift–distance relation in the static conformal geometry. Because the mathematical transport geometry of $A_{\text{clock}}$ across a static background is formally isomorphic to the transport geometry of a photon in an expanding FLRW metric with reconstructed scale factor $a_{\text{eff}}(z)$, standard cosmological integrators (like `hi_class` and `CLASS`) can be deployed natively as conformal-frame calculators for the background/acoustic-sector mapping tested here. The physical dynamical response $A_{\text{dyn}}(z)$ modifies the Hubble parameter and acoustic observables at late times (TEP-TH, Paper 27; TEP-BBN, Paper 29).

- The primary acoustic peaks ($100 \lesssim \ell \lesssim 2000$) generated at $z \sim 1089$ are preserved with extreme precision, because the mathematics of the acoustic horizon $r_s$ depend only on the conformal integration path, not on physical spatial stretching.

- The parameter conventionally identified as Dark Energy ($\Omega_\Lambda$) is reinterpreted within this implementation as the homogeneous temporal-shear background contribution, $\Omega_\phi$, occupying the same background-budget role as $\Omega_\Lambda$ in the reference FLRW calculation.

- The Big Bang singularity is reinterpreted, within TEP, as a temporal-horizon boundary of the conformal clock-rate field where $A_{\text{clock}} \to 0$ relative to the present epoch, driving the reconstructed scale factor $a_{\text{eff}} \to 0$ and creating the mathematical appearance of infinite density in standard FLRW reconstructions. The full nonsingular closure—finite curvature invariants, geodesic completeness, and the native chemical-evolution framework and local CMB-thermalization proof of concept—is developed in TEP-TH (Paper 27) and TEP-BBN (Paper 29), where the non-exact covariance/topology correction $C_T$ provides the transport closure beyond exact conformal shear.

- *Thermodynamic Cooling:* The adiabatic cooling of the CMB photon gas ($T \propto 1/a$ in standard cosmology) is preserved as $T \propto 1/A$. The energy density shifts natively via the conformal temporal shear without requiring physical spatial volume dilution.

*Operational definition of $\Omega_\phi$.* In this implementation, $\Omega_\phi$ is operationally defined as the homogeneous conformal-sector contribution that fills the same background budget slot occupied by $\Omega_\Lambda$ in the reference FLRW integration. A first-principles stress-energy derivation of $\rho_\phi$, $p_\phi$, and the effective equation of state belongs to the broader TEP-C0 action-level treatment.

*Archived EFT reference.* The Bellini–Sawicki $\alpha_i$ functions mapped from the TEP bi-metric action (step-3 fiducial) are archived in `results/03_alpha_functions.json`. Production CMB constraints use the native conformal implementation (Section 4), evaluating the strict isomorphism directly without relying on linear-perturbation mapping approximations.


## 3. Software Implementation: hi_class and the Finite-Turnover Conformal Regime


### 3.1 The hi_class Architecture


hi_class extends the CLASS Boltzmann solver to handle general scalar-tensor theories via the EFT formalism. This work uses hi_class v3.2.3 with the modified gravity (SMG) module enabled.


### 3.2 Native TEP Conformal Background Implementation

The native TEP background-only Hubble modification is implemented directly in hi_class via the `tep_mode` flag. When enabled, the background expansion history is modified as:

\begin{equation} \label{eq:4_implementation_01}
H_{\rm TEP}(z) = H_{\Lambda\rm CDM}(z) \times M(z), \quad M(z) = \frac{A(z)}{1 - \alpha_A(z)}
\end{equation}

where $S(z) = \exp[-(z/z_T)^{n_T}]$ is the redshift suppression factor, $A(z) = \exp[\epsilon_T \ln(1+z)\,S(z)]$ is the covariant conformal factor, and $\alpha_A = -d\ln A/d\ln(1+z)$. The production integration directly evaluates the exact HC conformal-frame mapping $M = A/(1-\alpha_A)$, ensuring computational fidelity to the underlying formal derivation (see Appendix A.3a). The transition function $f_T(z) = \ln(1+z)\,S(z)$ appearing in the exponent is the shared TEP-C0 implementation (Paper 26; `core/cosmology.py`: `f_T`, `conformal_factor_native`, `jordan_frame_M`):

\begin{equation} \label{eq:4_implementation_01b}
f_T(z) = \ln(1+z)\,S(z).
\end{equation}

The suppression factor $S(z)$ defines the physical profile of the conformal field: it drives $f_T \to 0$ for $z \gg z_T$, ensuring the field profile flattens asymptotically as it approaches the TEP temporal horizon; the $\ln(1+z)$ factor enforces $f_T(0)=0$, fixing the local reference frame so $H_0$ is anchored to the local observer. The function peaks at intermediate redshift ($z \sim z_T$), where the effective homogeneous temporal-shear contribution mimics apparent acceleration, and flattens out in the deep past.

*Implementation note:* an earlier development build used the *complement* $f_T = 1 - \exp[-(z/z_T)^{n_T}]$, which instead saturates to unity for $z \gg z_T$. This inverted the scalar field profile and corrupted the acoustic peak evaluation (see Appendix A.3a). The default TEP conformal parameters are:



```
tep_mode = yes
epsilon_T = 0.0066
z_T = 5.0
n_T = 2.0
```



#### Parameter-Scale and Amplitude Convention

**Turnover scales.** $z_T^{\rm HC}$ denotes the homogeneous/acoustic `hi_class` profile scale used here. $z_T^{\rm los}$ denotes the C0 line-of-sight supernova transport turnover. These scales are related projections of the temporal sector but are not numerically interchangeable.

**Amplitudes.** $\epsilon_T^{\rm HC}$ denotes the native `hi_class` homogeneous conformal amplitude reported here ($0.00547 \pm 0.00429$ from the 5-chain active posterior). $\epsilon_T^{\rm los}$ denotes the late-time line-of-sight transport amplitude fitted in TEP-C0. $\epsilon_T^{\rm CMB}$ denotes the C0 background/acoustic diagnostic amplitude. $\epsilon_{\rm dyn}$ denotes the dynamical temporal-horizon response in TEP-TH, while $\epsilon_{\rm field}=0.0175$ denotes the primordial spectral-flow parameter constrained by $n_s$ in TEP-TH. These are related projections of the same temporal sector, but they are not numerically interchangeable parameters.



The background conformal mapping is implemented through $M(z)=A/(1-\alpha_A)$. The associated linear scalar perturbation sector is closed separately through the Bellini–Sawicki runtime functions described in Section 3.3 and Appendix A.5, and validated in the active $\delta\phi$ run of Section 4.5. This implementation is the hi_class analogue of the CLASS native TEP module used in TEP-C0 (Paper 26).


### 3.3 Perturbation Stability and Closure

The present analysis natively closes the scalar perturbation sector by evaluating the adopted runtime Bellini–Sawicki Effective Field Theory (EFT) parameters in the pure conformal limit. While early formulations of the TEP acoustic mapping relied on the working assumption that scalar spatial fluctuations ($\delta\phi$) decouple or are heavily suppressed at recombination, the implementation developed here leverages the `hi_class` SMG framework to evolve the full Einstein-Boltzmann hierarchy actively.

Because the TEP framework maps its causal matter metric via the exact conformal relation $\tilde{g}_{\mu\nu}=A(\phi)^{2}g_{\mu\nu}$, the corresponding EFT functions ($\alpha_i$) in the Jordan frame are determined by the background derivative $\alpha_A \equiv -d\ln A / d\ln(1+z)$. For the implemented pure-conformal branch, we adopt the luminal EFT closure $\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, and $c_s^2=1$. The background conformal mapping $M = A/(1-\alpha_A)$ is geometrically derived from the bi-metric action (Appendix A.3a); the perturbative completion specified by these EFT coefficients is adopted as the pure-conformal branch of the Horndeski EFT, consistent with the conformal structure of the action. Although a negative kineticity frequently triggers ghost instabilities in canonical scalar-tensor theories, the full physical no-ghost discriminant $D$ in the Horndeski framework encompasses the braiding parameter, which in this closure is $\alpha_B = 2\alpha_A$.

Evaluating the full discriminant yields $D = \alpha_K + \frac{3}{2}\alpha_B^2 = \alpha_A^2$. The no-ghost discriminant is non-negative, $D = \alpha_A^2 \ge 0$. Because the finite-turnover profile $f_T(z)$ has a single extremum, $\alpha_A = -\epsilon_T\,df_T/d\ln(1+z)$ vanishes at the turnover. For $z_T = 5$ and $n_T = 2$, this occurs at $z_\star \simeq 2.64785$. Consequently, the discriminant $D = \alpha_A^2$ touches zero at $z_\star$ for every nonzero $\epsilon_T$. The relevant stability question is therefore whether $z_\star$ is a regular scalar-decoupling point, rather than whether $D$ remains bounded away from zero. Away from this point, $D > 0$; at the turnover all adopted EFT modification functions vanish and the implemented system reaches the GR/conformal decoupling limit. The decoupling limit occurs both at $\epsilon_T = 0$ and instantaneously at extrema of the finite-turnover conformal profile.

In the Bellini–Sawicki EFT used by `hi_class`, the scalar kinetic coefficient is $Q_s = 2M_\star^2\,D/(2-\alpha_B)^2$. At $z_\star$, all adopted EFT functions vanish ($\alpha_A = \alpha_B = \alpha_K = \alpha_M = 0$), so $D = Q_s = 0$ and the propagating scalar description reaches a degenerate GR/conformal limit. The linear solver completes the crossing without numerical divergence. Table 1 displays the analytic behavior of the EFT coefficients, while the finite spectra and completed active-perturbation chains provide the numerical regularity check. This establishes numerical regularity of the crossing within the adopted linear EFT closure. Whether the vanishing kinetic normalization represents exact constraint reduction or a strong-coupling limit at the level of the fully nonlinear action requires a separate canonical/nonlinear analysis and is not needed for the present linear acoustic-sector result. The `hi_class` SMG solver evaluates the EFT coefficients at each redshift step; no numerical regulator or tolerance threshold is applied, and the crossing is continuous in the neighbourhood of $\alpha_A = 0$.



Table 1: $D = 0$ crossing diagnostic at $z_\star \simeq 2.64785$ (fiducial $\epsilon_T = 0.0066$, $z_T = 5$, $n_T = 2$). $Q_s = 2M_\star^2 D/(2-\alpha_B)^2$ with $M_\star^2 = 1$ in reduced Planck units. The displayed EFT coefficients remain finite or vanish continuously through the turnover; $D$ and $Q_s$ vanish at $z_\star$, where the propagating scalar description becomes degenerate.

| $z - z_\star$ | $z$ | $\alpha_A$ | $\alpha_B$ | $D = \alpha_A^2$ | $Q_s$ | Linear solver status |
| --- | --- | --- | --- | --- | --- | --- |
| $-10^{-3}$ | $2.646848$ | $-4.31 \times 10^{-6}$ | $-8.61 \times 10^{-6}$ | $1.85 \times 10^{-11}$ | $9.27 \times 10^{-12}$ | Finite |
| $-10^{-4}$ | $2.647748$ | $-4.31 \times 10^{-7}$ | $-8.61 \times 10^{-7}$ | $1.85 \times 10^{-13}$ | $9.27 \times 10^{-14}$ | Finite |
| $-10^{-5}$ | $2.647838$ | $-4.30 \times 10^{-8}$ | $-8.61 \times 10^{-8}$ | $1.85 \times 10^{-15}$ | $9.26 \times 10^{-16}$ | Finite |
| $0$ | $2.647848$ | $0$ | $0$ | $0$ | $0$ | Finite |
| $+10^{-5}$ | $2.647858$ | $+4.29 \times 10^{-8}$ | $+8.58 \times 10^{-8}$ | $1.84 \times 10^{-15}$ | $9.20 \times 10^{-16}$ | Finite |
| $+10^{-4}$ | $2.647948$ | $+4.31 \times 10^{-7}$ | $+8.62 \times 10^{-7}$ | $1.86 \times 10^{-13}$ | $9.28 \times 10^{-14}$ | Finite |
| $+10^{-3}$ | $2.648848$ | $+4.31 \times 10^{-6}$ | $+8.61 \times 10^{-6}$ | $1.85 \times 10^{-11}$ | $9.27 \times 10^{-12}$ | Finite |

By evolving the implemented linear pure-conformal $\delta\phi$ scalar field through this adopted EFT closure, the numerical solver verifies that the continuous conformal transition smoothly manages the emergence into the late universe without triggering gradient instabilities or pathological phantom energies. At the fiducial amplitude ($\epsilon_T = 0.0066$), integrating the active perturbations yields an Integrated Sachs-Wolfe (ISW) residual of less than $0.001\%$ across the entire acoustic spectrum ($100 \le l \le 2000$). The background acoustic isomorphism is therefore preserved to the reported numerical precision under active linear perturbation evolution, validating that the active linear scalar fluctuations in the temporal shear field remain stable and do not distort the CMB damping tail.


### 3.3b Covariant Frame Alignment: Matter-Frame Hubble Friction

The TEP action defines the causal metric for matter particles as $\tilde{g}_{\mu\nu} = A(\phi)^2 g_{\mu\nu}$. Under this conformal rescaling, the matter-frame conformal Hubble rate is related to the Einstein-frame rate by the exact derivation of Appendix A.3a. Using explicit frame-labelled variables, the matter-frame conformal Hubble rate satisfies

\begin{equation}
\widetilde{\mathcal{H}} = \mathcal{H}_E + \frac{A'}{A}, \qquad \frac{A'}{A} = \alpha_A\,\widetilde{\mathcal{H}},
\end{equation}

where $\mathcal{H}_E = a_E H_E$ is the Einstein-frame conformal rate, primes denote derivatives with respect to Einstein-frame conformal time, and $\alpha_A \equiv -d\ln A/d\ln(1+z)$. Solving for $\widetilde{\mathcal{H}}$ yields

\begin{equation} \label{eq:3_3b_Htilde}
\widetilde{\mathcal{H}} = \frac{\mathcal{H}_E}{1 - \alpha_A},
\end{equation}

consistent with the exact background relation $\tilde{H} = A\,H_{\Lambda\rm CDM}/(1-\alpha_A)$ derived in Appendix A.3a (Eq. \ref{eq:a3a_exact}). In the Jordan-frame EFT, matter particles follow geodesics of $\tilde{g}_{\mu\nu}$, so their Euler equations must be evaluated with $\widetilde{\mathcal{H}}$ rather than the Einstein-frame rate $\mathcal{H}_E$.

The variable `index_bg_H` in the patched hi_class code stores the TEP-mapped Hubble rate $H_{\rm TEP}(z) = M(z)\,H_{\Lambda\rm CDM}(z)$, which already incorporates the full conformal-frame factor $M = A/(1-\alpha_A)$ (Section 3.2). This is the matter-frame rate $\widetilde{H}$, not the Einstein-frame rate $H_E$. The conformal-time counterpart `index_bg_H_conformal` is therefore $\widetilde{\mathcal{H}} = a\,\widetilde{H}$, which is already the full matter-frame conformal rate. No additional multiplication by $(1-\alpha_A)$ is applied; the displayed code in earlier drafts that showed such a multiplication was a documentation error and has been corrected. The production codebase evaluates $M = A/(1-\alpha_A)$ in the background Hubble setter, and `index_bg_H` stores the resulting mapped rate directly.

Because null geodesics are conformally invariant, photons and neutrinos (while relativistic) propagate using the same mapped conformal rate; the photon and collision terms use the conformal-time scale factor $\tilde{a} = A\,a_E$ and its derivative, which are the quantities stored in the mapped background. This is a direct consequence of conformal invariance of null trajectories under $g_{\mu\nu} \to A^2 g_{\mu\nu}$, not a separate frame assignment. The metric equations retain the mapped background consistently, preserving the CMB acoustic physics. The modification is minimal and upstream: the background Hubble setter applies the exact $M = A/(1-\alpha_A)$ factor, and all species natively use the resulting mapped conformal rate.


### 3.4 Pipeline Architecture

The full analysis pipeline, executed via `scripts/run_all.py`, consists of:


- *Step 0 (Setup):* Environment configuration and dependency check.

- *Step 1 (Install):* Install Cobaya, Planck 2018 likelihoods, and hi_class with the native TEP patch (`external/patches/hiclass_tep_native.patch`).

- *Step 2 (Background):* Compute the TEP-modified background expansion history $H(z)$ and density evolution.

- *Step 3 (Alpha Functions):* Compute Bellini–Sawicki coefficients from the TEP theoretical mapping (archived for reference).

- *Step 4 (CMB Spectra):* Run hi_class with native `tep_mode` at the Planck 2018 best-fit point. Compare TT, TE, and EE spectra against standard CLASS $\Lambda$CDM.

- *Step 5 (Matter-Frame Scan):* Dual-scan reconstruction of the acoustic scale in finite-turnover and power-law diagnostic limits.

- *Step 6 (Cobaya Config):* Generate the Cobaya YAML configuration for the MCMC pipeline with native TEP parameters.

- *Step 7 (MCMC):* Execute the Cobaya MCMC with hi_class, using real Planck + BAO + Pantheon+ likelihoods, for both the background-only configuration and the active-perturbation closure configuration (`gravity_model = tep`).

- *Step 8 (Posteriors):* Analyze MCMC chains with burn-in removal and weighted statistics.

- *Step 9 (Synthesis):* Combine all results into summary JSON and markdown.


Publication figures are generated separately via `python scripts/generate_figures.py` (not part of `run_all.py`). Both figures are written to `results/figures/` with filenames matching their publication numbering. Figure 3 requires step 04b. Include them in the static site with `cd site && npm run build`.

The running EFT $\alpha$-functions provide the linear cosmological realization of the dynamical temporal response $A_{\rm dyn}$. Their continuous evolution produces the required conformal perturbation behaviour across cosmological epochs without introducing a separate phenomenological epoch-screening function.

## 4. MCMC Parameter Estimation Pipeline

### 4.1 The Cobaya Framework

Cobaya provides a Python interface to CLASS/hi_class with extensive MCMC sampling capabilities. The transition from SciPy/Pandas pipelines to Cobaya enables:

- Native hi_class integration without file-based I/O bottlenecks

- Parallel tempering and adaptive Metropolis-Hastings sampling

- Direct Planck likelihood wrapper integration

- Seamless GetDist posterior visualization

### 4.2 Likelihood Configuration

The pipeline uses the following Planck 2018 likelihoods:

| Likelihood | Description | $\ell$ Range |
| --- | --- | --- |
| `planck_2018_lowl.TT` | Low-$\ell$ temperature | 2–29 |
| `planck_2018_lowl.EE` | Low-$\ell$ polarization | 2–29 |
| `planck_2018_lensing.native` | CMB lensing reconstruction | 8–400 |
| `bao.sdss_dr12_consensus_final` | BAO SDSS DR12 consensus | — |
| `sn.pantheonplus` | Type Ia supernovae (Pantheon+) | — |

### 4.3 Free Parameters and Priors

The MCMC pipeline samples standard $\Lambda$CDM parameters alongside the TEP amplitude parameter $\epsilon_T$:

| Parameter | Prior | Description |
| --- | --- | --- |
| $\Omega_b h^2$ | $\mathcal{U}(0.005, 0.1)$ | Baryon density |
| $\Omega_{\rm cdm} h^2$ | $\mathcal{U}(0.01, 0.99)$ | Cold dark matter density |
| $H_0$ | $\mathcal{U}(40, 100)$ | Hubble constant |
| $\tau$ | $\mathcal{U}(0.01, 0.8)$ | Optical depth |
| $A_s$ | $\mathcal{U}(10^{-10}, 5 \times 10^{-9})$ | Scalar amplitude |
| $n_s$ | $\mathcal{U}(0.94, 1.0)$ | Scalar spectral index |
| $A_{\rm planck}$ | $\mathcal{U}(0.9, 1.1)$ | Planck calibration nuisance |
| $\epsilon_T$ | $\mathcal{U}(-1, 1)$ | TEP amplitude parameter (background Hubble modification) |

### 4.4 Pipeline Execution

```
# Cobaya YAML configuration
theory:
classy:
path: /path/to/hi_class
extra_args:
output: tCl,pCl,lCl,mPk
lensing: yes
modes: s,t
non_linear: halofit
# Native TEP background-only Hubble modification
tep_mode: 'yes'
z_T: 5.0
n_T: 2.0
# epsilon_T is sampled in params below — do not duplicate here

likelihood:
planck_2018_lowl.TT: null
planck_2018_lowl.EE: null
planck_2018_lensing.native: null
bao.sdss_dr12_consensus_final: null
sn.pantheonplus: null

params:
logA:
prior: {min: 2.5, max: 3.5}
ref: {dist: norm, loc: 3.044, scale: 0.014}
proposal: 0.01
drop: true
A_s:
value: 'lambda logA: 1e-10*np.exp(logA)'
n_s:
prior: {min: 0.94, max: 1.0}
ref: {dist: norm, loc: 0.966, scale: 0.004}
proposal: 0.004
H0:
prior: {min: 40, max: 100}
ref: {dist: norm, loc: 67.4, scale: 0.5}
proposal: 1.5
omega_b:
prior: {min: 0.005, max: 0.1}
ref: {dist: norm, loc: 0.0224, scale: 0.0002}
proposal: 0.0003
omega_cdm:
prior: {min: 0.01, max: 0.99}
ref: {dist: norm, loc: 0.12, scale: 0.001}
proposal: 0.0015
tau_reio:
prior: {min: 0.01, max: 0.8}
ref: {dist: norm, loc: 0.054, scale: 0.007}
proposal: 0.01
A_planck:
prior: {min: 0.9, max: 1.1}
ref: {dist: norm, loc: 1.0, scale: 0.0025}
proposal: 0.005
epsilon_T:
prior: {min: -1.0, max: 1.0}
ref: {dist: norm, loc: 0.006, scale: 0.005}
proposal: 0.0005
latex: '\epsilon_T'
sigma8:
latex: '\sigma_8'

sampler:
mcmc:
burn_in: 0
max_tries: 10000
max_samples: 500000
Rminus1_stop: 0.05
Rminus1_cl_stop: 0.2
output_every: 10
drag: true
seed: 42
```

### 4.5 Perturbation-Mode Validation

In addition to the background-only MCMC configuration above, the pipeline includes an active perturbation closure configuration (`data/cobaya/tep_hiclass_perturbations.yaml`) that passes `gravity_model = tep` and `M2_evolution = yes` to the `hi_class` SMG module. This directs the Boltzmann solver to evolve the implemented linear pure-conformal scalar fluctuation sector $\delta\phi$ through the adopted Bellini–Sawicki EFT closure ($\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, $c_s^2=1$; Appendix A.5).

A combined 5-chain MCMC of the active-perturbation model (single-chain + 4-chain MPI; 58,180 accepted steps, 40,726 post-burn-in samples; Planck 2018 low-$\ell$ TT/EE + lensing + BAO + Pantheon+; cross-chain Gelman–Rubin $R-1 = 0.007$ at termination) ran successfully with finite posterior at every step. All five chains sample the same active-perturbation model, priors, and likelihood, and the quoted $R-1$ is recalculated across all five chains. This converged 5-chain active posterior serves as the primary HC posterior. It is compared below with the separately sampled background-only chain, which is retained as a solver-comparison diagnostic because its cross-chain $R$-statistic is undefined. The resulting posterior summaries are:

\begin{equation} \label{eq:5_mcmc_epsT_pert}
\epsilon_T = 0.00547 \pm 0.00429,
\end{equation}

with $H_0 = 66.77 \pm 1.73$ km/s/Mpc, $n_s = 0.9956 \pm 0.0043$, $\Omega_b h^2 = 0.02144 \pm 0.00257$, $\Omega_{\rm cdm} h^2 = 0.1155 \pm 0.0042$, $\tau = 0.0497 \pm 0.0075$, $A_{\rm planck} = 1.088 \pm 0.013$, $\sigma_8 = 0.858 \pm 0.016$, and $S_8 = 0.868 \pm 0.025$. Two parameters are prior-boundary limited in this low-$\ell$-only configuration: $n_s$ accumulates at the upper bound of its $\mathcal{U}[0.94, 1.00]$ prior ($n_s^{\rm max} = 1.00000$), and $A_{\rm planck}$ saturates the upper bound of its $\mathcal{U}[0.9, 1.1]$ prior ($A_{\rm planck}^{\rm max} = 1.1000$). This is a known feature of low-$\ell$-only CMB analyses, which lack the high-$\ell$ acoustic information needed to break the $n_s$–$A_{\rm planck}$–$\tau$ degeneracy. A dedicated sensitivity run with $A_{\rm planck}$ widened to $\mathcal{U}[0.9, 1.25]$ yields $A_{\rm planck} = 1.229 \pm 0.026$ (still near the new ceiling) but $\epsilon_T = 0.0063 \pm 0.0048$, consistent with the 5-chain active posterior at $0.12\sigma$. A parallel multi-chain validation run (`tep_native_mcmc.yaml`) with $n_s$ widened to $\mathcal{U}[0.9, 1.05]$ and a Gaussian $A_{\rm planck}$ prior (loc = 1.0, scale = 0.0025) yields $n_s = 1.046 \pm 0.005$ (still saturating the wider upper bound) and $\epsilon_T = 0.0066 \pm 0.0049$, consistent with the 5-chain active posterior at $0.17\sigma$. The $n_s$ and $A_{\rm planck}$ posteriors should therefore be interpreted as robustness diagnostics of the $\epsilon_T$ constraint under prior-boundary saturation, not as final spectral-index or calibration determinations. The boundary-limited $n_s$ and $A_{\rm planck}$ values are not treated as physical measurements. The TEP amplitude $\epsilon_T$, however, shifts by no more than $0.17\sigma$ across the alternative prior configurations. The $\epsilon_T$ posterior is stable across all prior configurations: the maximum shift across the 5-chain active posterior, the widened-$A_{\rm planck}$ run, and the widened-$n_s$ run is $0.17\sigma$. Direct comparison with the background-only chain ($\epsilon_T = 0.00602 \pm 0.00493$) yields $\Delta\epsilon_T = -0.00055$ ($-0.08\sigma$), $\Delta H_0 = +0.09$ km/s/Mpc ($+0.04\sigma$), $\Delta n_s = +0.00009$ ($+0.02\sigma$), and $\Delta S_8 = +0.0009$ ($+0.03\sigma$). The maximum parameter disagreement across all eight cosmological parameters is $0.07\sigma$, and $\Delta\chi^2 = -0.46$. This confirms that the late-time ISW contribution from the dynamical scalar field is observationally negligible at the current bound, and that the $\epsilon_T$ posterior is driven by background acoustic-peak shifts rather than by perturbation-sector physics. Figure 1 shows the background versus active-perturbation posterior comparison.


![Background vs Perturbation Posterior Comparison](figures/figure_1_perturbation_triangle.png)

**Figure 1.** Marginalized posterior triangle plot. **Blue:** background-only TEP chain with $\delta\phi$ frozen (single-chain, 13,104 post-burn-in samples). **Red:** active-perturbation TEP chain with $\delta\phi$ evolved through the adopted Bellini–Sawicki EFT closure ($\alpha_M=-2\alpha_A$, $\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, $\alpha_T=0$); combined 5-chain run (single-chain + 4-chain MPI), $R-1 = 0.007$ at 58,180 accepted steps (40,726 post-burn-in). Native `hi_class` `tep_mode` with $z_{\rm HC}=5.0$, $n_T=2.0$. Parameters shown: $\epsilon_T^{\rm HC}$ (native `hi_class` homogeneous conformal amplitude), $H_0$, $n_s$, $\sigma_8$. Contours show 68% and 95% credible regions. The near-complete overlap demonstrates that active scalar perturbations are observationally negligible at the current homogeneous-amplitude bound. Maximum posterior shift: $\lesssim 0.07\sigma$ across all eight cosmological parameters.

The hi_class configuration uses native `tep_mode` with the transition function $f_T(z)=\ln(1+z)\exp[-(z/z_T)^{n_T}]$ and fixed `z_T = 5.0`, `n_T = 2.0`, with `epsilon_T` sampled freely in `params`. This configuration natively explores the parameter space of the static conformal field, leveraging the strict isomorphism to evaluate the acoustic physics exactly. The production configuration is `data/cobaya/tep_hiclass_suite.yaml` (reference alternate: `data/cobaya/tep_native_mcmc.yaml`).

*Pipeline status.* The native-`tep_mode` joint MCMC against Planck 2018 low-$\ell$ TT/EE + lensing + BAO (SDSS DR12) + Pantheon+ was run using the structurally corrected hi_class engine, allowing $\Omega_\Lambda$ to natively fill the background cosmological budget. The background-only chain (`tep_hiclass_suite`; 18,720 accepted steps, 13,104 post-burn-in with 30% burn-in discard; single chain, so Gelman–Rubin $R-1$ is undefined; the sampler-internal $R-1$ reported by Cobaya reached $0.045$ at termination) is retained as a solver-comparison diagnostic. It gives a $\Lambda$CDM-compatible background while measuring the TEP amplitude parameter:

\begin{equation} \label{eq:5_mcmc_epsT}
\epsilon_T = 0.00602 \pm 0.00493,
\end{equation}

with $H_0 = 66.68 \pm 1.82$ km/s/Mpc, $\Omega_b h^2 = 0.0214 \pm 0.0027$, $\Omega_{\rm cdm} h^2 = 0.1150 \pm 0.0042$, $\tau = 0.050 \pm 0.008$, $A_{\rm planck} = 1.088 \pm 0.012$, and $S_8 = 0.867 \pm 0.026$. The result is consistent with the TEP dual-domain expectation: the homogeneous amplitude $\epsilon_T$ remains small ($\sim 10^{-3}$) on the largest scales, where the CMB bound from TEP-C0 (Paper 26) is much tighter. This homogeneous HC amplitude is smaller than the primordial temporal-horizon amplitude ($\epsilon_t = 0.0175$) reported in TEP-TH (Paper 27) because the two parameters describe different observational projections of the evolving temporal sector and are not numerically interchangeable.

*Multi-chain validation.* A parallel 4-chain run (`tep_native`; configuration `data/cobaya/tep_native_mcmc.yaml`) using a Gaussian $A_{\rm planck}$ prior (loc = 1.0, scale = 0.0025) was executed. After an initial short run (2,993 post-burn-in samples; $R-1$ for $\epsilon_T = 0.098$), the chain was extended to 8,960 accepted samples (max_samples increased from 500k to 1M), reaching parameter-level $R-1 = 0.032$, while the conservative class-level diagnostic remained $R-1 = 0.098$. The extended chain is therefore retained as a sensitivity run rather than the primary posterior. It yields $\epsilon_T = 0.0066 \pm 0.0049$ and $H_0 = 67.15 \pm 1.36$ km/s/Mpc, consistent with the background-only chain at $0.10\sigma$ and $0.24\sigma$ respectively. The widened-$A_{\rm planck}$ chain (below) provides a fully converged multi-chain determination (max $R-1 = 0.036$, all parameters $R-1 < 0.05$), and the two agree to $0.05\sigma$. Together they confirm the single-chain result is not an artefact of the sampling configuration.

*High-$\ell$ TTTEEE attempt.* A dedicated production run adding `planck_2018_highl_plik.TTTEEE` to the baseline likelihood was attempted. The `tep_mode`-modified `hi_class` produces CMB power spectra that trigger numerical overflow (`divide by zero`, `invalid value`) in the bundled `clipy` Python interface during the high-$\ell$ binning operation (`cmbonly.py: matmul`). Both the full `plik` and the `plik_lite` variants exhibit the same failure. This is an unresolved numerical incompatibility between the current `tep_mode` spectra and the Planck `clipy` high-$\ell$ interface; the present test does not isolate whether the failure originates in spectrum normalization, output formatting, or likelihood binning.

To circumvent this blockage, a `CAMB`-based TEP approximation was implemented. Because `CAMB` lacks a native `tep_mode`, the TEP Jordan-frame Hubble rate $H_{\rm TEP}(z) = H_{\Lambda{\rm CDM}}(z) \cdot M(z)$ (with $M(z) = A(z)/(1-\alpha_A)$) was mapped onto an effective dark-energy equation of state $w_{\rm eff}(a)$ that reproduces the same background expansion. The effective $w(a)$ is fed into `CAMB` via `DarkEnergyPPF.set_w_a_table`, which supports phantom crossing. The effective-$w(a)$ `CAMB` construction generates finite high-$\ell$ spectra and completes the `plik_lite` likelihood evaluation without numerical errors. Because this construction is an effective-background approximation rather than the native TEP perturbation implementation, it is used solely to validate the high-$\ell$ code path and is not included in parameter inference or model comparison. The native `hi_class tep_mode` high-$\ell$ TTTEEE production likelihood remains pending. The low-$\ell$ + lensing + BAO + Pantheon+ result therefore remains the primary joint-likelihood constraint in this paper. Acoustic-peak preservation is established separately by the direct spectra and sound-horizon calculations rather than by a completed high-$\ell$ likelihood analysis. A future definitive high-$\ell$ production run will require either a patched `clipy` wrapper, a native `CAMB` `tep_mode` implementation, or an alternate high-$\ell$ likelihood (e.g. ACT DR6, SPT).

*Planck calibration prior sensitivity.* The nuisance parameter $A_{\rm planck}$ (absolute CMB calibration) is implemented as a hard uniform prior on $[0.9, 1.1]$ in the 5-chain active posterior. The posterior mean is $A_{\rm planck} = 1.088 \pm 0.012$ with maximum sampled value $1.1000$, indicating saturation against the upper prior bound. To test whether this truncation biases the cosmological inference, a dedicated sensitivity test was executed with the prior widened to $[0.9, 1.25]$ (Step 20: `scripts/steps/step_20_aplanck_sensitivity.py`, configuration `data/cobaya/tep_hiclass_aplanck_sens.yaml`). The converged run (16,320 total samples; all parameters Gelman–Rubin $R-1 < 0.05$; maximum $R-1 = 0.036$) yields $A_{\rm planck} = 1.229 \pm 0.026$, confirming the old posterior was truncated by approximately $5.0\sigma$. The TEP amplitude from the widened run is $\epsilon_T = 0.0063 \pm 0.0048$ ($R-1 = 0.036$), consistent with the 5-chain active posterior at $0.12\sigma$ and with the multi-chain validation at $0.05\sigma$. The correlation between $A_{\rm planck}$ and $\epsilon_T$ is $r = -0.10$, and splitting at the posterior median $A_{\rm planck} = 1.236$ gives a difference in $\epsilon_T$ of only $-0.04\sigma$. Even a $0.1$ upward shift in $A_{\rm planck}$ would move $H_0$ by only $\sim 0.1$ km s$^{-1}$ Mpc$^{-1}$ (inter-chain comparison: $H_0$ shifts by only $0.11$ km s$^{-1}$ Mpc$^{-1}$ when $A_{\rm planck}$ shifts by $0.14$), well below its posterior width. The $\chi^2$ does decrease monotonically toward the old boundary within the old prior range, but there is no evidence of a degeneracy cascade with $\epsilon_T$. The TEP constraint on the homogeneous amplitude is robust against $A_{\rm planck}$ prior systematics. The widened-$A_{\rm planck}$ run is used only as a numerical robustness test of the $\epsilon_T$ posterior; the resulting calibration value should not be interpreted as a physically preferred Planck calibration model.

The companion paper TEP-C0 (Paper 26) provides the primary late-time constraints: Pantheon+ nested sampling favors the physical no-$\Lambda$ TEP M1 branch over baseline $\Lambda$CDM with BF approximately 4.6 (conservative $z_{\rm los}=5$), approximately 61.8 (fixed $z_{\rm los}=100$ benchmark), and approximately 40.3 (broad free-$z_{\rm los}$). Those model-comparison results are not re-derived here; they are used as the late-time empirical context for the `hi_class` acoustic-preservation implementation.

## 5. Results and Cosmological Constraints

### 5.1 The Acoustic Spectra

The physically meaningful test of the native TEP integration is to evaluate whether the conformal field exactly replicates the acoustic physics of the early universe without invoking spatial expansion. Because the conformal field mathematically mimics the FLRW scale factor, the recombination-era physics is evaluated natively within the static frame. Throughout this paper, "exact isomorphism" refers to the conformal background/acoustic mapping: the equality of the relevant sound-horizon and photon-transport integrals under the identification of the TEP conformal factor with the FLRW scale factor. The associated linear pure-conformal scalar perturbation sector is closed separately through the adopted Bellini–Sawicki EFT closure and validated by the active ($\delta\phi$) hi_class run reported in Section 4.5 and Appendix A.5. This perturbative closure applies to the pure-conformal sector implemented here; the fully disformal, nonlinear, and environmentally inhomogeneous screening sectors remain extensions of the present calculation.

#### 5.1.1 Sound-horizon and acoustic-peak preservation

Running hi_class native `tep_mode` against standard CLASS $\Lambda$CDM at the Planck 2018 best-fit point, with $\epsilon_T = 0.0066$, $z_T = 5$, $n_T = 2$, yields:

- *Sound horizon preserved to ~6 ppm:* $r_s^{\rm TEP}/r_s^{\Lambda\rm CDM} = 0.999994$. The comoving sound horizon integrates identically in the static conformal frame. The remaining $\sim$6 ppm offset is a numerical/implementation-level residual associated with the finite precision of the conformal-frame background mapping and output reconstruction. Analytically, the exact mapping used in the production implementation is $M=A/(1-\alpha_A)$, whose first-order expansion is $A(1+\alpha_A)$. Direct verification confirms that the discrepancy is not a failure of the conformal isomorphism.

- *Acoustic-peak morphology unchanged:* with $r_s$, the baryon loading, and the photon-baryon driving at $z \approx 1089$ all operating identically under the conformal clock-rate, the relative peak heights and the damping tail closely match $\Lambda$CDM.

The central result is therefore not that all cosmological observables are already closed, but that the CMB acoustic scale itself is not uniquely diagnostic of physical spatial expansion.

#### 5.1.1b Acoustic-scale preservation metrics

Table 2 quantifies the acoustic-scale preservation in three multipole ranges. The sound-horizon ratio $r_s^{\rm TEP}/r_s^{\Lambda\rm CDM} = 0.999994$ is independent of multipole because $r_s$ is a single integrated quantity; the $\ell$-centroid shift tracks the expected $-0.185\%$ angular-diameter-distance projection. The tabulated residuals are total TEP-versus-$\Lambda$CDM projection residuals, dominated by the angular-diameter-distance projection; the active-minus-background perturbation residual is below $0.001\%$ across the entire acoustic range.

| Multipole range | $\ell_{\rm peak}$ shift $\Delta\ell$ | $r_s^{\rm TEP}/r_s^{\Lambda\rm CDM}$ | Total TEP–$\Lambda$CDM projection residual (%) |
| --- | --- | --- | --- |
| $100 \le \ell \le 500$ | $-0.06$ | $0.999994$ | $0.67$ |
| $500 \le \ell \le 1000$ | $-0.36$ | $0.999994$ | $1.34$ |
| $1000 \le \ell \le 2000$ | $-0.64$ | $0.999994$ | $1.82$ |

#### 5.1.2 The residual is a late-time projection, largely degenerate with $H_0$

The field profile is active over intermediate redshift ($z \sim 1$–$15$, peaking near $z_T$), changing the apparent angular distance to last scattering. At the fiducial $\epsilon_T = 0.0066$ this shifts the angular acoustic scale by $\Delta\theta_s/\theta_s = +0.185\%$. This rigid rescaling produces a coherent, oscillatory $\Delta C_\ell/C_\ell$ pattern whose envelope reaches $\sim 1.8\%$ across $100 < \ell < 2000$. This is *not* a change in early-universe physics: it is a pure angular-diameter-distance projection, largely degenerate with $H_0$.

#### 5.1.3 Polarization Spectra ($C_\ell^{TE}, C_\ell^{EE}$)

The TE and EE spectra inherit the same behavior: the recombination-era polarization source is natively preserved by the conformal integration, and the only effect is the common $\theta_s$ projection shared with TT. Running hi_class with active scalar perturbations ($\delta\phi$ evolved through the adopted Bellini–Sawicki EFT closure) and comparing against the background-only TEP run and Planck 2018 $\Lambda$CDM, the maximum active-perturbation residuals in the polarization channels are:

| Multipole range | Total TE projection residual (%) | Total EE projection residual (%) |
| --- | --- | --- |
| $100 \le \ell \le 500$ | $1.16$ | $1.62$ |
| $500 \le \ell \le 1000$ | $2.14$ | $2.46$ |
| $1000 \le \ell \le 2000$ | $3.19$ | $3.62$ |

These are total TEP-versus-$\Lambda$CDM projection residuals, dominated by the common angular-diameter-distance projection. The active-minus-background perturbation residual is below $0.001\%$; the larger values tabulated here are total TEP-versus-$\Lambda$CDM projection differences. There is no additional polarization-specific distortion from the dynamical scalar sector at the current precision.

### 5.2 Cosmological Constraints: Late-Time Evidence and the CMB Bound

The cosmological constraints on TEP come from two complementary regimes, established in the companion paper TEP-C0 (Paper 26).

*Late-time evidence (supernovae).* A nested-sampling model comparison over the full $1701\times1701$ Pantheon+ statistical-plus-systematic covariance finds substantial Bayesian preference for the TEP geometry over $\Lambda$CDM:

| Model | Bayes factor vs $\Lambda$CDM |
| --- | --- |
| TEP, $z_{\rm los}=5$ | $\sim 4.6$ |
| TEP, $z_{\rm los}=100$ | $\sim 61.8$ |
| TEP, free $z_{\rm los}$ | $\sim 40.3$ |
| $w$CDM | $\sim 29.7$ |
| CPL | $\sim 53.3$ |
| Einstein–de Sitter | $\sim 6.2\times10^{-126}$ |

The TEP M1 branch improves the Pantheon+ likelihood relative to baseline $\Lambda$CDM with BF approximately 4.6 (conservative $z_{\rm los}=5$), approximately 61.8 (fixed $z_{\rm los}=100$ benchmark), and approximately 40.3 (broad free-$z_{\rm los}$) (TEP-C0, Paper 26). Those model-comparison results are not re-derived here; they are used as the late-time empirical context for the `hi_class` acoustic-preservation implementation. The model-comparison result is consistent with the TEP claim that the Etherington distance-duality relation is a mathematically native feature of the static conformal field. TEP shows that the supernova distance-redshift relation can be fit without treating late-time acceleration as primitive spatial acceleration.

*$z_{\rm los}$ distinction.* The $z_{\rm los} = 5$ profile is the conservative line-of-sight turnover used in the C0 supernova-sector transport benchmark. It should not be confused with the homogeneous acoustic-sector profile scale $z_T^{\rm HC} = 5$ used in the hi_class conformal implementation, which is a related but distinct projection of the temporal sector. The C0 free-$z_{\rm los}$ robustness test uses $z_{\rm los} \in [0.1, 150]$.

*Amplitude dictionary.* $\epsilon_T^{\rm los}$ denotes the late-time line-of-sight transport amplitude fitted in TEP-C0. $\epsilon_T^{\rm CMB}$ denotes the C0 background/acoustic diagnostic amplitude. $\epsilon_T^{\rm HC}$ denotes the native `hi_class` homogeneous conformal amplitude reported here ($0.00547 \pm 0.00429$ from the 5-chain active posterior; the background-only chain yields $0.00602 \pm 0.00493$ as a solver-comparison diagnostic). $\epsilon_{\rm dyn}$ denotes the dynamical response in TEP-TH. $\epsilon_{\rm field}=0.0175$ denotes the primordial spectral-flow parameter constrained by $n_s$ in TEP-TH. These are related projections of the same temporal sector, but they are not numerically interchangeable.

*Homogeneous (CMB) bound.* The low-$\ell$ Planck likelihoods used in this paper's hi_class MCMC (TT/EE + lensing) yield $\epsilon_T = 0.00547 \pm 0.00429$ (5-chain active posterior), consistent with zero at $\sim 1.3\sigma$. The homogeneous CMB amplitude and the primordial spectral-flow parameter are different observational projections of the same temporal sector and are not numerically interchangeable. Their differing numerical values therefore do not require a phenomenological epoch-screening mechanism. In the canonical TEP-TH/TEP-BBN architecture, no early-time screening function is imposed to restore a standard hot-Big-Bang thermal history. The low-$\ell$+lensing+BAO+Pantheon+ chains reported here serve as implementation and robustness tests of the native hi_class module. The native `hi_class tep_mode` high-$\ell$ TTTEEE production likelihood remains pending because of a `clipy`/`hi_class` interface incompatibility (Section 4.5). A `CAMB`-based effective-background mapping was used solely to validate the high-$\ell$ code path; because it is an effective-$w(a)$ approximation rather than the native TEP perturbation implementation, it is not included in parameter inference or model comparison (Section 4.5). The low-$\ell$ combination remains the primary joint-likelihood constraint. Acoustic preservation is established by the direct spectra and sound-horizon calculations.

*Native-TEP joint MCMC.* This paper's primary contribution is the verified hi_class implementation, demonstrating ppm-level sound-horizon preservation and acoustic-sector equivalence in the native static conformal geometry.

### 5.3 Structure Growth and the Matter Power Spectrum

The full hi_class Boltzmann closure with active SMG perturbations yields a linear growth amplitude in agreement with Planck and weak-lensing measurements:

- *Linear growth amplitude:* $\sigma_8 = 0.825 \pm 0.016$ at the fiducial TEP parameters ($\epsilon_T = 0.0066$, $z_T = 5$, $n_T = 2$), compared to $\sigma_8 = 0.823$ for standard $\Lambda$CDM at the same cosmology. The TEP value is a native output of the full SMG EFT solver with the adopted Bellini–Sawicki mappings; no phenomenological suppression factor is applied.

- *Growth-function diagnostic:* The linear growth rate $f\sigma_8$ from the hi_class matter power spectrum (computed via $P(k)$ at $z=0$ and $z=0.5$) shows excellent agreement between the finite-turnover TEP model and Planck+BOSS best-fit $\Lambda$CDM:


| Model | $f\sigma_8(z=0)$ | $f\sigma_8(z=0.5)$ |
| --- | --- | --- |
| $\Lambda$CDM | $0.823$ | $0.410$ |
| TEP (background-only) | $0.824$ | $0.413$ |
| TEP (active $\delta\phi$) | $0.824$ | $0.413$ |

The TEP deviation from $\Lambda$CDM is $0.001$ ($0.1\%$) at $z=0$ and $0.003$ ($0.7\%$) at $z=0.5$, well within current BOSS and eBOSS uncertainties ($\sim 3\%$). This confirms that the TEP covariant action, when closed through the adopted Bellini–Sawicki EFT and solved with the full Boltzmann hierarchy, naturally restores structure growth to the observationally consistent range.


The $\sigma_8$ result demonstrates that the TEP covariant action, when closed through the adopted Bellini–Sawicki EFT and solved with the full Boltzmann hierarchy, naturally restores structure growth to the observationally consistent range. Simplified EdS-only growth ODEs, which lack the SMG EFT perturbation closure, are insufficient for this sector; the full Boltzmann closure is required.

### 5.4 The Hubble Tension in TEP


The TEP framework offers a proposed reconciliation of the Hubble tension without invoking an early-universe crisis. The homogeneous background is exactly mathematically isomorphic to $\Lambda$CDM ($H_0 \approx 67$ km/s/Mpc from the CMB), while the apparent local $H_0 \approx 73$ km/s/Mpc arises from an environment-dependent clock-transport bias along the local distance ladder (Cepheid/SN Ia calibration in unscreened stellar atmospheres). The tension is a measurement-environment effect, bypassing the need for early-universe expansion.



![H0 in the TEP picture](figures/figure_2_H0_comparison.png)



**Figure 2.** Corpus-level $H_0$ comparison: HC acoustic posterior and Paper 11 local-ladder correction. **HC joint MCMC:** native `hi_class` `tep_mode` homogeneous posterior with $\epsilon_T^{\rm HC}=0.00547\pm0.00429$, $z_{\rm HC}=5.0$, $n_T=2.0$. **Planck 2018:** independent CMB constraint. **SH0ES uncorrected / TEP-corrected:** the local distance-ladder values are imported from Paper 11; HC does not independently re-analyse the Cepheid/SN Ia calibration data. This figure illustrates consistency of the HC early-universe sector with the broader TEP Hubble-tension interpretation; it is not a standalone HC distance-ladder test.

### 5.5 The Mathematical Limit of the Conformal Field

To explicitly map the action of the conformal field on the acoustic horizon, the acoustic scale is evaluated in a mathematically idealized geometry ($\Omega_m = 1.0$, $\Omega_\Lambda = 0.0$) using the hi_class native `tep_mode` implementation.

#### Regime I: Finite-turnover HC branch ($z_{\rm HC} = 5$)

In the standard TEP model, the profile $\exp[-(z/z_{\rm HC})^{n_T}]$ ensures the conformal field correctly matches the apparent late-time acceleration inferred from Pantheon+. The integration verifies this background/acoustic mathematical isomorphism:

| $\epsilon_T$ | $100\theta_s$ | $r_s$ [Mpc] | $\Delta D_C / D_C$ | Interpretation |
| --- | --- | --- | --- | --- |
| $0.00$ | $1.0403$ | $144.526$ | $0.00\%$ | Pure EdS reference (no TEP) |
| $0.05$ | $1.0548$ | $144.519$ | $-1.38\%$ | $r_s$ preserved; $\theta_s$ shifts from $D_C$ projection |

The sound horizon $r_s$ remains exact because the conformal field geometry accurately tracks the mathematics of the acoustic horizon without requiring physical stretching of space.

#### Regime II: Power-law diagnostic limit ($z_{\rm HC} \to \infty$)

Removing the empirical profile and forcing the conformal factor to grow as a pure unsuppressed power law $A(z) = (1+z)^{\epsilon_T}$ exposes the mathematical divergence of the bare field:

| $\epsilon_T$ | $100\theta_s$ | $r_s$ [Mpc] | $\Delta D_C / D_C$ | Interpretation |
| --- | --- | --- | --- | --- |
| $0.00$ | $1.0403$ | $144.526$ | $0.00\%$ | Pure EdS reference |
| $0.05$ | $0.7565$ | $100.584$ | $-4.30\%$ | $r_s$ mathematically squeezed by divergence |

This mathematical limit demonstrates that the $z_{\rm HC} \sim 5$ empirical fitting function accurately defines the physical profile of the conformal field, allowing it to mimic Dark Energy while preserving the CMB acoustic horizon without expanding space.


![Matter-frame dual-scan results](figures/figure_3_jordan_theta_s.png)



**Figure 3.** Jordan-frame acoustic-scale diagnostic. Background-only native `hi_class` `tep_mode` diagnostic in an Einstein-de Sitter geometry ($\Omega_m=1.0$, $\Omega_\Lambda=0.0$). **Left panel:** Finite-turnover HC branch ($z_{\rm HC}=5$, $\epsilon_T^{\rm HC}=0.05$, $n_T=2.0$); the acoustic scale is protected and stays near the Planck 2018 reference. **Right panel:** Power-law diagnostic limit ($z_{\rm HC}\to\infty$, $\epsilon_T^{\rm HC}=0.05$, $n_T=2.0$); removing the empirical profile exposes unphysical acoustic-horizon squeezing. The dashed line is the Planck 2018 acoustic reference value; the comparison is a diagnostic acoustic-scale recovery, not a full TT/TE/EE likelihood plot.

## 6. Falsifiable Predictions

The following near-term observational tests would strengthen or falsify the TEP-HC acoustic-sector and perturbation claims.

- **Small-scale CMB polarization from active scalar perturbations.** The TEP-HC linear scalar perturbation sector predicts a characteristic phase shift in the TE cross-spectrum at $\ell \gtrsim 1000$ ($\sim 0.1\%$–$0.3\%$) due to the $\alpha_B \neq 0$ running of the conformal scalar. CMB-S4 and Simons Observatory, targeting $\ell \sim 3000$ with $\mu$K-arcmin sensitivity, can test this deviation directly. A null result at $>3\sigma$ would place a tighter upper bound on the TEP scalar amplitude.

- **B-mode polarization from native tensor modes.** The TEP-TH tensor analysis yields $r(k_{\rm pivot}) = 9 \times 10^{-6}$ and $r_{\rm max} = 6.26 \times 10^{-4}$, well below current BICEP/Keck bounds ($r < 0.036$) but above the cosmic-variance floor for CMB-S4 ($r \sim 10^{-4}$–$10^{-3}$). A B-mode detection with $r \sim 10^{-3}$ would be inconsistent with the TEP native tensor prediction; a non-detection down to $r \sim 10^{-4}$ would remain compatible and would sharpen the bound on $p$ in the temporal-horizon profile.

- **Acoustic-peak consistency under `tep_mode` background.** The TEP background factor $M(z) = A/(1-\alpha_A)$ preserves the acoustic-peak locations to within the numerical integration tolerance of the Boltzmann solver (currently $\lesssim 10$ ppm). The current hi_class implementation reports $r_s^{\rm TEP}/r_s^{\Lambda\rm CDM} = 0.999994$, where the residual $\sim$6 ppm is understood as a numerical/implementation-level artifact of finite-precision conformal-frame background reconstruction. Any claimed physical deviation from the exact conformal isomorphism must be shown to exceed the standard solver interpolation noise ($\sim 10$ ppm) before it can be interpreted as a falsification of the background mapping, rather than as a C++ integration artifact.

- **Growth-factor amplitude from native EFT.** The TEP-HC active-perturbation run yields $\sigma_8 = 0.825 \pm 0.016$ at the fiducial parameters ($\epsilon_T = 0.0066$, $z_T = 5$, $n_T = 2$), giving a structurally higher linear growth amplitude than the standard Planck $\Lambda$CDM baseline ($0.811 \pm 0.006$). The MCMC posterior mean is $\sigma_8 = 0.858 \pm 0.016$. As Stage-IV weak-lensing surveys (Euclid, Rubin/LSST) resolve their internal calibration systematics, the $S_8$ consensus is expected to trend upward toward the TEP prediction if the conformal-frame Hubble-friction modification is physically realized. This is framed as a diagnostic trend rather than a binary kill-switch: TEP does not predict an exact $S_8$ threshold but rather a directionally higher growth amplitude arising from the same adopted Bellini–Sawicki EFT closure that preserves the acoustic scale.

Each test targets a distinct sector of the TEP-HC claim: active scalar perturbations (test 1), tensor modes (test 2), background isomorphism (test 3), and growth amplitude (test 4). A combined null result across all four would require a significant revision of the conformal-frame mapping.

## 7. Conclusion: The Static Conformal Universe

This paper implements and validates the native Temporal Equivalence Principle (TEP) conformal modification directly within the `hi_class` Boltzmann solver framework. By leveraging the mathematical isomorphism between the FLRW expanding scale factor $a(t)$ and the TEP conformal scalar field $A(\phi)$, this analysis demonstrates that the early-universe acoustic-sector observables can be reproduced at high fidelity under a static conformal temporal-transport mapping.

### 7.1 Summary of Results

- *The Mathematical Isomorphism:* The TEP conformal factor $A(\phi) = \exp(\beta_A\phi/M_{\rm Pl})$ dictates the clock-rates and photon phases in the causal matter metric $\tilde{g}_{\mu\nu} = A(\phi)^2 g_{\mu\nu}$. Because this scalar field evolves identically to the standard spatial scale factor $a(t)$, standard Boltzmann solvers can be used as conformal-frame calculators for the background/acoustic-sector mapping tested here. The parameter traditionally defined as Dark Energy ($\Omega_\Lambda$) is operationally reinterpreted within this implementation as the homogeneous temporal-shear background contribution filling the same background budget slot, $\Omega_\phi$.

- *CMB Acoustic Preservation (Pure-Conformal Consistency):* Because of the static conformal isomorphism, the hi_class native integration demonstrates that the background/acoustic-sector observables are preserved to parts-per-million ($r_s^{\rm TEP}/r_s^{\Lambda\rm CDM} = 0.999994$). This is a pure-conformal consistency check: the conformal transport geometry recovers the standard FLRW acoustic results in the regime where the conformal field dominates and disformal corrections are suppressed. It is not an independent confirmation of TEP, but rather a necessary consistency requirement that any viable conformal-frame alternative must satisfy. The background acoustic observables alone do not uniquely force the spatial-expansion interpretation; they can be naturally accommodated by the evolving background scalar field $A(\phi)$. The active-perturbation closure (Section 4.5) confirms that evolving the implemented linear pure-conformal scalar fluctuation sector $\delta\phi$ through the adopted Bellini–Sawicki EFT closure produces parameter posteriors indistinguishable from the background-only solver-comparison diagnostic to $0.07\sigma$, with the combined 5-chain active-perturbation run reaching Gelman–Rubin $R-1 = 0.007$ at 58,180 accepted steps. The converged 5-chain active posterior serves as the primary HC posterior; the single-chain background-only run is retained as a solver-comparison diagnostic because its cross-chain $R$-statistic is undefined.

- *The Temporal Horizon:* The result of this paper does not require the CMB acoustic peaks to originate from a physically expanding spatial metric beginning at a density singularity. In the TEP interpretation tested here, the same conformal transport integrals normally written in terms of the FLRW scale factor $a(t)$ are reproduced by the temporal conformal field $A(\phi)$. The limit conventionally described as $a\to0$ is therefore reinterpreted, at the level of clock transport and photon phase evolution, as a temporal-horizon limit $A_{\rm clock}\to0$ relative to the present epoch. This is the precise sense in which the present calculation removes the Big Bang singularity from the acoustic-sector interpretation: the sound horizon, photon-baryon driving, and acoustic-peak morphology are preserved without requiring physical spatial stretching back to a zero-scale-factor origin. In this precise but physically important sense, the CMB acoustic sector no longer requires a physical zero-scale-factor Big Bang; it can be equivalently represented as a conformal temporal-horizon limit of the clock-rate field. Because this temporal horizon is asymptotic, cosmological epochs typically defined by a finite "time since the Big Bang" are instead fundamentally mapped by their thermodynamic temperature and the exact conformal clock-rate, shifting the measurement of cosmic history from a linear stopwatch to a thermodynamic state. Crucially, as established in TEP-BBN, the observed radiation temperature ($T_{\rm obs}$) and the local matter temperature ($T_{\rm loc}$) are distinct physical quantities governed by temporal transport. The broader nonsingular closure—geodesic completeness and curvature regularity in TEP-TH, together with the native chemical-evolution framework and local CMB-thermalization proof of concept in TEP-BBN—completes the companion treatment beyond the acoustic sector considered here.

- *Cosmological Constraints:* A joint hi_class Cobaya MCMC (Planck 2018 low-$\ell$ TT/EE + lensing + BAO + Pantheon+) yields a close match to the conformal field parameters. The companion paper TEP-C0 (Paper 26) provides robust late-time evidence: BF approximately 4.6 (conservative $z_{\rm los}=5$), approximately 61.8 (fixed $z_{\rm los}=100$ benchmark), and approximately 40.3 (broad free-$z_{\rm los}$), reducing the phenomenological need to treat late-time acceleration as primitive spatial expansion.

### 7.2 Resolving the Cosmological Crises

Standard $\Lambda$CDM cosmology currently faces two severe crises: the Hubble Tension ($H_0$) and the unexpectedly massive high-redshift galaxy candidates observed by JWST. The Static Conformal Universe offers a unified TEP interpretation of both without invoking early-universe modifications.

- *The Hubble Tension:* In the broader TEP corpus, Paper 11 argues that the temporal shear field is environmentally screened. Supernova and Cepheid distance indicators probe different environmental projections of the temporal field, with Cepheids residing in comparatively dense stellar environments where the observable response is more strongly screened (yielding a lower inferred $H_0$), while the supernova propagation and host-environment sector samples a less locally screened projection (yielding a higher inferred $H_0$). Paper 11 argues that the tension is an artifact of environmental screening on local kinematic distance probes, not an early-universe physics crisis. HC does not independently re-analyse the distance-ladder data; it imports the interpretation.


- *JWST High-Redshift Galaxies:* Within the broader TEP interpretation, the temporal-horizon picture removes the finite-age assembly bottleneck by replacing the FLRW singularity with an asymptotic conformal-clock boundary. The massive galaxies observed by JWST therefore form strictly within standard astrophysical accretion models over vast timescales (Paper 12).

### 7.3 Synthesis of the Paradigm Shift

This analysis implements and explicitly validates the native TEP implementation within a rigorous Boltzmann solver framework. The acoustic indistinguishability of the static conformal background from $\Lambda$CDM at recombination demonstrates that the early-universe background physics cannot easily distinguish between a stretching spatial metric and an evolving conformal clock-rate field.

Late-universe Pantheon+ data in TEP-C0 favor the physical no-$\Lambda$ TEP branch over baseline $\Lambda$CDM with BF $\simeq 4.6$ (conservative $z_{\rm los}=5$), BF $\simeq 61.8$ (fixed $z_{\rm los}=100$ benchmark), and BF $\simeq 40.3$ (free-$z_{\rm los}$), providing a concrete conformal-frame alternative to the background expansion interpretation. The active-perturbation closure reported in Section 4.5 confirms that the implemented linear pure-conformal scalar fluctuation sector is numerically regular across the sampled evolution, including the $D = Q_s = 0$ turnover, and is observationally negligible at the current amplitude bound, with the $\delta\phi$-enabled Einstein–Boltzmann chain agreeing with the background-only solver-comparison diagnostic to $0.07\sigma$ across all cosmological parameters. By treating time itself as a dynamical, environmentally screened scalar field, TEP seeks to unify early-universe acoustic physics, late-time "acceleration", the $H_0$ tension, and JWST anomalies into a single, cohesive static geometric framework. The present paper provides both the hi_class background/acoustic benchmark and the perturbation-closure validation.


## References

Smawfield, M. (Paper 1). *Global Time Echoes: Distance-Structured Correlations in GNSS Clocks.* TEP Corpus. DOI: 10.5281/zenodo.17127229.

Smawfield, M. (Paper 6). *Universal Critical Density: Unifying Atomic, Galactic, and Compact Object Scales.* TEP Corpus. DOI: 10.5281/zenodo.18064365.

Smawfield, M. (Paper 9). *What Do Precision Tests of General Relativity Actually Measure?* TEP Corpus. DOI: 10.5281/zenodo.18109760.

Smawfield, M. (Paper 11). *The Cepheid Bias: Resolving the Hubble Tension.* TEP Corpus. DOI: 10.5281/zenodo.18209702.

Smawfield, M. (Paper 12). *The Temporal Equivalence Principle: A Unified Resolution to the JWST High-Redshift Anomalies.* TEP Corpus. DOI: 10.5281/zenodo.19000827.

Smawfield, M. (Paper 13). *The Temporal Equivalence Principle: Temporal Shear Recovery in Gaia DR3 Wide Binaries.* TEP Corpus. DOI: 10.5281/zenodo.19102061.

Smawfield, M. (Paper 26). *Temporal Equivalence Principle: A Covariant Alternative to Cosmic Expansion.* TEP Corpus. DOI: 10.5281/zenodo.20370143.

Smawfield, M. (Paper 27). *Temporal Equivalence Principle: Temporal Horizon Cosmology and the Absence of a Physical Big Bang Singularity.* v0.3 (Thika). DOI: 10.5281/zenodo.20723059.

Smawfield, M. (Paper 29). *Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium.* Paper 29 (Dubai). DOI: 10.5281/zenodo.21841148.

Bellini, E., & Sawicki, I. 2014, JCAP, 07, 050. *Maximal freedom at minimum cost: linear large-scale structure in scalar-tensor theories.*

Brax, P., Burrage, C., Davis, A.-C., & Gubitosi, G. 2019, Phys. Rev. D, 100, 083515. *Screening mechanisms in scalar-tensor theories.*

Cobaya Team. 2023, *Cobaya: Code for Bayesian Analysis of physical theories.* arXiv:2305.02971.

Hu, B., Raveri, M., Frusciante, N., & Silvestri, A. 2014, Phys. Rev. D, 89, 103530. *EFTCAMB/EFTCosmoMC: Numerical Notes.*

Knox, L., & Millea, M. 2020, Phys. Rev. D, 101, 043533. *Hubble constant hunter's guide.*

Lagos, M., Bellini, E., Jimenez, J. B., et al. 2018, JCAP, 03, 021. *hi_class: Horndeski in the Cosmic Linear Anisotropy Solving System.*

Lewis, A., Challinor, A., & Lasenby, A. 2000, Astrophys. J., 538, 473. *Efficient computation of cosmic microwave background anisotropies.*

Planck Collaboration. 2020, A&A, 641, A1. *Planck 2018 results. I. Overview and cosmological parameters.*

Planck Collaboration. 2020, A&A, 641, A6. *Planck 2018 results. VI. Cosmological parameters.*

Riess, A. G., Casertano, S., Yuan, W., et al. 2022, ApJ, 934, L7. *A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope and the SH0ES Team.*

Sawicki, I., & Bellini, E. 2015, Phys. Rev. D, 92, 084061. *Stability of dark energy and the generalized no-slip condition.*

Zumalacárregui, M., & García-Bellido, J. 2014, Phys. Rev. D, 89, 064046. *Transforming gravity: from derivative couplings to matter to second-order scalar-tensor theories beyond the Horndeski Lagrangian.*

## Appendix A: Technical Implementation Details

### A.1 hi_class Installation and Configuration

#### A.1.1 Building with TEP Support

hi_class is installed automatically by pipeline Step 1 (`step_00b_install.py`), which clones hi_class and applies the native TEP patch from `external/patches/hiclass_tep_native.patch` to `source/background.c`, `source/input.c`, and `include/background.h`. Manual rebuild:

```
cd external/hi_class/hi_class
make clean && make
```

**Screening projection notice.** Screening in TEP is represented at theory level by the environmental operator S_Σ(E). Quantities such as ρ_T, R_T(M), S_⊕(r), compactness Φ/c^2, local stellar density, coherence length, proximity, and boundary geometry are domain-specific projections of E, not independent screening mechanisms and not interchangeable universal thresholds.

### A.2 Cobaya Installation

```
pip install cobaya
cobaya-install planck_2018_lowl.TT planck_2018_lowl.EE \
planck_2018_lensing.native bao.sdss_dr12_consensus_final \
sn.pantheonplus --path /path/to/likelihoods
```

### A.3 TEP Module C Code Structure and Implementation Note

The native conformal modification is implemented directly in hi_class `source/background.c`, controlled by the `.ini` flags `tep_mode`, `epsilon_T`, `z_T`, `n_T`. The relevant functions are:

- `tep_f_transition(pba, z)`: returns the suppression factor $S(z) = \exp[-(z/z_T)^{n_T}]$; the full transition is $f_T(z) = \ln(1+z)\,S(z)$ (see `core/cosmology.py:f_T`).

- `tep_gamma_factor(pba, z)`: returns the exact covariant conformal factor $A(z) = \exp[\epsilon_T \ln(1+z)\,S(z)]$ (not linearised).

- The Hubble rate and its conformal-time derivative are mathematically mapped using the exact HC conformal-frame mapping $M(z) = A/(1-\alpha_A)$ in `background_functions` and in the initial-Hubble setter, explicitly evaluating the static conformal geometry.

*Implementation note (corrected bug).* An earlier build used $f_T = 1 - \exp[-(z/z_T)^{n_T}]$ (the complement of the suppression function). This incorrectly inverted the scalar field profile, erroneously mapping the peak kinetic energy to the early universe rather than intermediate redshifts, which logically corrupted the acoustic integration. In addition, the post-processing step that read the spectra used a hard-coded output index and could silently load a stale file from an earlier run. Both issues are fixed: the transition function now uses the shared TEP-C0 implementation (`core/cosmology.py`), correctly matching the field profile to the Pantheon+ apparent acceleration, and the analysis resolves the most recent hi_class output deterministically. *Sign convention (TEP disformal metric):* the distance integrand is multiplied by $A(z)$ for null-geodesic propagation in the conformal frame. The legacy SMG alpha-function stub (`smg_tep_*`) has been retired; production physics lives in the patched `background.c` (`external/patches/hiclass_tep_native.patch`).

### A.3a Derivation of the Conformal-Frame Factor $M(z)$

This appendix derives the background conformal mapping $M(z)$ from the bi-metric action (Equation \ref{eq:3_theory_01}) using a single frame convention held fixed throughout, demonstrating the exact conformal-frame relation under the adopted HC reference-density convention, implemented natively in the codebase.

*Setup and convention.* Matter, photons, and rods couple to the conformal metric $\tilde{g}_{\mu\nu} = A^2(\phi)\,g_{\mu\nu} + B(\phi)\,\nabla_\mu\phi\nabla_\nu\phi$. For the homogeneous background the disformal term contributes only through the time-time component and is absorbed into the lapse; the evolution is governed by the conformal part, so $B \to 0$ is imposed here (the disformal sector re-enters at the perturbative/GW level via $\alpha_T$, Section 2.2.2). The conformal part gives the standard map between the Einstein-frame scale factor $a_E$ and cosmic time $t_E$ and their conformal counterparts:

\begin{equation} \label{eq:a3a_map}
\tilde{a} = A(\phi)\,a_E, \qquad d\tilde{t} = A(\phi)\,dt_E.
\end{equation}

These two relations *define* the convention; every subsequent equation is derived from them. The transition factor $S(z)=\exp[-(z/z_T)^{n_T}]$ correctly forces $A(z)\to1$ at the local endpoint, so the code's redshift grid can be identified with the physical conformal-frame redshift. The explicit $(z_E,\tilde z)$ distinction is retained only to derive the frame relation.

*Physical Hubble rate.* The expansion rate measured by conformal-frame clocks and rulers is $\tilde H \equiv \tilde a^{-1}\,d\tilde a/d\tilde t = d\ln\tilde a/d\tilde t$. Using $d/d\tilde t = A^{-1}\,d/dt_E$ and $\ln\tilde a = \ln A + \ln a_E$,

\begin{equation} \label{eq:a3a_Htilde}
\tilde H = \frac{1}{A}\frac{d}{dt_E}\big(\ln A + \ln a_E\big) = \frac{1}{A}\Big(\frac{d\ln A}{dt_E} + H_E\Big),
\end{equation}

where $H_E = d\ln a_E/dt_E$ is the Einstein-frame rate. Because the TEP conformal factor $A(z)$ is evaluated as a function of the observable physical redshift (the matter-frame redshift $1+z = \tilde{a}_0/\tilde{a}$), the coupling $\alpha_A$ computed in the codebase is fundamentally the derivative with respect to the *matter-frame* scale factor:

\begin{equation} \label{eq:a3a_alpha}
\frac{d\ln A}{dt_E} = \frac{d\ln A}{d\ln \tilde{a}}\,\frac{d\ln \tilde{a}}{dt_E} = \alpha_A\,(A \tilde{H}), \qquad \alpha_A \equiv \frac{d\ln A}{d\ln \tilde{a}} = -\frac{d\ln A}{d\ln(1+z)},
\end{equation}

which matches the definition in Section 3.2. Substituting $d\ln A/dt_E = \alpha_A A \tilde{H}$ into (\ref{eq:a3a_Htilde}) yields $\tilde{H} = \alpha_A \tilde{H} + H_E/A$, or equivalently $\tilde{H}(1 - \alpha_A) = H_E/A$.

*Einstein-frame reference rate.* The remaining step is to relate the Einstein-frame Hubble rate $H_E$ to the reference $\Lambda$CDM rate $H_{\Lambda\rm CDM}$. Under the conformal transformation $\tilde{g}_{\mu\nu} = A^2 g_{\mu\nu}$, the spacetime determinant transforms as $\sqrt{-\tilde{g}} = A^4 \sqrt{-g_E}$, so the homogeneous energy density transforms as $\rho_E = A^4 \tilde{\rho}$. The Einstein-frame Friedmann equation gives $H_E^2 = \frac{8\pi G}{3}\,\rho_E = A^4 \frac{8\pi G}{3}\,\tilde{\rho}$. The TEP implementation convention identifies the matter-frame reference density used by the acoustic calculator with the standard $\Lambda$CDM density evolution, $\tilde{\rho} = \rho_{\Lambda\rm CDM}$, so that $H_E^2 = A^4 H_{\Lambda\rm CDM}^2$ and therefore $H_E = A^2\,H_{\Lambda\rm CDM}$. Substituting into $\tilde{H}(1 - \alpha_A) = H_E/A$ gives the exact conformal-frame relation under the adopted HC reference-density convention:

\begin{equation} \label{eq:a3a_exact}
\boxed{\;\tilde H(z) = \frac{A(z)}{1 - \alpha_A(z)}\,H_{\Lambda\rm CDM}(z)\;} \qquad \Longrightarrow \qquad M_{\rm exact}(z) = \frac{A}{1 - \alpha_A}.
\end{equation}

*Implementation Status.* The production codebase (`hiclass_tep_native.patch`) evaluates this exact HC conformal-frame mapping $M = A/(1-\alpha_A)$ directly, guaranteeing mathematical fidelity to the conformal evaluation without requiring first-order approximations.

### A.4 Saturation Scale in Cosmological Units

The candidate Temporal Topology saturation scale ρ_T ≈ 20 g/cm³ converts to cosmological units as:

\begin{equation} \label{eq:9_appendix_01}
\rho_T = 20 \text{ g/cm}^3 = 2 \times 10^4 \text{ kg/m}^3 \approx 1.1 \times 10^{34} \text{ eV/cm}^3
\end{equation}

In Planck units ($\hbar = c = G = 1$):

\begin{equation} \label{eq:9_appendix_02}
\rho_T \approx 4 \times 10^{-93} M_{\rm Pl}^4
\end{equation}

Compare to cosmic mean density today ($\rho_{\rm crit,0} \approx 10^{-123} M_{\rm Pl}^4$). The hierarchy ensures the vast cosmological voids evaluate the pure unsuppressed conformal field, accurately simulating the expansion of space.

*Intermediate environments and operational parameter bounds.* In the density-projection used for this order-of-magnitude comparison, between the terrestrial laboratory and the cosmic mean the screening transition is continuous. At stellar atmospheric densities ($\rho \sim 10^{-6}$ g/cm³), the field is partially screened; at interplanetary densities ($\rho \sim 10^{-23}$ g/cm³), it is essentially unscreened. Certain orbital datasets—notably the Galileo GNSS clock ensemble—fall outside the operational parameters established for valid TEP-GNSS screening analysis (Paper 1), because their orbital altitude and local gravitational environment do not satisfy the strict kinematic isolation required to isolate the conformal phase drift from standard relativistic corrections. These exclusions are documented in the TEP-GNSS pipeline and do not affect the cosmological bound, which operates in the deep unscreened regime where $\rho \ll \rho_T$.

### A.5 Stability Sector Closure

To formally verify the stability of the active scalar perturbations, the native `hi_class` SMG module was extended to evaluate the exact analytical limits of the TEP conformal geometry at runtime.

In a generalized Horndeski treatment, the solver enforces the following physical stability conditions:

- $c_s^2 \ge 0$ (no gradient instabilities)

- $D = \alpha_K + \frac{3}{2}\alpha_B^2 \ge 0$ (no ghosts)

- $|\alpha_M|$ bounded (sub-luminal Planck-mass running)

- $\alpha_T \approx 0$ (gravitational wave speed constraints)

For the conformal modification implemented here, the EFT parameters map strictly to the dynamical background derivative $\alpha_A$:

\begin{equation} \label{eq:a5_alpha_M}
\alpha_M = -2\alpha_A
\end{equation}

\begin{equation} \label{eq:a5_alpha_B}
\alpha_B = 2\alpha_A
\end{equation}

\begin{equation} \label{eq:a5_alpha_K}
\alpha_K = -5\alpha_A^2
\end{equation}

\begin{equation} \label{eq:a5_alpha_T}
\alpha_T = 0
\end{equation}

The substitution of the kineticity and braiding terms into the physical no-ghost discriminant yields an exact identity:

\begin{equation} \label{eq:a5_ghost_identity}
D = (-5\alpha_A^2) + \frac{3}{2}(2\alpha_A)^2 = \alpha_A^2
\end{equation}

This identity shows that the no-ghost discriminant is non-negative, $D = \alpha_A^2 \ge 0$. Because the finite-turnover profile $f_T(z)$ has a single extremum, $\alpha_A$ vanishes at the turnover redshift $z_\star$ (for $z_T=5$, $n_T=2$: $z_\star \simeq 2.64785$), and $D$ touches zero there for every nonzero $\epsilon_T$. For $D > 0$, the scalar branch has positive kinetic normalization $Q_s = 2M_\star^2 D/(2-\alpha_B)^2 > 0$ and the adopted luminal conformal-frame limit $c_s^2 = 1$ applies. At $z_\star$, $D = Q_s = 0$, so the propagating scalar description becomes degenerate and a propagation speed is not physically defined. The linear `hi_class` system passes continuously through this point without numerical divergence, as verified by the diagnostic reported in Section 3.3. Whether this degeneracy represents exact constraint reduction or a strong-coupling limit at the nonlinear level requires a separate analysis and is outside the scope of the present linear closure. A fully derived sound-speed expression for the disformal and nonlinear screening sectors is likewise outside the scope of the present pure-conformal closure.

The production codebase applies these adopted closure values during the calculation of the SMG perturbation coefficients, ensuring the pure-conformal branch is evaluated consistently without requiring pre-tabulated interpolation or analytical approximations.

# Unified TEP Parameter Dictionary

The TEP corpus uses related but distinct symbols across its papers. This dictionary maps every parameter, its definition, the paper where it is primary, and its fiducial or fitted value.

| Symbol | Definition | Primary Paper | Fiducial / Fitted Value |
| --- | --- | --- | --- |
| $A_{\rm clock}(z)$ | Exact observational clock/redshift map: $A_{\rm clock}=(1+z)^{-1}$ | TEP-TH | $(1+z)^{-1}$ (exact) |
| $A_{\rm dyn}(z)$ | Dynamical shear response: $\left(1+z/z_t\right)^{-\epsilon_t}$ | TEP-TH | Modifies late-time evolution |
| $\alpha_A$ | Temporal-shear conformal amplitude in Jordan-frame notation | TEP-HC | $-0.0028$ (Planck best-fit) |
| $\alpha_M$, $\alpha_B$, $\alpha_K$, $\alpha_T$ | Runtime Bellini–Sawicki EFT functions: $\alpha_M=-2\alpha_A$, $\alpha_B=2\alpha_A$, $\alpha_K=-5\alpha_A^2$, $\alpha_T=0$ | TEP-HC | Adopted from $\alpha_A$ |
| $\epsilon_T^{\rm los}$ | Late-time line-of-sight transport amplitude (C0 supernova fit) | TEP-C0 | $\mathcal{U}[0, 2.0]$ (prior); posterior peaked near $\sim 0.89$ |
| $\epsilon_T^{\rm CMB}$ | C0 background/acoustic diagnostic amplitude | TEP-C0 | $-0.0015\pm0.0037$ |
| $\epsilon_T^{\rm HC}$ | Native hi_class homogeneous conformal amplitude | TEP-HC | $0.00547\pm0.00429$ |
| $\epsilon_{\rm dyn}$ | Dynamical temporal-horizon response | TEP-TH | Determined by late-time shear |
| $\epsilon_{\rm field}$ | Primordial spectral-flow parameter constrained by $n_s$ | TEP-TH | $0.0175$ (from $n_s=0.965$) |
| $z_T^{\rm los}$ | C0 line-of-sight supernova transport turnover | TEP-C0 | $5$ (conservative), $100$ (benchmark), free (broad) |
| $z_T^{\rm HC}$ | Homogeneous/acoustic hi_class profile scale | TEP-HC | Fitted jointly with $\epsilon_T$ |
| $p$ | Temporal-horizon conformal exponent: $A_{\rm clock}\sim\eta^{-p}$ | TEP-TH | $0 \lt p\le\tfrac12$ (regular branch) |
| $r_s^{\rm TEP}/r_s^{\Lambda\rm CDM}$ | Pre-recombination sound-horizon ratio | TEP-HC | $0.999994$ ($<6$ ppm deviation) |
| $D=\alpha_K+\tfrac32\alpha_B^2$ | No-ghost discriminant (physical branch: $D=\alpha_A^2$) | TEP-HC | $\alpha_A^2\ge 0$ (non-negative; GR/decoupling limit at $\alpha_A=0$) |
| $r(k_{\rm pivot})$ | Native tensor-to-scalar ratio at Planck pivot | TEP-TH | $9\times10^{-6}$ |
| $r_{\rm max}$ | Maximum tensor-to-scalar ratio across transition profile | TEP-TH | $6.26\times10^{-4}$ |
| $H_0$ | Hubble parameter (TEP-C0 joint MCMC) | TEP-C0 | $66.70\pm0.58$ km s$^{-1}$ Mpc$^{-1}$ |
| $S_8$ | $\sigma_8\sqrt{\Omega_m/0.3}$ (TEP-HC joint MCMC) | TEP-HC | $0.868\pm0.025$ |
| $\sigma_8^{\rm HC}$ | Native hi_class matter-fluctuation amplitude at fiducial point ($\epsilon_T=0.0066$, $z_T=5$, $n_T=2$) | TEP-HC | $0.825\pm0.016$ (fiducial); $0.858\pm0.016$ (MCMC posterior mean) |

**Note:** Parameters with superscript labels ($^{\rm los}$, $^{\rm HC}$) are related projections of the same temporal sector but are not numerically interchangeable. The turnover scales $z_T^{\rm los}$ and $z_T^{\rm HC}$ describe different physical regimes; the amplitudes $\epsilon_T^{\rm los}$, $\epsilon_T^{\rm CMB}$, $\epsilon_T^{\rm HC}$, and $\epsilon_{\rm field}$ are constrained by different observables.


## Appendix B: Data Availability & Reproducibility


This work follows open-science practices. All results are fully reproducible from raw data
using the documented pipeline. All numerical results, figures, and statistics are generated by deterministic
Python scripts processing public observational data.



### Repository and Code


GitHub Repository: github.com/matthewsmawfield/TEP-HC



The repository contains a deterministic, version-controlled cosmological analysis pipeline
for CMB acoustic peak preservation tests and MCMC parameter estimation with the TEP conformal background.



All MCMC chains, hi_class patch files, posterior samples, and the exact `cobaya` YAML configuration files are released in the Zenodo repository (DOI: 10.5281/zenodo.20572722) under CC-BY 4.0. The `run_all.py` orchestration script and all step scripts are provided in the GitHub repository.



### Repository Structure


TEP-HC/
├── data/
│   ├── cobaya/              # Cobaya MCMC configurations
│   ├── external/            # Cobaya packages (likelihoods, data)
│   └── hi_class/            # TEP-CLASS implementation
├── external/
│   ├── hi_class/            # hi_class submodule
│   └── patches/             # TEP patch files
├── scripts/
│   └── steps/               # Analysis pipeline steps
├── core/                    # TEP shared constants and parameters
├── results/                 # Pipeline outputs, figures, MCMC chains
├── site/
│   └── components/          # Manuscript HTML sections
├── tests/                   # Verification tests
├── requirements.txt
├── CITATION.bib
└── README.md



### Software Environment


Key packages: NumPy, SciPy, Matplotlib, Cobaya, hi_class.
The pipeline has been tested on Python 3.10+.



### License


All code and manuscripts are released under CC-BY-4.0.