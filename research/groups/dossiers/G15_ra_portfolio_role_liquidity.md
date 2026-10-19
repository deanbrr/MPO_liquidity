# G15 — Real Assets in the total portfolio

## Inflation and diversification evidence, drought-era cash generation, the liquidity ladder, peers and organization

**Date:** 2026-10-18 · **Stream:** G15 (Real Assets cluster G10–G15) · **Status:** research dossier, design-grade · **Audience:** CIO, IC, Real Assets head, Corporate Finance (CF), TPA and quant team.

**Inputs read first.** Context §1A, re-read before finalizing: the user has now **confirmed** the sectors as real estate, infrastructure, and energy & natural resources; agriculture and timber are excluded. Real Assets invests through funds, co-investments, and direct assets or joint ventures (JVs). It sits inside the ~60% private allocation, and the $18bn size is a working figure. Also read: design brief §8 (interim Real Assets rules); groups synthesis v1.1 (§2 cash map and ladder, §3 specification format, §4 mechanisms); main synthesis v1.1 (§1, §2.3, §4.2–4.7); dossiers 03, 04, 05, 06, 07 and 08. None of them was edited.

**New computation.** `research/groups/addenda/G15_calcs/g15_ra_calcs.py` (project venv, `python -I -B`) writes `g15_ra_results.json`. It runs monthly steps on the canonical conventions: stream-G7 call table; T4′ = s\*(0.76), with exit-driven distributions at 0.45(1−θ) = 0.108× drought rates and calls ×1.38; S1 with crisis for 18 months. On top of these it adds an asset-level debt module with equity cures, an open-end redemption-queue state machine, ladder routes with market-depth caps, and public-data checks. The checks use FRED CSVs stored in `G15_calcs/data/`: BIS UAE residential prices, Brent and US CPI.

> **SYNTHETIC-DATA NOTICE.** Every Real Assets balance, sleeve, cash flow, ladder amount and stress loss below is computed on a synthetic book (§6.1) built from the working allocation v2. None of it is ADIC data, and none of it may be presented as ADIC data. Tables carrying [I-calc] book figures end with *SYNTHETIC – NOT ADIC DATA*. Public-data calculations (ODCE desmoothing, CPI-deflated index returns, UAE property cycles) are labelled [I-calc on S].

**Tags.** These follow the groups report:
- [S] sourced;
- [C] corrected;
- [P] practitioner consensus;
- [I] inference or default;
- [I-calc] synthetic arithmetic;
- [A] client statement;
- [U] unverifiable.

**Research note.** Consensus was not used, because its quota is exhausted. During the session the shared web-search budget ran out and then refilled. Some secondary facts therefore come from search-engine summaries of primary pages; these are flagged "via search summary" and are not load-bearing unless stated. Academic metadata was verified on Crossref, OpenAlex and Semantic Scholar.

---

## 1. Executive summary

**Bottom line.** For ADIC, Real Assets (RA) are three things:
- **A crisis-income floor.**
- **An inflation hedge, but only through infrastructure.**
- **A source of leverage and refinancing risk.**

They are not a drought-cash source, and they are not a liquidity reservoir. The conventional claim that "real assets produce income and help liquidity" holds only in a deep stress. In today's distribution drought, a perpetual income asset returns less cash per NAV dollar than a self-liquidating PE fund, because PE distributions include return of capital.

**Ten findings** (synthetic book: $18bn NAV, $4bn unfunded; real estate 50%, infrastructure 36%, energy & natural resources 14%).

1. **RA does not help the drought cash map; it slightly hurts it** [I-calc on S].
   - RA distributes ≈6.3% of NAV in the drought. PE distributes 9–11%: MSCI puts PE at 9% in H1-2026 [S]; stream G7 uses 11%.
   - Closed-end real-estate funds distribute only 7% of NAV, "about a third of the 10-year average" (Ares, Q3-2025) [S]. That is below PE.
   - RA nets **−$0.16bn** in the first 12 months (distributions $1.13bn, calls $1.28bn). The same NAV and unfunded run at PE rates nets +$0.76bn, so relabelling the $18bn from PE to RA lowers drought cash by ≈$0.5–0.9bn a year.
2. **RA helps in T4′, modestly.**
   - Two things drive the relief. Income persists: $0.54bn in 12 months, 3.0% of NAV, against 1.2% for PE-type exits at 0.108× drought rates. And RA's unfunded intensity is lower: U/NAV 0.22, against 0.32 for PE on census v1.1.
   - The 24-month T4′ drain is **−$2.46bn**, against −$2.69bn for PE rates at the same unfunded and −$3.76bn at PE's unfunded ratio.
   - Calls dominate: $3.33bn of calls plus $0.36bn of equity cures, against $1.23bn of distributions. Stopping new RA commitments cuts the drain to −$1.65bn [I-calc].
3. **RA is not a liquidity reservoir.**
   - Twelve-month SELL capacity is **$9.0bn** in normal markets, **$4.3bn** in the drought, **$0.9bn under T4′** (5% of NAV) and $3.6bn in an oil supply glut [I-calc].
   - Open-end queues persist: NFI-ODCE queues peaked at 19.3% of NAV in 1Q24 [S: Callan] and were "just above 10%" in Q1-2026 [S: Accordant].
   - On the queue machine, a full redemption returns 27% of ADIC's open-end stake within 12 months today and 10% under T4′ [I-calc].
   - Global LP-led secondary volume in core open-end real estate was **$2.65bn in 2025** [S: Ares], about the size of the synthetic open-end real-estate sleeve itself.
4. **Inflation: infrastructure hedges; private real estate hedges only in the long run.**
   - Real returns [I-calc on S]: NFI-ODCE −17.7% cumulative over 2022–24; MSCI private real-estate funds −14.2% over 2023–25; MSCI private infrastructure funds +19.1% over 2023–25.
   - On EDHECinfra data, infrastructure did better when US CPI was ≥ 4% (Q4-2019 to Q3-2024) [S: PGIM 2025].
   - The literature agrees:
     - real-estate returns move with *expected* inflation over the long run, not with inflation shocks, and adjust only gradually [S: Hoesli, Lizieri & MacGregor 2008];
     - listed infrastructure hedges about as well as equities, except firms with strong pricing power at 5-year horizons [S: Rödel & Rothballer 2012];
     - only direct infrastructure is even a partial short-run hedge [S: Wurstbauer & Schäfers 2015].
   - US CPI rose 3.98% in January–September 2026 [S: FRED], so the question is live again.
5. **Diversification after desmoothing is modest for real estate.**
   - Desmoothed private real estate correlates 0.66 with equities, against 0.82 for REITs [S: Shepard et al. 2015 via AQR 2019].
   - ODCE quarterly returns over 2022–26 have first-order autocorrelation 0.72. Geltner unsmoothing at φ = 0.6 deepens the 2022–24 drawdown from −18.8% to −28.2% [I-calc on S].
   - Infrastructure looks safer than its marks but not bond-like. MSCI's factor model gives a beta of 0.6 to a 50/40/10 portfolio, against ≈0.1 on smoothed valuations [S]. Infrastructure fund cash flows are "as volatile and cyclical" as other private equity [S: Andonov, Kräussl & Rauh 2021].
6. **Leverage is the hidden RA risk.**
   - Look-through LTV is **49%**: $17.4bn of non-recourse debt on $18bn of equity, and ≈$3.0bn of it matures each year. The US Mortgage Bankers Association (MBA) reports 17% of US commercial balances maturing in 2026 [S].
   - Under T4′ the levered *true* value of RA equity falls by ≈$7.3bn (41% of NAV) within 12 months, while lagged reported marks fall by only ≈$2.7bn, about a third of the true loss [I-calc].
   - Counting this debt at 100% against T5 would use 65% of the $26.6bn hard limit. RA debt therefore needs its own look-through limit, with only its contingent-recourse part (cures, guarantees) entering T5 [I].
7. **Oil-fiscal stress makes energy & NR and Gulf real estate wrong-way assets.**
   - UAE residential prices fell 36.5% from 2008Q2 to 2010Q4 and 30.2% from 2014Q4 to 2020Q3 (BIS) [I-calc on S]. Their 4-quarter changes correlate 0.32–0.36 with Brent changes at lags of 0–1 quarters.
   - Under the 2026 war, Dubai's Q3 transactions were −38% year on year and prices −5% to −15% since end-2025 [S: The National, citing Cavendish Maxwell and S&P].
   - Private energy fell 20.5% in 2015 [S: Cambridge Associates].
   - In a supply glut, the likeliest owner stress for 2027–29 (stream 03), both books lose together: −$1.0bn of true value within 12 months (−5.6% of RA NAV) and $0.7bn less 12-month ladder capacity than in the drought. In the Gulf-war state, energy income is a *transient* hedge [I-calc].
8. **Peers support 8–12% of NAV for ADIC's Real Assets, central 10%.**
   - ADIA: real estate narrowed to 2–7% (from 5–10%) in the 2025 Review; infrastructure range 2–7% [S].
   - US endowments above $3bn: ≈9% real assets, down 2pp in three years [S: Cambridge Associates FY2025].
   - NBIM: 2.1% actual (unlisted real estate 1.6%, renewables 0.5%) against limits of 7% and 2% [S].
   - GIC: 22% in its new "Real Assets" inflation bucket, which includes commodities, gold and listed assets [S].
   - The sub-limits are set in §6.7.
9. **Organization.**
   - RA brings a fourth private engine (income assets with an appraisal-smoothed NAV) and an asset-level debt module.
   - It needs boundary rules with Private Credit (real-estate and infrastructure debt), Capital Solutions (preferred equity, NAV financing), Secondaries (fund secondaries), Co-investment and PE (infrastructure-like PE).
   - Its envelope adds a look-through leverage budget and an owner-correlation budget.
   - Its shadow-IC seat brings appraisal-lag and refinancing realism, and recuses on its own envelope.
10. **Return cost.**
    - Swapping $18bn of PE for RA costs ≈$0.47bn a year of expected return, ≈26bp of NAV. This uses J.P. Morgan assumptions: PE 10.2% (2026 LTCMA), core real estate 7.9% and infrastructure 7.1% (2027 LTCMA) [S via dossiers 07 and 11]. The figure mixes LTCMA editions, a caveat noted in §8.
    - The swap buys lower beta, T4′ relief of $0.2–1.3bn over 24 months, and an infrastructure inflation hedge [I-calc].

**The Real Assets row of the cross-group cash map** ($bn; first 12 months unless stated; canonical conventions of groups synthesis §2.2) [I-calc].

| Group | NAV | Unfunded | Normal: dist / calls / **net** | Drought: dist / calls / **net** | S1: **net** | T4′: dist / calls + cures / **net** | T4′ net, 24 months | Supply glut / Gulf war: net (24 months) |
|---|---|---|---|---|---|---|---|---|
| **Real Assets** | 18.0 | 4.0 | 1.73 / 1.33 / **+0.40** | 1.13 / 1.28 / **−0.16** | **−1.14** | 0.58 / 1.78 + 0.13 / **−1.32** | **−2.46** (−1.65 with no new commitments) | −0.30 / −0.12 (−0.54 / −0.11) |
| Same NAV and unfunded at PE rates | 18.0 | 4.0 | 3.73 / 1.33 / +2.40 | 2.05 / 1.28 / +0.76 | −1.07 | 0.22 / 1.78 / −1.55 | −2.69 | as drought |

*SYNTHETIC – NOT ADIC DATA.* The second row applies stream-G7 PE rates (distributions 20% / 11% / 3.5%; T4′ at 0.108× drought). At PE's census-v1.1 U/NAV of 0.32, the second row becomes +0.30 (drought) and −2.23 / −3.76 (T4′, 12 / 24 months). New RA commitments run at $1.2bn a year, close to steady state for $4bn of unfunded. Equity cures apply to directly held sleeves only.

**IC-facing implications.**
- **(a)** Open-end core redemptions get no Tier-1 credit beyond the queue machine's P50. Lodge notices at Amber, as for hedge funds.
- **(b)** Do not present RA as drought liquidity. Present it as T4′ income and inflation protection, priced at ≈26bp of NAV a year against PE.
- **(c)** Cap energy & NR at ≤ 1.5% of NAV and GCC real estate at ≤ 1.0% of NAV, as owner-correlated exposures.
- **(d)** Set a look-through LTV limit of ≤ 50%, ≤ 60% on any directly held asset, and a maturity-wall rule: ≤ 25% of RA debt maturing within any 12 months.
- **(e)** Arrange REFINANCE capacity, meaning JV sell-down programmes and cash-out refinancing, only in Green or Amber. Under T4′ cash-out capacity is zero and JV sell-downs fall from $2.5bn to $1.1bn.

---

## 2. Core concepts and theory

### 2.1 Cash-flow anatomy: perpetual income assets versus self-liquidating funds

ADIC's Real Assets mix two economically different objects.

**(i) Perpetual income assets:** open-end core funds, JVs and direct assets. Value is a capitalized income stream,

$$V_t=\frac{NOI_{t+1}}{c_t},\qquad c_t=r_t-g_t,\qquad R_{t+1}=\underbrace{\frac{NOI_{t+1}-K_{t+1}}{V_t}}_{\text{cash yield}}+\underbrace{\frac{V_{t+1}-V_t}{V_t}}_{\text{appreciation}},$$

where:
- maintenance capex $K\approx\kappa\,NOI$, with κ ≈ 1/3 historically [S: Pagliari 2017 as used by AQR 2019];
- the free-cash-flow yield is therefore ≈(1−κ)c; NCREIF's 4.4% NOI yield in 2018 translated into 2.9% [S: AQR].

With asset-level debt at rate $i$, the equity cash yield is

$$y^E=\frac{(1-\kappa)c-LTV\cdot i}{1-LTV}.$$

**Worked example** [I-calc]: c = 4.6%, κ = 0.2, LTV = 45%, i = 5.5% → $y^E$ ≈ 2.2%. Positive leverage needs $(1-\kappa)c>i$. Core real estate has largely failed that test since the 2022–23 rate reset [I]; Accordant still finds ODCE debt "not yet broadly accretive" in Q1-2026 [S].

These assets return capital only when ADIC sells. HOLD yields income, never principal.

**(ii) Closed-end funds:** value-add/opportunistic real estate, core-plus/value-add infrastructure, energy & NR. They follow the PE commitment engine (calls on unfunded, then exit-driven distributions). Exit-driven distributions collapse in a drought exactly as PE's do.

Hence the central identity for the cash map:

$$\text{net}_{t}=\underbrace{y^{inc}_sN^{perp}_t}_{\text{sticky}}+\underbrace{d_s(e_t)N^{CE}_t}_{\text{exit-driven}}-\lambda_s U_t-\text{Cure}_t .$$

PE's distributions are almost all exit-driven: $d_s$ ≈ 20% normal, 9–11% drought. RA's blend is ≈4% sticky income plus ≈2–6% exit-driven. RA therefore wins only when $d_s(e_t)$ collapses, as in S1 or T4′. It loses whenever exits merely slow, which is today's drought.

### 2.2 Inflation hedging: two channels and two horizons

**Fama–Schwert regression.** Write

$$R_t=\alpha+\beta_E\,\mathbb E_{t-1}[\pi_t]+\beta_U(\pi_t-\mathbb E_{t-1}[\pi_t])+\varepsilon_t .$$

A complete hedge has β_E = β_U = 1. Fama & Schwert (1977) found US private residential real estate to be the one asset that hedged both components over their sample. The metadata were verified; this classic result is stated from the literature and the full text was not re-read in session [S].

**Gordon decomposition.** Under the Gordon model,

$$\Delta\ln V\approx\frac{\Delta g-\Delta r}{c}.$$

There are two channels:
- **Cash-flow channel.** Inflation raises $g$ through CPI-linked leases, regulated tariffs (RAB indexation) and toll escalators, with pass-through $\beta_\pi$.
- **Discount-rate channel.** If inflation raises real rates or risk premia, $r$ rises.

At c ≈ 4.6%, the duration term 1/c ≈ 22 means a 100bp rise in $r$ not offset by $g$ costs ≈20% of value [I-calc]. That is what 2022–24 did to core real estate (§4.1).

**Error-correction form.** The ECM separates the two horizons:

$$\Delta R_t=a+\beta\Delta\pi_t+\gamma\,(R_{t-1}-\delta\pi_{t-1}-\theta'x_{t-1})+\varepsilon_t,$$

with a small short-run β and a long-run δ near 1 (Hoesli, Lizieri & MacGregor 2008). Regime switching shows that the short-run hedge vanishes in turbulent states (Muckenhaupt, Hoesli & Zhu 2025). Infrastructure's pass-through depends on pricing power and contract design (Rödel & Rothballer 2012), and energy assets carry oil beta, not CPI beta.

### 2.3 Appraisal smoothing and desmoothing

Reported values follow $r^*_t=\phi r^*_{t-1}+(1-\phi)r_t$ (Geltner 1991, 1993). This inverts to

$$r_t=\frac{r^*_t-\phi r^*_{t-1}}{1-\phi},\qquad \mathrm{Var}(r^*)=\frac{1-\phi}{1+\phi}\mathrm{Var}(r)\ \text{(i.i.d. true returns)}.$$

Couts, Gonçalves & Rossi (2024) show that funds with similar holdings share a common smoothing component that single-fund unsmoothing leaves in, so systematic risk stays understated and average alpha is lower than previously thought [S]. Three things follow for ADIC:
- **(a)** Correlations and betas used in H and in the risk charge must be desmoothed with a pooled or common-factor model.
- **(b)** In stress, reported NAV overstates sale value: secondary buyers price true value, so the SELL haircut includes the appraisal lag.
- **(c)** The denominator effect runs in reverse at first. RA's reported share of NAV *rises* in a crash and then drifts down for 4–8 quarters.

### 2.4 Redemption rights as a run game

An open-end fund promises periodic liquidity against illiquid assets. Its redemption right is valuable in calm markets and, through strategic complementarity, worthless in a run: early redeemers are paid at stale NAV and late ones bear fire-sale costs (Diamond & Dybvig 1983 logic). Queues, gates and pro-rata payment are the contractual response. Real-asset funds therefore behave like hedge funds with soft gates (groups report §3.5): the right is a claim on a *queue*, not on cash. First-mover logic argues for lodging notices early, at Amber, because the queue is pro-rata on the queue at payment date.

### 2.5 Oil-fiscal transmission to Gulf real estate and energy assets

Two channels link Gulf property to oil:
- **The fiscal channel.** Oil revenue drives government spending, which drives employment, expatriate inflows, housing demand and developer liquidity.
- **The bank-credit channel.** Government deposits drive bank liquidity, which drives mortgage and developer credit.

Both lag oil by 2–6 quarters. Energy and NR assets load on oil directly.

ADIC's owner draw rises when oil is weak (context §1A). Both exposures are therefore wrong-way on the liability side: they lose value and cash exactly when the draw peaks. The exception is the Gulf-war state, where oil is high but Gulf assets face volume and physical risk (stream 03 state GW).

### 2.6 Organizational economics

RA is a division in ADIC's internal capital market (Stein 1997; Scharfstein & Stein 2000). Prices alone may not decentralize (Baumol & Fabian 1964), hence envelopes plus duals (groups report §4.3–4.4).

RA adds three agency problems:
- **Appraisal-based marks** give the group discretion over reported performance.
- **Capital-structure conflicts** arise when ADIC holds debt (Private Credit) and equity (RA) in the same asset.
- **Boundary arbitrage** lets a deal be labelled "infrastructure" or "PE" to land in the envelope with the lower hurdle.

---

## 3. Methods, models and trade-offs

| Task | Methods | Strengths | Weaknesses | ADIC use |
|---|---|---|---|---|
| Desmoothing | Geltner AR(1); Getmansky–Lo–Makarov MA(q); Couts–Gonçalves–Rossi common-factor; transaction-based indices; listed proxies (REIT- and infrastructure-implied cap rates) | Restores risk; simple | Noise amplification as φ → 1; endpoint effects; listed proxies carry equity noise | Pooled common-factor unsmoothing for H's covariance; Geltner φ by sleeve for NAV dynamics; listed-implied cap rates as the market-implied anchor |
| Inflation-hedge estimation | Fama–Schwert; ECM/VECM; Markov-switching VECM; horizon regressions; inflation-regime conditioning (CPI ≥ 4%) | Separates horizons and regimes | Few inflation episodes; appraisal lag biases short-run β to zero | Short-run β from regime-conditioned desmoothed returns; long-run pass-through from NOI and tariff data |
| Cash-flow engine | Closed-end: PE commitment engine with income; perpetual: income + appraisal NAV; debt module with cures | One kernel for all groups | Income cuts and cures need asset data | §6.3 equations |
| Open-end liquidity | Static haircut; queue state machine | The machine reproduces 2022–26 queues | Needs fund-level queue data | §6.3, calibrated in §4.4 |
| Oil/fiscal link | Lead-lag regressions (BIS UAE versus Brent); structural fiscal module (stream 03) | Simple, public data | Short sample; regime-dependent | GCC real estate and energy & NR load on stream-03 state Z |
| SELL/REFI choice | C2 reduced cost with depth caps | Comparable across groups | Depth parameters uncertain | §6.6 |

**Trade-offs.**
1. **Pooled versus fund-level unsmoothing.** Pooled is more robust (Couts et al.), but it can mis-assign smoothing in idiosyncratic assets. Pool by sector × vehicle.
2. **Exit-driven versus income split.** Exit-driven distributions are regime-dependent, while income responds to occupancy, rents, tariffs and oil. Modelling them separately is what makes the drought/T4′ asymmetry visible. A single "distribution rate" hides it.
3. **Queue machine versus static haircut.** A static 50% haircut on open-end funds misstates *timing*. The machine shows a slow trickle that improves with rescissions, not a cliff.

---

## 4. Empirical evidence and current market data

### 4.1 Inflation hedging, including 2021–2026

**Literature** [S].
- **Fama & Schwert (1977), *JFE* 5(2):115–146.** Private residential real estate was a complete hedge against expected and unexpected inflation in their US sample (full text not re-read).
- **Hoesli, Lizieri & MacGregor (2008), *JREFE* 36(2):183–206.** In US and UK multi-factor ECMs, returns are positively linked to *expected* inflation over the long run, but not to inflation shocks. Adjustment is "gradual and not within period", and direct real estate behaves differently from equities.
- **Rödel & Rothballer (2012), *JAI* 15(1):110–123.** A panel of 824 listed infrastructure firms, 46 countries and 37 years. Listed infrastructure hedges inflation about as well as other equities. Only firms with strong pricing power do better, slightly, at five-year horizons.
- **Wurstbauer & Schäfers (2015), *JPIF* 33(1):19–44.** US data for 1991–2013. Direct infrastructure is the only asset with even a partial short-run hedge. All series co-move with inflation over the long run.
- **Muckenhaupt, Hoesli & Zhu (2025), *JREFE* 70(2):189–239.** Listed real estate's short-run hedge moves toward zero or negative in turbulent regimes. It hedges better than stocks over long horizons.
- **Neville, Draaisma, Funnell, Harvey & Van Hemert (2021), *JPM* 47(8).** Across roughly 95 years of US, UK and Japanese data, commodities are the major asset class that reliably outperforms in inflation surges; unexpected inflation hurts bonds and equities [S, via search summary]. The paper's real-estate figures were not verified [U].

**The 2021–2026 episode** [I-calc on S]. CPI is FRED CPIAUCNS, December to December. Index returns are from NCREIF and the MSCI Private Capital Benchmarks Summary, Q2-2026.

| Year | US CPI | NFI-ODCE nominal / real | MSCI private real-estate funds, real | MSCI private infrastructure funds, real | MSCI private natural resources funds, real | MSCI ACWI Infrastructure, real |
|---|---|---|---|---|---|---|
| 2022 | 6.45% | +7.5% / +1.0% | — | — | — | — |
| 2023 | 3.35% | −12.0% / −14.9% | −9.1% | +5.0% | −1.7% | +1.4% |
| 2024 | 2.89% | −1.4% / −4.2% | −5.3% | +3.4% | +0.8% | +12.3% |
| 2025 | 2.68% | +3.8% / +1.1% | −0.4% | +9.7% | +2.2% | +18.9% |
| Cumulative | — | 2022–24: **−17.7%** | 2023–25: **−14.2%** | 2023–25: **+19.1%** | — | — |

Further data points:
- **2026.** CPI rose 3.98% in January–September (3.74% year on year to September) as the Gulf-war oil shock fed through [S: FRED].
- **Infrastructure in high-inflation regimes.** EDHECinfra infrastructure equity returned more in CPI ≥ 4% regimes over Q4-2019 to Q3-2024, by over 1pp a quarter in network utilities and transport, and beat MSCI ACWI and the Bloomberg Global Aggregate in those periods [S: PGIM, Chen & Shen, 14 Apr 2025].
- **Five-year cumulative returns.** Natural resources +60% and infrastructure +56% were the best in private capital to Q2-2026; private real estate managed +4% [S: MSCI].

**Reading.** In 2022–24 the discount-rate channel swamped the cash-flow channel for real estate.
- Income held up: the ODCE income return was 3.35% in the year to 1Q-2023 and 4.09% in 2025 [S: NCREIF].
- Appreciation absorbed the cap-rate reset: ODCE cap rates now sit at "roughly the 4.5% to 4.7% range" [S: Accordant].
- Infrastructure, with indexed tariffs and operating cash flows that are less rate-sensitive, kept its real value [I].

### 4.2 Diversification after desmoothing

- **Real estate.** Desmoothed private real estate correlates 0.66 with equities, against 0.82 for REITs, and 0.77 with REITs [S: Shepard et al. 2015, as reported by AQR 2019]. AQR expects desmoothed unlevered volatility of ≈11%, against ≈9% for 60/40 [S]. Over 1980–2012 REITs outperformed NCREIF by 1–3% a year unadjusted; the gap almost disappears after leverage and sector adjustment [S: AQR, citing Ang et al. 2013].
- **NFI-ODCE, 2022Q1–2026Q2** [I-calc on S: 18 quarterly gross returns from NCREIF's 2Q-2026 webinar].

  | | Reported | Geltner φ = 0.5 | φ = 0.6 | φ = 0.7 |
  |---|---|---|---|---|
  | Maximum drawdown | −18.8% | −24.2% | −28.2% | −35.5% |
  | Quarterly volatility | 3.1% | 4.0% | 4.7% | 6.2% |
  | Worst quarter | — | −10.5% | −13.3% | −17.8% |

  Reported AC1 is 0.72, and the worst quarter is 2022Q4 at every φ. ODCE's 40-year 3-year-trailing standard deviation is 6.9%, against 9.6% for NAREIT [S: NCREIF].
- **Infrastructure.** MSCI's beta to a 50/40/10 portfolio is ≈0.1 on smoothed valuations, ≈0.2 as a bond proxy, **0.6** in its factor model and 1.3 for listed US infrastructure [S: MSCI, Aug 2021]. Infrastructure *fund* cash flows are as volatile and cyclical as PE's and depend on quick exits [S: Andonov, Kräussl & Rauh 2021].
- **Risk-adjusted fund performance.** Average risk-adjusted profit per $1 committed is −17¢ for real estate and −10¢ for infrastructure funds [S: Gupta & Van Nieuwerburgh, verified in dossier 04].

### 4.3 Drought-era cash generation

| Item | Value | Source, as of |
|---|---|---|
| PE distribution rate | 9% (H1-2026); 11% (2025); all private capital 10–11%; historical ≈20% | MSCI Private Capital Benchmarks Summary, Q2-2026 [S] |
| Real-estate fund distributions | 7% of NAV, rolling four quarters, about a third of the 10-year average; distributions at a 10-year low | Ares, 11 Feb 2026 (data to Q3-2025) [S] |
| 2024 real-estate fund distributions | 9-month distributions −19% versus 2023 and −75% versus 2022 | Ares 2024 review [S, via search summary] |
| NFI-ODCE income return | 4.08% gross, trailing year to 2Q-2026 (total 4.45%); 3Q-2026 preliminary quarter 1.71% (income 1.02%) | NCREIF [S] |
| NFI-ODCE investor flows, 2025 | Contributions $12.2bn; distributions and redemptions $19.9bn; net −$7.7bn; 25 funds, GAV $277.5bn, NAV $227.3bn, leverage 27.1% (average 22.3% since 2000, range 15–34%) | NCREIF 4Q-2025 release [S] |
| Infrastructure fund yields | Open-end: target return ≈10%, yield ≥ 6%. Closed-end core/core-plus: 4–5%. Value-add: 3–4% | bfinance via Infralogic, 5 Jun 2026 [S] |
| Private real-asset fund returns | 2023 / 2024 / 2025 / Q1-26 / Q2-26: real estate −6.0 / −2.6 / 2.3 / −0.1 / 0.2; infrastructure 8.5 / 6.4 / 12.6 / 1.7 / 2.5; natural resources 1.6 / 3.7 / 4.9 / 6.9 / 3.6 (%) | MSCI, Q2-2026 [S] |

**What this does to ADIC's drought cash map.**
- Closed-end real estate, at 7%, distributes less than PE at 9%. Core income runs at 3–6%.
- RA's blended drought rate is therefore ≈6.3% of NAV, against PE's 9–11% [I-calc].
- In the drought RA helps only through its lower unfunded intensity, and on the synthetic book that is not enough: −$0.16bn.

### 4.4 Open-end queues, 2022–2026, and other gating precedents

| Date | NFI-ODCE queue or event | Source |
|---|---|---|
| GFC | Queues peaked at ≈15% of NAV | Callan [S] |
| 1Q24 | Peak at **19.3% of NAV** | Callan [S] |
| 4Q24 | Average 16.4%, median 13.4%; large funds 6–33%, one outlier at 56%; the decline came mostly from rescissions | Callan [S] |
| 3Q25 | ≈12% | Accordant [S, via search summary] |
| Q1-26 | "Just above 10% of NAV". Redemption payments "exceeded 10%" in the quarter. Leverage ≈27%; cost of debt ≈4.5%, >75% fixed. Acquisitions exceeded dispositions | Accordant, 25 Jun 2026 [S] |
| Nov-2022 to Feb-2024 | BREIT requests first exceeded its limits in November 2022. It filled ≈52% in December 2023 and 88% in January 2024, then 100% ($961m) in February 2024. The caps of 2% of NAV a month and 5% a quarter, and the 43% November-2022 fill, come via search summary | Bisnow, 1 Mar 2024; Blue Vault [S] |
| 2010–2017 | German open-ended property funds: SEB ImmoInvest frozen from May 2010, liquidation decided in 2012 and to be completed by 2017. Eighteen funds holding €33bn were terminated, and by 2015 they had paid out €11.6bn | IPE Real Assets; KanAm study via REFIRE [S] |
| 2016, 2020 | UK property funds suspended after the Brexit vote and in Covid. The FCA proposed notice periods of up to 180 days (CP20/15) | FCA [S] |

**Queue-machine calibration** [I-calc].
- **Today's queue.** In 2025, redemptions net of income distributions paid out ≈4–5% of NAV a year: $19.9bn of distributions and redemptions, less ≈4% income, on $227bn. That is ≈1.2% a quarter, consistent with "just above 10%" queues falling slowly.
- **ADIC's request.** If ADIC redeems a 6% stake into that queue, it receives 7% of the stake by 3 months, 27% by 12 months and 49% by 24 months.
- **Under T4′.** Queue 12% rising to ≈20%, capacity 0.6–1.5% of NAV a quarter, marks −17%: 3%, 10% and 26%.
- **Normal markets.** 34% by 3 months and 100% by 12 months.

### 4.5 Secondary pricing and market depth

- **LP-portfolio pricing by strategy** (Jefferies, % of NAV) [S/C: dossier 05].
  - Real estate: 83 (2019), 76 (2020), 79, 71, 71, 72, 70 (2025) and ≈68 (H1-26).
  - Infrastructure: 91 (H1-26).
  - Crisis pricing for real estate is 0.45–0.50 [S/I: dossier 05 calibration].
- **Volumes.** Real-estate secondaries hit a record $20.3bn in 2025, of which GP-led $14.5bn. LP-led volume was $5.8bn: **core open-end $2.65bn** and value-add/opportunistic $3.1bn. Core discounts have "compressed to single digits for many trades". Global direct real-estate volumes are −34% versus 2021 [S: Ares, Feb 2026, citing CBRE].
- **Depth is the binding constraint.** A seller of $2–3bn of open-end or closed-end real-estate interests would be 80–100% of a year's global LP-led flow in its segment. ADIC is a price-maker, so the ladder caps ADIC at 20% of annual segment volume [I].

### 4.6 Asset-level debt and the maturity wall

- **US commercial maturities.** MBA expects $875bn to mature in 2026, 17% of $5.0tn outstanding at 31 Dec 2025 (2025: $957bn). The highest shares by type are hotel 30% and industrial 23%; office is 17% and multifamily 13% [S: MBA NewsLink, 9 Feb 2026].
- **Prices.** The Green Street CPPI was 22% below its March-2022 peak by November 2023. The core sectors combined were −25%, office −35% and multifamily −30% [S: Bisnow, 8 Dec 2023].
- **Leverage and cap rates.** ODCE leverage is 27.1% [S]. Assets are estimated at ≈17% below replacement cost [S: Accordant].
- **When leverage wipes out equity.** CPP Investments sold Greenway Plaza (Texas office) "with no net proceeds" in fiscal 2026 [S].

### 4.7 Oil-fiscal stress and Gulf real estate

**UAE residential prices** (BIS selected series via FRED, nominal, 2010 = 100; last observation Q1-2024) [I-calc on S].
- 2008Q2 151.4 → 2010Q4 96.1: **−36.5%** in 10 quarters.
- 2014Q4 174.8 → 2020Q3 122.0: **−30.2%** over 23 quarters.
- Then +43.8% to 2024Q1.

**Lead-lag with Brent** (correlation of 4-quarter log changes; prices lagging Brent by L quarters).

| L (quarters) | 0 | 1 | 2 | 3 | 4 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| Correlation | 0.32 | 0.36 | 0.31 | 0.22 | 0.16 | 0.17 | 0.25 |

The sample is 2003–2024 with overlapping windows, so the effective n is ≈20 and these correlations are suggestive, not precise.

**Dubai 2008–10** [S: IMF PIN 10/20, 17 Feb 2010].
- The "mid-2008 bursting of the Dubai property bubble" came first.
- Dubai World then sought a standstill "through May 2010, including on bonded debt owed by Nakheel" (late November 2009).
- UAE hydrocarbon export revenues fell ≈45% in 2009, from $102.7bn to $56.8bn.
- Property prices were reported to have halved [S, press report of IMF comments, via search summary].

**The 2026 Gulf war.**
- Dubai Q3-2026 home sales fell 47% by value year on year (Dh72.6bn) and 38% by count (34,000) (Cavendish Maxwell).
- Monthly sales averaged 12,644 in March–September, against 17,198 in January–February (S&P, citing Dubai Land Department).
- Prices fell 5–15% from end-2025 to September 2026. S&P expects a "gradual" correction, with apartments falling faster given a large 2027–28 supply pipeline [S: The National, 7 Oct 2026].
- **Volume falls before price**, so time-to-cash, not the haircut, is the first casualty.

**Energy and natural resources.** The Cambridge Associates private energy benchmark fell 20.5% in 2015, against −32.9% for the S&P GSCI and −25.5% for MSCI World Natural Resources [S: CA Real Asset Dynamics, June 2016]. In the 2026 oil spike, MSCI natural-resources funds returned +6.9% in Q1-2026 [S]. Energy & NR is therefore a two-sided oil position. It hedges the Gulf-war state transiently and is wrong-way in supply gluts, which stream 03 rates as the likeliest owner stress of 2027–29.

---

## 5. Practitioner and peer practice, case studies

### 5.1 Peer allocations and organization (dated)

| Peer | Real-asset allocation | Vehicles and organization | Source, as of |
|---|---|---|---|
| ADIA | Real estate **2–7%**, narrowed from 5–10% in the 2025 Review. Infrastructure **2–7%** (website range; not restated in the Review text). PE raised to 15–20% | Separate Real Estate and Infrastructure departments. Infrastructure: minority stakes "independently or alongside partners"; a financial investor not seeking operational control; direct portfolio with capital recycling; listed holdings; private credit; secondaries. Real estate: equity, debt and development, through partners and managers | ADIA website; 2025 Review [S] |
| GIC | **Real Assets 22%** (31 Mar 2026; 23% in 2025) in its new Strategic Portfolio. The three groups are Equities (growth), Fixed Income (income) and Real Assets (inflation). It increased commodities, gold and infrastructure for "inflation resilience" | Separate Real Estate and Infrastructure departments. Infrastructure is mainly private, with funds, debt and structured listed positions; real estate is private plus debt | GIC Report 2025/26, 24 Jul 2026 [S] |
| NBIM | Unlisted real estate **1.6%**, renewable infrastructure **0.5%** (30 Jun 2026). Limits are 7% and 2% | JVs with partners (25% of Regent Street with The Crown Estate, 2010; 50% of Borssele 1&2, 2021). Real-estate debt ratio ≤ 25% | NBIM [S]; dossier 06 [S] |
| CPP Investments | Real estate, infrastructure and energy grouped as "Real assets" from fiscal 2026. Five-year return 7.9%, total fund 6.6%. Its share was not verified [U] | Programmatic JV sell-downs: 50% of seven offices to Oxford for C$730m; 49% of Island Star Mall for ≈C$871m; a C$1.0bn industrial JV with Dream | CPP fiscal-2026 release, May 2026 [S] |
| CalPERS | Real assets returned 6.3% in FY2025-26 (private assets lagged a quarter). A Total Portfolio Approach started in July 2026 against a 75/25 reference portfolio. Share not verified [U] | — | CalPERS, 13 Jul 2026 [S] |
| US endowments | >$3bn cohort averages **9%** real assets, mostly private. The peer average fell 2pp in three years | — | Cambridge Associates FY2025, Feb 2026 [S] |
| Yale, Harvard, Future Fund, NZ Super | Current real-asset weights not verified in session [U]. Yale's CIO cited real estate as the main drag in FY2025 [S] | — | Yale News, Oct 2025 [S] |

### 5.2 Direct platforms versus funds

- Larger pension funds manage real estate internally more often, at lower cost and with higher net returns. Delegation to intermediaries "increases costs and disproportionally reduces returns" [S: Andonov, Eichholtz & Kok 2015, *JFM* 22:73–103].
- Public institutions underperform private ones in infrastructure funds. ESG preferences explain ≈25–40% of public investors' increased allocations and ≈30% of the underperformance [S: Andonov, Kräussl & Rauh 2021].
- **Practice** [P]. Large sovereigns combine direct and JV positions with operating partners (ADIA, GIC, NBIM, CPP) with funds for access and specialist sectors.
- **For ADIC** [I]: a JV/direct core with operating partners, and funds for value-add, energy & NR and new sectors. This is consistent with the user's description.

### 5.3 Liquidity policies seen in practice

- Debt caps (NBIM ≤ 25%).
- Notice periods and caps (FCA CP20/15; BREIT 2% a month / 5% a quarter).
- Programmatic partial sales (CPP).
- Liquidation as the end-state of failed open-end funds (Germany 2010–17).
- Inflation-bucket framing (GIC).

None of these peers counts open-end real-asset redemptions as short-horizon liquidity [I, from the evidence above].

---

## 6. Design implications for the ADIC framework

### 6.1 Synthetic book (SYNTHETIC defaults)

The ten sleeves below sum to $18.0bn NAV and $4.0bn unfunded.

**Vehicle shares.** Open-end funds 26%; closed-end funds 37%; JV, direct and co-investment 37%.

**Look-through debt.** $17.4bn (49% LTV). Of this, $6.6bn is on directly held sleeves.

| Sleeve | NAV | Unfunded | LTV | Net cash income yield | Exit-driven distributions, normal / drought | Notes |
|---|---|---|---|---|---|---|
| Real estate, open-end core | 2.7 | 0 | 27% | 3.25% | 0 / 0 | ODCE-anchored |
| Real estate, closed-end value-add/opportunistic | 2.6 | 1.2 | 60% | 1.0% | 18% / 6% | Ares 7% total in the drought |
| Real estate, JV/direct (global) | 1.7 | 0.2 | 45% | 3.0% | ADIC-controlled (SELL only) | Development unfunded |
| Real estate, JV/direct (GCC) | 1.2 | 0.2 | 45% | 4.5% | ADIC-controlled | Owner-correlated |
| Real estate, co-investment | 0.8 | 0 | 60% | 1.5% | 12% / 4% | GP-controlled exits |
| Infrastructure, open-end core | 2.0 | 0 | 50% | 5.5% | 0 / 0 | bfinance ≥ 6% target |
| Infrastructure, closed-end core-plus/value-add | 2.5 | 1.3 | 55% | 4.0% | 8% / 4% | |
| Infrastructure, direct/co-investment | 2.0 | 0.3 | 55% | 5.0% | 2% / 1% | Partner-led exits |
| Energy & NR, closed-end | 1.6 | 0.6 | 35% | 4.0% | 10% / 6% | Oil-elastic |
| Energy & NR, direct/co-investment | 0.9 | 0.2 | 40% | 7.0% | ADIC-controlled | Oil-elastic |

*SYNTHETIC – NOT ADIC DATA.*

### 6.2 State and decision variables

**State per sleeve:**
- reported NAV $N^{rep}$ and true value $N^{eco}$;
- unfunded $U$;
- debt $D$ with maturity ladder $D_{\tau}$, rate mix (fixed/floating, hedges) and covenant LTV/DSCR;
- income run-rate $y$;
- queue position $(Q,R)$ for open-end holdings;
- GCC and oil flags;
- partner and consent terms (ROFO/ROFR, buy–sell, drag/tag);
- appraisal date and lag.

**Global states** come from main §4.1: exit window $e_t$, macro regime $z_t$, oil/fiscal state $Z_t$ (N, B, SG, DB, SS, GW) and CFP stage.

**Decisions:**
- closed-end pacing;
- SELL fraction by route (secondary, asset sale, redemption notice);
- JV sell-down;
- cash-out refinancing;
- acquisition or development debt (LEVER);
- hedge requests to the Overlay (rates, FX, oil);
- envelope requests.

### 6.3 Equations

**Closed-end sleeve** (PE engine, real-asset parameters):

$$C_t=\big(1-(1-\lambda_{s}m^C_t)^{\Delta}\big)U_t,\qquad D^{CE}_t=\Big[y^{inc}f^{inc}_{s,Z}(t)+d^{real}_{s}\big(e_t\big)\Big]N_t\Delta,$$

where:
- under T4′, $d^{real}=0.108\,d^{real}_{D}$ and $m^C=1.38$;
- under S1, $d^{real}=0.318\,d^{real}_D$ for 18 months and $m^C=1.25$ for 12.

**Perpetual sleeve:**

$$I_t=y^{inc}f^{inc}_{s,Z}(t)N_t\Delta,\qquad N^{rep}_{t+1}=N^{rep}_t\big(1+(1-\phi)r_t+\phi\,r^*_{t-1}\big)\ \text{(Geltner lag)}.$$

The default φ_q is 0.65 for real estate (consistent with ODCE's AC1 of 0.72 over 2022–26), 0.6 for infrastructure and 0.5 for energy & NR [I; dossier 04 defaults].

**Debt and cures.** These apply where ADIC funds the equity, i.e. JV, direct and co-investment sleeves:

$$\text{Cure}_t=\max\!\Big(0,\ D^{mat}_t-LTV^{max}_{s}(t)\,\frac{D^{mat}_t}{LTV_0}\big(1+v_{s}(t)\big)\Big),\qquad D^{mat}_t=0.17\,D_t\Delta .$$

| Parameter | Real estate | GCC real estate | Infrastructure | Energy & NR |
|---|---|---|---|---|
| $LTV^{max}$, normal | 60% | 60% | 65% | 55% |
| $LTV^{max}$, stress | 50% | 45% | 55% | 45% |
| True value change $v$ under T4′ (ramped over 12 months) | −25% | −30% | −12% | −30% |

In closed-end and open-end funds, cures come through calls or income cuts.

**Open-end queue machine** (quarterly, pro-rata):

$$Q_{k+1}=Q_k(1-\rho_k)+n_k-p_k\frac{Q_k}{Q_k+R_k},\qquad \text{ADIC paid}_k=p_k\frac{R_k}{Q_k+R_k}\,\mathrm{NAV}_k,\qquad p_k=\min(\bar\kappa_k,Q_k+R_k).$$

Calibration ($Q_0$, $n_k$, $\rho_k$, $\bar\kappa_k$):
- normal: 2%, 1%, 5%, 3%;
- drought: 10%, 1.5%, 8%, 1.2%;
- T4′: 12%, 3.5→1%, 1→10%, 0.6→1.5%, with marks −17% over 4 quarters.

**Oil/fiscal loading:**
- GCC real-estate income factor: 0.95 (year 1) and 0.85 (year 2) in SG; 0.90 in GW.
- GCC exit-driven distributions ×0.5 in SG and GW.
- Energy & NR income factor $1+\beta_{oil}\Delta\ln P_{oil}$, with β_oil = 0.8 and a floor of 0.2.
- Energy exit-driven distributions ×0.3 in SG, reflecting the bid–ask freeze.

Estimate on BIS/Brent data and update with ADIC asset data.

**Inflation pass-through** (for FBE and scenario consistency):
- NOI growth: $g_t=g_0+\beta_\pi\pi_t$;
- value change: $\Delta\ln V_t\approx(\Delta g_t-\Delta r_t)/c_t$.

| $\beta_\pi$ default | Value |
|---|---|
| Regulated or indexed infrastructure | 0.8 |
| Real estate, long leases | 0.4 |
| Real estate, short leases | 0.7 |
| Energy & NR (on CPI) | 0; the asset loads on oil instead |

These are [I] values to be fitted to asset data.

### 6.4 The Real Assets row, the carve-out and the cross-group map

**Rows.** The RA row is in §1. By sector (12 months; real estate / infrastructure / energy & NR):

| State | Real estate | Infrastructure | Energy & NR |
|---|---|---|---|
| Drought | −0.07 | −0.07 | −0.02 |
| T4′ | −0.60 | −0.45 | −0.28 |
| Supply glut | −0.08 | −0.07 | −0.15 |

**Under v2**, PE falls to $34bn of NAV. PE unfunded is $16.4bn on census v1.1 as chosen by the user, or ≈$10.9bn at U/NAV 0.32 (context §1A caveat). The private-book re-run must carry both.

**T4′ new commitments.** Canonical T4′ assumes $12bn a year of new commitments. Under v2, RA's $1.2bn should come out of that total rather than be added to it.

**The L4 budget.** RA's line is B_RA = 2.5 / 1.3 ($bn, 24 / 12 months, do-nothing), or 1.6 / 1.1 with an RA pacing stop [I-calc].

**Sensitivity: empirical calls.** With calls ×1.0 rather than the canonical ×1.38, RA's T4′ drain is −$0.84bn over 12 months and −$1.70bn over 24 [I-calc]. Buyout calls historically fell in downturns (main §2.3(d)). In 2009, though, real-estate funds kept calling capital that some LPs could not meet, and value-add/opportunistic fundraising fell to under a third of its 2007 peak [S, via search summary: IPE Real Assets, PERE]. ×1.38 therefore stays canonical.

**The L8 row** (private NAV + unfunded ≤ 0.80W). RA contributes $22bn, against $23.8bn for the same NAV held as PE at U/NAV 0.32.

*SYNTHETIC – NOT ADIC DATA.*

### 6.5 Liquidity-ladder entries

| Route (sleeve) | Normal: months to first cash / price per $ NAV | Drought | T4′ | Supply glut (oil crisis) | 12-month cash, $bn: normal / drought / T4′ / supply glut | Recourse tier; CFP stage |
|---|---|---|---|---|---|---|
| Open-end real estate: redemption (queue machine) or secondary, whichever is better | Redemption at NAV (34% by 3 months); secondary 3 months / 0.96 | Redemption 27% by 12 months; secondary 0.94 | Redemption 10% by 12 months; secondary 4 months / 0.82 | As drought | 2.72 / 0.73 / 0.28 / 0.73 | Notice at Amber (A); secondary at Red |
| Open-end infrastructure: same | 0.97 | 0.96 | 0.86 | 0.96 | 2.01 / 0.54 / 0.21 / 0.54 | Same |
| Closed-end real estate: LP secondary | 5 months / 0.71 | 0.68 | 7 months / 0.475 | 0.68 | 0.25 / 0.23 / 0.07 / 0.23 | Red (R); excluded from Phase I |
| Closed-end infrastructure: LP secondary | 4 months / 0.91 | 0.90 | 7 months / 0.72 | 0.90 | 0.92 / 0.86 / 0.24 / 0.86 | Red; priced lever |
| Energy & NR closed-end: LP secondary | 5 months / 0.82 | 0.80 | 8 months / 0.55 | 8 months / 0.60 | 0.23 / 0.21 / 0.05 / 0.06 | Red |
| Global real estate JV/direct: asset sale | 6 months / 0.95 | 7 months / 0.90 | 12 months / 0.73 | 7 months / 0.90 | 0.81 / 0.44 / 0.02 / 0.44 | Red; Board and owner at Black |
| GCC real estate JV/direct: asset sale | 6 months / 0.93 | 0.90 | 12 months / 0.70 | **12 months / 0.75** | 0.56 / 0.31 / 0.01 / 0.01 | Red |
| Infrastructure direct: sale | 6 months / 0.96 | 0.94 | 12 months / 0.82 | 0.94 | 0.97 / 0.58 / 0.03 / 0.58 | Red |
| Energy & NR direct: sale | 6 months / 0.90 | 0.88 | 12 months / 0.62 | 12 months / 0.65 | 0.29 / 0.27 / 0.01 / 0.01 | Red |
| **SELL routes, total** (3 / 12 / 24 months) | 1.59 / **9.02** / 13.46 | 0.34 / **4.31** / 10.07 | 0.13 / **0.92** / 3.21 | 0.34 / **3.60** / 8.50 | | |
| JV sell-down (≤ 40% of JV/direct NAV) | 3–9 months / 0.95 → $2.51bn | 0.92 → $2.43bn | 20% at 0.80 → $1.06bn | $1.97bn (GCC and energy impaired) | | Amber; this is a partial SELL (see §6.6) |
| Cash-out refinancing (to 55/60/50% LTV) | $0.90bn | $0.90bn | **$0** (cures instead) | $0.53bn | | Green/Amber only |

*SYNTHETIC – NOT ADIC DATA.* Market-depth caps apply per year: core open-end real estate $0.53bn and value-add/opportunistic closed-end real estate $0.62bn (20% of 2025 segment volume); infrastructure open-end $0.5bn, infrastructure closed-end $1.5bn and energy closed-end $0.5bn are [I]. Prices are proceeds per $ of *reported* NAV, and execution probabilities are 0.95 normal to 0.45–0.6 under T4′.

**Ladder rules.**
- RA holds no HQLA, so its weight in ADIC-LCR(30d) is zero.
- Open-end notices count at the queue-machine P50 and never in 30-day rows.
- Closed-end and direct sales are Red and are excluded from Phase-I recovery, as for PE, Secondaries and Co-investment.
- JV sell-downs and cash-out refinancing count only if pre-arranged and only in Green or Amber.
- Equity cures enter $O^{stress}$ (the stressed outflows that the contingent-liquidity charge, CLC, prices).

### 6.6 SELL / HOLD / REFINANCE / LEVER for Real Assets

All actions are scored with the groups report §3.0 rules: C2 full reduced cost on one kernel, common random numbers, and `priced_on` flags.

**SELL** (asset or stake sale; LP secondary; open-end redemption).
- *Rule:* SELL iff $p^{ceq}>p^*$, where $p^{ceq}$ uses depth-capped, state-dependent prices (§6.5), and appraisal lag is a cost, not an alpha.
- *Open-end redemption* is a notice decision: lodge when $P(\text{Red within }4q)\cdot\Delta\text{queue position value}>$ forgone income and re-entry cost.
- *A late-life value-add real-estate fund* at 0.68 of NAV is a HOLD unless ℓ̄ exceeds the implied annual cost. That cost is 11.3–21.0% a year for real estate at 68%, against 5.0–14.1% for infrastructure at 91% (dossier 06, T = 5).

**HOLD** (fund calls; keep income).
- Income counts as cash.
- Calls on development and closed-end commitments are contractual. Call default is inadmissible.

**REFINANCE** (cash-out, keep exposure).
- *Instruments:* cash-out refinancing of asset-level debt; recap; sale-leaseback or ground-lease sale; a NAV facility on real-asset fund interests (CF owns it; Capital Solutions prices it).
- *Rule:* REFINANCE iff $s_B+f/T+\lambda_{Lev}+\text{covenant charge}<\bar\ell_{[0,T]}$.
- *Economics:* asset-level debt at roughly S+175–250bp for core assets [P] is far cheaper than an LP NAV facility (S+300bp + OID, groups §2.3). But the capacity exists only before stress: $0.9bn in Green or Amber, $0 under T4′.
- *JV sell-down* sells 25–49% of an asset while keeping control and fees. Context §1A and brief §8 file it under REFINANCE, but exposure falls, so the optimizer must score it as a partial SELL plus a retained-control premium. **Flagged for the user.**

**LEVER** (acquisition or development debt).
- *Condition:* only if ADD passes, REFINANCE passes, $(1-\kappa)c>i$ under P95 rates, and DSCR/LTV covenants hold under T4′ values.
- *Example:* core infrastructure clears modestly at S+200bp, with α\* +0.4% after charges (dossier 06). Core real estate does not today.
- *Treatment:* non-recourse, outside CF facilities. It counts in look-through leverage and in $O^{stress}$ through cures.

### 6.7 Allocation range, sub-limits and constraints

**Range.** RA is **8–12% of NAV**, central 10% ($14–21bn on $177bn). The rationale:
- **(i) Peers.** Payout-constrained sovereigns cluster at 4–14% for real estate plus infrastructure (ADIA ranges), large endowments at ≈9%, and liquidity-maximizing NBIM at ≈2%.
- **(ii) Cash map.** Per $18bn relabelled from PE, RA reduces the 24-month T4′ drain by $0.2–1.3bn but worsens drought cash by $0.5–0.9bn a year and costs ≈26bp of NAV a year in expected return. Both costs scale linearly, while the T4′ relief stays small next to the $13.9bn facility need. Above ≈12% the Tier-1 value bought per basis point of return therefore falls [I].
- **(iii) Liquidity.** At 10%, RA's T4′ 12-month SELL capacity is ≈5% of its NAV; it is not a reservoir.
- **(iv) Inflation.** The infrastructure share carries the hedge.
- **(v) L8.** RA's lower U/NAV eases the overcommitment row.

**Sub-limits.** All are [I], to be set by the IC.

| Sub-limit | Limit |
|---|---|
| Infrastructure | ≥ 35% of RA |
| Energy & NR | ≤ 15% of RA and ≤ 1.5% of NAV (owner wrong-way) |
| GCC real estate | ≤ 1.0% of NAV (fiscal wrong-way) |
| Open-end funds | ≤ 30% of RA (queue risk) |
| Closed-end value-add/opportunistic real estate | ≤ 2% of NAV |
| Look-through LTV | ≤ 50% (49% on the synthetic book) |
| Any directly held asset's LTV | ≤ 60% |
| Debt maturing within 12 months | ≤ 25% of RA debt |
| Floating-rate share unhedged | ≤ 30% |
| RA unfunded | ≤ 30% of RA NAV |
| Single asset | ≤ 1% of NAV (groups §3.0) |
| Single operating partner or GP | ≤ 20% of RA |

**Leverage accounting.** Non-recourse RA debt is reported in look-through leverage but carries a separate limit. Only contingent recourse (guarantees, completion support, expected cures at T4′: $0.36bn) enters T5 [I].

### 6.8 Objective terms, FTP and charges

The RA FTP follows groups §4.3, with two additions.
- **(a) A refinancing CLC:** $c_{buf}\sum_h\omega_h\,\text{Cure}^{s^*}_{h}$.
- **(b) An owner-correlation charge:** $\eta\cdot[\text{CF}^{RA}_{base}-\text{CF}^{RA}_{SG}]+\eta'\cdot[N^{eco}_{base}-N^{eco}_{SG}]$, which prices the SG wrong-way loss of $0.15bn of cash and $1.0bn of true value within 12 months.

**Desmoothing.** Risk charges use desmoothed betas: real estate ≈0.6–0.8 and infrastructure ≈0.5–0.6 against equities (dossier 04 defaults: real estate value-add 0.77, infrastructure 0.5–0.7).

**Inflation credit.** The objective credits infrastructure through the SS (2022-type) scenarios, where duration fails (stream 03). No explicit inflation-hedge bonus is added, to avoid double counting.

### 6.9 Links to other groups and to Corporate Finance; organization; the IC seat

| Counterparty | Boundary rule | Conflict control | Internal liquidity |
|---|---|---|---|
| PE | Classify by cash-flow profile [I]: an "infrastructure" label needs ≥ 50% contracted or regulated revenue and leverage ≤ 65%, otherwise it is PE. The same GP's PE and real-asset funds sit on one overlap graph (V24) | Recuse from rival envelopes | Transfers count zero |
| Co-investment | Co-investments in real-estate, infrastructure and energy deals belong to RA (user: RA "invests through funds plus co-investments") | One draw per company (V24a) | — |
| Private Credit | Senior real-estate and infrastructure loans → PC; equity → RA | ADIC may not lend to its own JV assets without ≥ 50% external syndication. In workouts ADIC acts as one position under CRO/CF arbitration, with information barriers | Lending to RA assets raises zero |
| Capital Solutions | Preferred equity and NAV financing → CS | CS quotes are reserve prices behind ≥ 3 RFQs (groups §4.2) | Zero unless refinanced externally |
| Secondaries | Real-estate and infrastructure fund secondaries; the Secondaries desk forecasts external clearing prices for RA's SELL | The desk never quotes where it may bid | A Secondaries purchase of an RA stake raises zero |
| Overlay | Rate caps and swaps on floating asset debt; FX; oil hedges for energy & NR, coordinated with owner-level hedging (stream 03) | Services transfer pricing (groups §4.3) | Contingent VM charged at CLC |
| CF | Look-through leverage reporting; FTP; refinancing CLC; owns any NAV facility on RA interests | — | Cures and calls are budgeted outflows |

**Envelopes.** RA's envelope has seven components:
- NAV band;
- closed-end pacing $P_{RA}$;
- 12- and 24-month liquidity budgets (calls + cures);
- look-through leverage budget;
- owner-correlation budget (energy & NR + GCC real estate);
- open-end share;
- inflation-beta floor (infrastructure share).

**The Real Assets head's shadow-IC seat** (brief §8, rule 1; the IC grows to 13 mandate seats) brings:
- **(i)** true-versus-reported NAV and appraisal lag;
- **(ii)** refinancing walls, LTV/DSCR headroom and cure exposure;
- **(iii)** cap-rate, replacement-cost and NOI views;
- **(iv)** operating-partner and JV governance;
- **(v)** local GCC real-estate intelligence, which carries a home-market advocacy conflict to disclose;
- **(vi)** power-demand and energy-transition views shared with PE.

The head recuses on RA envelopes and is scored on total-portfolio regret (groups §7).

### 6.10 Calibration targets and data needs

**Targets** for V-gates on SYN-ADIC-177 v2:

| Target | Value |
|---|---|
| Closed-end real-estate distributions, drought | 6–8% of NAV |
| Open-end real-estate net income | 3–3.5% |
| ODCE-type queue | 10% today; 15–20% stressed peak; clearing in 8–16 quarters |
| Closed-end real-estate secondary price | 0.68–0.72 normal; 0.45–0.5 crisis |
| Infrastructure secondary price | ≈0.91 |
| Look-through LTV | 45–55% |
| Debt maturing | 15–20% a year |
| Reported AC1, real estate | 0.6–0.75 |
| GCC real-estate peak-to-trough in a 2-year oil bust | −25% to −35% |
| Energy & NR in an oil bust | −15% to −25% |

**Data ADIC must supply.** These are listed in §9.

---

### SPECIFICATION CARD — Real Assets (Group 8)

| Item | Specification |
|---|---|
| **Mandate** [A] | Real estate, infrastructure, energy & natural resources (no agriculture or timber). Funds (open- and closed-end), co-investments, JVs and direct assets. Part of the ~60% private allocation; working NAV $18bn, unfunded $4bn |
| **Data fields** | `holding_id`, `group=RA`, `sector`{RE, INF, ENR}, `subsector`, `region`, `gcc_flag`, `vehicle`{OE, CE, JV, DIRECT, COI}, `control`{ADIC, partner, GP}, `nav_rep`, `nav_eco`, `appraisal_date`, `phi`, `unfunded`, `dev_capex_commit`, `income_yield`, `noi`, `capex`, `cap_rate`; debt: `debt_bal`, `ltv`, `dscr`, `covenants`, `maturity_ladder`, `fixed_share`, `hedge_ids`, `recourse_flag`, `guarantees`; open-end: `queue_pos`, `notice_date`, `gate_terms`, `fund_queue_pct`; consents: ROFO/ROFR, buy–sell, drag/tag, transfer consent; forecasts u/a/f (yield-on-cost, IRR, exit cap, NOI growth); `oil_beta`, `beta_pi`, `is_synthetic` |
| **Return and NAV** | $R=\frac{NOI-K}{V}+\Delta V/V$; $V=NOI_{+1}/c$; $\Delta\ln V\approx(\Delta g-\Delta r)/c$; reported NAV Geltner-lagged with φ_q 0.65 (real estate) / 0.6 (infrastructure) / 0.5 (energy & NR); true value desmoothed with a pooled common factor |
| **Cash flows** | Closed-end: $C=(1-(1-\lambda m^C)^\Delta)U$; $D=[y^{inc}f^{inc}_{Z}+d^{real}(e)]N\Delta$. Perpetual: $I=y^{inc}f^{inc}_ZN\Delta$. Cures: $\max(0,D^{mat}-LTV^{max}_sV^{mat}(1+v_s))$. T4′: $d^{real}$×0.108 and calls ×1.38. S1: ×0.318 for 18 months and calls ×1.25 for 12 |
| **Parameter defaults** | Distributions, drought: closed-end real estate 7% (Ares 2026); open-end real estate 3.25% net (ODCE income 4.08%); open-end infrastructure 5.5% (bfinance ≥ 6%); closed-end infrastructure 4% + 4%; energy & NR 4% + 6%. Calls: G7 table 29/28/30%. Debt maturity 17% a year (MBA). LTV: open-end real estate 27% (NCREIF), closed-end value-add real estate 60%, infrastructure 50–55%, direct 45% |
| **Liquidity** | Ladder in §6.5. Open-end queue machine (§6.3); notice at Amber; zero weight in 30-day rows. Closed-end and direct: Red, depth-capped at ≤ 20% of annual segment volume. 12-month SELL capacity $9.0 / 4.3 / 0.9 / 3.6bn (normal / drought / T4′ / SG) |
| **Stress behaviour** | T4′: income ×0.85 / 0.92 / 0.60 (real estate / infrastructure / energy & NR); true value −25% / −12% / −30% (GCC real estate −30%); LTV^max 50 / 55 / 45%. SG: GCC real-estate income 0.95 → 0.85, value −10% → −15%; energy & NR income ×0.68, exits ×0.3, value −20%. GW: GCC real-estate income ×0.9, exits ×0.5; energy & NR income ×1.25 |
| **SELL** | Depth-capped secondary, asset sale or redemption, at state prices: closed-end real estate 0.71 → 0.475; closed-end infrastructure 0.91 → 0.72; direct real estate 0.95 → 0.73. Excluded from Phase I except open-end notices |
| **HOLD** | Fund calls and development capex; income counts as cash |
| **REFINANCE** | Cash-out refinancing to target LTV (Green/Amber; $0.9bn); recap; ground lease or sale-leaseback; NAV facility (CF). JV sell-down is scored as a partial SELL with a control premium (flag) |
| **LEVER** | Asset-level acquisition or development debt, only if $(1-\kappa)c>i$ at P95 rates and covenants hold at T4′ values |
| **Forecasts and biases** | Business plans: NOI growth, exit cap, yield-on-cost, capex and timelines, traffic and commodity decks. Fusion: FBE with Geltner-corrected actuals and a market-implied anchor (listed-implied cap rates, secondary prices, oil futures). Priors: exit-cap optimism +25–50bp; development cost and time uplifts per the Green Book reference class (works duration up to 4–25%, capex up to 24–66% for buildings to civil engineering); traffic forecasts per Flyvbjerg et al. 2005; marks lag 1–2 quarters (more in stress); one $\kappa_g\ge1$ (groups §5) |
| **Synthetic defaults** | The ten-sleeve book in §6.1; look-through debt $17.4bn; new closed-end commitments $1.2bn a year |
| **Links** | PC (real-estate and infrastructure debt), CS (preferred equity and NAV financing), Secondaries (fund secondaries), Co-investment (boundary), PE (infrastructure-like PE; shared GPs), Overlay (rates, FX, oil hedges), CF (look-through leverage, FTP, refinancing CLC). Intra-ADIC transfers raise zero |
| **Limits** | §6.7 |
| **Outputs** | Cash-map row; L4 budget; ladder entries; cure schedule; owner-correlation metric; desmoothed risk |

*SYNTHETIC – NOT ADIC DATA* for every default.

---

## 7. Implementation notes

1. **Engine.** Reuse RFT-TA v2 for closed-end sleeves. Add a perpetual-asset class that has income, a Geltner-lagged reported NAV and a true-value process driven by $(r,g,\text{oil},Z)$. Run monthly steps inside quarterly H decisions. The reference implementation is `G15_calcs/g15_ra_calcs.py`: `run_book`, `queue_machine`, `ladder_cbc`, `refinance_capacity`, `true_nav_impact`.
2. **Desmoothing.** Fit φ by sector × vehicle on pooled data. Cap φ ≤ 0.8, because noise explodes as φ → 1. Do not desmooth the first observation. Use transaction-based or listed-implied series for validation. Run the Couts et al. common-factor correction before estimating H's covariance.
3. **Double counting.** For open-end funds, take the better of redemption and secondary sale, never their sum. JV sell-down and asset sale draw on the same NAV, so the ladder must decrement a single position. Development unfunded and closed-end unfunded must not overlap.
4. **Levered equity floors.** Floor true equity at zero by asset. Recall CPP's "no net proceeds" sale. Cures are optional for ADIC: walking away from a non-recourse asset can dominate, so model cure-versus-handback as a real option, with $V_{handback}=0$ less reputational and partner costs.
5. **Depth caps and price impact.** Use a concave impact $p=p_0(1-\psi\,q/\text{Vol})$ and calibrate ψ to deferral and discount data when ADIC's flow is ≥ 10% of segment volume.
6. **Queue machine.** Use a quarterly step, pro-rata payment and stochastic rescissions. Keep NAV marks inside the payment, because redemptions in a falling market crystallize mark-downs.
7. **Oil and fiscal coupling.** Drive the GCC real-estate and energy factors from stream 03's state $Z_t$ and fiscal module, not from equity. Include a lag of 2–6 quarters for GCC real estate.
8. **Testing.**
   - V-gates: queue clearing time; drought distribution rate; T4′ cure total; intra-ADIC transfers net to zero; RA share of L8.
   - Property-based tests: no negative NAV; cures ≤ maturing debt; the ladder never exceeds NAV.
9. **Provenance.** Store each sleeve's appraisal date and φ in the bitemporal registry. A reported NAV older than two quarters triggers an automatic stale-mark haircut in pricing.

## 8. Risks and limitations

- **Synthetic book.** The sleeve weights, yields and LTVs are defaults. The sign of the drought result depends on the closed-end share and pacing. With no new commitments, drought net turns positive.
- **The PE comparison is rate-based.** On census v1.1, PE's drought net is driven by vintage, and the relabel comparison uses G7 rates. The groups engine must re-run the carve-out with RFT-TA v2.
- **Evidence gaps.**
  - Infrastructure closed-end distribution rates in the drought are inferred from yields, not measured.
  - Open-end infrastructure queue data were not found.
  - McKinsey's infrastructure DPI figure is unverified [U].
  - Yale, Harvard, CPP, Future Fund and NZ Super weights were not verified.
  - Some 2024–25 secondary facts come via search summaries.
- **Mixed CMA editions** (J.P. Morgan 2026 for PE, 2027 for real estate and infrastructure) affect the 26bp return-cost estimate.
- **Short samples.** The UAE lead–lag rests on ≈20 effective observations. 2026 Dubai data are preliminary and exclude any physical damage.
- **Model risk.** Common-factor smoothing, regime-dependent pass-through and the cure option are first-order but weakly identified. Ranges must be shown.
- **Governance.** Appraisal discretion and boundary arbitrage are agency risks. The controls are an external valuation cycle, stale-mark haircuts and cash-flow-based classification.

## 9. Open questions (what ADIC must supply or confirm)

1. The RA size and the vehicle split: open-end, closed-end, JV/direct, co-investment.
2. Sector and region weights, including GCC real estate and Gulf-located energy and infrastructure.
3. Asset-level debt by asset: balance, maturity, fixed/floating, hedges, covenants, recourse and guarantees.
4. Open-end fund terms and current queue positions.
5. JV agreements: ROFO/ROFR, buy–sell, consent, drag/tag.
6. RA unfunded by fund and vintage, plus development budgets.
7. Appraisal policy: frequency, appraiser rotation, lag.
8. Business-plan forecasts with dates, for the point-in-time archive.
9. Whether energy & NR exposure is hedged, and whether oil hedging is coordinated with the owner.
10. Whether JV sell-down is a REFINANCE or a partial SELL in ADIC's books.
11. Whether non-recourse RA debt counts in T5.
12. Whether the IC accepts the 8–12% range and the sub-limits in §6.7.
13. Whether Gulf real estate is a policy or strategic holding, which would place it outside the optimizer.

## 10. References

**Academic** (metadata verified on Crossref, OpenAlex or Semantic Scholar):
- Andonov, A., Eichholtz, P., & Kok, N. (2015). Intermediated investment management in private markets: Evidence from pension fund investments in real estate. *Journal of Financial Markets* 22, 73–103. https://doi.org/10.1016/j.finmar.2014.11.002
- Andonov, A., Kräussl, R., & Rauh, J. (2021). Institutional investors and infrastructure investing. *Review of Financial Studies* 34(8), 3880–3934. https://doi.org/10.1093/rfs/hhab048
- Baumol, W. J., & Fabian, T. (1964). Decomposition, pricing for decentralization and external economies. *Management Science* 11(1), 1–32. https://doi.org/10.1287/mnsc.11.1.1
- Couts, S. J., Gonçalves, A. S., & Rossi, A. (2024). Unsmoothing returns of illiquid funds. *Review of Financial Studies* 37(7), 2110–2155. https://doi.org/10.1093/rfs/hhae006
- Diamond, D. W., & Dybvig, P. H. (1983). Bank runs, deposit insurance, and liquidity. *Journal of Political Economy* 91(3), 401–419. https://doi.org/10.1086/261155
- Fama, E. F., & Schwert, G. W. (1977). Asset returns and inflation. *Journal of Financial Economics* 5(2), 115–146. https://doi.org/10.1016/0304-405X(77)90014-9
- Flyvbjerg, B., Skamris Holm, M. K., & Buhl, S. L. (2005). How (in)accurate are demand forecasts in public works projects? *Journal of the American Planning Association* 71(2), 131–146 (verified in dossier 07). https://doi.org/10.1080/01944360508976688
- Geltner, D. (1991). Smoothing in appraisal-based returns. *JREFE* 4(3), 327–345. https://doi.org/10.1007/BF00161933 ; Geltner, D. (1993). Estimating market values from appraised values without assuming an efficient market. *JRER* 8(3), 325–345. https://doi.org/10.1080/10835547.1993.12090713
- Gupta, A., & Van Nieuwerburgh, S. (2021). Valuing private equity investments strip by strip. *Journal of Finance* (NBER w26514, verified in dossier 04). https://www.nber.org/system/files/working_papers/w26514/w26514.pdf
- Hoesli, M., Lizieri, C., & MacGregor, B. (2008). The inflation hedging characteristics of US and UK investments: A multi-factor error correction approach. *JREFE* 36(2), 183–206. https://doi.org/10.1007/s11146-007-9062-6
- Muckenhaupt, J., Hoesli, M., & Zhu, B. (2025). Listed real estate as an inflation hedge across regimes. *JREFE* 70(2), 189–239 (online 16 Oct 2023). https://doi.org/10.1007/s11146-023-09964-x
- Neville, H., Draaisma, T., Funnell, B., Harvey, C. R., & Van Hemert, O. (2021). The best strategies for inflationary times. *Journal of Portfolio Management* 47(8), 8–37. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3813202
- Pagliari, J. L. (2017). Another take on real estate's role in mixed-asset portfolio allocations. *Real Estate Economics* 45(1), 75–132. https://doi.org/10.1111/1540-6229.12138
- Rödel, M., & Rothballer, C. (2012). Infrastructure as hedge against inflation—fact or fantasy? *Journal of Alternative Investments* 15(1), 110–123. https://doi.org/10.3905/jai.2012.15.1.110
- Scharfstein, D. S., & Stein, J. C. (2000). The dark side of internal capital markets: Divisional rent-seeking and inefficient investment. *Journal of Finance* 55(6), 2537–2564. https://doi.org/10.1111/0022-1082.00299
- Wurstbauer, D., & Schäfers, W. (2015). Inflation hedging and protection characteristics of infrastructure and real estate assets. *Journal of Property Investment & Finance* 33(1), 19–44. https://doi.org/10.1108/JPIF-04-2014-0026

**Index providers, managers and practitioners:**
- Accordant Investments (25 Jun 2026). Private real estate enters a new cycle: Q1 2026 NFI-ODCE insights. https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights
- AQR (Ilmanen, Chandra, McQuinn, 2019). Demystifying illiquid assets: Expected returns for private real estate. https://www.aqr.com/insights/research/white-papers/demystifying-illiquid-assets-expected-returns-for-private-real-estate
- Ares (11 Feb 2026). Real estate secondary market volume hits record $20 billion in 2025. https://www.ares.com/us/news-and-insights/real-estate-secondary-market-volume-hits-record-20-billion-2025 ; Ares (2025). Real estate secondary market rebounds in 2024. https://www.ares.com/es/news-and-insights/perspectives/real-estate-secondary-market-rebounds-in-2024
- Callan (2025). 4Q24 Real Estate Performance: Highlights and Key Issues. https://www.callan.com/blog/4q24-real-estate/
- Cambridge Associates (June 2016). Real Asset Dynamics. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2016/06/Real-Asset-Dynamics-June-2016.pdf ; (20 Feb 2026). FY2025 Annual Review of Endowments: Asset Allocation. https://publishedresearch.cambridgeassociates.com/fiscal-year-2025-annual-review-of-endowments-asset-allocation-and-implementation/
- ION Analytics / Infralogic (5 Jun 2026). Open-ended funds' appeal endures despite lull (bfinance data). https://ionanalytics.com/insights/infralogic/open-ended-funds-appeal-endures-despite-lull/
- MBA (9 Feb 2026). 17% of commercial and multifamily mortgage balances to mature in 2026. https://newslink.mba.org/?p=270033 (also https://www.mba.org/news-and-research/newsroom/news/2026/02/09/17-percent-of-commercial-and-multifamily-mortgage-balances-to-mature-in-2026)
- MSCI (2026). Private Capital Benchmarks Summary, Q2 2026. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf ; Global Private Infrastructure Asset Index, Q1 2026. https://www.msci.com/data-and-analytics/private-asset-solutions/global-private-infrastructure-asset-index-q1-2026-results ; Hayes & Liu (4 Aug 2021). Assessing private infrastructure in a multi-asset-class portfolio. https://www.msci.com/research-and-insights/blog-post/assessing-private-infrastructure-in-a-multi-asset-class-portfolio
- NCREIF. NFI-ODCE 4Q-2025 press release (30 Jan 2026). https://ncreif.org/__static/jdj5jdewjezar2nuz3rrtevsy2rnqm5l/NFI-ODCE-Press-Release-for-4Q-2025.pdf ; 2Q-2026 press release. https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf ; 2Q-2026 webinar (16 Sep 2026). https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf ; index returns. https://ncreif.org/indices/index-returns/
- PGIM (Chen & Shen, 14 Apr 2025). Direct infrastructure equity: performance and return attribution. https://www.pgim.com/es/en/institutional/insights/asset-class/multi-asset/multi-asset-solutions/direct-infrastructure-equity-performance-return-attribution
- Green Street CPPI via Bisnow (8 Dec 2023). https://www.bisnow.com/news/national/capital-markets/green-street-cre-prices-fell-another-3-but-may-well-have-hit-bottom-121991
- BREIT repurchases: https://bluevaultpartners.com/breit-fulfills-all-redemption-requests-for-first-time-since-2022/ ; https://www.bisnow.com/national/news/capital-markets/breit-fulfills-all-redemption-requests-for-first-time-in-more-than-a-year-123143
- German open-ended funds: https://realassets.ipe.com/propertyeu/investors-opt-to-liquidate-sebs-immoinvest-fund/10087425.article ; https://refire-online.com/markets/kanam-study-shows-how-fast-open-ended-funds-are-liquidating
- FCA CP20/15 (3 Aug 2020). https://fca.org.uk/news/press-releases/fca-consults-new-rules-improve-open-ended-property-fund-structures
- 2009 real-estate fund stress (via search summary): PERE, "$30bn raised in real estate funds in 2009", https://www.perenews.com/30bn-raised-in-real-estate-funds-in-2009/ ; IPE Real Assets, "Capital calls face defaults and delays", https://realassets.ipe.com/capital-calls-face-defaults-and-delays/30290.article

**Peers and official sources:**
- ADIA, Investments (ranges): https://www.adia.ae/en/investments ; 2025 Review: https://www.adia.ae/en/pr/2025a/index.html ; infrastructure: https://www.adia.ae/en/pr/2025a/infrastructure.html ; real estate: https://www.adia.ae/en/pr/2025a/real-estate.html
- GIC Report 2025/26 (24 Jul 2026): https://www.gic.com.sg/uploads/2026/07/GIC_AR_2025-26_PRINT.pdf
- NBIM, Fund value (30 Jun 2026): https://www.nbim.no/en/investments/the-funds-value/ ; investment areas: https://www.nbim.no/en/investments/investment-areas/
- CPP Investments fiscal 2026 results: https://www.newswire.ca/news-releases/cpp-investments-net-assets-total-793-3-billion-at-2026-fiscal-year-end-814459989.html
- CalPERS, FY2025-26 preliminary return (13 Jul 2026): https://www.calpers.ca.gov/newsroom/calpers-news/2026/calpers-posts-preliminary-investment-return-for-fiscal-year-2025-26
- Yale FY2025: https://news.yale.edu/2025/10/24/yale-reports-investment-return-fiscal-2025
- IMF PIN 10/20 (17 Feb 2010), UAE 2009 Article IV: https://www.imf.org/en/News/Articles/2015/09/28/04/53/pn1020
- The National (7 Oct 2026). Dubai home sale transactions fall in third quarter: https://www.thenationalnews.com/business/property/2026/10/07/dubai-home-sale-transactions-fall-in-third-quarter-due-to-regional-uncertainty/
- FRED: BIS residential property prices, UAE (QAEN628BIS) https://fred.stlouisfed.org/series/QAEN628BIS ; Brent (DCOILBRENTEU) https://fred.stlouisfed.org/series/DCOILBRENTEU ; CPI (CPIAUCNS) https://fred.stlouisfed.org/series/CPIAUCNS

**Project sources reused (verified upstream):** groups synthesis v1.1; main synthesis v1.1; dossiers 03 (oil-shock states, UAE fiscal), 04 (PE engine defaults, Geltner), 05 (Jefferies pricing series), 06 (NBIM debt cap, cost of selling), 07 (J.P. Morgan 2027 LTCMA real estate 7.9% and infrastructure 7.1%; Flyvbjerg; Green Book) and 11 (J.P. Morgan 2026 LTCMA PE 10.2%).
