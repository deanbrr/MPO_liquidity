# G3: Capital Solutions group (structured and hybrid capital)

**Instrument library, stress behaviour, regime-dependent opportunity set and decision economics for ADIC's Capital Solutions book**

- **Stream:** G3, group dossier
- **As of:** 2026-10-18
- **Working NAV:** about US$8bn. This is the synthetic working allocation in context §1A, not ADIC data.
- **Evidence tags:**
  - **[S]** sourced fact, cited and dated. The primary document was read in this session unless noted.
  - **[C]** a trade-press summary or search excerpt not checked against the primary document.
  - **[P]** practitioner consensus.
  - **[I]** my inference, design default or synthetic calculation.
  - **[K]** a classic reference cited from knowledge whose bibliographic details were not re-verified in this session.

**Research caveats.** The shared WebSearch budget ran out several times, and the Consensus connector exposed only authentication tools (not called). Primary PDFs were read from locally extracted text: Rede NAV 2026, Proskauer NAV FY2025, Lazard 1H-2026, IMF GFSR 2024 Ch. 2, IPEV 2025, ILPA NAV Part I, Clifford Chance 2026, Erel-Flanagan-Weisbach 2024, Böni-Manigart 2022 and Blackstone's Q2-2026 10-Q. Numbers tagged [I] or "synthetic" are illustrative and must never be shown as ADIC data; the §5.6 examples were computed in this session, with equations and inputs given so they can be re-implemented. **Not verified:** Expedia's later redemption of its 2020 preferred; the 2024 Apollo-Intel and similar corporate hybrid deals; Tactical Opportunities Fund IV/V sizes beyond trade press; any market-wide preferred-equity pricing survey (none found; open question 5).

---

## 1. Executive summary

1. **What "does interesting financial deals" means [S/I].** Leading platforms describe one product: capital between senior debt and control equity that earns a contractual return plus equity participation. KKR spans "senior debt to structured equity and everything in between". Blackstone calls Tactical Opportunities a "thematically driven, hybrid capital investment strategy". Apollo Hybrid Value invests mainly in preferred and convertible structured equity. Ares offers "private debt, equity and hybrid solutions". I map the group onto seven families (§2.1): A fund finance; B GP and LP solutions; C corporate structured equity; D junior capital; E rescue and special situations; F asset-based and specialty finance; G structured LP/secondary solutions (a boundary case with Secondaries).

2. **A large, crowded, growing market [S].**
   - 2025-26 closes: Apollo HVF III US$6.5bn (May 2026); Ares Opportunistic Credit more than US$9.8bn, including ASOF III with more than US$8.3bn of equity (March 2026); Oaktree Opportunities XII about US$16bn (February 2025); 17Capital Credit Fund 2 US$7.5bn (March 2026); AlpInvest SPF II US$3.2bn (April 2025); GTCR Capital Solutions I US$1.25bn (July 2026). Blackstone Tactical Opportunities has US$44.3bn committed (June 2026).
   - NAV financing is about US$100bn outstanding (FFA, via ILPA 2024). 2030 projections run from about US$150bn to US$600-700bn depending on definition; show that spread, don't hide it.
   - Preferred and other structured solutions were 14% of GP-led secondary volume in 1H-2026, up from 10% (Lazard). KKR projects private ABF at about US$9.2tn by 2029.

3. **Pricing now, and its regime swing [S].** NAV loans (Rede, June 2026) carry weighted-average target margins of 4.8% secured and 6.1% recourse-light; banks target 3.0% secured, alternative lenders 5.6%; 36% of lenders expect spreads to rise and 17% to fall. Proskauer FY2025 shows primary LTVs mostly below 25% (largest share 5-10%), secondaries facilities at 25-70%, OID mostly 1-2%, and no minimum MOIC in 49% of facilities. With SOFR at 3.89% (15-Oct-2026), an alternative-lender secured NAV loan yields about 9.5% before fees. Spreads widened 140bp in 2022 and were 533-982bp by LTV band in 2023, so senior fund finance swings 150-250bp by regime, and junior and rescue capital swing more. Preferred terms have moved to minimum cash pay, capped PIK, step-ups and anti-priming protection (Clifford Chance, April 2026).

4. **Plan on about 9-11% net, not mid-teens [S].** Blackstone Tactical Opportunities: 1.6x gross MOIC, 10-11% total net IRR, 15-16% on realised deals (June 2026). Böni-Manigart (448 funds): mean net IRR 9.0% for mezzanine and 12.6% for special situations (median 8.0%, SD 23%). Erel-Flanagan-Weisbach (532 USD funds, 1992-2015 vintages): mezzanine 8.4%, distressed 8.3%; gross alpha of about 4% roughly equals fees, and net alpha is zero once equity risk is priced. Yield-based forecasts need haircuts for losses, extension and fees, and an equity beta.

5. **Stress shows up as PIK and extension before default [S].** Fitch's US private-credit default rate hit 6.0% (12 months to April 2026) and 6.3% to August [C]. At January 2026, 60% of trailing default events were interest deferrals or PIK introductions and 27% distressed extensions. Proskauer's narrower senior index was 2.51% in Q2-2026. The PIK share of BDC interest income doubled from 2019 to 2023 (IMF). Recoveries fall with subordination and in recessions: about 33% for direct loans vs 52% for syndicated loans (Fed FEDS Note, KBRA DLD data); 15.9-35.9% for preferred stock (Moody's); 28% historical and 18% expected for subordinated bonds (Moody's 2008). PIK-heavy junior instruments were impaired in Mallinckrodt and Cineworld.

6. **The "natural hedge against the DPI drought" is only an opportunity hedge, and only if liquidity is available [S/I].**
   - *Cash channel: no hedge.* NAV loans repay from distributions, and preferred equity switches to PIK. In a synthetic 15%-LTV NAV loan, WAL stretches from 1.3 years (normal) to 2.2 (drought) and 3.3-4.7 (crisis). Cash back by year 2 falls from 114% of outlay to 78%, then 46-21%, while IRR barely moves (10.8% to 9.9%). In a synthetic Monte Carlo, normal-to-drought cuts PE distributions by US$8.1bn and the book's cash returned by US$1.7bn: the same direction.
   - *Value channel: no hedge.* Private-debt cash flows load on equity factors (Erel et al.), and marks lag traded loans (IMF).
   - *Opportunity channel: a real hedge.* Funds raised when ex-ante BB credit spreads are wide earn higher net multiples and beat bond benchmarks (the IRR effect is positive but insignificant), while a higher ex-ante TED spread lowers outperformance (Böni-Manigart). DPI pressure is the top driver of structured-solution supply (Lazard). NAV lenders expect more DPI-motivated deals in 2026: net +17%, against −27% experienced in 2025 (Rede).
   - *The catch [I].* A 13% drought deal only breaks even at a 9% liquidity shadow price, and waiting for a crisis pays only above about 21% crisis returns. Fund counter-cyclical deployment from low-shadow-price sources (the book's own repayments, tail-hedge payoffs, pre-committed facilities, co-investment rights), not idle cash.

7. **In-house pricing for REFINANCE, with conflict controls [I].** Package the group's NAV and preferred pricing knowledge as a calibrated quote function feeding the REFINANCE rungs of the MCL curve (streams 05 and 08). Internal funding of ADIC's own PE book raises no external liquidity (context §1A): a 20% internal anchor in a US$3bn facility cuts external liquidity one-for-one to US$2.4bn. The group prices, structures and arranges; third parties fund. Because IPEV (2025) warns that indicative offers can be deliberately high or low, require an independent pricing owner, third-party RFQs and IC sign-off on related-party deals.

8. **SELL / HOLD / REFINANCE / LEVER for the book [S/I].** SELL by syndication (31% of NAV lenders syndicate, on average just under half of what they underwrite; Rede) or credit secondaries (LP credit at 91% of NAV in 2025; credit GP-led volume more than tripled; Jefferies). REFINANCE and LEVER through back-leverage (secondaries-style facilities below 3-4% at 25-70% LTV; Proskauer) or rated feeders and CFOs. On an 11%-yield book, D/E 0.5 at SOFR+3.0% lifts RoE to 12.8% with a 33% cushion to a 50% LTV trigger; D/E 1.0 adds 1.8pp but cuts the cushion to 17%.

---

## 2. Core concepts and theory

### 2.1 Taxonomy and group boundaries

| Family | Instruments | Seniority and return mechanics | Platform evidence | Boundary rule for ADIC [I] |
|---|---|---|---|---|
| **A. Fund finance** | NAV loans to funds; hybrid NAV-plus-uncalled facilities; fund-level preferred equity | Structurally senior to LP equity. Floating margin plus OID. LTV-based cash sweeps. | 17Capital Credit (advance rates 5-20% of NAV); AlpInvest; Rede/Proskauer surveys [S] | Capital Solutions as **lender**. When ADIC is the **borrower** on its own PE book, it is the PE group's REFINANCE action (§6.10). |
| **B. GP and LP solutions** | GP-commitment and management-company loans; GP stakes; LP portfolio facilities and recaps | Unsecured loans or preferred equity with seniority over portfolio cash flows. GP stakes are minority equity in managers (fee-related earnings plus carry). | 17Capital Strategic Lending (US$450m GP financing and US$970m LP facility, April 2026) [S]; Blackstone GP Stakes [S]; Blue Owl [C] | Capital Solutions. Conflict check against the PE group's GP relationships. |
| **C. Corporate structured equity** | Preferred and convertible preferred; holdco PIK notes; minority recaps | Behind funded debt, ahead of common. Dividends in cash or PIK. Minimum return; puts, calls and step-ups; warrants. | Apollo HVF; KKR Capital Solutions; GTCR; Harvest Structured Capital [S] | Capital Solutions. Aggregate exposure with Co-investment where both sit alongside the same GP. |
| **D. Junior capital** | Mezzanine; second lien; PIK-toggle debt with warrants | Subordinated debt paying cash plus PIK, plus a kicker | HPS Strategic Investment Partners (SIP V US$17bn investable) [S] | Junior debt with a kicker belongs to Capital Solutions; senior and unitranche loans belong to Private Credit. |
| **E. Rescue and special situations** | Secured rescue loans; DIP and exit financing; discounted credit; stressed structured equity | Senior to junior, priced for distress, often with warrants | Oaktree Opps XII categories; Ares ASOF III; Tactical Opportunities [S] | Capital Solutions, as a regime-dependent sleeve |
| **F. Asset-based and specialty** | Amortising receivables, equipment and royalty pools; specialty lending platforms | Overcollateralised, self-amortising, mostly fixed-rate [S: KKR] | KKR ABF; Blackstone BXCI ABF [S] | Senior ABF to Private Credit; mezzanine and equity ABF to Capital Solutions (to confirm) |
| **G. Structured LP and secondary solutions** | Preferred equity into LP portfolios; deferred consideration; tail-end solutions | Preferred claim on portfolio distributions | AlpInvest LP recaps for sovereign funds [S]; Hollyport (legacy secondaries) [C] | An equity purchase belongs to Secondaries; a senior or preferred claim belongs to Capital Solutions. |

### 2.2 Payoff geometry

Let $V_T$ be enterprise value at exit, $D_T$ the senior debt ahead of the instrument, and $C_T$ the instrument's accreted claim (principal or liquidation preference plus PIK accruals). A hybrid claim with warrants on $n_w$ new shares at strike $K$, with $n_0$ existing shares, pays:

$$\Pi_T=\underbrace{(V_T-D_T)^+-(V_T-D_T-C_T)^+}_{\text{capped senior-to-equity claim}}+\underbrace{\frac{n_w}{n_0+n_w}\big(E_T-n_0K\big)^+}_{\text{dilution-adjusted warrants}},\qquad E_T=(V_T-D_T-C_T)^+ .$$

- The claim is a long call struck at $D_T$ minus a call struck at $D_T+C_T$. It is concave around the claim and convex again through the kicker.
- A **fund NAV loan** pays $\min(B_T,\ \text{NAV}_T)$. That is debt plus a short put on a diversified NAV struck far out of the money (LTV 5-20%) [I].
- A **minimum-MOIC or minimum-return floor** adds a digital-like payoff in early-redemption states. It makes the instrument expensive for the issuer exactly when the company does well. Its convexity is the opposite of the NAV loan's (stream 05).
- A **convertible** adds $\max(R_\tau,\ \theta(V_\tau-D_\tau))$ conversion optionality.

### 2.3 Contract features as embedded options [S/I]

1. **PIK toggle:** the issuer's option to borrow from the investor at the PIK rate, exercised when the issuer is weak (adverse selection). The claim compounds while coverage erodes, which the IMF says "can lead to compounding losses" [S]. Modern terms cap accrual and add minimum cash pay [S: Clifford Chance].
2. **Dividend step-ups:** a synthetic maturity forcing refinancing. Expedia stepped up 100bp at years 5-7 and 150bp at years 8-9 [S].
3. **Call premiums and make-wholes:** compensation for the issuer's refinancing option, which leaves the investor with regime-dependent negative convexity.
4. **Puts, drag rights, step-in and springing governance:** state-contingent control transfers, the incomplete-contracts logic Kaplan and Strömberg (2003) find in VC securities [S]. Investors now "price control" alongside yield, so weaker governance costs more [S: Clifford Chance].
5. **LTV sweeps on NAV loans:** WAL shortens when portfolios distribute and lengthens in droughts, so cash velocity is pro-cyclical with PE exits even when IRR is stable (§5.6 B).

### 2.4 Default, recovery and their correlation

- **Structural view.** Default occurs when $V$ falls below the claims ahead of it (Merton 1974 [S]). A first-passage barrier represents covenants (Black-Cox 1976 [unverified: paper text not read; the reading follows its title and Ayache-Forsyth-Vetzal's description of structural models]).
- **Reduced-form view.** Default arrives at an intensity (Jarrow-Turnbull 1995), which is stochastic in Lando's (1998) Cox-process framework. Recovery is a fixed fraction of an equivalent default-free bond in Jarrow-Turnbull, and a fraction of pre-default market value in Duffie-Singleton (1999) [S]. §3.1 uses recovery of the accreted claim [I].
- **Default and recovery move together.** Recoveries are lower when default rates are high (Altman, Brady, Resti and Sironi 2005 [S]) and when the defaulter's industry is in distress (Acharya, Bharath and Srinivasan 2007 [S]). A crisis therefore raises PD and LGD together. This matters most for families C to E, where LGD is already high.

### 2.5 Valuation practice and the lag

- **IPEV (December 2025) [S]:**
  - Non-traded debt is valued by a yield analysis or DCF. The implied spread is calibrated at entry, then the rate and spread are moved for market and credit changes.
  - "Par value or face value or cost value is not automatically Fair Value, even if there is sufficient Enterprise Value to cover the liability."
  - Warrants are valued separately from the loan.
  - Rolled-up (PIK) interest is carried at the expected present value of the recoverable amount.
  - Convertibles are split into debt and equity components.
- **IMF (2024) [S]:** BDC loan marks react much less to credit shocks than B-rated leveraged-loan prices. The gap is absorbed by BDC share discounts and persists for several quarters.
- **Implication:** reported returns on families A to F are smoothed. True betas are higher than mark-based estimates, and covenant tests on reported NAV trigger late [I].

### 2.6 The natural-hedge hypothesis, formalised [I]

Let $d_t$ be ADIC's PE distributions, $c_t$ the Capital Solutions book's cash returned (income plus principal net of losses), $\Delta V^{CS}_t$ and $\Delta V^{PE}_t$ economic value changes, $\pi_t$ the expected excess return on new Capital Solutions deployment, and $\ell_t$ ADIC's liquidity shadow price (stream 08). The hedge has three testable conditions:

$$\textbf{cash: } \operatorname{Cov}(c_t,d_t)<0;\qquad \textbf{value: } \operatorname{Cov}(\Delta V^{CS}_t,\Delta V^{PE}_t)<0;\qquad \textbf{opportunity: } \operatorname{Cov}(\pi_t,d_t)<0\ \text{and}\ \pi_t>\ell_t\ \text{in drought states}.$$

The evidence in §4 and the synthetic tests in §5.6 indicate:
- the first two conditions fail;
- the third holds on its first leg;
- the second leg of the third, $\pi_t>\ell_t$, is precisely what is in doubt when ADIC itself is liquidity-constrained.

---

## 3. Methods, models and trade-offs

### 3.1 Contractual cash-flow engine: a state machine per position

**State.** Each position $i$ carries $z_{i,t}=(C_{i,t},\ \text{status}_{i,t},\ \text{age}_{i,t},\ h_{i,t},\ \text{flags})$, with status in {performing, PIK, amended, default, workout, redeemed} and $h$ the covenant headroom. Time steps are monthly; NAV-linked tests are quarterly with reporting lag.

**Income and accrual.**

$$q_{i,t}=C_{i,t}\,r_{i,t}\Delta,\quad r_{i,t}=\mathbb 1_{\text{float}}\,b_t+m_i+\text{step}_i(\text{age}),\quad \text{cash}_{i,t}=q_{i,t}(1-a_{i,t}),\quad C_{i,t+\Delta}=C_{i,t}+q_{i,t}\,a_{i,t}$$

- $b_t$ is the floating base rate and $m_i$ the margin.
- $a_{i,t}\in[0,\bar a_i(\text{age})]$ is the PIK share. Two limits apply: the contractual window, such as Expedia's 100% option to year 3 and 50% to year 6, and a cumulative cap $\sum_u q_{i,u}a_{i,u}\le\kappa^{PIK}_iC_{i,0}$.

**Principal.**
- NAV loans: $P_{i,t}=\min\{C_{i,t},\ \sigma_i(\ell_{i,t})\,(D^{pool}_{i,t}-\text{cash}_{i,t})^+\}$, where $\sigma$ steps up with $\ell=C/\text{NAV}$.
- ABF: a scheduled amortisation.
- Preferred, holdco and mezzanine: bullet.

**Redemption at call, exit or maturity.**

$$R_{i,t}=\max\Big\{\kappa_i(\text{age})\,C_{i,t},\ \ m^{\min}_iI_{i,0}-\textstyle\sum_{u<t}\text{cash}_{i,u},\ \ MW_{i,t}\Big\}$$

$\kappa$ is the call premium schedule, for example 105/103/102/101/100% (Expedia), and $MW$ a make-whole.

**Default and workout.** The claim converts to $R^{rec}_{i}C_{i,\tau_d}$, paid after a workout lag of 12-24 months [I]. Distressed exchanges and amendments are modelled as status changes (margin up, PIK on, maturity extended), not as terminal defaults. Fitch counts them as default events [S], so the amendment hazard is calibrated to Fitch's event mix and only a fraction of amendments later become loss events.

### 3.2 Hazards (competing risks), regime- and exit-factor-dependent

$$\lambda^{d}_{i,t}=\exp\!\big(\alpha^{d}_{f,S_t,x_t}+\beta_1\ln\text{Cov}_{i,t}+\beta_2\,\text{ICR}^{-1}_{i,t}+\beta_3\,\text{OAS}^{HY}_t\big)$$

$$\lambda^{p}_{i,t}=\exp\!\big(\alpha^{p}_{f,S_t,x_t}+\gamma_1(y_i-y^{refi}_t)^++\gamma_2x^{exit}_t\big)\mathbb 1\{\text{age}>t^{nc}_i\}$$

$$p^{PIK}_{i,t}=\operatorname{logit}^{-1}\!\big(\theta_{f,S_t}+\theta_1\text{ICR}^{-1}_{i,t}+\theta_2\mathbb 1\{x_t=\text{drought}\}\big),\qquad \text{LGD}_{i}\sim\text{Beta}\big(\mu_{sen,S_t}(\text{Cov}_{i,\tau}),\phi\big)$$

- $f$ is the family, $S_t$ the regime in {expansion, inflationary late-cycle, crisis, recovery}, and $x_t$ the persistent exit factor (drought or normal). Both follow the shared scenario engine in cluster C1.
- Cov is enterprise-value or NAV coverage of the claim, ICR is interest cover, and $t^{nc}$ is the non-call period.
- The exit hazard of the underlying company comes from the PE engine (stream 04). It triggers redemption plus the kicker.

### 3.3 Structural kicker and conversion valuation

$$\ln V_{t+\Delta}=\ln V_t+\big(\mu_{S_t}-\tfrac12\sigma^2_{S_t}\big)\Delta+\sigma_{S_t}\sqrt\Delta\,\varepsilon_t+J_t\mathbb 1\{S_t=\text{crisis}\}$$

- This is simulated jointly with the PE engine's company and factor shocks, so the same $V$ paths drive the PE, Co-investment and Capital Solutions books. That avoids double-counting or inconsistent marks.
- Payoffs follow §2.2.
- Issuer call and holder conversion or put decisions are optimal-stopping problems, solved by least-squares Monte Carlo (Longstaff-Schwartz 2001 [S]) or on a lattice.
- For convertibles with credit risk, use the Ayache-Forsyth-Vetzal (2003) [S] partial-differential-equation (linear-complementarity) formulation with an explicit default and recovery model. Use the Tsiveriotis-Fernandes (1998) split only as a benchmark: a cash-only part discounted at a risky rate, and an equity part discounted at the risk-free rate. AFV show that it can be internally inconsistent.

### 3.4 NAV-loan pool model

- Use stream 04's regime-switching, factor-driven Takahashi-Alexander model (RFT-TA; Takahashi & Alexander 2002) for the borrower fund: economic NAV, a reported-NAV filter, and a distribution hazard driven by the exit factor.
- The loan is then:

$$B_{t+1}=B_t-\sigma(\ell_t)\big(D^{pool}_t-I_t\big)^+,\quad I_t=B_t r_t\Delta,\quad \ell_t=\frac{B_t}{N^{rep}_t}$$

- Covenants run on **reported** NAV $N^{rep}$, which lags economic NAV:
  - $\ell^{trig}$ (sweep goes to 100%) and $\ell^{def}$ (default) are tested on reported NAV;
  - recovery is $\min(B,\ h\,N^{fire})$ at a fire-sale haircut tied to the secondary-price model (stream 05).
- Lenders call full foreclosure rare and prefer refinancing or monetisation plans [S: ILPA 2024].

### 3.5 Portfolio dependence

- Use a two-factor t-copula. One factor is credit (HY OAS and private-credit losses); the other is the PE exit factor.
- Each family has its own loadings: ABF loads lightly on the exit factor [S: KKR describes "limited sensitivity to corporate cash flows"], while families A, C and G load heavily.
- Recovery means shift down in crisis, following Altman et al. and Acharya et al. Concentration is aggregated by look-through company and by GP across all ADIC groups.

### 3.6 Opportunity-set model

- **Deal arrival:** $N^{opp}_{f,t}\sim\text{Poisson}\big(\Lambda_f(S_t,x_t)\big)$.
- **Pricing:**

$$s_{f,t}=s_{f,0}+s_{f,1}\,\text{OAS}^{HY}_t+s_{f,2}\mathbb 1\{x_t=\text{drought}\}+s_{f,3}\,\text{BankShare}_t$$

  This follows C1's NAV-loan rule (SOFR + $s_0$ + $s_1$·HY OAS) plus a competition term, because banks took 60% of 2025 NAV volume at lower margins [S: Rede].
- **Calibration:** funds launched when ex-ante BB credit spreads are higher earn higher net multiples and outperform IG and HY bond benchmarks (the IRR coefficient is positive but insignificant). A higher ex-ante TED spread lowers outperformance [S: Böni & Manigart 2022, Table 5]. Calibrate the spread effect on multiples or PME rather than IRR, and add an ex-ante funding-liquidity (TED-type spread) term to the vintage-return model [I]. Capacity is limited by team bandwidth and by the group's dry powder.

### 3.7 Trade-offs

| Approach | Best for | Strengths | Weaknesses |
|---|---|---|---|
| Contractual cash flows only (yield to expected exit) | Reporting; group forecasts | Transparent, IC-legible | Ignores extension, PIK drift, default clustering and kicker risk; overstates returns (§4.4) |
| Reduced-form hazards plus Beta LGD | Diversified pools (A, D, F); stress testing | Easy to calibrate to default and PIK statistics; handles amendments as states | Kicker and conversion values are ad hoc; needs coverage covariates |
| Structural EV plus waterfall | Single-name equity-linked positions (C, E, B-stakes) | Consistent with PE paths; prices kickers and conversion; captures default-recovery correlation | Needs EV and capital-structure data; vol calibration; computationally heavier |
| **Hybrid (recommended)** | Reduced form for pools and structural for equity-linked names, on a common factor and V-path engine | Consistent across groups; scalable | More code; requires a position-level family tag |

### 3.8 Ideas from other disciplines [I]

- **Actuarial science:** workout-recovery development triangles (Mack's 1993 distribution-free chain-ladder standard error, or bootstrap); Bühlmann (1967) credibility to shrink group forecasts toward the realised priors in §4.4.
- **Insurance:** structured solutions are "liquidity reinsurance" sold to GPs and LPs, and their premium reprices after events like catastrophe cover. That repricing is the opportunity premium.
- **Bank ALM:** internal quotes work like an FTP curve set by an independent desk (§6.10); committed undrawn back-leverage is haircut, as LCR treats committed facilities.
- **Control theory:** covenant and PIK logic is a hybrid automaton (discrete status, continuous claims), specified as an explicit state machine the challenge agent can test.
- **Operations research and machine learning:** a mixed-integer program for allocation, syndication and back-leverage sizing; survival models with monotone constraints and conformal intervals for PIK toggles and amendments.
- **Real options:** dry powder and standby capacity are options on regime shifts (§5.6 C2).

---

## 4. Empirical evidence and current market data (dated, sourced)

### 4.1 Platforms that define the space

| Platform | Vehicle | Size and date | Mandate | Tag |
|---|---|---|---|---|
| Apollo | Hybrid Value Fund III | ~US$6.5bn, 5-May-2026 (Fund I US$3.3bn 2019; II US$4.6bn 2022) | Structured equity incl. preferred and convertible | [S] |
| Blackstone | Tactical Opportunities | Committed US$44.3bn incl. co-invest; realised US$45.1bn at 1.9x, unrealised US$16.6bn at 1.2x; 1.6x gross; net IRR 11% total, 16% realised (30-Jun-2026) | Hybrid capital, frequent use of structure | [S] 10-Q |
| Blackstone | GP Stakes (BSCH I-II) | Net return 12% since 2014; AUM US$13.1bn (30-Jun-2026) | Minority GP stakes: cash yield plus appreciation | [S] 10-Q |
| KKR | Capital Solutions | n/a | Senior debt to structured equity | [S] |
| Ares | Opportunistic Credit / ASOF III | >US$9.8bn incl. ASOF III >US$8.3bn equity, 30-Mar-2026; >US$17bn deployed, >US$11bn realised, "de minimis" realised losses | Debt, equity and hybrid; stressed credit | [S] |
| Oaktree | Opportunities XII | ~US$16bn, February 2025 | Rescue, DIP and exit financing; "opportunistic capital solutions" | [S/C] |
| HPS (BlackRock) | SIP V; next vintage | SIP V US$17bn investable (US$12bn equity), 11-Apr-2023; next fund US$6.6bn toward US$10bn (18-Mar-2026) | Junior capital, large companies | [S]; [C] |
| Carlyle AlpInvest | SPF II | US$3.2bn (platform >US$4bn), 7-Apr-2025 | Fund, GP-commitment and LP-portfolio financings; credit secondaries | [S] |
| 17Capital (Oaktree) | Credit Fund 2; Strategic Lending | US$7.5bn, 31-Mar-2026; >US$20bn deployed in 130+ deals | NAV loans at 5-20% advance; GP and LP loans or preferred | [S] |
| Goldman Sachs | Capital Solutions Group | Formed 13-Jan-2025 | Bank financing, origination and structuring | [C] |
| GTCR | Capital Solutions Fund I | ~US$1.25bn, 29-Jul-2026 | Minority structured equity and debt | [C] |
| Harvest Partners | Structured Capital | Fact sheet 30-Jun-2025 | PIK preferred, holdco PIK, convertible preferred, warrants; US$50-400m | [S] |
| Hollyport | Secondary Opportunities IX | US$4.5bn, November 2025 | Legacy LP-led (≤70%) and GP-led (≤30%); a Secondaries analogue | [C] |

**Verification notes.** No KKR vehicle literally named "Strategic Investments" was found. KKR's site describes Capital Solutions [S], and a 2024 KKR 10-Q excerpt describes a credit-side Strategic Investments Group doing rescue, stressed and event-driven deals [C]. "Goldman Sachs Capital Solutions" is the bank's January-2025 financing group, not an investment fund [C]. Hollyport is a legacy-secondaries buyer and maps to the Secondaries group.

**Inference [I].** ADIC's US$8bn book is about the size of one flagship hybrid fund. It therefore competes with, and can co-invest alongside, these platforms. Its edge must come from:
- ticket flexibility;
- speed;
- sovereign long-duration capital;
- information from ADIC's LP relationships, which is also the source of the conflicts in §6.10.

### 4.2 Market size and growth

| Market | Size / growth | Date | Source |
|---|---|---|---|
| PE NAV facilities | ~US$100bn now; US$600bn by 2030 | 2024 | FFA via ILPA [S] |
| | US$700bn "opportunity" by 2030 (~US$150bn deployment a year) | accessed October 2026 | 17Capital homepage [S] |
| | "about US$150bn by 2030"; ~US$60bn a year of deal flow in 17Capital's segment; ~US$4tn of unrealised buyout value | 1-Sep-2026 | 17Capital article [S] |
| NAV lending activity | Weighted-average completed per lender €330m (2023), €626m (2024 ex one outlier), €829m (2025); deals completed per lender 4.4 → 5.4; banks 60% of volume (27% in 2024); 75% of lenders expect volume growth in 2026 | June 2026 | Rede [S] |
| GP-led structured solutions | Preferred equity and other structured solutions 14% of GP-led volume (1H-2026) vs 10% (2025) | August 2026 | Lazard [S] |
| Preferred equity in secondaries | 5% of 2025 volume vs 7-10% in 2021-24 | 2026 | Campbell Lutyens via stream 05 [S] |
| Private ABF | "could reach approximately US$9.2tn by 2029"; earlier estimate US$5.2tn → US$7.7tn by 2027 | data to 31-Mar-2024; May-2023 piece | KKR [S] |
| Private credit (total) | ~US$1.7tn vs ~US$1.4tn leveraged loans and ~US$1.3tn HY | June 2023 data | Fed FEDS Note [S] |
| Credit secondaries | Credit GP-led volume more than tripled in 2025; LP credit pricing 91% of NAV | 2025 | Jefferies [S] |
| GP stakes | Blue Owl GP Stakes VI targeting US$13bn, with closing drifting into 2026 | 2025-26 | PEI [C] |

### 4.3 Pricing and terms

| Instrument | Current terms | Regime anchors | Source |
|---|---|---|---|
| **NAV loan, secured** | Weighted-average target margin 4.8% (2025) vs 5.2% (2024); banks 3.0% vs alternative lenders 5.6% | +140bp in 2022, reversed in 2023 (Rede 2025, via stream 08 verification); 2023 spreads by closing LTV 533/681/764/982bp (Proskauer, via stream 05) | Rede 2026 [S] |
| **NAV loan, recourse-light** | 6.1% (2025) vs 6.6%; banks 4.2% vs alternative lenders 6.8% | 36% of lenders expect higher spreads vs 17% lower | Rede 2026 [S] |
| **NAV facility terms (primary)** | Closing LTV: <5% (23%), 5-10% (32%), 10-25% (36%), 25%+ (9%). Fee/OID: 1-1.5% (33%), 1.5-2% (30%), 2-3% (21%). Spread: 4-5% most common; 7%+ in 21% of deals. Maturity: 5 years (45%). Sweep: LTV-based (63%), fixed (21%), none (16%). | WAL "often well short of five years" | Proskauer FY2025 [S] |
| **NAV facility terms (secondaries)** | LTV 25-50% (57%), 50-75% (43%); spread ≤3% (67%), 3-4% (33%); LTV-based sweeps (83%) | | Proskauer FY2025 [S] |
| **Lender minimum MOIC** | <1.15x (28%), 1.15-1.3x (11%), 1.3-1.45x (6%), ≥1.45x (6%), none (49%) | Weakening attributed to competition | Proskauer FY2025 [S] |
| **NAV LTV norms** | Conventional PE facilities "rarely exceed 20% LTV", seldom below 5% | | Rede 2026 [S]; 17Capital 5-20% [S] |
| **Holdco PIK vs NAV** | Narrower NAV spreads strengthen NAV loans "particularly relative to Holdco PIK notes or co-invest equity" | | Rede 2026 [S] |
| **GP financing** | Security can include carried interest, GP commitments and management fees; pricing "vary widely" | | Rede 2026 [S] |
| **Rescue preferred (Expedia, May 2020)** | US$1.2bn liquidation preference bought at 98%; 9.5% dividend; accrual allowed to year 3 and ≤50% to year 6; step-ups +100bp at years 5-7 and +150bp at years 8-9; call at 105/103/102/101/100%; 8.4m ten-year warrants at US$72 (strike notional ≈ 50% of face); board seats | Priced at near-zero policy rates [K] | Expedia 8-K [S] |
| **Structured preferred market practice (2025-26)** | Minimum cash pay plus capped PIK; step-ups after an agreed period; tighter call protection and enhanced make-wholes; consent rights over debt, asset sales and senior amendments; anti-priming and short-circuit provisions | Response to PIK-heavy impairments and liability-management disputes | Clifford Chance, 21-Apr-2026 [S]; Osler, 19-Jun-2025 [S] |

### 4.4 Realised returns: the anchor for "underwritten vs actual"

| Evidence | Result | Source |
|---|---|---|
| Blackstone Tactical Opportunities (all vehicles) | 1.6x total gross MOIC; net IRR 11% total and 16% on realised investments; main funds 10% total and 15% realised (30-Jun-2026) | 10-Q [S] |
| Böni-Manigart: 448 funds, Preqin, cut-off December 2020 | Mean (median) net IRR: all 9.19% (8.46%); mezzanine 9.04% (9.4%); special situations 12.62% (8.0%, SD 23.1%); distressed 8.37% (8.3%); direct lending 8.78% (7.9%). Net multiples: mezzanine 1.34x, distressed 1.37x. Mean PME vs HY 1.06. Top quartile IRR 23.3%, bottom −3.6%. | FAJ 78(4) [S] |
| Erel-Flanagan-Weisbach: 532 USD-denominated funds, Burgiss-MSCI, 1992-2015 vintages | Average IRR 8.6% (mezzanine 8.4%, distressed 8.3%). Risk-adjusted profit ≈ 0 with equity and bond factors (RAP −$0.001 per $1, t = −0.01; GPME with a stock factor +$0.041, t = 1.48; both insignificant). 15% of holdings (20% value-weighted) carry equity features. Gross IRR 13.9% and gross alpha ~4.1% on a 65-fund subsample, with fees ≈ 3.1-3.9% a year. | NBER w32278 [S] |
| Ares opportunistic credit | Realised loss ratio "de minimis" on more than US$11bn realised | Ares [S] (manager claim) |

**Inference [I].**
- Underwritten gross returns in the mid-teens convert to about 9-11% net realised. The gap is roughly 3-4pp of fees (EFW) plus 1-2pp of losses, extension and kicker shortfall.
- The 4-6pp gap between Tac Opps' realised and total net IRR shows that winners exit first and the unrealised remainder underperforms. This is the same adverse inventory selection seen in PE (stream 04).

### 4.5 Defaults, stress modes and recoveries

| Item | Value | Date | Source |
|---|---|---|---|
| Fitch US private-credit default rate (TTM) | 5.6% (December 2025) → 5.8% (January 2026) → 6.0% (April 2026, record) → 6.3% (August 2026) | 2026 | Funds Society [S/C], Bloomberg Law [C], Webull/Benzinga for August [C] |
| Fitch components | Model-implied credit opinion (MCO) default rate 4.5-4.7%; privately monitored rating (PMR) default rate 9.2-9.4% | January 2026 | [S/C] |
| Fitch default-event mix (TTM, 89 events) | Interest deferral or PIK introduction 60%; distressed maturity extension 27%; uncured payment default 6%; bankruptcy or out-of-court restructuring 8% | January 2026 | [S/C] |
| Proskauer Private Credit Default Index (senior and unitranche) | 2.46% (Q4-25), 2.73% (Q1-26), 2.51% (Q2-26); 716 loans, US$195.6bn | 28-Jul-2026 | Proskauer [S] |
| KBRA Direct Lending Index default rate | 1.5% TTM, par-weighted, vs 1.28% for leveraged loans | 1-Jun-2026 | J.P. Morgan via Penn Mutual [C] |
| Listed BDC stress | S&P BDC Index down more than 20% since June 2025 | 18-Jun-2026 | Penn Mutual [S] |
| PIK prevalence | PIK share of BDC interest income doubled since 2019; more than a third of public firms resembling private-credit borrowers had interest cover below 1 | April 2024 | IMF GFSR [S] |
| Losses over a cycle | Private-credit credit losses below HY and comparable to leveraged loans (2013-22); PE-sponsored loans default less in stress | April 2024 | IMF [S] |
| Recovery: direct loans vs syndicated loans vs HY | ~33% vs 52% vs 39% post-default value | February 2024 | Fed FEDS Note, KBRA DLD data [S] |
| Recovery: preferred stock (471 impairments, 1983-2008) | 35.9% where a dividend omission is not followed by a bond default; 15.9% where it is part of a bond default | 5-Nov-2009 | Moody's Analytics [S] |
| Recovery by seniority | Historical: first-lien loans 87%, second-lien 61%, senior unsecured 40%, subordinated 28%. Expected under top-heavy structures: 68%, 21%, 32%, 18%. | 24-Jun-2008 | Moody's via CFO.com [S] |
| Behaviour in restructurings | PIK-heavy junior instruments impaired, equity zero (Mallinckrodt, Cineworld) | April 2026 | Clifford Chance [S] |

### 4.6 Valuation lag

| Evidence | Source |
|---|---|
| BDC accounting prices of loans react far less to credit shocks than B-rated loan prices. Price-to-NAV discounts absorb the gap and persist for several quarters. | IMF 2024, Fig. 2.10 [S] |
| Debt is valued by yield or DCF with calibration. Par is not fair value merely because EV covers the claim. Warrants are valued separately. PIK is carried at expected recoverable value. | IPEV 2025 §§3.8, 5.6, 5.7 [S] |
| Smoothing at the fund level for PE is about 0.5 per quarter (stream 04's derivation, not a figure reported by Brown, Ghysels & Gredil 2023, whose abstract gives fund betas and total risk). Private-credit smoothing is plausibly similar or larger, given the IMF evidence. | stream 04 derivation [I]; [I] |

### 4.7 Does the DPI drought feed this book? Evidence on demand

- **The drought [S]:** MSCI's PE distribution rate was 11/9/11/11% in 2022-25 and 9% in H1-2026, against about 20% historically (stream 04).
- **NAV lenders [S: Rede 2026]:** the net share seeing more DPI-motivated deals was −53% last year and −27% in 2025, but turns to +17% for 2026 (39% expect more, 22% fewer). 42% of lenders financed continuation vehicles in 2025, and 75% expect more.
- **Secondaries [S]:** Lazard's top opportunity (30% of respondents) is "Persistent DPI and liquidity pressures"; structured solutions reached 14% of GP-led volume; credit GP-led volume more than tripled in 2025 (Jefferies); Proskauer finds liquidity demand drives secondaries NAV borrowing.
- **Competitor supply: the cyclicality evidence is mixed [S: IMF 2024, pp. 60-61]:** private-credit lending did not dry up in March 2020, but the BIS finds capital deployment in PE and private credit positively correlated with stock-market returns (Aramonte & Avalos 2021), and BDC new lending contracts when banks tighten; new lending by private-credit funds seems less procyclical than BDC lending. Where competitors do retreat in stress, the opportunity premium widens [I; corrected 2026-10-18: previously stated unconditionally].
- **Counter-evidence [S]:** most 2025 NAV loans funded follow-ons and new deals, not DPI (Rede); follow-ons were 45% of primary use of proceeds and dividend recaps 7% (Proskauer); credit-secondary issuance is held back by software exposure (Lazard). Drought demand is real but mostly growth capital and liquidity bridges for GPs, not a mirror of ADIC's own cash shortfall.

### 4.8 Regime read for the current state (October 2026)

Rates [S, stream 06]: SOFR 3.89% (15-Oct-2026); FOMC target raised to 3.75-4.00% (16-Sep-2026); 10-year UST 5.09% (16-Oct-2026). Credit [S]: Fitch's private-credit default rate is at a record, software has been re-rated (stream 04), and NAV lenders see a pricing inflection (Rede). **[I]** In C1's grid this is **inflationary late-cycle × drought**: a rich opportunity set (pricing, terms, demand), a high ADIC liquidity shadow price (stream 08 uses 9% a year for years 1-2), and a back book in its PIK and extension phase.

---

## 5. Practitioner and peer practice; case studies

### 5.1 Expedia, 2020: what crisis-regime hybrid capital looks like [S]

- **Terms (Expedia 8-K, April 2020).** Apollo and Silver Lake each bought 600,000 Series A preferred shares for US$588m: US$1,000 liquidation preference bought at 98%. Each also received warrants over 4.2m shares, 8.4m in aggregate, at US$72 with a ten-year term and net settlement.
- **Dividends.** The dividend is 9.5%, which may accrue at the issuer's option until year 3. From year 3 to year 6 at most 50% may accrue, and after that it is paid in cash. It steps up 100bp at each of years 5-7 and 150bp at years 8-9, and is subject to leverage-based adjustments.
- **Calls and governance.** Optional redemption is at 105/103/102/101% in years 1-4 and par thereafter. The preferred is non-convertible, and each investor may designate a board member.
- **Inference [I].** Warrant strike notional of about 50% of face is the crisis-regime kicker size. The PIK window is the crisis-regime cash concession. Once PIK capacity is set, investors re-take control through step-ups and call protection.

### 5.2 PIK-heavy junior capital in restructurings [S]

- In Mallinckrodt (emerged November 2023) and Cineworld (administration July 2023), PIK-heavy junior instruments emerged materially impaired, with no recovery for equity despite years of accrued dividends (Clifford Chance 2026).
- The market response, in the same source:
  - minimum cash pay;
  - caps on total PIK accrual relative to principal;
  - stronger anti-priming and short-circuit protections.

  These are now default features of the instrument library. The same source notes that conversion into common stock is often used instead of enforcement, letting investors take equity without an insolvency-style process [S]. Model conversion as a workout branch, not only an upside option.

### 5.3 NAV lending through the drought [S]

Rede (2026) describes NAV as now an established tool with margins converging on 4-7%. Banks have moved to larger recourse-light deals; alternative lenders win on flexibility (sweep, maximum LTV, acceleration grace). ILPA (2024) treats NAV facilities as fund-level leverage that should count toward LPA borrowing limits, notes that distribution-purpose proceeds are often recallable, and cites the FFA's 80/20 split between portfolio support and distributions. **[I]** As lender, Capital Solutions' drought edge is structuring flexibility, not price. As LP, ADIC must strip NAV-loan "synthetic DPI" out of its distribution forecasts (stream 05).

### 5.4 LP portfolio recapitalisations for sovereign funds [S/I]

AlpInvest's SPF II completed "LP portfolio recapitalizations for sovereign wealth funds" [S]. **[I]** That is the REFINANCE product ADIC might buy for its PE book, and also what its Capital Solutions group might sell to other LPs. A team doing both holds MNPI-adjacent knowledge of peers' liquidity and needs information barriers (§6.10).

### 5.5 Competition and capacity

Record 2025-26 fundraises (Ares, Oaktree, 17Capital, Apollo, HPS) and bank NAV pricing at 3.0% secured compress the senior end [S]. **[I]** The group's advantage lies in complex structures, mid-size tickets where alternative lenders dominate, and counter-cyclical deployment where long-dated sovereign capital is scarce. It should not compete with banks for commoditised senior NAV loans.

### 5.6 Worked examples (synthetic, computed in this session)

**A. Expedia-terms preferred under five synthetic scenarios** (price 0.98; accrued dividends compound into the preference amount [I]; warrant payoff = 0.504 × max(m−1, 0) per $1 face, where m = stock/strike):

| Scenario | IRR | MOIC | Preference amount at exit |
|---|---|---|---|
| S1 recovery: called end-year 2 at 103%, m = 1.6 | 25.6% | 1.55x | 1.00 |
| S2 base: cash pay, par at year 4, m = 1.25 | 12.8% | 1.54x | 1.00 |
| S2b base without kicker | 10.1% | 1.41x | 1.00 |
| S3 drought: PIK in years 1-3, 50% in years 4-6, par at year 6, kicker out of the money | 10.0% | 1.75x | 1.52 |
| S4 distress: restructured at year 3, recovery 35.9% | −21.7% | 0.48x | 1.31 |
| S5 default within a bond default, recovery 15.9% | −40.3% | 0.21x | 1.31 |

- In the drought, PIK preserves IRR on paper, at 10.0% with the MOIC rising to 1.75x, but defers all cash.
- The loss tail (S4-S5) is severe because the accreted claim, 1.31x of face, is exactly what is impaired.
- The kicker adds about 2.7pp in the base case.

**B. NAV loan, lender view** (15% LTV, SOFR 3.9% + 5.6%, 1.5% OID, sweep of 50%/75%/100% at LTV <20/20-30/≥30%; fund growth g and distribution rate δ by regime):

| Fund path | IRR | WAL | Maximum LTV | Cash returned by year 2 |
|---|---|---|---|---|
| Normal (g 12%, δ 20%) | 10.8% | 1.3y | 15.0% | 114% of outlay |
| Drought (6%, 10%) | 10.3% | 2.2y | 15.0% | 78% |
| Crisis (−25% de-smoothed, then recovery) | 10.1% | 3.3y | 18.6% | 46% |
| Deep crisis (−45%, −10%) | 9.9% | 4.7y | 31.8% | 21% |

The IRR is robust. Cash velocity collapses when PE distributions collapse, which is the cash-channel failure of the natural-hedge claim.

**C. Natural-hedge Monte Carlo** (20,000 paths × 10 years; Markov states N/D/C with rows (.80, .15, .05), (.20, .72, .08), (.15, .55, .30); starting in D; PE NAV held at US$70bn with distribution rates 20/10/6%. The Capital Solutions book is US$8bn: 40% fund finance, 35% structured equity with PIK share 25/50/80% and exit rate 25/10/5%, and 25% ABF amortising at 30%. Annual losses: fund finance 0.2/0.5/3%, structured equity 1/3/10%, ABF 1/2/5%.)

| State | PE distributions | CS cash income | CS cash returned |
|---|---|---|---|
| Normal | US$15.4bn | US$0.74bn | US$4.11bn |
| Drought | US$7.4bn | US$0.63bn | US$2.43bn |
| Crisis | US$3.4bn | US$0.47bn | US$1.38bn |

- The book's cash returned moves with PE distributions (correlation +0.96, largely by construction), while the opportunity index moves against them (−0.91).
- Moving from N to D costs −US$8.1bn of PE distributions and −US$1.7bn of Capital Solutions cash. The book amplifies the shortfall by about 21% rather than offsetting it.

**C2. Deploy now or wait.** The excess value per $1 is $(\text{IRR}_s-r_f-\ell_s)\times4$ years, with $r_f$ = 4%, expected IRR 11/13/16% in N/D/C, and waiting values solved on the Markov chain:

| Shadow price ℓ (N, D, C) | From N: deploy now vs wait for D/C | From D: deploy now vs wait for C |
|---|---|---|
| 0.5%, 3%, 6% | 0.26 vs 0.20 | 0.24 vs 0.15 |
| 0.5%, 6%, 12% | 0.26 vs 0.08 | 0.12 vs 0.00 |
| 0.5%, 9%, 15% | 0.26 vs −0.03 | 0.00 vs −0.08 |

- Holding idle dry powder for the "hedge" does not pay under these assumptions.
- Waiting from D only pays if crisis deals return at least 20.8% (with ℓ_C = 12%).
- At ℓ_D = 9%, a 13% drought deal is only break-even.

**D. Back-leverage on an 11%-yield book** (50bp a year of facility fees per unit of debt):

| Lender pricing | D/E | RoE | Book LTV | Asset fall to trigger |
|---|---|---|---|---|
| Bank, SOFR+3.0% | 0.5 | 12.8% | 33% | −33% (to 50% LTV) |
| Bank, SOFR+3.0% | 1.0 | 14.6% | 50% | −17% (to 60% LTV) |
| Alternative lender, SOFR+5.6% | 0.5 | 11.5% | 33% | −33% |
| Alternative lender, SOFR+5.6% | 1.0 | 12.0% | 50% | −17% |

**E. Internal anchoring of ADIC's own NAV facility** (US$20bn pool, 15% LTV, US$3bn facility):

| Lender pricing | Internal anchor | External liquidity | External interest |
|---|---|---|---|
| Bank, 3.0% | none | US$3.0bn | US$207m a year |
| Bank, 3.0% | 20% | US$2.4bn | US$166m a year |
| Alternative lender, 5.6% | none | US$3.0bn | US$285m a year |
| Alternative lender, 5.6% | 20% | US$2.4bn | US$228m a year |

Internal anchoring saves interest only because it replaces external liquidity one-for-one.

---

## 6. Design implications for the ADIC framework

### 6.1 Role of the group in the total-portfolio approach (TPA) [I]

The group plays three roles, and each must be modelled separately:
- **(i) a contractual-yield book** with PE-linked cash velocity and a concave payoff;
- **(ii) a regime-contingent deployment option**, the opportunity hedge, priced against λ;
- **(iii) a pricing service** for ADIC's REFINANCE actions, under conflict controls.

Decisions are taken at total-portfolio level using the shared duals (stream 08 LAPV). Group P&L is attribution only.

### 6.2 State variables

**Position level**, per $i$:
- Claim and status: $C_{i,t}$, status, age, $h_{i,t}$.
- Coverage: $\text{Cov}_{i,t}$ and ICR.
- Underlying links: the linked EV path $V_{i,t}$, or for NAV loans the pool NAV and distributions.
- Kicker state: $(n_w,K)$ or the conversion ratio.
- Group and family tags; look-through company and GP IDs.
- Encumbrance flag.

**Book level:**
- Unfunded commitments $U^{CS}_t$.
- Dry powder $DP_t$.
- Back-leverage $B^{CS}_t$ and its LTV.
- Syndication pipeline.

**Market:**
- $S_t$ and $x^{exit}_t$ (C1).
- SOFR, HY OAS and private-credit losses.
- NAV-spread index $s^{NAV}_t$ (Rede/Proskauer-calibrated).
- Bank share of NAV lending.
- Credit-secondary price $\pi^{cr}_t$.

**Belief:** the three return series and fused forward beliefs (stream 07).

### 6.3 Decision variables (per quarter)

- New commitments by family $n_{f,t}\ge0$, either deal-by-deal or as budget envelopes.
- Sell-down or syndication fraction $x^{syn}_{i}$ at origination.
- Secondary sale $x^{sell}_{i,t}\in[0,1]$.
- Back-leverage draw or repay $b^{CS}_t$.
- Rated-feeder or CFO issuance $c^{CS}_t\in\{0,1\}$, a lumpy action with a 6-12 month lag [I].
- Amendment responses on distressed positions: grant PIK or extension, enforce, or sell.
- Standby capacity agreements $k_t$: pre-negotiated co-investment or sidecar rights, which carry a fee.
- Pricing-service outputs for PE-group REFINANCE candidates. These are information, not a decision of this group.

### 6.4 Constraints

| # | Constraint | Default |
|---|---|---|
| 1 | Liquidity survival (Tier 1): include Capital Solutions unfunded commitments, back-leverage margin and cure needs, and PIK-reduced cash income in the joint stress | α = 5% (prior deck) |
| 2 | Back-leverage LTV chance constraint: $\Pr(\text{LTV}^{CS}_t\ge\text{LTV}^{trig})\le5\%$ over the facility life under the ambiguity set | Trigger 50% at D/E ≤ 0.5 [I] |
| 3 | Encumbrance cap on the book | ≤ 40% of book NAV pledged [I] |
| 4 | Look-through concentration across all groups: company ≤ 1% of total NAV; GP ≤ 5% (all claims plus LP NAV) | [I] |
| 5 | Family budgets: E (rescue) ≤ 25% of book outside crisis; F (ABF) ≥ 15% as a low-PE-beta ballast | [I] |
| 6 | PIK budget: book-level accrued-not-paid ≤ 15% of NAV; new deals require minimum cash pay ≥ 50% of the coupon after year 2 | [I], following Clifford Chance practice [S] |
| 7 | Related-party rule: no Capital Solutions funding of ADIC's own fund interests unless external funding share is ≥ 80%, an independent price check is done and IC approves | §6.10 [I] |
| 8 | Inter-group transfers count zero toward liquidity raised | context §1A |

### 6.5 Objective terms (Tier 2)

The book contributes to the portfolio objective in four ways:
- the scenario LAPV of position cash flows, using the shared kernel $\pi_{s,t}$ (stream 08), so that PIK deferral is penalised exactly when cash is dear;
- minus risk-budget charges on de-smoothed beta (equity plus credit loadings);
- minus a liquidity charge on unfunded commitments and on back-leverage cure risk;
- plus the option value of standby capacity, valued with the same duals.

Deal acceptance rule:

$$\text{LAPV}_i-\lambda_R\,\Delta\text{CVaR}_i-\kappa^{conc}_i-\kappa^{tc}_i>0 .$$

### 6.6 Instrument library: formulas and default parameters

All parameters are [I] unless tagged. "Base" is the inflationary-late × drought state of October 2026.

| # | Instrument | Cash-flow formula (see §3.1) | Base parameters | Anchors |
|---|---|---|---|---|
| 1 | Senior NAV loan (diversified buyout pool) | Floating $b_t+m$; OID; LTV sweep σ(ℓ); bullet at T ≤ 5y | m = 5.6% (alternative lender) or 3.0% (bank); LTV 10-15%; OID 1.5%; PD 0.5% a year; LGD 20% | Rede, Proskauer [S]; PD/LGD [I] ("low default rates" [S: Rede]) |
| 2 | Hybrid NAV / fund-level preferred | Preferred return accrues (PIK); distribution sweep 50-100%; minimum MOIC; residual share θ | Accrual 12-14%; MOIC floor 1.3x; advance 15-30%; θ 0-10% | Stream 05 worked example; Lazard share [S]; pricing [I] |
| 3 | GP-commitment / management-company loan | Fixed or floating; amortises from fees and carry | 11-13%; LTV vs GP NAV 20-30%; PD 1% | Rede description [S]; 17Capital deal types [S] |
| 4 | GP stake | Fee-related earnings yield plus carry plus terminal value | Cash yield 6-8%; growth with AUM; target net 12% | BXGP 12% net [S] |
| 5 | Structured preferred (operating company) | §3.1 with step-ups, PIK window and caps, call schedule, warrants | Dividend 11-13% at today's rates; OID 2%; 100% PIK to year 2 then ≥50% cash; calls 105→100; warrant coverage 10-20% (50% in crisis); PD 3% a year; recovery 25% (range 16-36%) | Expedia, Clifford Chance, Moody's [S] |
| 6 | Convertible preferred | Max(redemption, conversion); conversion share θ | Coupon 7-9%; conversion premium 20-30% | Apollo HVF scope [S]; terms [I] |
| 7 | Holdco PIK note | Full PIK, bullet, structurally subordinated | 12-14% PIK; PD 3.5%; recovery 15% | Harvest securities [S]; Rede comparison [S]; numbers [I] |
| 8 | Mezzanine / junior debt | Cash 7-9% + PIK 2-4% + warrants 1-3% fully diluted | PD 2.5%; recovery 28% (range 18-28%) | EFW / BM returns; Moody's subordinated [S] |
| 9 | Rescue / special situations | Secured rescue loan with warrants or discounted purchase | Gross target 15-20%; PD 6-10% a year; recovery 50% (secured) | BM special situations 12.6% mean, SD 23% [S]; Oaktree categories [S] |
| 10 | ABF (mezzanine or equity tranche) | Amortising pool cash flow less losses, with overcollateralisation trigger | Yield 10-12%; pool loss 1-2% (5% crisis); WAL 2-4y | KKR features [S]; numbers [I] |
| 11 | LP portfolio preferred (structured secondary) | Priority claim on LP distributions until accrual or MOIC met | As #2 | AlpInvest LP recaps [S] |
| 12 | Rated note feeder / CFO (exit or refinance of the book) | Senior notes, mezzanine notes, retained equity; LTV and liquidity triggers | Senior LTV 35-45%; senior coupon ≈ SOFR+250-300bp | Astrea / Octus via stream 05 [S]; PBBD effective 1-Jan-2025 [C] |

### 6.7 Regime-dependent opportunity set and parameter grid

Each cell is a multiplier or add-on relative to expansion × normal. All are [I], anchored as noted.

| Item | Expansion × normal | Late-cycle × drought (now) | Crisis | Recovery |
|---|---|---|---|---|
| Deal flow Λ (A, B, C, G) | 1.0 | 1.3-1.5 (Rede / Lazard drought demand [S]) | 1.5-2.0, capacity-capped | 1.0-1.2 |
| Deal flow Λ (E rescue) | 0.3 | 0.8 | 2.0-3.0 | 0.8 |
| NAV-loan margin add-on | 0 (4.8% secured [S]) | +50-100bp (36% expect rises [S]) | +140bp (2022 [S]) to +300bp; LTV caps −5pp | −25bp |
| Structured-preferred coupon add-on; kicker coverage | 0; 5-10% | +100bp; 10-20% | +300-500bp; up to ~50% (Expedia [S]) | −50bp; 5% |
| PIK share of income (C, D) | 15% | 30% | 60-80% | 20% |
| Annual loss-relevant default rate (book-weighted) | 1.0% | 2.5% (Fitch: ~6% event rate, of which ~14% hard defaults and ~87% PIK, deferral or extension [S]; assume a quarter of soft events become losses; junior and structured names higher) | 6-8% | 1.5% |
| Recovery multiplier | 1.0 | 0.9 | 0.7 (Altman / Acharya direction [S]) | 1.0 |
| Prepayment / call hazard | 25% a year | 10% | 5% | 35% (refinancing wave) |
| Expected vintage IRR (net) | 9-10% | 11-12% | 14-18% | 9% |
| Book cash-velocity multiplier | 1.0 | 0.6 | 0.35 | 1.1 |

### 6.8 The three return series for this group

| Series | Definition | Typical bias | Correction (default) |
|---|---|---|---|
| **Underwritten** | Deal-model IRR at close: contractual cash and PIK yield + OID/fees ÷ expected WAL + expected kicker ÷ WAL − expected loss | Assumes on-schedule refinancing or exit, so WAL is too short; base-case exit multiple for the kicker; benign PD | Prior [I]: realised net ≈ underwritten gross − 4 to 6pp. EFW, BM and Tac Opps report realised returns; none of them measures underwritten returns (VL R5) |
| **Current actual** | Since-inception IRR on cash plus fair-value marks (yield method) | Marks smooth and lag (IMF); PIK carried near face; minimum-MOIC floors counted as certain | De-smooth (Geltner 1991 or Getmansky-Lo-Makarov 2004, with λ ≈ 0.5); haircut accrued PIK by p(default) × LGD; value floors with enforcement probability < 1 (Clifford Chance: formal enforcement uncommon [S]) |
| **Group forecast** | Forward "yield to expected exit" | Equals contractual yield; ignores extension, PIK drift and default clustering; kicker overstated | Fuse via credibility (stream 07): forecast − E[loss | regime] − extension drag (WAL × Δcarry) − 50% kicker haircut; weight 0.3-0.5 on group view until ADIC realised data calibrate it |

**Debiased forward return (expected IRR):**

$$\mathbb E[r_i]\approx y^{cash}_i+y^{PIK}_i\,(1-p_iL_i)+\frac{OID_i}{\text{WAL}_i(S)}+\frac{\rho\,\mathbb E[\text{kicker}_i]}{\text{WAL}_i(S)}-PD_i(S)\,LGD_i(S)-\delta^{ext}_i(S)$$

with $\rho\approx0.5$ and WAL taken from the regime-dependent sweep and prepayment hazards.

### 6.9 Test protocol for the natural-hedge claim (on ADIC data)

1. Build quarterly series from ADIC history: $d_t$ (PE distributions), $c_t$ (Capital Solutions cash returned), group deal flow and pricing.
2. Regress $c_t=a+b\,d_t+\Gamma'\text{controls}+\epsilon_t$ and $\pi^{new}_t=a'+b'\,d_t+\epsilon'_t$. Use HAC errors and a regime dummy.
3. Accept the cash hedge only if $b<0$ at 90% confidence.
4. Accept the opportunity hedge if $b'<0$ and realised vintage IRRs in drought quarters exceed ADIC's estimated $\ell_t$ plus the hurdle.
5. Report hedge ratios in dollars ($\Delta c/\Delta d$). The synthetic prior is +0.21, a procyclical amplifier.

### 6.10 In-house pricing service for REFINANCE, and conflict controls

**Quote function.** A quantile regression, or a monotone gradient-boosted model, of spread or all-in yield on:
- LTV and structure (secured, recourse-light, preferred, CFO);
- pool features (strategy, age, concentration, GP tier);
- lender type;
- regime factors.

Training data are the group's own term sheets and bids plus the Rede and Proskauer distributions. The output is a P10/P50/P90 band, which feeds the REFINANCE rungs of the MCL curve (streams 05 and 08).

**Liquidity rule.** Liquidity raised = external funding only (context §1A). Capital Solutions participation in ADIC's own facility is an investment decision, judged on its LAPV like any other. It is never a liquidity source.

**Controls [I]:**
1. **Pricing independence:** a risk or treasury desk, not the deal team, owns the quote model (the FTP principle).
2. **Market test:** at least three third-party RFQs on any ADIC refinancing; the in-house quote is the reserve price, not the execution price.
3. **IPEV §5.8 discipline:** record the motivation behind any indicative quote, since quotes may be "deliberately high" or low [S].
4. **Information barriers:** separate third-party LP and GP lending from PE-group relationship data; pre-clear any case where ADIC is both LP and lender in one fund.
5. **Compensation neutrality:** no reward for winning internal mandates.
6. **IC disclosure** of related-party economics and the competing third-party quote.

**Should ADIC refinance with third parties?** Yes, whenever the purpose is liquidity [I]. The group designs the structure and RFQ and negotiates terms. It co-invests a minority only if that lowers the external price by more than the LAPV cost of the retained risk. Each 10% internal anchor removes 10% of external liquidity (Example E).

### 6.11 SELL / HOLD / REFINANCE / LEVER for the Capital Solutions book

| Action | Definition | Economics and test |
|---|---|---|
| **SELL** | (a) Syndicate at origination (sell-down to co-investors, keep fees). (b) Secondary sale of positions or fund interests (credit LP pricing 91% of NAV in 2025 [S]). (c) Credit GP-led or strip sale. | Sell if the cash-equivalent price ≥ LAPV(hold) + κ^irr + option value (stream 08). Price = yield-based mark × (1 − regime discount); credit discount 8-12% normal, 20-30% crisis [I]. Execution probability <1 (27% of secondary processes failed or paused in 1H-2026 [S: Lazard]). |
| **HOLD** | Carry; manage amendments (PIK, extension) | LAPV of contractual flows with regime hazards; amendment decision = max(grant, enforce, sell) by LSM |
| **REFINANCE** | Asset-level back-leverage (NAV or secondaries-style facility on the book); rated-note feeder or CFO | All-in cost SOFR + 3-6% (bank to alternative lender [S: Rede, Proskauer]); covenant chance constraint; encumbrance cap. CFO senior ≈ SOFR+250-300bp at 35-45% LTV (stream 05 [S]), 6-12 month lead time [I]. |
| **LEVER** | Raise exposure (new commitments) with back-leverage | LEVER ≡ ADD + REFI (stream 08). RoE = r_A + (r_A − r_B)·D/E − fees. Example D: D/E 0.5 → +1.8pp RoE with a 33% cushion. Cap D/E at 0.5 outside expansion [I]. |

### 6.12 Synthetic-data defaults (always labelled SYNTHETIC)

- **Book:** US$8.0bn NAV in 40 positions.
- **Family weights:**
  - A (fund finance) 30%;
  - C (structured equity) 20%;
  - D (junior) 15%;
  - E (rescue) 10%;
  - F (ABF) 15%;
  - B (GP and LP solutions) 10%.
- **Commitments:** US$1.2bn unfunded (delayed-draw NAV and hybrid tranches, 30%/60% drawn).
- **Position sizes:** lognormal with median US$150m (range US$50-600m).
- **Vintages:** 2019-2026.
- **Three return series per position:**
  - underwritten gross = family base + N(0, 2pp);
  - actual = underwritten − 1.5pp ± 4pp, with 2022-23 vintages lower;
  - forecast = contractual yield.
- **Regime paths:** from the C1 engine.
- **Distressed seeds:** 3 positions in PIK/amendment status and 1 in workout, matching the 2026 environment.

### 6.13 Calibration targets and data needs

**Calibration targets:** Fitch event mix (60/27/6/8%) and PCDR of 5.8-6.3% in late-cycle × drought; Proskauer senior default rate ≈ 2.5%; recoveries of 16-36% (preferred), 18-28% (subordinated) and ≈ 33% (direct loans); Rede margin and Proskauer LTV, OID and sweep distributions; total net IRR ≈ 10-11% (Tac Opps-like) with BM/EFW strategy IRRs for synthetic vintages; NAV-loan WAL of 1.5-3 years in normal and drought regimes.

**Data needs (ADIC):** position terms (coupon, PIK windows and caps, step-ups, calls and make-wholes, MOIC floors, warrants, covenants, seniority, collateral); monthly cash flows and quarterly marks with methodology; underwriting models; amendment history; look-through EV and leverage; the term-sheet and bid archive; back-leverage documents; syndication history; the related-party register.

### 6.14 SPECIFICATION CARD (Capital Solutions, G3)

| Field | Specification |
|---|---|
| **Scope** | Families A-G (§2.1). Junior debt with a kicker → Capital Solutions; senior/unitranche → Private Credit. Equity purchase of LP interests → Secondaries; preferred claim → Capital Solutions. |
| **Data fields (per position)** | id, family, group=CS, counterparty, GP id, look-through company ids, currency, commitment, funded, unfunded, claim $C$, coupon type (fixed or float), margin, base, PIK window and cap, step-up schedule, call schedule, make-whole, minimum MOIC, put and redemption dates, warrants $(n_w,K,T)$ or conversion θ, seniority rank, collateral, LTV or coverage, ICR, covenants (trigger and default), status, amendment log, mark, mark method, underwritten IRR, actual IRR, forecast IRR, encumbrance, syndication share |
| **Cash-flow equations** | $q=C r\Delta$; cash $=q(1-a)$; $C_{t+\Delta}=C+qa$ with $a\le\bar a(\text{age})$ and cumulative cap; NAV sweep $P=\min\{C,\sigma(\ell)(D^{pool}-\text{cash})^+\}$; redemption $R=\max\{\kappa C,\ m^{\min}I_0-\sum\text{cash},\ MW\}$; default → $R^{rec}C$ after a 12-24 month lag |
| **Hazards** | $\lambda^d,\lambda^p$ and $p^{PIK}$ per §3.2, with intercepts by (family, regime, exit factor); LGD ~ Beta(μ(seniority, regime, coverage), φ = 4); default-recovery correlation through the regime |
| **Kicker** | Structural $V$ paths shared with PE / Co-investment; dilution-adjusted warrant payoff $\frac{n_w}{n_0+n_w}(E-n_0K)^+$; conversion $\max(R,\theta(V-D))$; issuer calls and holder puts by LSM |
| **Parameter defaults** | §6.6 table, plus regime grid §6.7. SOFR 3.89% (15-Oct-2026); NAV secured 4.8% / recourse-light 6.1% (Rede 2026); LTV 5-20% primary, 25-70% secondaries; OID 1-2%; minimum MOIC: none in 49% of deals (Proskauer FY2025); recoveries per §4.5 |
| **Liquidity terms** | Positions illiquid. Exits via redemption, refinancing, syndication or credit secondaries (91% of NAV in 2025; 20-30% discount in crisis [I]); execution probability 0.7-0.9. Unfunded drawn per schedule plus a stress add-on (delayed-draw tranches drawn faster in stress [I]). |
| **Stress behaviour** | Late-cycle × drought: PIK share ×2, prepayment ÷2.5, cash velocity ×0.6, default 2.5%. Crisis: PIK 60-80%, recoveries ×0.7, NAV LTVs ×1.2-2.1 (synthetic B), back-leverage triggers tested monthly. Marks lag by about 2 quarters. |
| **SELL** | Syndicate / secondary / strip; cash-equivalent price vs LAPV(hold) + κ + option value |
| **HOLD** | LAPV under regime hazards; amendment policy by LSM (grant, enforce, sell) |
| **REFINANCE** | Back-leverage at SOFR+3-6% with an LTV chance constraint ≤ 5% breach; rated feeder or CFO (lumpy, 6-12 months) |
| **LEVER** | ADD + REFI; D/E ≤ 0.5 outside expansion; encumbrance ≤ 40% |
| **Forecasts and biases** | The group forecasts yield to expected exit. Biases: short WAL, kicker optimism, PD understatement, PIK carried at face. Correction per §6.8. Fused weight on group view 0.3-0.5 until ADIC realised data are available. |
| **Pricing service (for PE REFINANCE)** | Quantile model P10/P50/P90 of NAV, preferred and CFO pricing by LTV, structure and regime. Independent owner, three or more third-party RFQs, IC disclosure. Internal participation never counts as liquidity. |
| **Opportunity set** | Λ, pricing add-ons, kicker coverage and vintage IRR by regime (§6.7). Deploy-vs-wait solved with state-contingent ℓ (C2). Standby capacity valued as an option. |
| **Synthetic defaults** | §6.12, labelled SYNTHETIC |
| **Links** | PE: overlap on GPs and funds (look-through), and REFINANCE pricing. Secondaries: structured secondaries, shared MCL curve. Co-investment: shared V paths, holdco financing. Private Credit: family boundary, ABF split. Public Markets: liquid HY/loans as hedge and price proxy. Overlay: CDX HY / equity-put hedges of book beta; tail-hedge payoffs fund crisis deployment. Treasury: back-leverage, dry-powder budget. |
| **IC outputs** | Book cash-yield fan by regime; P(loss > 10% of book); P(net IRR < hurdle); PIK accrued and forecast; covenant-breach probabilities; opportunity dashboard (deal flow, pricing vs history); decision cards per position (stream 08); related-party log |

---

## 7. Implementation notes

**Libraries.** `numpy` with `numba` or `JAX` for path simulation (monthly × 120 × 50k paths × 40-100 positions is feasible vectorised by family); `pandas` for terms and ledgers; `scipy.optimize.brentq` for IRR; `QuantLib` for callable and convertible instruments and make-whole discounting; `lifelines` / `scikit-survival` for cause-specific hazards; `PyMC` / `NumPyro` for hierarchical recoveries and regime intercepts; `statsmodels` for HAC tests (§6.9); `LightGBM` (monotone) plus `MAPIE` for the quote function; `cvxpy`, plus `pyomo` or OR-Tools for lumpy syndication, CFO and back-leverage decisions.

**Algorithms.** Vectorise the state machine over paths, drawing hazards from the regime path with common random numbers across policy variants. Solve issuer calls, holder puts and amendments by LSM on (coverage, ICR, regime, age). Use importance sampling for crisis tails (C1's rare-event gates).

**Numerical pitfalls.**
1. IRR is ill-defined for PIK-only paths (no interim cash) and has multiple roots with unfunded draws. Report MOIC, NPV at the hurdle and LAPV alongside it.
2. Path-dependent floors and caps (minimum MOIC, PIK caps) make values non-convex in sizing. Grid-search the size.
3. The same EV must drive PE, Co-investment and Capital Solutions claims. Separate draws double-count diversification.
4. Covenants on **reported** NAV versus economics on de-smoothed NAV. Keep both.
5. Amendments are not terminal defaults, but Fitch counts them as default events. Calibrate amendment hazards to Fitch's event mix and loss hazards to hard defaults plus amendment conversion.
6. Recovery and default must be correlated through the regime. Independent draws understate tail loss.
7. Unit consistency: dividend accrual compounding conventions differ by document, so encode them per position.
8. Fund-level performance data (Preqin, Burgiss) cover vintages to about 2015-18, before the high-rate regime. Shrink, don't extrapolate.

---

## 8. Risks, pitfalls and limitations

- **The natural-hedge illusion.** Smoothed marks and stable IRRs hide pro-cyclical cash velocity; the book amplifies ADIC's drought shortfall (§5.6 B-C). Its hedge value lies only in cheaply funded new deployment.
- **PIK drift and stale marks** delay loss recognition: 60% of Fitch's 2026 default events are PIK or deferral [S], and IPEV requires PIK at recoverable value, not face [S].
- **Enforcement and priming risk.** Preferred enforcement is uncommon and liability-management disputes show senior flexibility priming junior capital [S: Clifford Chance]. Hazard models miss document risk; add legal-review scores.
- **Concentration and wrong-way exposure.** Lending to funds and GPs where ADIC is an LP doubles exposure to the same exit factor.
- **Competition.** Record fundraising and bank entry (60% of NAV volume [S]) compress pricing; the model must let the opportunity premium vanish in benign states.
- **Definitional inconsistency.** Default rates run from 1.5% to 6.3% by definition (KBRA, Proskauer, Fitch), and NAV market size from US$100bn to US$700bn. Always cite the definition.
- **Model risk.** Crisis parameters rest on 2008-09, 2020 and anecdotes such as Expedia; fund-performance samples pre-date the 2022+ rate regime.
- **Governance, reputation and regulation.** Conflicts are the main non-financial risk (§6.10), and rescue lending or enforcement carries reputational risk for a sovereign owner. NAIC/SVO treatment of rated feeders [C] and Basel endgame effects on bank appetite [S: Clifford Chance] are moving targets.

---

## 9. Open questions (what ADIC must supply or confirm)

1. **Mandate and mix:** holdings by family A-G and instrument; fund commitments vs co-investments vs directs.
2. **Overlap:** does the group lend to, or hold preferred in, funds or companies where PE, Secondaries or Co-investment are exposed? A look-through register is needed.
3. **Data:** position terms, cash flows, marks and mark methodology, amendment logs, underwriting models, and available vintages.
4. **Underwritten vs realised:** realised-to-underwritten gaps by family, to replace the external priors in §6.8.
5. **Pricing data:** a term-sheet and bid archive for the quote function. No market-wide preferred pricing survey was found.
6. **Governance:** group compensation, valuation ownership, related-party and information-barrier policies.
7. **Back-leverage and structured exits:** facilities, rated feeders or CFOs in place and their covenants; owner acceptability of an Astrea-like vehicle (stream 05).
8. **Boundaries:** confirm the Capital Solutions vs Private Credit (junior, ABF) and Capital Solutions vs Secondaries (structured LP solutions) rules.
9. **Risk appetite:** reputational limits on rescue capital and enforcement; any policy or compliance constraints on instruments (PIK interest, preferred dividends, enforcement).
10. **Dry powder and standby capacity:** current unfunded commitments; co-investment or sidecar rights usable as cheap standby capacity in stress.
11. **Shadow price:** the optimiser's liquidity shadow-price path (stream 08) for the deploy-vs-wait rule.

---

## 10. References

**Platforms and transactions**
1. Apollo (5-May-2026). *Apollo Hybrid Value Fund III raises $6.5 billion.* https://www.apollo.com/insights-news/pressreleases/2026/05/apollo-hybrid-value-fund-iii-raises-6-5-billion-3287636
2. Blackstone Inc. Form 10-Q, quarter ended 30-Jun-2026 (fund performance tables, segment descriptions). https://www.sec.gov/Archives/edgar/data/0001393818/000119312526340208/d158269d10q1.pdf
3. KKR. *Capital Solutions* (accessed 18-Oct-2026). https://www.kkr.com/invest/credit/capital-solutions
4. KKR & Co. Form 10-Q, Q3-2024 (Strategic Investments Group description; search excerpt [C]). https://www.sec.gov/Archives/edgar/data/1404912/000140491224000029/kkr-20240930.htm
5. Carlyle (7-Apr-2025). *AlpInvest Partners raises over $4 billion for portfolio finance platform.* https://carlyle.com/media-room/news-release-archive/alpinvest-partners-raises-over-4-billion-portfolio-finance-platform
6. HPS Investment Partners (11-Apr-2023). *HPS closes Strategic Investment Partners V.* https://www.hpspartners.com/insights-and-news/hps-investment-partners-close-capital
7. PEI Private Credit (18-Mar-2026). *BlackRock's HPS raises $6.6bn for junior capital fund* (summary only [C]). https://www.pei-privatecredit.com/blackrocks-hps-raises-6-6bn-for-junior-capital-fund/
8. Ares Management (30-Mar-2026). *Ares raises over $9.8 billion for leading opportunistic credit strategy.* https://www.businesswire.com/news/home/20260330751690/en ; text read via https://stocktitan.net/news/ARES/ares-raises-over-9-8-billion-for-leading-opportunistic-credit-byffnb8p0bwi.html
9. SFNet (13-Feb-2025). *Oaktree closes Opportunities Fund XII at $16 billion.* https://www.sfnet.com/home/chapters/canada/news-detail/2025/02/13/oaktree-closes-opportunities-fund-xii-at-$16-billion
10. Markets Media (13-Jan-2025). *Goldman Sachs creates Capital Solutions Group* [C]. https://www.marketsmedia.com/goldman-sachs-creates-capital-solutions-group
11. 17Capital. *About us*; *NAV finance*; homepage (accessed 18-Oct-2026). https://www.17capital.com/about-us ; https://www.17capital.com/nav-finance ; https://17capital.com/?p=2428
12. 17Capital (31-Mar-2026). *17Capital closes Credit Fund 2 at $7.5 billion.* https://www.17capital.com/insights/17capital-closes-credit-fund-2-at-7-5-billion
13. 17Capital (1-Sep-2026). *Structural drivers of a fast-growing asset class.* https://www.17capital.com/insights/structural-drivers-of-a-fast-growing-asset-class
14. ION Analytics / Mergermarket (12-Nov-2025). *Hollyport Capital closes Fund IX on USD 4.5bn* [C]. https://ionanalytics.com/insights/mergermarket/hollyport-capital-closes-fund-ix-on-usd-4-5bn-amid-surging-demand-for-secondaries/
15. Alternatives Watch (29-Jul-2026). *GTCR closes $1.25bn Capital Solutions strategy* [C]. https://www.alternativeswatch.com/2026/07/29/gtcr-new-capital-solutions-strategy-1-25-billion
16. Harvest Partners. *Structured Capital fact sheet, as of 30-Jun-2025.* https://harvestpartners.com/wp-content/uploads/Harvest-Partners-Structured-Capital-As-of-June-30-2025.pdf
17. Private Equity International (2025). *Blue Owl's latest GP stakes flagship to 'drift into 2026'* (search excerpt [C]). https://www.privateequityinternational.com/blue-owls-latest-gp-stakes-flagship-to-drift-into-2026/
18. Expedia Group Form 8-K (April 2020): Series A preferred and warrants. https://www.sec.gov/Archives/edgar/data/1324424/000119312520117346/d913320d8k.htm

**Market data and practice**
19. Rede Partners (June 2026). *NAV Financing Market Report 2026* (36-lender survey). https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf ; landing page https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026
20. Rede Partners (June 2025). *NAV Financing Market Report 2025* (2022 widening of 140bp; via stream 08 verification). https://www.rede-partners.com/s/Rede-NAV-report-2025_FINAL.pdf
21. Proskauer (2026). *Insights on the NAV Financing Market, Full Year 2025.* https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
22. Proskauer (2024). *Insights on the NAV Lending Market, Full Year 2023* (via stream 05). https://www.proskauer.com/uploads/insights-on-the-nav-lending-market-2023
23. Proskauer (28-Jul-2026). *Private Credit Default Index: 2.51% for Q2 2026.* https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-251-for-q2-2026
24. ILPA (2024). *NAV-Based Facilities: Part I, Overview and Current Market Practices.* https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf
25. Lazard (August 2026). *Interim Secondary Market Report 2026.* https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
26. Jefferies (10-Feb-2026). *2025 Global Secondary Market Review.* https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/
27. Campbell Lutyens (2026). *2025 Secondary Market Flash Report* (via stream 05). https://campbell-lutyens.com/media/qwydmsgy/2025-secondary-market-flash-report_campbell-lutyens.pdf
28. KKR (2025-26). *Asset-Based Finance: Private Credit Hidden in Plain Sight.* https://www.kkr.com/insights/abf-private-credit ; KKR (May 2023). *Asset-Based Finance: A Fast-Growing Frontier in Private Credit.* https://www.kkr.com/insights/asset-based-finance-fast-growing-frontier-private-credit
29. Clifford Chance (21-Apr-2026). *Control as economics: the new preferred equity playbook.* https://www.cliffordchance.com/content/dam/cliffordchance/briefings/2026/05/Control%20as%20economics.pdf
30. Osler, Hoskin & Harcourt (19-Jun-2025). *Return of the hybrid: the rise of structured equity solutions.* https://www.osler.com/en/insights/updates/return-of-the-hybrid-the-rise-of-structured-equity-solutions/
31. Funds Society (2-Mar-2026). *U.S. private credit default rate continues to climb* (Fitch PCDR). https://www.fundssociety.com/en/news/alternatives/u-s-private-credit-default-rate-continues-to-climb/
32. Bloomberg Law (18-May-2026). *US private credit defaults hit new record of 6% in April: Fitch* [C]. https://news.bloomberglaw.com/financial-accounting/us-private-credit-defaults-hit-new-record-of-6-in-april-fitch
33. Webull / Benzinga (2026). *Private credit defaults climb to 6.3% in August, Fitch says* [C, single secondary source]. https://www.webull.com/news/15578827387765760
34. Penn Mutual Asset Management (18-Jun-2026). *The PIK picture: tracking non-cash income in BDC portfolios.* https://www.pennmutualam.com/market-insights/blogs/chart-of-the-week/2026-06-18-the-pik-picture-tracking-non-cash-income-in-bdc-portfolios
35. IPEV (December 2025). *International Private Equity and Venture Capital Valuation Guidelines.* https://www.privateequityvaluation.com/Portals/0/Documents/Guidelines/2025%20IPEV%20Valuation%20Guidelines.pdf
36. Moody's Analytics (5-Nov-2009). *Preferred stock default recoveries approach those of senior unsecured bonds.* https://ir.moodys.com/press-releases/news-details/2009/Moodys-Analytics-Preferred-Stock-Default-Recoveries-Approach-Those-of-Senior-Unsecured-Bonds/default.aspx
37. CFO.com (24-Jun-2008). *Holders of distressed debt beware* (Moody's LGD expectations vs history). https://www.cfo.com/news/holders-of-distressed-debt-beware/672046/
38. Mayer Brown (February 2025). *Insurance company investment* slides (PBBD effective 1-Jan-2025) [C]. https://mayerbrown.com/-/media/files/perspectives-events/events/2025/02/insurance-company-investment-slides.pdf%3Frev=-1
39. Chapman and Cutler (2022). *NAIC bond definition and rated debt feeder funds* [C]. https://www.chapman.com/media/publication/15063_Chapman-NAIC-Bond-Definition-Rated-Debt-Feeder-Fund.pdf

**Official and academic**
40. IMF (April 2024). *Global Financial Stability Report*, Ch. 2, "The Rise and Risks of Private Credit." https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf
41. Cai, F., & Haque, S. (23-Feb-2024). *Private Credit: Characteristics and Risks.* FEDS Notes, Federal Reserve Board. https://doi.org/10.17016/2380-7172.3462 ; https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html (the recovery figures, Figure 15, are KBRA DLD data; the note cites S&P Global only for repeat defaults, and its 26-Feb-2024 correction concerns Figure 13)
42. Erel, I., Flanagan, T., & Weisbach, M. S. (2024). *Risk-Adjusting the Returns to Private Debt Funds.* NBER WP 32278 (March 2024). https://doi.org/10.3386/w32278 ; https://www.nber.org/papers/w32278. All figures in this dossier are from this version. An April 2026 draft with the same title and authors (not peer-reviewed; no journal version in Crossref) revises most of the numbers but not the conclusion.
43. Böni, P., & Manigart, S. (2022). Private debt fund returns, persistence, and market conditions. *Financial Analysts Journal* 78(4), 121-144. DOI 10.1080/0015198X.2022.2092384. https://rpc.cfainstitute.org/research/financial-analysts-journal/2022/private-debt-fund-returns-persistence-market-conditions
44. Merton, R. C. (1974). On the pricing of corporate debt: the risk structure of interest rates. *Journal of Finance* 29(2), 449-470. https://doi.org/10.1111/j.1540-6261.1974.tb03058.x
45. Jarrow, R. A., & Turnbull, S. M. (1995). Pricing derivatives on financial securities subject to credit risk. *Journal of Finance* 50(1), 53-85. https://doi.org/10.1111/j.1540-6261.1995.tb05167.x
46. Duffie, D., & Singleton, K. J. (1999). Modeling term structures of defaultable bonds. *Review of Financial Studies* 12(4), 687-720. https://doi.org/10.1093/rfs/12.4.687
47. Ayache, E., Forsyth, P. A., & Vetzal, K. R. (2003). Valuation of convertible bonds with credit risk. *Journal of Derivatives* 11(1), 9-29. https://doi.org/10.3905/jod.2003.319208
48. Longstaff, F. A., & Schwartz, E. S. (2001). Valuing American options by simulation: a simple least-squares approach. *Review of Financial Studies* 14(1), 113-147. https://doi.org/10.1093/rfs/14.1.113
49. Altman, E. I., Brady, B., Resti, A., & Sironi, A. (2005). The link between default and recovery rates. *Journal of Business* 78(6), 2203-2228. https://doi.org/10.1086/497044
50. Acharya, V. V., Bharath, S. T., & Srinivasan, A. (2007). Does industry-wide distress affect defaulted firms? Evidence from creditor recoveries. *Journal of Financial Economics* 85(3), 787-821. https://doi.org/10.1016/j.jfineco.2006.05.011
51. Kaplan, S. N., & Strömberg, P. (2003). Financial contracting theory meets the real world: an empirical analysis of venture capital contracts. *Review of Economic Studies* 70(2), 281-315. https://doi.org/10.1111/1467-937X.00245
52. *(Withdrawn 2026-10-18: Kaplan, S. N., & Schoar, A. (2005), Journal of Finance 60(4), 1791-1823, was listed but never cited in the body. The number is kept so that refs 53-55 keep their numbers.)*
53. Black, F., & Cox, J. C. (1976). Valuing corporate securities: some effects of bond indenture provisions. *Journal of Finance* 31(2), 351-367. https://doi.org/10.1111/j.1540-6261.1976.tb01891.x
54. Tsiveriotis, K., & Fernandes, C. (1998). Valuing convertible bonds with credit risk. *Journal of Fixed Income* 8(2), 95-102. https://doi.org/10.3905/jfi.1998.408243
55. Lando, D. (1998). On Cox processes and credit risky securities. *Review of Derivatives Research* 2(2-3), 99-120. https://doi.org/10.1007/BF01531332
56. Takahashi, D., & Alexander, S. (2002). Illiquid alternative asset fund modeling. *Journal of Portfolio Management* 28(2), 90-100. https://doi.org/10.3905/jpm.2002.319836
57. Geltner, D. M. (1991). Smoothing in appraisal-based returns. *Journal of Real Estate Finance and Economics* 4(3), 327-345. https://doi.org/10.1007/BF00161933 (the smoothing model behind λ in §6.8; not Geltner's 1993 *JRER* paper)
58. Getmansky, M., Lo, A. W., & Makarov, I. (2004). An econometric model of serial correlation and illiquidity in hedge fund returns. *Journal of Financial Economics* 74(3), 529-609. https://doi.org/10.1016/j.jfineco.2004.04.001
59. Brown, G. W., Ghysels, E., & Gredil, O. R. (2023). Nowcasting net asset values: the case of private equity. *Review of Financial Studies* 36(3), 945-986 (online 25-Jul-2022). https://doi.org/10.1093/rfs/hhac045
60. Bühlmann, H. (1967). Experience rating and credibility. *ASTIN Bulletin* 4(3), 199-207. https://doi.org/10.1017/S0515036100008989 (DOI 10.1017/S0515036100008023 is the 1969 sequel with the same title, *ASTIN Bulletin* 5(2), 157-165)
61. Mack, T. (1993). Distribution-free calculation of the standard error of chain ladder reserve estimates. *ASTIN Bulletin* 23(2), 213-225. https://doi.org/10.2143/AST.23.2.2005092 ([I] the probable intended work for "Mack" in §3.8, where the dossier gave no year or title)
62. Aramonte, S., & Avalos, F. (6-Dec-2021). The rise of private markets. *BIS Quarterly Review*, December 2021. https://www.bis.org/publ/qtrpdf/r_qt2112e.htm (the "BIS work" of §4.7, as cited by ref 40, p. 61)

**Sibling dossiers (internal, read-only):** `research/dossiers/04_pe_cashflows.md` (MSCI drought data, RFT-TA); `05_secondaries_navfin.md` (NAV, preferred and CFO mechanics, Proskauer 2023, Astrea); `06_leverage.md` (SOFR, FOMC, UST; NAV margins); `08_action_valuation.md` (LAPV, LEVER ≡ ADD+REFI, ℓ path); `research/clusters/C1_portfolio_math.md` (regimes, exit factor, NAV-loan spread rule).

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 (2.2 item 12; 2.4 item 4; 2.5; 2.6 items 2 and 4), `research/literature/G3_cap_solutions.lit.md` §2 and `research/literature/recheck/G3_cap_solutions.recheck.md`. Metadata for new refs 56-62 was confirmed in Crossref (ref 62 on the BIS page).

- §1 item 5 and §4.5 recovery row: the 33/52/39% recoveries are re-sourced from "S&P" to KBRA DLD data (FEDS Note Figure 15); ref 41 gains DOI 10.17016/2380-7172.3462.
- §1 item 6 and §3.6: the Böni-Manigart claim is narrowed to net multiples and PME against IG and HY bonds (IRR coefficient positive but insignificant, Table 5), and the negative ex-ante TED-spread effect is added; §3.6 adds a funding-liquidity term.
- §2.4 structural view: Black-Cox loses [K]; the first-passage reading is marked [unverified] because the paper's text was not read.
- §2.4 reduced-form view: recovery conventions separated (Jarrow-Turnbull: fraction of an equivalent default-free bond; Duffie-Singleton: fraction of market value; Lando: Cox process); Lando loses [K].
- §3.3: Tsiveriotis-Fernandes demoted to a benchmark, because AFV show it can be internally inconsistent; [K] dropped.
- §3.4: Takahashi & Alexander (2002) cited; ref 56 added.
- §3.8: "Mack" named as Mack (1993), ref 61 ([I] probable intended work); Bühlmann (1967) added as ref 60 with Crossref DOI 10.1017/S0515036100008989 (…8023 is the 1969 sequel).
- §4.4 EFW row: parenthesis relabelled. The both-factor estimate is RAP −$0.001 (t = −0.01); +$0.041 (t = 1.48) is the stock-factor GPME.
- §4.6: smoothing ≈ 0.5 attributed to stream 04's derivation, not to Brown-Ghysels-Gredil; ref 59 added.
- §4.7: the "BIS work" is named as Aramonte & Avalos (2021), ref 62; the lead now gives the IMF's "mixed" verdict (VL A3), and the opportunity-premium sentence is conditional.
- §6.8 underwritten row: "[S-anchored: EFW, BM, Tac Opps]" retagged [I], since none of these measures underwritten returns (VL R5).
- §6.8 current-actual row: Geltner specified as the 1991 *JREFE* paper (ref 57); GLM written out (ref 58).
- Ref 42: DOI 10.3386/w32278 and a note on the April 2026 revision added; figures stay on the March 2024 version.
- Ref 51: subtitle ": an empirical analysis of venture capital contracts" added.
- Ref 52: Kaplan & Schoar (2005) withdrawn as an orphan; the number is kept.
- Refs 53-55: pages and DOIs added; [K] and the failed-DOI note dropped.
