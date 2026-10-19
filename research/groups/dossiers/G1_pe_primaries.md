# G1 · Private Equity group: the fund-commitment program as a controllable system

*Group research dossier for the ADIC multi-period robust Total Portfolio Approach (TPA) framework. Prepared 2026-10-18.*

**Evidence tags.** **[S]** sourced fact (citation in §10). **[P]** practitioner consensus or a secondary summary I could not check against the primary document. **[I]** my inference, design default or **synthetic** model output. Every number produced by my own scripts is tagged **[I, synthetic]** and must never be presented as ADIC data.

**Scope boundary.** Stream 04 owns the generic call/distribution/NAV engine (RFT-TA) and the DPI-drought data; Stream 05 owns secondary and NAV-financing pricing; Stream 07 owns belief fusion; Stream 08 owns action valuation. This dossier adds what is specific to the PE group: program design and pacing, the group's levers and their costs, GP relationships and access, fees and fund-level mechanics that move LP cash flows, and how the group's forecasts are produced, graded and fused.

**Research caveats.** The session's shared WebSearch budget was exhausted early and only briefly refilled; Consensus exposed only authentication tools, so it was not used. Primary sources were therefore read directly (NBER, author manuscripts, ILPA, Bain, MSCI, Evercore, Cliffwater/ERSRI), mostly by extracting PDF text locally. Items I could not verify are flagged where used. Vendor pacing-tool internals (Cambridge Associates, Hamilton Lane, StepStone, BlackRock, MSCI/Burgiss, Neuberger Berman) were **not** verified this session.

---

## 1. Executive summary

1. **The PE program is a linear system with long delays, and the controllable input is the commitment flow.** A commitment raises *exposure* (unfunded + NAV) immediately, but calls arrive over about six years and distributions over 5–15. In my synthetic calibration with Stream-04 buyout parameters, one dollar a year of steady commitments supports **6.9 dollars of NAV and 2.4 of unfunded** in a normal regime (25% distribution rate, 28% call rate). The same pace supports about **10 dollars of NAV** after five drought years [I, synthetic].
2. **Slowing pacing is a loan from the future at roughly the forgone vintage's IRR, and it is slow.** Pausing one year of commitments at the mature-program pace ($5.1bn) [I, synthetic]:
   - returns only **20%** of the forgone amount as cash in year 1 and **≈69%** by year 4;
   - then *costs* cash in years 6–14, so cumulative 2027–40 net cash flow is **−$4.1bn**;
   - has an implied financing rate of **≈10.5–11%**, before access, vintage-hole and co-investment costs.

   That is more than an LP-level NAV facility (≈7–9% all-in) and similar to selling quality buyout interests (8–15% implied; Stream 05). Its advantages are that it needs no counterparty and can be partly reversed. The engine reproduces the published ERSRI "no new commitments" case: about 46% of forgone commitments returned as cash within four years against about 40% in the plan, and NAV −30% against −32%, both relative to the base case [S/I].
3. **Control exposure, not NAV.** I tested two proportional pacing rules after a −20% denominator shock plus a four-year drought [I, synthetic]:
   - A high-gain rule keyed to NAV undershoots the 30% target to **22.6%** and produces a near-zero commitment year, a bullwhip.
   - The same gain keyed to exposure (U+N) bottoms at **28.2%** with half the commitment volatility.

   Recommendation: model predictive control (MPC) on economic exposure, with move-suppression and IC-approved pacing corridors.
4. **GP skill is persistent, but hard to see in advance.**
   - Top- versus bottom-quartile buyout firms differ by **8.03pp a year** in expected net returns (interquartile range) [S: Korteweg & Sorensen].
   - One fund's result says little: per-fund signal-to-noise is **0.15 for buyout and 0.035–0.05 for VC**. With five past funds, top-quartile history implies only a **47%** (buyout) or **37%** (VC) chance of top-quartile expected returns [S].
   - Using what LPs know at fundraising, post-2000 buyout shows essentially **no** persistence, apart from avoiding bottom-quartile GPs. VC persistence survives: previous top-quartile VC GPs averaged a PME of **1.70** against **0.91** for bottom quartile [S: Harris, Jenkinson, Kaplan & Stucke].

   Access penalties should therefore sit mainly on a short list of access-constrained franchises (top VC and growth, elite buyout with strong DPI), not on every re-up.
5. **The current fundraising market lowers the cost of skipping most GPs.**
   - Buyout fundraising fell **16%** in 2025 to $395bn, and the number of buyout funds closed fell **23%** [S: Bain].
   - In H1-2026 US PE raised **$159.6bn across 223 funds**; two closes were about **24%** of that capital; **23** first-time funds closed against a 2021–23 average of **181** a year [S: PitchBook via Cherry Bekaert].
   - In normal years about **15%** of fund series fail to re-raise, about **20%** in stress [S: Bain].

   For most GPs, then, the chance of losing access after a skip is low today, while elite GPs remain oversubscribed (a "K-shaped" market).
6. **ADIC's scale is worth roughly 1pp a year of net return through fees.**
   - Within a single fund, fee tiers differ on average by about **91bp** of management fee and **5.8pp** of carry [S: Begenau & Siriwardane, via summary].
   - In my fee model, moving from 2.0%/1.5%/20% to 1.25%/0.75%/15% raises net IRR from **9.8% to 11.1%** at 14% gross [I, synthetic]. Modelled gross-to-net IRR spreads are **2.5–4.6pp** [I, synthetic].
   - ILPA's model LPA supplies bracketed reference terms: 8% preferred return, 80% catch-up, 20% carry, 100% fee offset, 10+1+1-year term [S].
7. **Subscription lines distort the "actual" return the IC sees.** In Albertus & Denes, funds using lines show IRR **+2.6pp** and TVPI −0.006. Bottom-quartile funds are **8.3pp** more likely to use them, and a line worth 25% of fund size held for one year adds **1.4%** to carry [S]. ILPA recommends lines of at most 180 days and 15–25% of uncalled capital, a preferred return accruing from the draw date, and IRR reported with and without the line [S]. ADIC should rank funds on PME or direct alpha, and treat line balances as near-certain deferred calls in stress.
8. **Market state, October 2026 [S]:**
   - Distributions: PE distribution rate **9%** in H1-2026 [MSCI]. Buyout distribution yield **14.8%** against a 23.4% long-run average [PitchBook].
   - LP behaviour: **53%** of LPs say undrawn commitments constrain new commitments [PEI via Bain]. About **two-thirds** would hold out for MOIC over near-term liquidity [ILPA via Bain]. Roughly **one in five** are reducing buyout allocations [ILPA poll via Bain].
   - Secondaries: sovereign wealth funds rose from **12% to 21%** of LP-led secondary volume in H1-2026 [Evercore].
   - Continuation vehicles: up **62%** year on year but still under 10% of exit value. LPs tolerate about one per year per GP [Bain].
9. **The synthetic book's unfunded figure is load-bearing and looks unusual.**
   - About $29bn of PE unfunded on $52bn NAV is **U/NAV ≈ 0.55**. A mature program in my engine shows **0.24–0.33**, and that ratio matches MSCI-implied industry ratios [I].
   - Matching 0.5 needs about 20% a year commitment growth, which implies 2026 PE net cash flow of **−$5 to −7bn**. A mature program implies **+$0.2bn**.
   - ADIC must supply unfunded by vintage before any liquidity conclusion is drawn.
10. **Deliverable.** §6 gives a program-level specification: state, decisions, transitions linked to the Stream-04 engine, access penalties, constraints, objective terms and parameter tables. It ends with a **Specification Card**.
    - Defaulting on a capital call is **inadmissible**. ILPA model remedies include 10% interest, forfeiture of distributions, a forced sale at 50% of value and forfeiture of up to 100% of the interest [S].
    - So is counting a sale to ADIC's own Secondaries group as liquidity raised.

---

## 2. Core concepts and theory

### 2.1 The program as a delayed linear system
Index fund interests by $i$, with GP $g(i)$, strategy $s(i)$ and vintage $v(i)$, on a quarterly grid. Stream 04 E1–E7 give the asset dynamics. At program level the bookkeeping is:
$$U_{t+1}=U_t+n_t-C_{t+1}+Rc_{t+1}-Ex_{t+1}-\textstyle\sum_i\phi_{i,t}U_{i,t},\qquad E_t\equiv U_t+N^{e}_t,$$
- $n_t$: new commitments.
- $Rc$: recallable distributions.
- $Ex$: expired, never-called commitment.
- $\phi$: fraction sold.
- $N^e$: economic NAV (Stream 04 E2).

**Two multipliers summarise the program.** Under constant commitments $n$ and regime $r$:
$$N^\* = M_N(r)\,n,\qquad U^\* = M_U\,n.$$
Here $M_N=\sum_a \mathrm{NAV}_a$ per \$1 committed is also the *dollar-duration* of invested capital.
- **Synthetic values [I]**, using Stream-04 buyout parameters (call schedule 20/25/30/35/40% of remaining unfunded, L = 16, B = 2.0, G = 11%):
  - normal regime: $M_N=6.88$ and $M_U=2.41$, with a 25.0% distribution rate and a 28.3% call rate on unfunded plus new commitments;
  - permanent drought ($m^D=0.5$, $\kappa=0.6$): $M_N=16.1$.
- **Faster fund growth.** If the fund grows at $g_W$, use $M_N(g_W)=\sum_a \mathrm{NAV}_a(1+g_W)^{-a}$; that is, older vintages are smaller.
- **Over-commitment.** The over-commitment ratio is $OC_t=E_t/(w^\*W_t)$ [S: Cliffwater/ERSRI use (unfunded + FV) ÷ target]. On a balanced 6%-growth path my engine gives $E/N=1.43$.

**What the delays imply for control [I].**
- The transfer function from $n$ to $N$ peaks at a lag of about 5–8 years; from $n$ to $E$ the effect is immediate.
- Feedback on a lagged state with high gain produces oscillation. This is the bullwhip effect familiar from inventory control.
- The program should therefore be steered on $E$, with $N$ as a monitored outcome (§3.2).

### 2.2 What a commitment buys
A primary commitment buys four things:
1. a claim on the fund's net cash flows;
2. an option to re-up in the GP's next fund;
3. a flow of co-investment and alternative-vehicle opportunities;
4. **information**: incumbent LPs learn about the GP faster than outsiders.

Theory explains why these options exist.
- **Screening.** Lerner & Schoar model illiquidity as a GP's screen for "deep-pocket" LPs with few liquidity shocks. Transfer restrictions are less common in later funds of the same firm and where LPs have few liquidity shocks [S: NBER w9146]. **Implication:** a *forced-looking* sale can signal the wrong LP type and raise ADIC's future cost of access.
- **Hold-up.** In Hochberg, Ljungqvist & Vissing-Jørgensen, persistence arises from informational hold-up between incumbent LPs and GPs [S: *RFS* abstract, checked in the 2026-10-18 literature review; previously cited only as summarised by Korteweg & Sorensen].
- **Bargaining over side vehicles.** Lerner, Mao, Schoar & Zhang (*JFE* 2022; NBER w24941, 2018, lists the authors as Lerner, Schoar, Mao & Zhang) use custodial data on 112 LPs.
  - Alternative vehicles were **32%** of LP investments and **17%** of commitments.
  - On average they *underperformed* the GPs' main funds.
  - LPs with better past performance obtained better alternative vehicles, which the authors read as bargaining on outside options [S: NBER w24941; figures not re-checked against the *JFE* 2022 version].

### 2.3 Skill, persistence and learning
**LP skill: real, but time-varying.**
- *1990s endowments.* Lerner, Schoar & Wongsunwai find endowments far better at re-up decisions [S: NBER w11136, working-paper figures]:
  - the follow-on funds they reinvested in earned **31%** IRR, against **7%** for those they passed on;
  - for public pensions the figures were **6%** against **−2%**.
  - Reinvestment rates were about 60% (public pensions, insurers), 50% (endowments, advisors) and 39% (corporate pensions, banks).
- *1999–2006.* Sensoy, Wang & Weisbach study 14,380 investments by 1,852 LPs in 1,250 funds (1991–2006). The early endowment edge came mainly from **access** to top VC partnerships, and it vanished in 1999–2006 [S].
- *Cross-LP skill.* Cavagnaro, Sensoy, Wang & Weisbach find a one-standard-deviation rise in LP skill worth **1–2pp** a year in the published abstract (about 3pp in the 2016 working paper) [S/P].

**GP skill: Korteweg & Sorensen's variance decomposition [S].**
- *Spread.* Top- versus bottom-quartile spreads in expected annual net returns:
  - buyout: **8.03pp** (interquartile) and **13.70pp** (12.5–87.5 percentiles);
  - VC: **6.60pp**.
- *Spurious persistence.* Overlap between contemporaneous funds explains about **44%** of observed autocorrelation.
- *Signal-to-noise per fund.* VC **0.035–0.051**; buyout **0.141–0.148**; other **0.185–0.208**.
- *Learning is slow.* Identifying top-quartile VC firms with reasonable certainty needs 25 or more past funds.
- *Geography and fund size.* Persistence is lower in the US, then Europe, and highest in the rest of the world. Smaller funds show more persistence.

**Persistence at the moment of decision [S: Harris, Jenkinson, Kaplan & Stucke, NBER w28109].**

*Measured on final performance:*
- *Buyout.* Top-quartile firms repeat **34.8%** of the time and finish above median **57.3%**. Bottom quartile stays bottom **39.2%**. Prior-top funds average a PME of 1.30 against 1.01 for prior-bottom funds.
- *Perfect foresight.* Knowing in advance which prior funds would end top quartile would have been worth **+2–2.5%** a year against random selection.
- *VC.* Top-quartile firms repeat **45%** of the time.

*Measured on information available at fundraising:*
- *Post-2000 buyout.* Persistence disappears; only bottom-quartile avoidance helps.
- *First-time buyout funds* perform at least as well as any quartile.
- *VC.* Persistence survives: PME **1.70** for prior-top funds against **0.91** for prior-bottom.
- *Interim quartile noise.* Only **57%** of buyout funds showing top quartile at fundraising ended top quartile, and about 23% of bottom-quartile ones ended above median.
- *Fund size.* No significant buyout size–performance relation.

**Learning rule [I, built on K&S].** Let $\gamma_g\sim N(\mu_g,\sigma_g^2)$ be GP $g$'s persistent annual net alpha against the strategy-vintage benchmark. On a new performance signal $y$ (PME- or direct-alpha-based, annualised), apply the Kalman update
$$\mu_g\leftarrow\mu_g+K_g(y-\mu_g),\quad \sigma_g^2\leftarrow(1-K_g)\sigma_g^2,\quad K_g=\frac{\sigma_g^2}{\sigma_g^2+\tilde\sigma^2_{\varepsilon}(a)}.$$
- $\tilde\sigma^2_\varepsilon(\text{final})$ is set so that the first final-fund gain equals K&S's $s_\gamma$.
- $\tilde\sigma^2_\varepsilon(a)$ is larger for interim signals at young ages.

### 2.4 Fund-level mechanisms that move LP cash flows
- **Subscription lines.**
  - *Usage and effect [S: Albertus & Denes, Burgiss data 2014Q2–2019Q1].* 26.6% of funds used lines. Mean leverage among users was 5.8% of called capital, and lines persist across the fund's life.
  - *Agency.* Lines mainly shift *timing*, but they raise carry and the chance of reaching the hurdle: hurdle reached only because of the line in 0.6% of funds with a 1-year line, up to 5.5% with a 4-year line.
  - *Industry evidence.* ILPA cites a Cobalt study of 498 funds: median IRR **+206bp by year 3**, falling to **35–45bp** by end of life [S].
  - *Simulation.* Schillinger, Braun & Cornel find standard use moderate but extended use able to change rankings [S: SSRN abstract via Crossref, checked in the 2026-10-18 literature review]. Albertus & Denes (2020 version) dispute the cash-management reading [S]. Their 2026 *JFQA* version is subtitled "Agency Costs and Cash Flow Management" [unverified: whether it keeps this reading; no abstract or text was accessible].
  - *Liquidity risk.* ILPA flags the risk that many lines are cleared simultaneously in a market event, bunching calls on LPs [S].
- **GP-level NAV loans and dividend recaps.** These pull distributions forward and leave the fund levered.
  - ILPA treats NAV facilities as fund-level leverage and wants LPAC consent for distribution use.
  - About 20% of facilities have funded distributions [S: via Stream 05].
  - Such distributions are often recallable [S: via Stream 05].
- **Continuation vehicles (CVs).**
  - *LP choice.* Sell at the CV price, roll, or (under ILPA guidance) keep the status quo. Elections run at least 30 calendar days or 20 business days, and non-responses default to sell [S: via Stream 05].
  - *Pricing.* GP-led deals averaged about **99% of fair market value** in H1-2026, and single-asset CVs often price at or above NAV [S: Evercore].
  - *LP elections.* LPs "overwhelmingly" take liquidity, and GPs roll their full carry in about 70% of deals [S: Hamilton Lane 2022]. A roll rate of about 15% by value in 2025 has been attributed to Houlihan Lokey [P, secondary, unverified].
- **Term extensions.** ILPA's model LPA [S]:
  - term: 10 years, plus up to two 1-year extensions (the first needs LPAC consent, the second a majority in interest);
  - management fee: ends at the initial term;
  - commitment period: 5 years, plus 1.
- **Recycling.** Capital may be re-called for investments realised within 12 months, and for fees and expenses. ILPA notes some LPs cap total investment at 110% of commitments [S].

### 2.5 Fees and net economics
- **ILPA whole-of-fund model LPA [S].**
  - Management fee: on commitments during the commitment period; afterwards on unrealised cost net of write-downs.
  - Fee income offset at 100%.
  - Waterfall: 8% compounded preferred return; 80/20 catch-up; 20% carry; clawback. These are bracketed defaults, and the fee rates are left blank.
  - ILPA also publishes a deal-by-deal (American) model. Deal-by-deal carry is paid earlier, which raises the present value of carry and the clawback exposure. Whole-of-fund carry waits until contributions plus the preferred return have been returned [I].
  - VC and growth have wider dispersion. Their gross-to-net gaps are likely larger than buyout's, but this was not verified for this session [I].
- **Sorensen, Wang & Yang.** The LP's break-even alpha is **3.08%** a year under 2/20 [S, via Stream 04 verification].
- **Phalippou.** Funds beat the S&P 500 on average before fees and fall short after fees [S].
- **CEM.** A total cost of about **380bp** on a fees-paid basis, or **571bp** of NAV: management fees about half, carry about a third [P: Top1000funds summary; the primary report was not accessed].

### 2.6 Admissibility
- **Defaulting on capital calls is not a lever for a sovereign LP.** ILPA model remedies [S]:
  - 10% interest;
  - forfeiture of distributions;
  - a forced sale at **50%** of the lesser of contributions or value;
  - forfeiture of up to **100%** of the interest.
- **Reputational and legal cost.** For an LP whose access depends on deep-pocket status (§2.2), the reputational damage would exceed the legal remedies [I].
- **Also inadmissible:**
  - using excuse rights to manage liquidity;
  - transfers without GP consent;
  - counting an internal transfer to ADIC's Secondaries group as liquidity (context file, §1A);
  - moving material non-public information (MNPI) between the PE group and the Secondaries or Capital Solutions groups.

---

## 3. Methods and models: trade-offs

### 3.1 Pacing methods
| Method | Mechanism | Strengths | Weaknesses | Role at ADIC |
|---|---|---|---|---|
| OC rule of thumb | Commit so that (U+FV)/target ≈ 1.3–1.9× [S: ERSRI 1.5–1.9×] | Simple, IC-legible | Ignores regime, lags, cash | Guard-rail metric |
| Deterministic TA ("Yale") | Average call, distribution and NAV path [S: Stream 04] | Transparent | No dispersion or regime | Baseline and sanity check |
| Stochastic TA plus MPC | Linear state-space; re-optimise each period [S: Luxenberg et al.] | Convex; produces duals | Model-error sensitive | Core pacing optimiser |
| RFT-TA engine (Stream 04) | Regimes, exit factor, effective-age clock | Scenario-ready | More parameters | Plant model for all G1 decisions |
| Parametric policy search | $n_t=f_\theta(\text{state})$, tuned on 50k paths | Robust; interpretable rules | Local optima | IC "pacing playbook" |
| Stochastic programming with integer tickets | Scenario tree plus MILP for fund-level tickets | Captures lumpiness and minimum tickets | Heavy | Annual commitment budget allocation |
| Market timing of vintages | Commit more after low fundraising | Predictability exists | Investable gains "modest at best" [S: Brown et al. w26755] | Small tilt only |

### 3.2 Control-theoretic results [I, synthetic]
The experiment applies a −20% shock to total fund value $W$ and a four-year drought. The target PE NAV share is 30%, with feed-forward pace growing with $W$:

| Rule | Gain k | Peak NAV/W | Trough NAV/W | Relative s.d. of commitments | Minimum commitment (× plan) |
|---|---|---|---|---|---|
| NAV-targeting | 0.30 | 41.7% | 25.6% | 0.21 | 0.41 |
| NAV-targeting | 0.60 | 39.9% | **22.6%** | 0.46 | **0.03** |
| Exposure-targeting | 0.30 | 41.4% | 28.3% | 0.15 | 0.45 |
| Exposure-targeting | 0.60 | 39.6% | **28.2%** | 0.23 | 0.00 |

**Lessons.**
1. The denominator spike (to about 40–45%) cannot be undone quickly by pacing. It must be tolerated through bands, or met with SELL or REFINANCE.
2. Exposure feedback removes most of the overshoot.
3. Without integral action or a growth-adjusted feed-forward, proportional rules carry a steady-state error.

**Default.** MPC on $E^{econ}$ with a move-suppression penalty, or the rule $n_t=n^{ff}_t+k_E(E^\*_t-E_t)$ with $k_E\approx0.15$–0.3 a year, clipped to a corridor.

### 3.3 Valuing levers on one kernel
Let $\mu_{t,s}=m_{t,s}(1+\lambda_{t,s})$, where $m$ is the pricing kernel and $\lambda$ is the liquidity multiplier, i.e. the dual. This avoids the units error flagged in Stream 04's verification. A lever $\ell$ with cash-flow change $\Delta CF^\ell$ is worth
$$\mathcal V^\ell=\sum_{t,s}\mu_{t,s}\,\Delta CF^\ell_{t,s}\;-\;\kappa^{GP}_\ell\;-\;H^{vint}_\ell\;-\;\text{Irrev}_\ell .$$

For a pacing cut, $\sum m\,\Delta CF=-\mathrm{NPV}_m(\text{vintage})$. The cut pays only if $\lambda$ in years 1–4 sufficiently exceeds $\lambda$ in years 6–14.

**Implied financing rates for the IC.** Synthetic rows are [I]; the others come via Stream 05:

| Lever | Cash speed | Implied cost of liquidity | Extra costs |
|---|---|---|---|
| Pause one vintage | 20% of forgone in year 1; ≈69% by year 4 | ≈10.5–11% (IRR of ΔNCF) [I, synthetic] | Access penalty, vintage hole, co-investment flow |
| Halve pace for two years | 10% in year 1; ≈63% by year 4 | ≈10.7% [I, synthetic] | Same, smaller per year |
| LP-level NAV facility | 6–12 weeks | ≈7–9% all-in [via 05] | Covenant and sweep put |
| LP-led sale, quality buyout | 3–9 months | 8–15% against own forecasts [via 05] | Access signal; tail-end ≈70% of NAV [S: Evercore] |
| Preferred equity | 2–4 months | 12–20% [via 05, I] | Path dependence |
| Default | n/a | Inadmissible | Forced sale at 50% to 100% forfeiture [S: ILPA] |

### 3.4 Modelling access and relationships
| Option | Form | Data | Use |
|---|---|---|---|
| Tier table | Fixed $\kappa$ by GP tier | Judgment | Day-1 default |
| Markov access state | {in, waitlist, out}; transitions depend on skip, sale and demand | ADIC re-up history | Scenario engine |
| Relationship-capital logit | $p=\sigma(\theta_0+\theta_1 RC-\theta_2 D-\theta_3 S)$ | Commitments, demand proxies | Optimiser penalty (§6.5) |
| Real-option least-squares Monte Carlo (LSMC) | Sequence of re-up options on $\gamma_g$ beliefs | Fund-level performance | Valuing must-keep relationships |

### 3.5 Producing and grading forecasts
- **GP projections and house look-through models** (EBITDA growth, leverage, exit multiple, exit date). Known biases:
  - optimistic timing (the deck's memo corpus);
  - inflated interim NAVs around fundraising at weaker GPs [S: Brown, Gredil & Kaplan; Barber & Yasuda, title and venue only];
  - IRR inflated by subscription lines [S: Albertus & Denes];
  - interim quartiles that are noisy [S: HJKS, 57%].
- **NAV roll-forward:** lagged NAV plus beta times public return, plus calls minus distributions (Stream 04 E7).
- **Pacing models.** Stream 04.
- **Grading** applies Stream 07's proper scoring with PE-specific metrics (§6.9).

---

## 4. Empirical evidence and current market data

### 4.1 Market state relevant to the PE group (dated)
| Item | Value | As of | Source |
|---|---|---|---|
| Global private-capital fundraising | $1.3tn, about flat; buyout −16% to $395bn | FY2025 | [S] Bain GPER 2026 |
| Funds closed | −18% all strategies; −23% buyout; average buyout fund +4% | FY2025 | [S] Bain |
| US PE fundraising | $159.6bn across 223 funds (FY2025: $308bn across 551; 2021–24: $371–408bn a year, up to 1,095 funds) | H1-2026 | [S] PitchBook via Cherry Bekaert |
| Concentration | KKR NA XIV ($23bn) plus Clearlake VIII ($14.8bn) ≈ 24% of YTD (derived); experienced versus emerging managers $139.3bn vs $20.3bn | H1-2026 | [S] same |
| First-time funds | 23 closed, against a 2021–23 average of 181 a year | H1-2026 | [S] same |
| LP constraint | 53% limited by undrawn commitments (+15pp year on year) | Survey Aug–Oct 2025 | [S] PEI via Bain |
| LP preference | About two-thirds lean toward MOIC over near-term liquidity | 2025–26 | [S] ILPA via Bain |
| LP allocation | About one in five reducing buyout allocations; a large majority maintaining or increasing | Mid-2026 | [S] Bain midyear |
| LP demands | Top-quartile results, often >20% net IRR for buyout, plus top-quartile DPI | 2026 | [S] Bain |
| Re-raise failure | About 15% of fund series in normal times; about 20% in the GFC; about 70% of expected re-raises done | 2026 | [S] Bain |
| Distributions | PE distribution rate 9% (MSCI); buyout distribution yield 14.8% vs 23.4% long-run (PitchBook) | H1-2026 / 30 Jun 2026 | [S] via Stream 04; Cherry Bekaert |
| DPI by vintage | 2017–21 vintages below the historical benchmark (average median DPI of 2010–17 vintages) for every vintage | Q3-2025 | [S] Bain |
| Stale marks | "marks that likely don't reflect a realistic clearing price" for vintages from 2015 to the 2022–23 rate reset | Q2-2026 | [S] MSCI |
| Holding periods | Average at exit about 7 years; about 32–33k unsold companies (about $3.8tn) | 2025–26 | [S] Bain |
| CVs | +62% year on year, 37% a year since 2022; <10% of exit value; LPs tolerate about one CV a year | 2025 | [S] Bain |
| Seller mix | SWFs 12% → 21% of LP-led volume; 88% intermediated; LP-led dry powder $90bn (−15% YTD) | H1-2026 | [S] Evercore |
| Pricing | Quality buyout "in the 90s"; tail-end about 70% since 2022; GP-led about 99% of FMV | H1-2026 | [S] Evercore |
| Software | Q1-2026 marks −8% (US −8.9%, Europe −4.2%) | 31 Mar 2026 | [S] Bain midyear |
| Geography | US stocks beat buyout over the past decade; PE still leads in Europe | Q3-2025 | [S] Bain (MSCI data) |
| Evergreen PE (US) | $99bn, from $50bn a year earlier | 2026 | [S] Cherry Bekaert |

### 4.2 Synthetic calibration of the PE-primaries program [I, synthetic; not ADIC data]
History: normal regime to 2021, drought 2022–26 ($m^D=0.5$, $\kappa=0.6$, $G=7\%$); end-2026 NAV scaled to $52bn.

| Commitment history | 2026 pace ($bn) | Unfunded ($bn) | U/NAV | 2026 calls | 2026 distributions | 2026 NCF |
|---|---|---|---|---|---|---|
| Flat (mature) | 5.1 | 12.3 | 0.24 | 4.9 | 5.2 | **+0.2** |
| 7% a year growth | 7.8 | 17.0 | 0.33 | 6.5 | 4.1 | −2.4 |
| 10% a year to 2022, then flat | 6.6 | 15.7 | 0.30 | 6.2 | 3.9 | −2.3 |
| 15% a year growth | 11.5 | 22.9 | 0.44 | 8.4 | 3.2 | −5.2 |
| 20% a year growth | 14.2 | 26.8 | 0.52 | 9.6 | 2.7 | **−6.9** |

The engine's 2026 distribution rate is 10.6%, against MSCI's 9–11%.

**Pacing levers from 2027 (mature pace, drought persisting to 2029):**

| Lever | ΔNCF 2027–30 (cumulative) | ΔNCF 2027–40 (cumulative) | ΔNAV 2031 |
|---|---|---|---|
| Pause 2027 | +$3.6bn (69% of forgone) | −$4.1bn | −8.6% |
| Pause 2027–28 | +$6.4bn (63%) | −$7.8bn | −16.1% |
| Halve 2027–28 | +$3.2bn (63%) | −$3.9bn | −8.0% |

- Under a U-shaped recovery the four-year release is 61–66% of forgone commitments.
- **Subscription lines.** A one-year call delay on new vintages lifts unfunded by **$4.3bn by 2031**. That is near-certain deferred calls that conventional unfunded reports understate.
- **PV dollar-duration** per \$1 committed: 4.39 (normal, 8% discount) and 7.75 (drought).

### 4.3 Synthetic gross-to-net (ILPA-style waterfall; Stream-04 schedule) [I, synthetic]
| Gross IRR | 8% | 11% | 14% | 18% | 22% |
|---|---|---|---|---|---|
| Net IRR (fees 1.75% / 1.25%, 20% carry, 8% preferred return) | 5.5% | 8.1% | 10.1% | 13.7% | 17.4% |
| Spread | 2.5pp | 2.9pp | 3.9pp | 4.3pp | 4.6pp |

These spreads understate the often-quoted 4–6pp, because TA's long holding life spreads fees over more years. Treat them as lower bounds.

---

## 5. Practitioner and peer practice; case studies

1. **Cliffwater pacing plan for Rhode Island ERSRI (December 2023) [S].**
   - *Program.* Annual commitments of $240–480m (about 87% buyout and 13% VC).
   - *Base case.* PE NAV drifts from 16.2% of plan assets to 11.9–12.5% by 2029–32, against a 12.5% target. OC goes from 1.93× to about 1.5×.
   - *No new commitments:*
     - PE NAV falls from $1.76bn to $1.11bn by 2027 (−32% against the base case) and $0.83bn by 2028;
     - OC reaches 1.00× by 2026;
     - annual net cash flow rises by only +$18m in 2024, then +$87m, +$165m and +$208m in 2025–27, so about **40%** of the $1.2bn forgone returns within four years.
   - *Denominator shock (assets −10%).* PE weight rises from 16.2% to 18.4%; with a combined shock, 21–23%.

   **Lessons:** (i) pacing cuts release cash slowly; (ii) plans should show both reported and economic OC; (iii) the "no new commitments" scenario belongs in every IC pack.
2. **The 2022–26 LP playbook [S].**
   - Pacing cuts: 53% of LPs constrained.
   - Proactive intermediated portfolio sales, with SWFs the fastest-growing seller group.
   - CV elections, and tolerance for GP NAV facilities.
   - Concentration on proven managers: experienced-to-emerging fundraising about 7:1.
3. **Endowment-model lesson.** The 1990s endowment edge was access to top VC (Sensoy et al.) and better re-up selection (Lerner et al.). Both are now harder to obtain. The edge that remains is **disciplined, graded re-up decisions**, plus fee bargaining at scale (Begenau & Siriwardane) [S/I].
4. **ILPA documents are de facto contract templates.**
   - Subscription lines (2017);
   - continuation funds (2023; draft update June 2026, per Stream 05);
   - NAV facilities (2024);
   - model LPAs (2020).

   ADIC's side letters should encode: IRR with and without lines; the preferred return accruing from the draw date; LPAC consent for distribution-purpose NAV loans; a status-quo option in CVs; no management fee during extensions [S/I].
5. **Tooling.** Data come from MSCI/Burgiss, Hamilton Lane (Cobalt), SPI by StepStone and Preqin [S]. Practitioners project legacy funds with TA-type curves and add curves for new commitments, as Cliffwater does. Vendor pacing methodologies were not verified this session.

---

## 6. Design implications for the ADIC framework

### 6.1 Interfaces
**PE (G1) supplies:**
- program state;
- the commitment budget by strategy and quarter;
- GP access scores and penalties;
- fund-level forecasts with grades;
- the CV, extension and NAV-loan event calendar.

**G1 consumes:**
- the RFT-TA engine (Stream 04);
- secondary bids (Secondaries G2, Stream 05);
- NAV-facility and preferred-equity terms (Capital Solutions G3);
- co-investment value per dollar (Co-investment G4);
- PE-beta hedges and synthetic replacement of forgone vintage beta (Overlay G7);
- liquidity duals $\lambda_{t,s}$ (optimiser, Stream 01).

### 6.2 State variables
| Symbol | Meaning | Level |
|---|---|---|
| $K_i,U_i,C^{cum}_i,D^{cum}_i,N^{rep}_i,V_i$ | Commitment, unfunded, cumulative calls and distributions, reported and economic NAV | Fund interest |
| $a_i,a^e_i,T^{LPA}_i,x_i$ | Age, effective age, LPA term, extensions used | Fund interest |
| $B^{SL}_i,\ B^{NAVL}_i$ | Estimated fund-level subscription-line and NAV-loan balances | Fund interest |
| $Rc^{avail}_i$ | Recallable distributions still callable | Fund interest |
| $\mathcal F_i$ | Fee and carry state: basis (committed or invested), rate, hurdle balance, carry accrued, clawback exposure | Fund interest |
| $(\mu_g,\sigma_g^2)$ | Belief about GP alpha (§2.3) | GP |
| $RC_g,\ D_g,\ S_g,\ \tau_g$ | Relationship capital, demand index, recent skip or sale flags, next fundraise date | GP |
| $E_t,\ OC_t,\ H^{v}_t,\ H^{g}_t$ | Exposure, over-commitment ratio, vintage HHI, GP HHI | Program |
| $\Lambda_t$ | Remaining pacing budget and corridor position | Program |
| $S_t, X_t, F_t$ | Regime and exit factor (Stream 04); fundraising-cycle index (aggregate fundraising / NAV) | Market |

### 6.3 Decision variables
| Decision | Domain | Admissibility notes |
|---|---|---|
| $n_{s,t}$: commitment budget by strategy and quarter | $\ge0$, within corridor | IC-approved corridor; overrides logged |
| $K_{g,f}$: ticket to fund $f$ of GP $g$ | $\{0\}\cup[K^{min},\min(K^{max},\psi\cdot\text{FundSize})]$ | Only when $g$ is in market; realised $\tilde K=\min(K,A_{g,f})$ under cutbacks |
| Re-up choice | {up-size, same, down-size, skip} | Feeds $S_g$ and $RC_g$ |
| $\phi_{i,t}$: fraction of interest sold | [0,1]; executed through Stream 05 | Sale to the ADIC Secondaries group carries no liquidity credit |
| $b_t$: LP-level NAV-facility draw | Within LTV and encumbrance caps | Investment-policy permission (open question) |
| $e_{i,j}$: CV election | {sell, roll, status quo, roll + top-up} | Conflict check if G2 or G4 is a CV buyer |
| Extension vote, consent to GP NAV loans | {approve, condition, deny} | LPAC seat required |
| Side-letter terms at commitment | Fee tier, subscription-line opt-out or prefunding, co-investment rights | Negotiated |

### 6.4 Transitions, coupled to Stream 04
- **T1 New fund.** $\tilde K_{g,f}$ enters as a new cohort. Its alpha prior is the posterior $\mu_g$, shrunk to the strategy mean. Initial calls are $\lambda^0_s\tilde K$.
- **T2 Subscription-line shift.** The call hazard is evaluated at age $a-\tau^{SL}_i$. In crisis, add a clean-up call $c^{SL}B^{SL}_i$ (Stream 04 E5 stress add-on).
- **T3 GP NAV loan.**
  - $D_{i,t}\mathrel{+}=\ell_{i,t}V_{i,t}$, with a recallable share $\rho^{rc}$.
  - The loan accrues at $r_b+m$.
  - Repayment is swept from future distributions: $D_{i,\tau}\leftarrow D_{i,\tau}-\min(D_{i,\tau},\,s\,B^{NAVL}_{i,\tau})$.
- **T4 CV election.** For an asset share $\omega_j$:
  - **sell** pays $p_j\omega_jV_i$;
  - **roll** keeps $\omega_jV_i$ under new fees and carry $(f^{CV},c^{CV})$ and a new term;
  - **status quo** leaves terms unchanged.
- **T5 Extension.** When $a>T^{LPA}$ and an extension is approved, the effective-age clock continues and the management fee steps to $m^{ext}$ (ILPA model: 0).
- **T6 Sale.** $(U_i,V_i)\leftarrow(1-\phi)(U_i,V_i)$. Proceeds follow Stream 05's price $\pi\cdot N^{ref}$ plus post-reference adjustments. The buyer assumes the sold unfunded.
- **T7 Recycling.** Distributions flagged recallable increase $U_i$ (capped at 110% of commitment if the LPA says so).
- **T8 Fees.** These are explicit cash flows inside calls. Do not net them inside $G$; Stream 04's verification flags fee-drift omission.

### 6.5 Relationship and access sub-model
- **R1 Belief** (§2.3). Prior $\sigma_{\gamma}$: buyout 6.0%, VC 4.9% a year [S: K&S, $100\sigma_\gamma^2$ = 0.361 and 0.243]. First final-fund gain $s_\gamma$: buyout 0.15, VC 0.04.
- **R2 Expected excess value per \$ committed.**
$$v_g=\Big[(\mu_g-h_s)\Phi(z)+\sigma_g\varphi(z)\Big]\cdot D^{PV}_s,\qquad z=(\mu_g-h_s)/\sigma_g.$$
- **R3 Access probability.**
$$p_{g,k}=\sigma(\theta_0+\theta_1RC_g-\theta_2D_g-\theta_3S_g),\qquad RC_{g,t+1}=\delta RC_{g,t}+\tilde K_{g,t}/\bar K.$$
- **R4 Relationship value.**
$$O_g=\sum_{k\ge1}\beta^{\tau_k}\,p_{g,k}\,v_g\,K_{g,k}.$$
- **R5 Penalty.** $\kappa^{GP}_g(\text{action})=O_g(\text{baseline})-O_g(\text{after skip or sale})$.
- **R6 Co-investment link.** $\mathbb E[\text{CoinvFlow}_{g}]=\rho_g\,p_g\,\tilde K_g$, with $\rho\approx0.2$ by default (alternative vehicles = 17% of commitments [S: Lerner et al.]). G4 values each dollar.

**Worked illustration [I, synthetic].** A buyout GP with $E[(\gamma-h)^+]=1.5\%$, a ticket of $500m and $D^{PV}=4.4$ gives one-fund value ≈ $33m. A skip that cuts access probability by 0.3 costs about $10m (2% of the ticket), and about 3–4% including later funds. For an elite VC GP with $E[(\gamma-h)^+]=4\%$, $D^{PV}\approx5.5$, $\Delta p=0.8$ and a $150m ticket, the penalty is about $26m, or **≈18%** of the ticket.

### 6.6 Constraints
| Constraint | Default [I unless tagged] |
|---|---|
| No default on calls (hard; calls are exogenous obligations) | [S: ILPA remedies] |
| OC band, economic and reported | 1.25–1.6× economic; tighten the upper bound in drought |
| Pacing corridor | Annual $n$ within 0.75–1.25× plan; IC override to 0.5–1.5× |
| Vintage concentration | Any vintage ≤15% of PE NAV; vintage HHI ≤0.10 (synthetic base 0.076) |
| GP concentration | GP ≤6% of exposure; top-10 GPs ≤45%; ADIC ≤15–20% of any fund [P]. Rationale: fund-level buyout volatility is about 33% (via Stream 04), of which roughly 28% is idiosyncratic [I]; with an effective 60–90 funds the program's idiosyncratic volatility is about 3–3.6% |
| Strategy and geography bands | IC-set; see the synthetic defaults in §6.12 |
| Tier-1 liquidity (deck) | Stressed 12-month calls = $\sum_s\lambda^{12m,str}_sU_s+c^{SL}\sum B^{SL}$; default stressed call rate 0.30–0.35 of U |
| Sale budget | LP-led sales ≤ IC cap a year; flag core-GP interests; GP-led execution probability ≈0.73 [S: via 05 verification] |
| Monotonicity | Pacing non-decreasing in the cushion above the protected distribution floor (Stream 11) |

### 6.7 Objective terms (Tier 2)
$$\max\ \mathbb E\Big[\text{TA}(\cdot)\Big]+\sum_{t,s}\mu_{t,s}\Delta CF_{t,s}-\sum_g\kappa^{GP}_g-w_\Delta\sum_t(n_t-n_{t-1})^2-w_H\,H^v-\text{fees}$$
The terms are:
- **TA:** the target-attainment objective of Streams 01 and 11.
- **Liquidity:** $\mu_{t,s}\Delta CF_{t,s}$ uses NPV-consistent duals.
- **Access:** $\kappa^{GP}$ penalises skips and sales.
- **Move suppression:** $w_\Delta(n_t-n_{t-1})^2$ stands for the organisational and relationship cost of lumpy pacing.
- **Vintage concentration:** $w_HH^v$.
- **Fees:** explicit fee drag.

### 6.8 SELL / HOLD / REFINANCE / LEVER for the PE group
| Action | Instruments | Economics | Program-level side effects |
|---|---|---|---|
| **SELL** | LP-led single, portfolio or strip sale; tail-end clean-up; deferred-payment sale; CV *sell* election (cash at ≈99% of FMV) | Stream 05 price; liquidity released = price + avoided stressed calls | Vintage hole if young funds are sold; $\kappa^{GP}$ if a core GP; signalling (lower when intermediated) |
| **HOLD** | Baseline; CV status quo or roll; approve extensions with fee step-down | RFT-TA continuation value | Ageing NAV; adverse selection in residual assets |
| **REFINANCE** | LP-level NAV facility; preferred equity; consent to GP NAV loans (pulls distributions forward) | Stream 05 cost ladder; covenant put | Encumbrance; recall risk on NAV-loan distributions |
| **LEVER** | Over-commit or up-size re-ups; CV roll + top-up; ADIC-level borrowing to fund calls (Stream 06) | Marginal fused $\hat\alpha$ net of fees, $\lambda$ and the Tier-1 gate | Higher $E$ and $OC$; more stressed calls |
| **SLOW PACING** | Cut $n_{s,t}$ within the corridor | Implied financing rate ≈ forgone vintage IRR; cash slow (20% of forgone in year 1) | Vintage hole in years 6–14; access; lower co-investment flow |
| **Inadmissible** | Call default; excuse abuse; non-consented transfer; intra-ADIC transfer counted as liquidity | n/a | n/a |

### 6.9 How the PE group's forecasts enter return fusion
**Forecast object per fund and quarter:**
- call and distribution vectors with P10, P50 and P90;
- expected terminal TVPI;
- exit-date and multiple assumptions for the top holdings;
- a source tag (GP projection, look-through, roll-forward or pacing model).

**The three series:**
- **Underwritten:** the IC memo's net IRR and TVPI targets and pacing.
- **Actual:** since-inception PME or direct alpha. Net IRR is reported but flagged when lines are used.
- **Forecast:** the PE group's view.

**Pipeline:**
1. Convert each series to an implied forward alpha on economic NAV and a timing multiplier $\kappa^F_i$ (Stream 04 E3).
2. Remove bias. The level bias $b_F$ applies by GP tier and strategy. The timing slip $\delta^F$ (quarters) defaults to +2 to +4 in normal regimes and +4 to +8 in drought [I], pending ADIC's history. A fundraising haircut applies when an underperforming GP is in market [S: BGK].
3. Fuse with Stream 07's GLS/credibility model.

**Grading** (per GP, strategy, analyst and forecast vintage), on rolling 4–8 quarter windows:
- **Level:** Mincer–Zarnowitz regression $D^{real}=a+bD^{fcst}$, where $b<1$ signals optimism.
- **Timing:** centroid shift $\Delta c=\frac{\sum\tau D^{fcst}_\tau}{\sum D^{fcst}_\tau}-\frac{\sum\tau D^{real}_\tau}{\sum D^{real}_\tau}$.
- **Calibration:** P10–P90 coverage and CRPS.
- **Terminal:** TVPI error for exited funds.

Credibility weights follow Bühlmann–Straub, $Z=n/(n+k)$.

### 6.10 Parameter defaults
| Parameter | Default | Source |
|---|---|---|
| Normal-regime multipliers $M_N$, $M_U$; distribution and call rates | 6.88; 2.41; 25%; 28% | [I, synthetic; Stream-04 parameters] |
| Drought distribution rate (2026) | 10.6% in the engine | [I] vs MSCI 9–11% [S] |
| Exposure gain $k_E$; MPC horizon | 0.15–0.3 a year; 8–12 quarters | [I] |
| GP alpha prior s.d.; first-fund gain $s_\gamma$ | Buyout 6.0%, 0.15; VC 4.9%, 0.04 | [S: K&S] |
| Hurdle $h_s$ for access value | 0 to +1% over the strategy benchmark | [I] |
| $\Delta p$(access) after a skip | Elite 0.6–0.8; core 0.2–0.4; open market 0–0.1 | [I] (lower now: [S] Bain/PitchBook) |
| Co-investment ratio $\rho$ | 0.2 | [S-derived: Lerner et al.] |
| Fees (headline → ADIC tier) | 1.75–2.0% → 1.25–1.5% on commitments; 20% → 15–17.5% carry; 8% preferred return; 100% offset | [S: ILPA; Begenau & Siriwardane range] |
| Subscription lines | Usage 26.6%; leverage 5.8% of called capital; IRR +2.6pp | [S: Albertus & Denes] |
| GP NAV loans | LTV 5–30%; spread 4–7%; 20% used for distributions | [S: via Streams 04/05] |
| CV | Price ≈99% of FMV; roll share ≈15% by value | [S: Evercore]; [P: unverified] |
| Term | 10+1+1 years; commitment period 5+1 years | [S: ILPA] |

### 6.11 Calibration targets and data needs
**Targets:**
- MSCI distribution and contribution rates;
- the ERSRI no-new-commitment release, about 40–46% of forgone commitments in four years;
- HJKS persistence matrices and K&S variance shares;
- Bain DPI-by-age;
- ADIC's own re-up and access outcomes and CV elections.

**ADIC data:**
- the fund ledger with daily cash flows, fees and carry;
- side letters (fee tiers, MFN, co-investment rights, subscription-line opt-outs);
- subscription-line and NAV-loan disclosures per fund;
- the GP fundraising calendar and allocation cutbacks;
- PE group forecast archives;
- IC memos (underwriting);
- secondary-sale history and GP reactions.

### 6.12 SPECIFICATION CARD (G1, PE primaries)
| Item | Specification |
|---|---|
| **Data fields** | Fund: id, GP, strategy (large / mid buyout, growth, VC, sector), region, vintage (first cash flow and first close), K, U, calls, distributions (flagged recallable), NAV (reported, economic), fees, carry state, line balance and days outstanding, NAV-loan balance, LPA term and extensions, LPAC seat. GP: belief (μ, σ²), tier, demand index, next fundraise, relationship capital, skip and sale flags, co-investment history. |
| **Cash-flow and return equations** | Stream 04 E2–E7 per fund, plus T1–T8. Program: $E=U+N^e$, $OC=E/(w^\*W)$. Pacing: MPC on $E$ or $n=n^{ff}+k_E(E^\*-E)$. |
| **Parameter defaults** | §6.10, e.g. $M_N$ 6.88; $k_E$ 0.15–0.3; buyout $s_\gamma$ 0.15; $\rho$ 0.2; ILPA fee terms |
| **Liquidity terms and stress** | Calls are sticky (rates 27–31%, via Stream 04) and fall only modestly in crisis; add subscription-line clean-up. Distributions collapse (9–11% rate). Pacing changes act with 1–4 year lags: 20% of forgone in year 1. |
| **SELL** | LP-led sale at the Stream 05 price, or CV sell election. Cost = buyer's excess return + $\kappa^{GP}$ + vintage hole. Best for tail-end and non-core GPs. |
| **HOLD** | Baseline; status-quo or roll CV option; extensions only with fee step-down |
| **REFINANCE** | LP-level NAV facility (≈7–9%); preferred equity (12–20%); conditional consent to GP NAV loans |
| **LEVER** | Over-commit or up-size where fused alpha > hurdle; roll + top-up in high-conviction CVs; never fund via call default |
| **Slow pacing** | Implied financing ≈ vintage IRR (10.5–11% synthetic) plus access penalty; use only for multi-year, anticipated liquidity needs |
| **Forecasts and biases** | GP projections, look-through, roll-forward, pacing model. Biases: timing optimism; fundraising-period NAV inflation; subscription-line IRR inflation; interim-quartile noise. Graded by MZ, centroid shift, CRPS and coverage. |
| **Synthetic defaults** | Labelled SYNTHETIC: 120 interests, about 70 GPs. Mix: large buyout 40%, mid buyout 25%, growth 12%, VC 8%, sector 10%, special situations 5%. Regions: US 60%, Europe 28%, Asia 12%. NAV $52bn. Two unfunded cases: $12bn (mature) and $25bn (working assumption). GP tiers: elite 10% of GPs (20% of NAV), core 50% (60%), other 40% (20%). |
| **Links** | G2 bids (no liquidity credit for internal transfers); G3 facility terms; G4 co-investment flow ($\rho$); G5 liquidity reservoir; G6 shared GPs and lenders; G7 beta hedge and synthetic vintage replacement; Treasury payout and calls |

---

## 7. Implementation notes
- **Libraries.**
  - Simulation: numpy, numba or JAX; xarray (path × quarter × fund).
  - Optimisation: cvxpy (MPC, convex surrogate); Pyomo with HiGHS or OR-Tools (MILP tickets and fund-size caps); mpi-sppy (scenario trees).
  - Statistics: PyMC or NumPyro (hierarchical K&S learning, access logits); lifelines (re-raise and allocation hazards); scoringrules (CRPS); statsmodels.
- **Algorithms.**
  - Use common random numbers across lever variants.
  - Compute the implied IRR of ΔNCF with a bracketed root-finder.
  - Use LSMC for re-up option chains.
  - Run policy search with CMA-ES over rule parameters $(k_E,\text{corridor},w_\Delta)$.
- **Pitfalls.**
  - Vintage conventions: lines shift first-cash-flow vintages [S: ILPA].
  - Recallables double-counted in U.
  - Fees netted into growth.
  - Duals used as rates (use NPV).
  - Integer tickets and per-fund caps make the problem non-convex. Solve the budget as an LP, then allocate tickets by MILP.
  - Access logits are non-convex. Apply them as scenario penalties or piecewise-linear cuts.
  - Fit K&S parameters on post-2000 data and do not over-fit them.
  - FX for non-USD funds.
  - Quarter-lag alignment to the payout date.
  - Run the scripts in isolated mode (`python -I`).

## 8. Risks, pitfalls and limitations
- **Structural drought.** Distribution normalisation may never return to 2017–19 levels. Use the Stream-04 Φ sensitivity.
- **Optimizer's curse in GP selection.** Shrink posteriors, and remember that post-2000 buyout persistence at fundraising is weak.
- **Relationship-value inflation.** $\kappa^{GP}$ is judgmental. Report break-even $\kappa$ rather than point estimates.
- **Endogenous GP behaviour.** Lines, NAV loans and CVs respond to the same drought; GPs control the timing.
- **Conflicts of interest.** G2 or G3 as counterparties; the PE group grading its own forecasts (independent grading agent).
- **Synthetic-book risk.** U/NAV mismatch (§1, item 9).
- **Evidence gaps.** Several market figures come through other streams. CEM and CV roll rates are secondary-source only. The seed references named in the brief were verified except the published Cavagnaro magnitude (abstract summary). Hochberg et al., previously seen via K&S only, was checked against its *RFS* abstract in the 2026-10-18 literature review.

## 9. Open questions (ADIC to supply or confirm)
1. **Unfunded.** True PE-primaries unfunded by vintage and strategy, and the commitment history since 2010. This decides the sign of near-term PE cash flow.
2. **GPs and terms.** The GP list, tiers, next fundraise dates and allocation cutbacks; side-letter fee tiers; co-investment rights.
3. **Fund-level leverage.** Can ADIC opt out of subscription lines or prefund? Current line and NAV-loan exposure per fund.
4. **Pacing governance.** IC policy on the corridor, OC band, and override governance.
5. **Liquidity instruments.** Are LP-level NAV facilities and preferred equity permitted under the investment policy?
6. **Track records.** History of re-ups skipped and subsequent access; CV elections; secondary sales and GP reactions.
7. **Forecast archive.** PE group forecast archives (projections versus realisations) for bias calibration.
8. **Internal transfers.** Treatment of intra-ADIC transfers (PE to Secondaries) and the conflict walls between groups.

## 10. References
**Academic**
- Albertus, J. F., & Denes, M. (2020). Private Equity Fund Debt: Capital Flows, Performance, and Agency Costs (version 26 May 2020; every Albertus & Denes figure in this dossier comes from this version). https://conference.nber.org/conf_papers/f141738/f141738.pdf. Earlier version: "Distorting Private Equity Performance: The Rise of Fund Debt", *SSRN Electronic Journal* (2019), SSRN 3410076, DOI 10.2139/ssrn.3410076. Journal version, same two authors and main title: Albertus, J. F., & Denes, M. (2026). Private Equity Fund Debt: Agency Costs and Cash Flow Management. *Journal of Financial and Quantitative Analysis*, online 7 May 2026, pp. 1–64 (no volume or issue yet). DOI 10.1017/s0022109026102890 (Crossref, OpenAlex) [unverified: whether its figures match the 2020 version; neither index has an abstract and the publisher page returned 403].
- Begenau, J., & Siriwardane, E. (2024). Fee Variation in Private Equity. *Journal of Finance* 79(2), 1199–1247. DOI 10.1111/jofi.13319. Working paper: "How do Private Equity Fees vary across Public Pensions?", NBER w29887 (2022), https://doi.org/10.3386/w29887. Summary (source of the figures quoted here): https://corpgov.law.harvard.edu/2024/05/10/fee-variation-in-private-equity/
- Brown, G., Gredil, O., & Kaplan, S. (2019). Do Private Equity Funds Manipulate Reported Returns? *JFE* 132(2), 267–297. DOI 10.1016/j.jfineco.2018.10.011. NBER w22493: https://www.nber.org/papers/w22493
- Brown, G., Harris, R., Hu, W., Jenkinson, T., Kaplan, S., & Robinson, D. (2021). Can Investors Time Their Exposure to Private Equity? *JFE* 139(2), 561–577 (online 2020). DOI 10.1016/j.jfineco.2020.08.014. Working paper (source of the §3.1 wording): NBER w26755 (2020), https://www.nber.org/papers/w26755
- Barber, B., & Yasuda, A. (2017). Interim Fund Performance and Fundraising in Private Equity. *JFE* 124(1), 172–194. DOI 10.1016/j.jfineco.2017.01.001 (usage rests on title and venue only). https://escholarship.org/uc/item/01h178mf
- Cavagnaro, D., Sensoy, B., Wang, Y., & Weisbach, M. (2019). Measuring Institutional Investors' Skill at Making Private Equity Investments. *JF* 74(6), 3089–3134. DOI 10.1111/jofi.12783. Working paper, titled "Measuring Institutional Investors' Skill from Their Investments in Private Equity": NBER w22547 (2016), https://www.nber.org/papers/w22547
- Harris, R., Jenkinson, T., & Kaplan, S. (2014). Private Equity Performance: What Do We Know? *JF* 69(5), 1851–1882. DOI 10.1111/jofi.12154. NBER w17874: https://www.nber.org/papers/w17874
- Harris, R., Jenkinson, T., Kaplan, S., & Stucke, R. (2020/2023). Has Persistence Persisted in Private Equity? NBER w28109; *JCF* 81, 102361 (2023), DOI 10.1016/j.jcorpfin.2023.102361. https://www.nber.org/system/files/working_papers/w28109/w28109.pdf
- Korteweg, A., & Sorensen, M. (2017). Skill and Luck in Private Equity Performance. *JFE* 124(3), 535–562. DOI 10.1016/j.jfineco.2017.03.006. https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf
- Lerner, J., & Schoar, A. (2002/2004). The Illiquidity Puzzle: Theory and Evidence from Private Equity. NBER w9146; *JFE* 72(1), 3–40, DOI 10.1016/s0304-405x(03)00203-4. https://www.nber.org/papers/w9146
- Lerner, J., Schoar, A., & Wongsunwai, W. (2007). Smart Institutions, Foolish Choices: The Limited Partner Performance Puzzle. *JF* 62(2), 731–764. DOI 10.1111/j.1540-6261.2007.01222.x. NBER w11136 (the source of the §2.3 figures; it lists the third author as "Wan Wong" and its title ends "Choices?"): https://www.nber.org/papers/w11136
- Lerner, J., Mao, J., Schoar, A., & Zhang, N. R. (2022). Investing outside the box: Evidence from alternative vehicles in private equity. *JFE* 143(1), 359–380 (online 2021). DOI 10.1016/j.jfineco.2021.05.034. Working paper (source of the figures in §2.2 and §6.5): Lerner, J., Schoar, A., Mao, J., & Zhang, N. (2018). Investing Outside the Box: Evidence from Alternative Vehicles in Private Capital. NBER w24941. https://www.nber.org/papers/w24941 [unverified: the 32%/17% figures were not re-checked against the *JFE* version; Crossref and OpenAlex have no abstract and the publisher page returned 403].
- Phalippou, L. (2009). Beware of Venturing into Private Equity. *JEP* 23(1), 147–166. https://www.aeaweb.org/articles?id=10.1257/jep.23.1.147
- Schillinger, P., Braun, R., & Cornel, J. (2019). Distortion or Cash Flow Management? Understanding Credit Facilities in Private Equity Funds. *SSRN Electronic Journal*, SSRN 3434112, DOI 10.2139/ssrn.3434112 (SSRN ID confirmed and abstract checked via Crossref in the 2026-10-18 literature review). https://www.fa.mgt.tum.de/cefs/media-news/article/cefs-study-on-distortion-or-cash-flow-management-understanding-credit-facilities-in-private-equity-funds-receives-wide-attention/
- Sensoy, B., Wang, Y., & Weisbach, M. (2014). Limited Partner Performance and the Maturing of the Private Equity Industry. *JFE* 112(3), 320–343. DOI 10.1016/j.jfineco.2014.02.006. https://www.nber.org/papers/w18793
- Hochberg, Y., Ljungqvist, A., & Vissing-Jørgensen, A. (2014). Informational Holdup and Performance Persistence in Venture Capital. *RFS* 27(1), 102–152 (online 2013). DOI 10.1093/rfs/hht046 (abstract checked in the 2026-10-18 literature review).
- Via Stream 04 / 05 (verified there; metadata confirmed in the 2026-10-18 literature review):
  - Takahashi & Alexander (2002). Illiquid Alternative Asset Fund Modeling. *JPM* 28(2), 90–100. DOI 10.3905/jpm.2002.319836.
  - Luxenberg, Boyd, van Beek, Cao & Kochenderfer (2022). Strategic Asset Allocation with Illiquid Alternatives. ICAIF '22 proceedings, pp. 249–256. DOI 10.1145/3533271.3561769. Preprint: https://arxiv.org/abs/2207.07767
  - Sorensen, Wang & Yang (2014). Valuing Private Equity. *RFS* 27(7), 1977–2021. DOI 10.1093/rfs/hhu013. NBER w19612: https://www.nber.org/papers/w19612
  - Robinson & Sensoy (2016). Cyclicality, performance measurement, and cash flow liquidity in private equity. *JFE* 122(3), 521–543. DOI 10.1016/j.jfineco.2016.09.008. NBER w17428: https://www.nber.org/papers/w17428
  - Nadauld, Sensoy, Vorkink & Weisbach (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *JFE* 132(3), 158–181. DOI 10.1016/j.jfineco.2018.11.007. NBER w22404: https://www.nber.org/papers/w22404
  - Gourier, Phalippou & Westerfield (2024). Capital Commitment. *JF* 79(5), 3407–3457. https://doi.org/10.1111/jofi.13382

**Industry and standards**
- Bain & Company (2026). *Global Private Equity Report 2026*. https://www.bain.com/globalassets/noindex/2026/bain-report_global-private-equity-report-2026.pdf
- Bain & Company (8 June 2026). Midyear report press release. https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html
- Cherry Bekaert (2026). *Private Equity Mid-Year 2026 Report* (PitchBook data as of 30 June 2026). https://www.cbh.com/insights/reports/private-equity-mid-year-2026-report/
- Cliffwater for ERSRI (December 2023). *PE/PC/RA Pacing Plan*. https://data.treasury.ri.gov/dataset/40fb544c-65c5-464f-ba49-e3f65d1adc36/resource/7783fe26-a966-4850-82e0-f3f931812015/download/1a-cliffwater-pe-pc-ra-pacing-plan-dec-2023-final.pdf
- Evercore (July 2026). *H1 2026 Secondary Market Review*. https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
- Hamilton Lane (2022). *Market Overview: Investment Activity*. https://experience.hamiltonlane.com/investment-activity1
- ILPA (2017). *Subscription Lines of Credit and Alignment of Interests*. https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf
- ILPA (2020). *Model LPA, Whole of Fund*. https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf; overview: https://ilpa.org/model-lpa/
- ILPA (2023, 2024) Continuation funds and NAV facilities guidance (via Stream 05): https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf; https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf
- MSCI (October 2026). *Private Capital Benchmarks Summary Q2 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- CEM Benchmarking PE cost study (via Top1000funds; primary not accessed). https://www.top1000funds.com/?p=16071
- Synthetic scripts (this stream, not ADIC data; session scratchpad, may not persist): C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g1_scripts\ (g1_program_calib.py, g1_control.py, g1_fees.py, g1_ersri_check.py).

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.5 (G1 version updates) and §2.6 item 3 (Albertus & Denes), and the citation-integrity table in `research/literature/G1_pe_primaries.lit.md` §2. Metadata marked "Crossref" or "OpenAlex" was re-confirmed there on 2026-10-18. No number or conclusion in this dossier changed.

- §2.2 Hold-up: Hochberg et al. tag "as summarised by Korteweg & Sorensen; the original was not fetched" → *RFS* abstract, checked in the literature review.
- §2.2 Bargaining: author order updated to the published Lerner, Mao, Schoar & Zhang (*JFE* 2022). NBER w24941 stays the source of the figures; the tag says they were not re-checked against the *JFE* version.
- §2.4 Simulation: Schillinger et al. tag "summary only" → SSRN abstract checked via Crossref. The Albertus & Denes reading is now tied to the 2020 version, and the 2026 *JFQA* subtitle is flagged [unverified].
- §8 Evidence gaps: Hochberg et al. removed from the unverified list because its abstract has now been checked. The Cavagnaro caveat is unchanged.
- §10 Albertus & Denes: added the 2019 SSRN version (DOI 10.2139/ssrn.3410076, Crossref) and the 2026 *JFQA* version (DOI 10.1017/s0022109026102890; same authors, Crossref and OpenAlex). Its figures are unverified.
- §10 Begenau & Siriwardane: "pp. 1199–1247 (volume and issue not re-verified)" → *JF* 79(2), 1199–1247, DOI 10.1111/jofi.13319 (Crossref); added NBER w29887.
- §10 Brown, Gredil & Kaplan: *JFE* 132(2) → 132(2), 267–297, DOI 10.1016/j.jfineco.2018.10.011.
- §10 Brown, Harris, Hu, Jenkinson, Kaplan & Robinson: NBER w26755 (2020) only → *JFE* 139(2), 561–577 (2021), DOI 10.1016/j.jfineco.2020.08.014 (OpenAlex); the WP is kept as the source of the §3.1 wording.
- §10 Barber & Yasuda: *JFE* 124(1) → 124(1), 172–194, DOI 10.1016/j.jfineco.2017.01.001; the title-and-venue-only caveat is kept.
- §10 Cavagnaro et al.: added DOI 10.1111/jofi.12783 and the different title of WP w22547.
- §10 Harris, Jenkinson & Kaplan (2014): *JF* → *JF* 69(5), 1851–1882, DOI 10.1111/jofi.12154.
- §10 Harris, Jenkinson, Kaplan & Stucke: added DOI 10.1016/j.jcorpfin.2023.102361.
- §10 Korteweg & Sorensen: added DOI 10.1016/j.jfineco.2017.03.006.
- §10 Lerner & Schoar: *JFE* 72(1) → 72(1), 3–40, DOI 10.1016/s0304-405x(03)00203-4.
- §10 Lerner, Schoar & Wongsunwai: added DOI 10.1111/j.1540-6261.2007.01222.x and the WP's author and title variant.
- §10 Lerner, Schoar, Mao & Zhang (2018), NBER w24941 → Lerner, Mao, Schoar & Zhang (2022), *JFE* 143(1), 359–380, DOI 10.1016/j.jfineco.2021.05.034 (Crossref, OpenAlex). The WP is kept as the source of the figures [unverified in the published version].
- §10 Schillinger et al.: "SSRN 3434112 (summary only)" → DOI 10.2139/ssrn.3434112; SSRN ID confirmed.
- §10 Sensoy, Wang & Weisbach: added DOI 10.1016/j.jfineco.2014.02.006.
- §10 Hochberg et al.: "Hold-Up … *RFS* 27(1) (cited via K&S; not fetched)" → "Holdup … *RFS* 27(1), 102–152", DOI 10.1093/rfs/hht046.
- §10 Via Stream 04/05: short-form list → full entries. These add the ICAIF '22 version of Luxenberg et al. (DOI 10.1145/3533271.3561769), *RFS* 27(7) for Sorensen, Wang & Yang, and the *JFE* versions of Robinson & Sensoy and Nadauld et al.
- Not applicable here:
  - the G4 barrier re-run, because no barrier statistic appears in this dossier. "[S: BGK]" in §6.9 means Brown, Gredil & Kaplan, not Broadie–Glasserman–Kou;
  - the 2026-10-18 re-checks of streams 10, 11, 13, 14 and G3, because none of those works is cited here.
