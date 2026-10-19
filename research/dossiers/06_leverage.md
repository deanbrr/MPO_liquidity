# Stream 06: Portfolio-level leverage for an endowment-model SWF with illiquid assets (ADIC)

**As of:** 2026-10-18. **Scope:** when and how ADIC (~US$177bn, ~60% private, mostly PE; mandated 5–10% annual distribution; 10% nominal USD target; leverage permitted; large OTC overlay with a tail hedge and an opportunistic book) should use leverage at the portfolio and asset levels, and how to put leverage into the multi-period framework as decision variables.

**Evidence tags.** [S] = sourced fact (with date). [P] = practitioner consensus. [I] = my own inference or calculation. In the references, [V] = checked in this session against the primary source or an authoritative page; [K] = cited from domain knowledge and not re-checked in this session (please verify before external use).

**Research-process caveat.** The session's shared web-search budget ran out partway through this stream. I kept going with direct fetches of known primary-source URLs only. Some items therefore rest on search-result excerpts rather than full-document reads, and they are flagged "(via search excerpt)". Gaps that could not be closed are listed in Section 9.

---

## 1. Executive summary

1. **Levering beta cannot reach the 10% target at October-2026 funding costs.** [I, using S rates] SOFR was 3.89% on 15 Oct 2026, the fed funds target is 3.75–4.00% after the 16 Sep 2026 hike, and the 10y UST was 5.09% on 16 Oct 2026. Take an illustrative unlevered portfolio with arithmetic mean 8% and volatility 11% (log-growth ≈7.4%). Reaching 10% log-growth by levering the whole portfolio then needs **L ≈ 2.36×** at 4.05% short-term funding, which is about 72% of full Kelly. It is **infeasible at any leverage** once funding costs ≥4.65% (synthetic futures funding) or 5.8% (AA term debt). The 10% must come from return sources (α*, mix, selection). Gearing the whole book will not get there.
2. **For ADIC, leverage is mainly a liquidity and implementation tool, and only selectively a return tool.** The DPI collapse is the binding problem. Jefferies (Jul 2026) puts LP portfolios' annual distribution yield **near 10% in H1 2026**, below 20% since 2023, against a **25% average since 2001** [S]. On ~US$106bn of private NAV that is a swing of roughly **US$16bn a year** of lost cash [I], about the same size as a 9% payout. Leverage is rational when it (a) bridges *temporary* liquidity gaps instead of forcing secondary sales at 87–91% of NAV; (b) implements exposure synthetically in the liquid overlay ("lever the liquid, not the illiquid"); (c) finances specific assets whose forward return clears the all-in cost of financing plus risk and liquidity shadow costs; and (d) gives countercyclical dry powder to *buy* secondaries in stress.
3. **Funding cost curve (Oct 2026), by source** [S unless noted]:
   - UST repo: about SOFR flat to +10bp [P].
   - CP/ECP for AA issuers: SOFR plus a few to tens of bp [P].
   - AA sovereign-related term bonds: **UST+55–99bp**. Examples: Mubadala 10y at T+55 in Oct 2025 (via search excerpt); PIF 10y sukuk at **T+85** on 21 Jan 2026; PIF 3/7/30y at T+95–99 in May 2026 (via search excerpt). That is roughly **5.6–6.1% all-in at 10y**.
   - Equity-index futures: implied financing averaged ~30bp over the risk-free rate in 2021–23 and peaked above 140bp in Dec 2024 (D. E. Shaw). The June-2026 roll was **+81bp over 3m SOFR**, the richest June roll since at least 2007 (CME, via search excerpt). Morgan Stanley data showed ~200bp over fed funds on 26 Jun 2026 (Reuters).
   - PE NAV facilities: **4–7% margins** (Rede, Jun 2026), with LTV 5–30% at close.
   - **The implied financing rate of a secondary sale is often the most expensive source of all.**
4. **The asset-level lens comes down to a three-way comparison priced with the optimizer's liquidity shadow price λ.** [I] HOLD is worth $e^{\alpha^* T}$. SELL is worth $(1-d)(1+\lambda)$. LEVER is worth $e^{\alpha^* T} + \lambda - (c-r_f)\tau - $ covenant and recourse costs. Worked example: a buyout LP interest with α* ≈ +0.2%/yr, 9% discount, λ = 15% in stress. Portfolio-level AA term debt beats selling for any plausible bridge duration. A **NAV loan beats selling only if repaid within ~2 years**. For a structural gap, sell (or restructure the payout).
5. **The cheapest tail protection is the payout band plus a small debt-funded liquidity reserve, not return-seeking leverage.** [I, stylized Monte Carlo, Section 6.9] At 7.5% payout, the 5-year probability of a forced secondary sale is **6.4% with no debt**. It falls to **0.1%** with a 10%-of-NAV term-debt reserve (cost ≈10bp/yr) and to **0.2%** with a 5% reserve plus cutting the payout to 5% in stress. Investing 10% of NAV of debt in the liquid book adds ~30bp/yr in expected terms but lowers 5th-percentile terminal wealth by ~4pp. At 20%, the debt/NAV ratio breaches 25% (the Moody's downgrade analog) in **35%** of paths. At a 10% payout and no debt, the forced-sale probability rises to **27%**.
6. **Fixed claims change the system's risk structure.** [I, actuarial] Payouts proportional to NAV cannot cause ruin. Fixed-dollar payouts and debt service create an absorbing barrier. Using Dufresne's reciprocal-gamma result, a fixed-dollar payout of 7.5% of initial wealth with μ = 8% and σ = 12% has a **~58% eventual-ruin probability**, against 15.5% at 5%. Leverage adds fixed claims, so the payout rule and the debt policy must be optimized jointly.
7. **Recommended limits (defaults, from peers):**
   - Recourse debt ≤10% of adjusted NAV (CPP 9.7% at Mar 2025; Temasek ≈5% at Mar 2026; Moody's OTPP upgrade/downgrade triggers at <10% / >25% adjusted leverage).
   - Gross economic exposure ≤ ~1.3× NAV (OTPP's "funding and other" line was −32% of net investments in 2025, so ≈1.32×).
   - Stressed 30-day LCR ≥1.0 hard (CPP minimum 1.0; actual 6.9).
   - An NSFR-style rule that bars funding illiquid assets with short-term debt, plus an encumbrance cap.
   - Chance constraints on covenant breach.
   - BoE-style ≥250bp yield-shock collateral buffers on any rates overlay, and FSB (Dec 2024) margin-preparedness practices.

---

## 2. Core concepts and theory

### 2.1 What "leverage" means for ADIC
- **Recourse (financial) leverage:** debt with a claim on the whole fund (bonds, CP, revolvers, repo) divided by NAV. This is what rating agencies and owners focus on. DBRS excludes CPP's C$113.3bn of repo from its financial-leverage analysis because the repo "optimize[s] how this exposure is achieved" rather than adding risk [S, Sep 2025]. Moody's nets "nettable repurchase agreements and derivatives" to get OTPP's 17% adjusted leverage [S, Jul 2026]. **Definitions differ across agencies, so the framework must compute each one.**
- **Economic (exposure) leverage:** gross risk exposure, including derivative notionals, divided by NAV. A practical proxy is $1+$ |funding line|/NAV. OTPP's line implies ≈1.32× (2025) and ≈1.43× (2024) [S].
- **Look-through leverage:** debt inside fund structures and portfolio companies, including GP NAV facilities and subscription lines. ILPA (2024) notes that GPs sometimes treat NAV-facility SPVs as outside fund-level leverage limits [S]. ADIC's PE book is therefore levered already, and leverage at the ADIC level stacks on top of it.
- **Encumbrance:** assets pledged to repo, IM or NAV facilities are unavailable for other liquidity needs. Moody's cut OTPP's liquidity score one notch, citing "Asset Encumbrance" as the key driver [S].

### 2.2 Frictionless optimal leverage: Merton, Kelly and volatility drag
For a portfolio with arithmetic mean μ and volatility σ, financed at rate $r_b$, the log-growth rate at leverage $L$ is [K: Merton 1971, continuous-time model; Kelly 1956 is the source of the log-growth criterion itself, for discrete bets]

$$g(L) = r_b + L(\mu - r_b) - \tfrac{1}{2}L^2\sigma^2 .$$

The growth-optimal (Kelly) leverage is $L_K = (\mu - r_b)/\sigma^2$, and maximum growth is $r_b + \tfrac12 SR^2$ [K: the continuous-time result for log utility (Merton 1971). Kelly (1956) does not contain these formulas; they were previously cited here to a Wikipedia summary of Kelly 1956]. The CRRA investor's leverage is $L^* = (\mu - r_b)/(\gamma\sigma^2)$, so "fractional Kelly" with fraction $f$ is the same as CRRA with $\gamma = 1/f$. Three consequences matter for ADIC:
- **Kinked financing.** Lending earns $r_f$ but borrowing costs $r_b > r_f$. That creates an inaction band, $r_f < \mu - \gamma\sigma^2 < r_b$, in which $L^* = 1$ exactly. Wider borrowing spreads widen the band.
- **Volatility drag** grows with $L^2$. Leverage raises arithmetic return linearly and drag quadratically.
- **Parameter uncertainty.** Practitioners cut the Kelly fraction "to reduce the chance of ruin, reduce volatility, and account for model error" (Wikipedia, citing MacLean, Thorp & Ziemba) [V/K]. Half-Kelly or less is the standard ceiling [P]. Ang, Papanikolaou & Westerfield (2014) show that illiquidity raises *effective* risk aversion [V], which shrinks the admissible fraction further.

### 2.3 Leverage aversion and betting-against-beta: what to lever
Frazzini & Pedersen (2014) model investors who are "prohibited from using leverage" and therefore bid up high-beta assets [V]. A BAB factor that is long levered low-beta assets earns significant risk-adjusted returns across asset classes. When funding tightens, BAB returns are low. Asness, Frazzini & Pedersen (2012) apply the same logic to risk parity: safer assets earn higher risk-adjusted returns, so they should be levered [V]. **For an AA-rated sovereign investor that can borrow cheaply, the efficient use of leverage is on low-volatility, high-Sharpe exposures**: duration and carry, core infrastructure and real-asset debt capacity, market-neutral α, defensive equity. It is not efficient on the PE-heavy aggregate, which already carries embedded leverage (Stafford 2022 replicates PE with levered small-value stocks [K]). The caveat is that funding-constrained levered investors "must de-lever when they hit their margin constraints" [V: F&P abstract]. Sizing must be survivable in the funding-stress regime.

### 2.4 Illiquidity: theory that bounds leverage
- **Ang, Papanikolaou & Westerfield (2014, *Management Science*):** an asset that cannot be traded for intervals of *uncertain* length raises risk aversion, makes it state-dependent, and cuts allocations to both liquid and illiquid risky assets. Investors would give up ~2% of wealth to hedge illiquidity crises arriving once a decade [V]. *Implication:* uncertainty about time to liquidity, which is exactly what a falling DPI creates, should cut leverage capacity.
- **Dimmock, Wang & Yang (2024, *Management Science*):** alternatives with lock-ups that can still be sold early at a proportional cost produce *endogenous, time-varying rebalancing boundaries*. Staggered lock-ups ("liquidity diversification") raise allocations and welfare, and crises push holdings well away from targets [V]. *Implication:* model SELL as a proportional-cost option with regime-dependent discounts, and manage vintage diversification as a liquidity asset.
- **Sorensen, Wang & Yang (2014, *RFS*):** fees, carry and illiquidity are costly, and "LPs may just break even" net of risk and illiquidity costs [V]. *Implication:* PE's forward α* must be estimated net of the LP's illiquidity cost before any leverage is laid on it.

### 2.5 Funding liquidity, margins and spirals
Brunnermeier & Pedersen (2009) describe two spirals [V]:
- **Loss spiral:** losses force sales into an illiquid market, which causes more losses.
- **Margin spiral:** higher volatility and illiquidity raise margins, which force more deleveraging.

When margins are destabilizing, liquidity is fragile and there can be multiple equilibria. Gorton & Metrick (2012) document the 2007–08 "run on repo": concerns about collateral liquidity raised haircuts and drained funding [V]. (From memory of the paper, their haircut index rose from near zero to roughly 45–50% for structured collateral [K, verify].) Related work: Geanakoplos (2010) on the leverage cycle [K], Adrian & Shin (2010) on procyclical leverage [K], Gârleanu & Pedersen (2011) on margin-based pricing [K], Shleifer & Vishny (2011) on fire sales [K]. *Modeling implications:* haircuts, margins, spreads and capacity are **state variables** that jump together in stress. They must not be modeled as constants.

### 2.6 Drawdown constraints, CPPI and control barrier functions
Grossman & Zhou (1993) require wealth ≥ αM, where M is running maximum wealth. With CRRA utility, the optimal policy holds risky assets in proportion to the cushion $W-\alpha M$ [V]. That is the CPPI logic. It is also a **control-barrier-function** rule [K: Ames et al. 2017]: with $h(x) = W - \alpha M \ge 0$, enforcing $\dot h \ge -\kappa h$ forces exposure toward zero as $h \to 0$.

*Illustration [I]:* α = 0.75 (25% maximum drawdown) and 1.2× exposure at the peak imply a multiplier k = 4.8. After a 10% drawdown, allowed exposure falls to 4.8 × (1 − 0.75/0.9) = 0.8×.

With 60% illiquids, **all of that procyclical deleveraging falls on the ~40% liquid sleeve and the overlay**. Leverage that may need to be cut quickly should therefore sit where cutting is cheap (futures and the overlay), not in NAV loans or asset-level debt. A decayed drawdown (Grossman-Zhou's own extension) or a soft barrier reduces whipsaw.

### 2.7 Leverage × spending × illiquidity
- **Proportional vs fixed claims [I].** If payouts are a fixed share s of NAV, wealth follows GBM with drift μ − s and never hits zero. Fixed-dollar payouts D (or debt service $cB$) create an absorbing barrier. For GBM with continuous fixed withdrawals, the present value of the withdrawals is reciprocal-gamma distributed (Dufresne 1990, a paper written explicitly for pension funding [K]; used by Milevsky & Robinson 2000 [K]), giving
  $$P(\text{ruin}) = P\!\left(\Gamma_\nu < \tfrac{2D}{\sigma^2 W_0}\right),\qquad \nu = \tfrac{2\mu}{\sigma^2}-1 .$$
  Values are in Section 6.9. Leverage converts part of a proportional system into a fixed-claim one, so payout policy and debt policy interact nonlinearly.
- **Endowment behavior in shocks.** Brown, Dimmock, Kang & Weisbenner (2014, *AER*) find that endowments cut payouts below stated policy after negative shocks but not after positive ones ("hoarding"), with real operating cuts [V]. *Implication:* the 5–10% band is an implicit liquidity option. Model it explicitly and price it, so the IC can see what it buys.
- **Public-finance analog: tax smoothing** (Barro 1979 [K]). Debt should absorb *temporary* shocks, while *permanent* shocks call for adjusting the "tax", which here means the payout or allocation. Applied to DPI: if the decline is cyclical (exit windows shut), borrowing to smooth is rational. If it is structural (longer holds, CV-led exits, lower distribution yields), debt only delays the adjustment and compounds it. The framework should estimate the cyclical/structural split and make the leverage decision depend on it.

### 2.8 Ideas transferable from other disciplines
- **Bank treasury / ALM:**
  - Basel III **LCR**: unencumbered HQLA / 30-day stressed net outflows ≥100%, with haircuts of Level 1 0%, Level 2A 15%, Level 2B 25–50% [V page; haircut levels K].
  - **NSFR**: available stable funding ≥ required stable funding [K].
  - **Funds transfer pricing (FTP):** charge each asset the term-funding cost matching its time to liquidity plus a contingent-liquidity charge. This gives ADIC an internal "price of illiquidity" per strategy [I].
- **Insurance:** the matching adjustment rewards matching illiquid assets to illiquid liabilities. ADIC's analog is that a *flexible* payout band supports a larger illiquid book, and a rigid one supports a smaller one [I].
- **Control theory:**
  - Model predictive control: re-plan every quarter and execute only the first step (Boyd et al. 2017) [V].
  - Tube or robust MPC for bounded disturbances [K].
  - Barrier functions for covenants [K].
- **Operations research:**
  - Multistage stochastic programming with recourse (Russell–Yasuda Kasai ALM [K]).
  - SDDP [K].
  - Chance constraints via the scenario approach [K].
  - CVaR linearization (Rockafellar–Uryasev 2000) [K].
- **Real options:**
  - Refinancing is an American option. Agarwal, Driscoll & Laibson (2013) give a closed-form optimal refinancing differential via the Lambert-W function [V]. The threshold rises with rate volatility and fixed costs and falls with loan size [K].
  - SELL is an exercise decision with a state-dependent strike (the discount).
- **Decision science:** value of information (is it worth paying for better marks or GP look-through data?), pre-mortems, and explicit exchange rates between P(10%) and P(floor breach) elicited from the IC.

---

## 3. Methods/models and trade-offs

| Method | What it gives for leverage | Strengths | Weaknesses | Role in ADIC |
|---|---|---|---|---|
| Closed-form (Merton/Kelly with kinked funding; Dufresne ruin; Grossman-Zhou) | Intuition, bounds, IC-friendly sanity checks | Transparent, instant | Frictionless; no illiquidity or regimes | Guardrails and challenge-agent checks |
| Regime-switching Monte Carlo of the whole balance sheet | Distributions of LCR, covenant headroom, forced sales, rating metrics | Handles path dependence, nonlinear covenants and haircuts | Policy must be specified; no optimization by itself | Core evaluator (extends the deck's 50k-path engine) |
| Multistage stochastic programming (scenario trees) | Optimal financing mix and duals (shadow prices) | Explicit recourse; duals give λ | Scenario explosion ($b^T$); weak at fat tails unless scenarios are chosen carefully | Annual strategic funding plan (2–3 stages) |
| SDDP (Markov-chain variant for regimes) | Many-stage convex funding and liquidity policies with cuts | Scales in stages | Needs convexity and stagewise structure; Julia ecosystem (SDDP.jl) is most mature | Optional research track |
| Adjustable robust optimization (affine decision rules) | Policies robust to haircut and spread uncertainty sets | Tractable, guarantees under the set | Conservative; set calibration is subjective | Tier 1 robust floor and liquidity gate |
| MPC with chance constraints (scenario approach) | Quarterly re-optimization with P(breach) ≤ ε | Practical; sample-size guarantees | Myopic beyond horizon; needs a terminal value | Operating engine for overlay and financing |
| Real options / LSMC | SELL/REFI/LEVER exercise boundaries per asset | Handles discrete, irreversible actions | Per-asset; needs a portfolio overlay | Asset-level lens |
| RL / policy search (constrained) | Nonlinear policies in a rich simulator | Flexible | Opaque, data-hungry, overfits the simulator | Research benchmark only, not production |

**Recommended architecture [I]:**
- An **inner convex one-period financing-mix problem** (LP/QP in cvxpy). It allocates the funding need across sources using regime-dependent cost curves and capacities, and returns duals λ (marginal value of liquidity) and $\mu_k$ (capacity shadow prices).
- An **outer policy layer** of parametric decision rules: affine in state, with targets for the reserve, recourse debt and NAV-loan use, and SELL/LEVER thresholds. These are tuned by **simulation-based policy search** under chance constraints, re-run quarterly as **MPC**.
- **Real-options screens** for discrete asset actions.

This hybrid avoids scenario-tree explosion, copes with nonconvex covenants and discrete actions, and still produces the shadow prices the IC needs.

---

## 4. Empirical evidence and current market data (dated, sourced)

### 4.1 Base rates (Oct 2026)
- **SOFR** 3.89% on 15 Oct 2026, with US$3.03trn volume (NY Fed API) [S].
- **FOMC** raised the target range to **3.75–4.00%** on 16 Sep 2026 by a 12–0 vote, the first hike since 2023 [S]. The statement says "Inflation remains elevated" [S].
- **UST par curve, 16 Oct 2026:** 3m 4.26%, 2y 4.74%, 5y 4.89%, **10y 5.09%**, 30y 5.43% [S]. The 10y was 5.31% on 5 Oct [S].
- *Implication [I]:* funding is expensive by the standards of the past decade, the curve slopes upward, and refinancing risk is live. The short end is pricing further hikes (3m bills about 37bp above SOFR).

### 4.2 Spreads and terms by funding source
| Source | Level / terms | As of | Status |
|---|---|---|---|
| AA sovereign-related USD bonds | Mubadala (Aa2/AA/AA) 10y ≈T+55 | Oct 2025 | via search excerpt |
| | PIF 10y sukuk **T+85** (IPT T+120; ~US$11bn book); Saudi sovereign 10y ≈79bp | 21 Jan 2026 | [S] Emirates NBD |
| | PIF US$7bn 3/7/30y, book US$23.8bn [S]; spreads T+95–99 (via search excerpt); Aa3/A+ | May 2026 | partly [S] |
| Crisis analog (AAA endowment) | Harvard taxable 5/10/30y at 5.03%/6.06%/6.53%, ≈**T+335–337.5bp**; plus US$1bn tax-exempt | Dec 2008 | [S] Harvard Magazine |
| Equity-index futures implied financing | ~30bp over risk-free on average 2021–23; >140bp peak Dec 2024 | 2012–2024 | [S] D. E. Shaw |
| | June-2026 ES roll +81bp over 3m SOFR (vs +38bp in Q2 2025) | Jun 2026 | via search excerpt (CME) |
| | Equity financing ~200bp over fed funds on 26 Jun 2026, then 89bp; dealer equity financing ≈US$211bn | Jun–Jul 2026 | [S] Reuters/Kitco |
| PE NAV facilities | Margins converging on **4–7%**; recourse-light vs secured gap narrowing; "may rise from here" | Jun 2026 | [S] Rede |
| | LTV 5–30% at close (AllianceBernstein, via search excerpt); OID 1–3% (via search excerpt) | 2026 | partial |
| | Market ≈US$100bn (FFA estimate), US$600bn projected by 2030; 80% of use is portfolio support, 20% distributions | Jul 2024 | [S] ILPA |
| UST repo / CP | Repo ≈SOFR to SOFR+10bp, haircut ≈2% bilateral/tri-party normal; CP for A-1+/P-1 issuers at small spreads | — | [P] (not verified) |

### 4.3 Secondary market and DPI (the SELL comparator)
Jefferies, *Global Secondary Market Review*, Jul 2026 [S]:
- H1 2026 volume **US$118bn**, of which LP US$56bn and GP-led US$62bn.
- **Average LP pricing 87% of NAV.** By strategy: buyout 91%, infrastructure 91%, credit 89%, venture 79%, real estate 68%. Tail-end funds (10y+) trade at 25%+ discounts; Asia/RoW at 35%+.
- Liquidity was the motive for 45% of LP sellers. **Pensions and SWFs supplied 48%** of LP volume.
- 33% of LP sales were structured, and **26% used deferred payment**.
- Dedicated dry powder US$290bn; capital overhang 1.2×.
- Distribution yield **~10%** in H1 2026, against a **25% average since 2001**.

*Implications [I]:*
- At these prices the market can absorb ADIC-sized sales: 15 deals above US$1bn and 5 above US$2bn in H1 2026.
- Selling is costly in IRR terms (Section 6.9) and is used heavily by peers.
- Deferred-payment sales are seller financing and should be modeled as SELL plus a receivable.

### 4.4 Stress analogs that set the stress-regime parameters
- **UK LDI, Sep–Oct 2022** [S, BoE]:
  - 30y gilt yields rose more than 35bp on two days in the same week, against a previous largest daily rise of 29bp since 2000.
  - The four-day rise was more than twice any move since 2000.
  - Mechanism: falling prices raised leverage, which triggered collateral calls; funds sold gilts into illiquid markets.
  - Response: minimum resilience of **~250bp**, made up of about **170bp** systemic (a 1-in-100 five-day shock to 30y index-linked gilts) plus about **80bp** (99.8th percentile five-day shock over a 10-year look-back). Collateral must be deliverable within **five days**. Liquid assets held against the shock must be unencumbered.
- **FSB (10 Dec 2024)** issued eight recommendations on margin and collateral-call preparedness for non-banks [S]:
  - tolerance-setting and contingency funding plans;
  - stress tests across "extreme but plausible" scenarios;
  - diversified liquid collateral.

  It cites March 2020, Archegos (2021), the 2022 commodities turmoil and LDI as the motivating episodes.
- **Harvard, 2008** [S]:
  - Raised US$2.5bn (Dec 2008), partly to fund swap terminations.
  - Swap notional US$3.52bn with a termination value of −US$330.4m at 30 Jun 2008.
  - Private-partnership distributions slowed sharply while capital calls continued.

  The lessons: leverage hidden in a hedging program, interacting with illiquidity and spending, forced expensive crisis-time funding even for an AAA borrower.

---

## 5. Practitioner and peer practice, with case studies

| Institution | Leverage metric | Value | As of | Source |
|---|---|---|---|---|
| CPP Investments | Recourse debt / adjusted net assets | **9.7%** (C$76.6bn) | 31 Mar 2025 | DBRS [S] |
| | Repo liabilities | C$113.3bn (vs C$72.1bn) | F2025 | DBRS [S] |
| | Derivative notional | C$724.9bn | F2025 | DBRS [S] |
| | Stressed 1-month LCR | **6.9× vs 1.0 minimum** | F2025 | DBRS [S] |
| | Recourse leverage, base CPP | 36% of net assets (18% in F2021) | F2025 | CPP AR (via search excerpt) |
| | Net assets; FY return; benchmark | C$793.3bn; 7.8%; benchmarks 13.2% | F2026 | CPP release [S] |
| OTPP | Moody's adjusted leverage | **17%** (2021–25: 20/19/18/17/17%) | 31 Dec 2025 | Moody's [S] |
| | Upgrade / downgrade factor | <10% / **>25% sustained** | Jul 2026 | Moody's [S] |
| | "Funding and other" | −C$87.3bn = **−32%** of net investments (−43% in 2024) | 2025 | OTPP [S] |
| | Derivative notional / total assets | 3.1× | 2025 | Moody's [S] |
| | Gross assets funded by repo and short sales | 6.0% (11.5% end-2019) | 2025 | Moody's [S] |
| | Liquid assets / gross investments; Level 3 | 32%; 52% | 2025 | Moody's [S] |
| Temasek | Total debt / NPV | ≈5% (S$25.5bn / S$518bn) | 31 Mar 2026 | investor presentation (via search excerpt) |
| | S&P adjusted LTV | "well below" 10% threshold | Mar 2025 | S&P (via search excerpt) |
| NBIM (GPFG) | Leverage cap | ≤5% of NAV of the equity + FI portfolios; securities borrowing ≤5%; unlisted real estate debt ratio ≤25% | mandate amended 9 Dec 2025 | NBIM [S] |
| Canadian pensions | Repo borrowing | >C$90bn, +14% y/y; ~half with maturity >1 month | May 2024 FSR | BoC via Finadium [S, secondary] |
| Harvard | Debt after FY2025 issues (US$450m tax-exempt + US$750m taxable) | ≥US$8.2bn, +32% in two years | Apr 2025 | Harvard Crimson [S] |
| US universities | Municipal issuance | US$26bn in H1 2025, roughly all of 2024; six elite schools >10% | Aug 2025 | Semafor [S] |

**What peers teach [I]:**
1. **Leverage is used to diversify, not to concentrate.** CPP describes leverage as a way to build "a more diversified and resilient portfolio" at its targeted market risk [S: DBRS]. The levered assets are government bonds and other financing assets, with repo as the main tool. Read across to ADIC: lever the low-risk, liquid sleeve, not PE.
2. **Recourse debt stays small relative to NAV and liquidity buffers stay very large.** CPP: 9.7% recourse debt, LCR 6.9×. OTPP: 17% adjusted leverage. Temasek: ≈5%. Agencies anchor ratings on these ratios, as in the OTPP triggers.
3. **Economic leverage can be large if it is liquid and collateral-managed.** OTPP runs about 1.3–1.4× gross exposure and 3.1× derivative notional/assets, but Moody's notches its liquidity down for encumbrance.
4. **Norway is the "no-leverage" anchor.** The 5% cap allows only cost-minimization and operational leverage, and a 25% debt cap applies inside real estate. The rationale is that the fund has no short-term liquidity needs. ADIC has *large* mandated outflows, which argues for more contingent liquidity, not more leverage.
5. **Endowments borrow when illiquidity and spending pressure collide** (Harvard 2008 and 2025; US$26bn of H1 2025 university issuance). Borrowing is a bridge, and terms reprice violently in crises (T+335 in 2008).
6. **GP-level NAV facilities are a governance problem for LPs.** ILPA recommends LPAC consent for distribution-motivated NAV loans and treating NAV loans as fund-level leverage. NAV-loan distributions are often **recallable**, and LP-led alternatives (secondary sale, LP-level financing) may be cheaper [S].
7. **Gaps:** GIC's public framework pages (Strategic Portfolio plus the GIC Portfolio "within the approved risk parameters") say nothing about leverage or borrowing [S]. NZ Super's public "how we invest" page gives no leverage limits [S]. I could not verify HOOPP or Dutch pension-fund repo and swap figures in this pass.

---

## 6. Design implications for the ADIC framework

### 6.1 Placement in the two-tier architecture
- **Tier 1 (gate):** every leverage action is tested inside the robust floor (≥7% worst-case 5y annualized under misspecification) and the liquidity survival gate. The gate now includes debt maturities, interest, NAV-facility LTV cures, repo haircut add-ons and overlay margin, all in one joint stress.
- **Tier 2 (stretch):** leverage competes with other actions on Δ P(10%) and α* net of shadow costs, *priced with* λ.

### 6.2 State variables (quarterly, with monthly or daily sub-steps for margin)

**Market regime and rates**
- Regime posterior $\pi_t$ over {Normal, Tight, Stress}, from the state/fragility engine.
- Base rates $r_t$ (SOFR) and the UST curve.

**Assets** (for each asset or fund interest $i$)
- Reported NAV $P_{i,t}^{rep}$ and economic value $P_{i,t}^{eco}$ (desmoothed).
- Unfunded commitments $U_{i,t}$ and fund age.
- Look-through leverage $\ell^{lt}_{i,t}$, including GP NAV facilities and sub-lines.
- Asset-level debt $D_{i,t}$ with its maturity ladder, rate type, covenants (LTV$^{max}_i$, DSCR$^{min}_i$) and recourse flag.
- Fused return belief $(\hat\mu_i, \hat\sigma_i, \hat\beta_i, SE_i)$ built from underwritten, current-actual and strategy-forecast returns (from the return-fusion stream).

**Funding sources** (for each source $k$)
- Balance $B_{k,t}$, maturity buckets $B_{k,t}^{(m)}$, rate, spread and covenants.
- Capacity $\bar B_k(s_t)$ and haircut $h_k(s_t)$.

**Collateral and liquidity**
- HQLA holdings by level $A^{(1,2A,2B)}_t$.
- Encumbered assets $Enc_t$.
- Cash reserve $R_t$.

**Overlay**
- Notionals $N_{m,t}$ for the tail hedge and the opportunistic book.
- IM$_t$, VM history, CSA terms (thresholds, minimum transfer amounts, eligible collateral) and counterparty exposures.

**Liabilities and rating proxies**
- Payout-policy state: band position, trailing-NAV base, any discretionary cut in force.
- Rating proxies: recourse debt / adjusted NAV, adjusted leverage, liquid inflows / outflows, encumbrance.

### 6.3 Decision variables

**Portfolio level**
- Issuance and repayment $\Delta B_{k,t}$ by source and tenor: term bonds at 3/5/10/30y, CP/ECP, repo, revolver draws, LP-level NAV facility draws.
- Synthetic exposure $N_{j,t}$ (futures, TRS, swaps).
- Reserve target $R_t$.
- Payout $s_t \in [5\%, 10\%]$, where discretion exists.
- Commitment pacing $C_t$.

**Asset level**
- $a_{i,t} \in \{\text{SELL}(x_i), \text{HOLD}, \text{REFI}(\text{terms}), \text{LEVER}(\Delta D_i)\}$.
- Secondary-sale structure: cash or deferred.

### 6.4 Dynamics (core equations)

**Liquid book:**

$$L_{t+1} = L_t(1+r^L_{t+1}) + \textstyle\sum_i (Dist_{i,t} - Call_{i,t}) - Pay_t - \sum_k c_{k,t}B_{k,t} + \sum_k(\Delta B^+_{k,t}-\Delta B^-_{k,t}) - \Delta IM_t + VM_t + \sum_i (1-d_{i}(s_t))\,x_{i,t}P_{i,t}$$

**Private assets and commitments:**
- $P_{i,t+1} = (P_{i,t} + Call_{i,t} - Dist_{i,t} - x_{i,t}P_{i,t})(1+r^P_{i,t+1})$
- $U_{i,t+1} = U_{i,t} - Call_{i,t} + C_{i,t}$

**Cash flows:**
- $Call_{i,t} = \kappa_i(s_t, age)\,U_{i,t}$
- $Dist_{i,t} = \delta_i(s_t, age)\,P_{i,t}$

These follow Takahashi-Alexander [K] with regime-dependent rates. The current yield $\delta \approx 10\%$/yr [S] should be tested against 25% (long-run) and ~5% (stress, assumption).

**Margin and collateral:**
- $IM_t = \sum_m im_m(s_t)|N_{m,t}|$
- Stressed HQLA: $H_t = \sum_j (1-h_j(s_t))A^{unenc}_{j,t}$

**Facility LTV:** $LTV_{k,t} = B_{k,t}/\sum_{i\in \mathcal{P}_k} P^{rep}_{i,t}$. A breach triggers a cash sweep or paydown, as ILPA describes [S].

**Equity:** $E_t = L_t + R_t + \sum_i P_{i,t} - \sum_k B_{k,t} - \sum_i D_{i,t}^{recourse} + MTM^{ov}_t$.

### 6.5 Cost curves and availability by regime (defaults)

Each cost curve is convex piecewise-linear in utilization:

$$c_k(B,s) = r_t + \sigma_k(s) + \eta_k(s)\big(B/\bar B_k(s)\big)^2 .$$

| Source $k$ | Normal spread $\sigma_k$ | Tight | Stress | Capacity $\bar B_k$ (Normal → Stress) | Haircut / IM | Basis |
|---|---|---|---|---|---|---|
| UST repo (term ≤3m) | 0–10bp | +10bp | +25bp | (1−h) × UST holdings | 2% → 5% | [P] |
| Agency/IG repo | 10–25bp | +25bp | +75bp | ↓50% | 5–8% → 15–25% | [P]; GM 2012 direction [V] |
| CP/ECP (A-1+/P-1) | 5–25bp | +50bp | unavailable or +200bp | program size → 0 | — | [P]; 2008/2020 CP freezes [K] |
| AA term bonds 5–10y | UST+60–100bp | +150bp | +300–350bp | market access → limited | — | Mubadala/PIF 2025–26 [S/excerpt]; Harvard 2008 [S] |
| Committed revolver | SOFR+50–100bp drawn (assumed) | same | same if committed (counterparty risk) | committed amount | — | assumption; Mubadala has RCFs [S] |
| LP-level NAV facility | SOFR+400–700bp (default 550) | +100bp | +200bp; LTV caps −10pp | 10–20% of pool | LTV covenant 25% | Rede 2026 [S]; AB (via search excerpt) |
| Equity futures / TRS | SOFR+30–80bp (default 50) | +80bp | +150–200bp | dealer balance sheet | IM 5–8% → 10–15% | D. E. Shaw, CME, Reuters [S/excerpt]; IM [P] |
| Receive-fixed swaps (duration) | ≈0 funding | — | — | — | yield-shock buffer ≥250bp | BoE 2023 [S] |
| Secondary sale (implied) | $r_{sell}=(1+g)(1-d)^{-1/T}-1$ | d +5pp | d +15–25pp | ~US$290bn dry powder | — | Jefferies 2026 [S]; stress d [I] |

### 6.6 Constraints (recommended defaults; IC to ratify)

1. **Liquidity coverage (hard):** $\dfrac{H_t + \text{committed undrawn lines surviving stress}}{\text{30d stressed outflows}} \ge 1.0$. Soft target ≥1.5. Outflows include payout, calls at the stressed κ, maturities, interest, P99 VM plus ΔIM, repo haircut add-ons and NAV-loan cures. The 12-month version is ≥1.0 under the joint stress.
2. **Survival horizon:** months covered under the joint stress ≥24, with 36 as the target (deck).
3. **Stable funding (NSFR-style):** equity plus debt with maturity >1y ≥ Σ RSF$_j$ × assets. RSF factors: 0–5% for HQLA, 50% for listed equities, 100% for private and encumbered assets [K]. This keeps short-term funding from financing illiquids.
4. **Recourse leverage:** recourse debt / adjusted NAV ≤10% as target and 15% hard. $P(\text{adj. leverage}_t > 20\%\ \text{for any}\ t\le 3y) \le 5\%$, set below the Moody's 25% downgrade analog.
5. **Economic leverage:** gross exposure / NAV ≤1.30× (OTPP analog). Report look-through leverage separately.
6. **Encumbrance:** encumbered / total assets ≤15%, with an IC-set range of 10–20%. OTPP funds 6.0% of gross assets with repo and short sales [S].
7. **Covenant chance constraints:** $P(LTV_{k,t} > LTV_k^{max}\ \text{within}\ 12\text{m}) \le 2\%$ for each facility, and similarly for DSCR on asset-level debt.
8. **Maturity concentration:** ≤20% of debt maturing in any rolling 12 months. Weighted-average funding maturity ≥ the duration of the projected liquidity gap.
9. **Kelly cap on discretionary leverage:** exposure ≤ $f \cdot (\hat\mu - c)/\hat\sigma^2$ with $f \le 0.5$, shrunk further with $SE(\hat\mu)$ and an illiquidity adjustment.
10. **Drawdown barrier:** discretionary (overlay) exposure ≤ $k(E_t - \alpha M_t)/E_t$, using a decayed high-water mark.
11. **Robust floor (Tier 1):** worst-case over the ambiguity set (μ shrinkage, haircut and discount sets, DPI scenarios) of 5y annualized return ≥7%, holding at least 95% of the time.
12. **Overlay-specific:** P99 margin plus ΔIM is covered by unencumbered HQLA *after* repo haircut add-ons. Tail-hedge MTM counts as liquidity only when collateralized daily under the CSA with eligible collateral. Any rates overlay keeps a ≥250bp yield-shock buffer with ≤5-day collateral mobility.

### 6.7 Objective terms
Tier 2 maximizes $\Delta P(\text{ann. return}_H \ge 10\%)$ and/or $\mathbb{E}[\log E_H]$, net of:
- **financing cost** $\sum_k c_k(B_k,s)B_k$;
- **expected fire-sale loss** $\mathbb{E}[\sum_i d_i(s)\,x^{forced}_i P_i]$;
- **covenant cure cost** $\lambda_{cov}P(\text{breach})\cdot LGB$;
- **rating migration cost** $\Delta spread \cdot B \cdot P(\text{downgrade})$;
- the **liquidity penalty**, i.e. CVaR of the LCR shortfall;
- **volatility drag**, which is implicit in log objectives.

The duals of constraints 1–3 give λ (in $ per $ of liquidity), which feeds the asset-level lens.

### 6.8 Decision rules

**(a) Portfolio LEVER test.** Add leverage only if all four hold:
1. Tier 1 passes with the new debt and its stress terms included.
2. The use of proceeds has $\alpha^{*}_{use} = \hat\mu_{use} - c_k - \hat\beta_{use}\pi_p > SC$, where $\pi_p$ is the reverse-optimized portfolio premium per unit β and $SC$ is the sum of shadow costs.
3. $\Delta P(10\%)/\Delta P(\text{floor breach})$ exceeds the IC's elicited exchange rate.
4. The rating proxy stays inside its bounds with ≥95% probability.

For the aggregate portfolio, $\alpha^*_{use} = r_f - c_k < 0$ by construction under reverse optimization. Levering the whole book is therefore a *risk-budget* decision, justified only if ADIC is below its risk budget (for example because of cash drag from reserves). It is never an α decision.

**(b) Asset LEVER test** (asset-level or fund-interest financing)
- Rule: lever iff $\hat\mu_i - c_i(\ell) - \hat\beta_i\pi_p - \kappa\,SE_i - SC_i > 0$.
- Leverage cap: $\ell_i \le \min\{\ell^{Kelly}_i f,\ \ell: P(\text{cov. breach}) \le \varepsilon\}$.
- *Example [I]:*
  - Core infrastructure asset: fused $\hat\mu$ = 8.5%, non-recourse debt at SOFR+200bp = 5.9%, β = 0.5, $\pi_p$ = 3.8%. Then α* = 8.5 − 5.9 − 1.9 = +0.7%, and after an assumed 0.3% liquidity/refinancing charge it is +0.4%. **LEVER modestly**, subject to DSCR headroom.
  - Buyout fund interest financed with a NAV loan: $\hat\mu$ = 9%, c = 9.4%, β = 1.3. Then α* = 9 − 9.4 − 4.9 = −5.3%. **Do not lever for return.**

**(c) HOLD / SELL / LEVER for liquidity** (λ = marginal value of a dollar of liquidity from the optimizer; T = asset's remaining hold; τ = borrowing duration)

$$V_H = e^{\alpha^*T},\qquad V_S = (1-d)(1+\lambda),\qquad V_L = e^{\alpha^*T} + \lambda - (c-r_f)\tau - \text{cov./recourse cost}.$$

*Example [I]:* buyout LP interest with α* = +0.2%/yr, T = 5, d = 9%.
- **Normal times (λ = 0):** HOLD (1.010) beats SELL (0.91).
- **Stress (λ = 0.15):** SELL = 1.0465.
- **LEVER with AA term debt** (c − r_f ≈ 1.9%): 1.141 for τ = 1, 1.065 for τ = 5.
- **LEVER with a NAV loan** (c − r_f ≈ 5.5%): 1.105 for τ = 1, 0.885 for τ = 5. It breaks even with SELL at **τ ≈ 2.1 years**.
- **Rule:** use NAV loans only as short bridges. For structural shortfalls use AA term debt (within its limits) or SELL.
- *Risk-neutral shortcut:* SELL beats "HOLD plus borrow at c" iff $g_{fwd} < (1+c)(1-d)^{1/T}-1$. For buyout (d = 9%, T = 5) the break-even $g^*$ is 2.1% vs 4.05% short-term debt, **3.8% vs 5.8% AA term debt**, and 7.4% vs a 9.4% NAV loan. Comparable thresholds against AA term debt: credit 3.4%, venture 0.9%, tail-end −0.1%, real estate −2.1%. *Read-out:* selling at today's discounts pays only for assets whose credible forward growth is low. The fused forecast and its credibility, built from the underwritten/actual/forecast data, is the decisive input.

**(d) REFINANCE rule.** Refinance when PV(rate saving) − fees exceeds the option value of waiting. Use the Agarwal-Driscoll-Laibson closed form as a screen [V] or LSMC for complex terms. Refinance early, regardless of rate, if a maturity wall breaches constraint 8 or if expected spreads in the Tight regime would push the debt-service share of payout above its limit.

**(e) Payout band and reserve policy (joint).** Optimize the parameters of "pay 7.5%; drop to 5% while the regime posterior on Stress exceeds 0.5 or LCR < 1.25; restore once LCR > 1.5 for two quarters", together with the reserve size $R$ (debt-funded T-bills). Report the trade-off frontier (Section 6.9) to the IC and the owner.

### 6.9 Quantified examples (all [I]; computed in this session)

**A. Total-portfolio leverage arithmetic** (μ = 8%, σ = 11%, $g = r_b + L(\mu-r_b) - L^2\sigma^2/2$)

| Funding $r_b$ | Kelly $L_K$ | g(1.0) | g(1.1) | g(1.3) | g(1.5) | L for g = 10% |
|---|---|---|---|---|---|---|
| 4.05% (repo/CP) | 3.26 | 7.40% | 7.66% | 8.16% | 8.61% | 2.36 (≈0.72 Kelly) |
| 4.65% (futures, SOFR+75) | 2.77 | 7.40% | 7.60% | 7.98% | 8.31% | infeasible (max 9.29%) |
| 5.80% (AA 10y term) | 1.82 | 7.40% | 7.49% | 7.64% | 7.74% | infeasible (max 7.80%) |

**B. Eventual-ruin probability with *fixed-dollar* payouts** (Dufresne)

| μ / σ | D/W₀ = 5% | 7.5% | 10% |
|---|---|---|---|
| 7% / 12% | 29.7% | 74.3% | 94.5% |
| 8% / 12% | 15.5% | 57.9% | 87.9% |
| 9% / 12% | 7.0% | 40.9% | 77.6% |
| 10% / 12% | 2.8% | 26.0% | 64.2% |

Proportional payouts carry zero ruin risk in this model. These numbers show why the mandate's "5–10% of the fund" should be expressed proportionally to NAV, ideally a smoothed NAV, and why debt service needs a budget.

**C. Implied annual cost of selling** (T = 5): buyout and infrastructure at 91% of NAV cost 5.0/8.0/11.1/14.1% for forward growth of 3/6/9/12%. Venture at 79% costs 8.0/11.1/14.3/17.4%. Real estate at 68% costs 11.3/14.5/17.7/21.0%. Compare NAV loans at 7.9–10.9% and AA term debt at ≈5.8%.

**D. Stylized ADIC balance-sheet Monte Carlo** (40,000 paths, quarterly, 5 years)
- *Balance sheet:* E₀ = US$177bn; 60% private; unfunded = 25% of private NAV.
- *Regimes:* quarterly P(N→S) = 3.5% and P(S→S) = 75%, so stress takes 12.3% of quarters.
- *Liquid book:* 10.8%/11% in Normal and −6%/9% per quarter in Stress, ≈6.5% unconditional.
- *Private (economic):* 11.9%/15% in Normal and −4%/8% per quarter in Stress, ≈8.5% unconditional. Correlation 0.7; appraisal smoothing 0.6/0.4.
- *Private cash flows:* distributions 10% / 5% of NAV per year; calls 25% / 22% of unfunded; new commitments 6% / 3% of NAV (Normal / Stress).
- *Debt:* SOFR 3.9% plus 60bp in Normal and 300bp in Stress; 5-year average maturity; 50% rollover failure in Stress.
- *Overlay:* 15% of NAV, IM 7% / 12%.
- *Forced sales:* triggered when unencumbered liquid assets fall below 8% of NAV, restoring to 12% at a 9% / 25% discount.

| Policy | P(forced sale) | Median E₅/E₀ | P05 E₅/E₀ | P(debt/E > 25%) | Cum. payout / E₀ |
|---|---|---|---|---|---|
| No debt, 7.5% payout | 6.4% | 1.040 | 0.498 | 0 | 38.7% |
| 10% debt invested in liquid book | 2.3% | 1.055 | 0.460 | 2.0% | 38.9% |
| 20% debt invested | 0.9% | 1.070 | 0.418 | 35.4% | 39.2% |
| 10% debt held as reserve | 0.1% | 1.035 | 0.501 | 0.8% | 38.6% |
| Pre-emptive sale of 10% of private at 91% | 2.6% | 1.031 | 0.495 | 0 | 38.4% |
| Payout 7.5% → 5% in stress | 2.7% | 1.049 | 0.525 | 0 | 37.5% |
| 5% reserve + stress payout cut | 0.2% | 1.047 | 0.525 | 0 | 37.5% |
| No debt, 10% payout | 26.9% | 0.914 | 0.422 | 0 | 49.0% |
| 10% reserve, 10% payout | 2.9% | 0.910 | 0.434 | 1.9% | 48.9% |

**Readings** (sensitive to the assumptions; illustrative only):
1. A reserve or the payout band nearly eliminates forced sales for ~5–10bp/yr.
2. Return-seeking leverage buys ~3bp/yr of median return per 1% of NAV borrowed, at ~0.4pp of P05 per 1%, and pushes rating metrics through thresholds nonlinearly.
3. **Expected** forced-sale losses are small (0.06% of E₀ over 5y at a 25% discount; 0.12% at 40%). The reserve's carry therefore exceeds the expected loss it avoids, and its case rests on three things: Tier 1 tail constraints; unmodeled fire-sale costs (signalling, governance, selling at the trough); and **dry-powder optionality**. Deploying 5% of NAV into secondaries at a 25% stress discount captures ≈1.7% of NAV per episode, about 20bp/yr at one episode every ~8 years, assuming fair marks.
4. A 10% payout with no contingent liquidity is the most dangerous configuration.

**E. ADIC liquidity arithmetic [I]:**
- Payout 5–10% = US$8.9–17.7bn a year, or 12–25% of the ~US$71bn liquid book.
- Distributions at a 10% yield on ~US$106bn private NAV ≈ US$10.6bn a year, against ≈US$26.6bn at the 25% long-run yield.
- Calls ≈ US$6.6bn a year, assuming 25% of an assumed US$26.6bn unfunded.
- So at today's yields the liquid book funds roughly US$5–14bn a year, where it used to be replenished.

### 6.10 Calibration targets (initial values)
- **Rates:** SOFR 3.89% (15 Oct 2026); 10y UST 5.09% (16 Oct 2026); fed funds 3.75–4.00% (16 Sep 2026).
- **AA term spread:** T+55–99bp in Normal; T+300–350bp in Stress (Harvard 2008 analog).
- **Futures financing:** SOFR+30–80bp in Normal; +140–200bp peaks (Dec 2024; Jun 2026).
- **NAV loans:** SOFR+4–7%; LTV 5–30%.
- **Secondary pricing:** buyout 91 / infra 91 / credit 89 / venture 79 / RE 68 / all 87% of NAV (H1 2026); tail-end and Asia discounts ≥25% / 35%.
- **Distribution yield:** ~10% (H1 2026) against 25% long-run.
- **Peer leverage:** CPP recourse debt 9.7%, LCR 6.9; OTPP adjusted leverage 17%, gross ≈1.32×, notional/assets 3.1×; Temasek debt/NPV ≈5%; NBIM ≤5%.
- **Overlay buffers:** BoE LDI buffer 250bp (170 + 80), with 5-day collateral mobility.

### 6.11 Data needs
1. Facility-level terms for every borrowing and derivative agreement: ISDA/CSA, repo GMRA, NAV facilities, asset-level debt (maturity, covenants, cure mechanics, recourse).
2. GP look-through data: fund-level NAV-facility use and recallable distributions (ILPA template), sub-line use, portfolio-company net debt/EBITDA.
3. Cash-flow history per fund: calls, distributions and age, to calibrate regime-dependent κ and δ.
4. Secondary bids and indications by strategy and vintage, with ADIC's own transaction history.
5. Dealer funding runs: futures roll financing, TRS spreads, repo haircuts by collateral.
6. Rating-agency methodology mappings, if ADIC (or its parent) is rated.
7. The exact distribution rule: NAV base, timing, discretion inside the band, owner's tolerance.
8. Historical liquidity events: 2008–09, 2020, 2022.

### 6.12 Agentic and IC integration (brief)
- **Deterministic Treasury & Leverage Engine:** owns all numbers (optimizer, simulator, duals).
- **LLM agents:**
  - *Covenant & Facility Parser:* extracts structured covenant objects from credit agreements, CSAs and LPAs, with human verification.
  - *Funding-Market Scout:* gathers current terms with citations and staleness flags. It suggests; it never sets parameters.
  - *Adversarial Funding-Stress agent:* builds joint stresses such as a CP freeze plus a 3× repo haircut plus a 20% NAV markdown plus a downgrade plus equities −30% plus rates +150bp.
- **Rubric checks per stage** (in the spirit of Sakana's verification layer): every leverage recommendation passes Tier 1; ablations with and without leverage, reserve and payout flexibility; comparison against a no-leverage baseline.
- **IC panel:** recourse and economic leverage; LCR fan; survival horizon; P(covenant breach); P(rating trigger); funding mix and cost by source; **λ (marginal value of liquidity)**; and the HOLD/SELL/LEVER/REFI table with α* versus financing.

---

## 7. Implementation notes

- **Python stack:**
  - `numpy`/`numba` for the vectorized Monte Carlo (the balance-sheet simulator above runs 40k paths × 20 quarters in seconds in compiled code).
  - `scipy.special.gammainc` for the ruin formula.
  - `cvxpy` (OSQP/ECOS/Clarabel; Gurobi or MOSEK if licensed) for the one-period financing-mix LP/QP and its duals. `cvxportfolio` covers MPO and MPC backtests.
  - `Pyomo` + `mpi-sppy` for scenario-tree stochastic programs (progressive hedging). `SDDP.jl` (Julia) if many-stage policies are needed.
  - `hmmlearn` or `statsmodels` MarkovRegression for regimes.
  - `QuantLib-Python` for swaps and futures carry.
  - `PyMC`/`NumPyro` for return fusion.
  - `SALib` for global sensitivity.
  - `OR-Tools`/`Pyomo` MILP for discrete SELL/REFI choices with fixed costs.
- **Algorithms:**
  - Policy search over 5–15 rule parameters by CMA-ES or Bayesian optimization, with chance constraints checked on held-out scenarios. The scenario approach gives sample sizes: for ε = 2% and confidence 1−β = 99%, a few thousand scenarios is the right order for a handful of decision variables [K: Calafiore & Campi].
  - Linear or affine decision rules for robust Tier 1 [K: Ben-Tal et al.].
- **Complexity:** a scenario tree with branching b and T stages has $b^T$ nodes (e.g., 20³ = 8,000). Prefer simulation plus policy search, MPC with a short horizon, and scenario reduction.
- **Numerical pitfalls:**
  - **Smoothed NAVs** understate vol and correlation. Desmooth (Getmansky-Lo-Makarov 2004 [K]) for risk, but test covenants on *reported* NAV with its reporting lag.
  - **Jumps:** haircuts, discounts and capacity jump with the regime. Use mixture or Student-t shocks, not Gaussian.
  - **Nonconvexities** (fixed fees, minimum issue sizes, discrete actions) break duals. Compute λ from the convex relaxation and validate by simulation.
  - **Market impact:** ADIC's own selling moves secondary prices. Add size-dependent discount slopes.
  - **Clocks:** margin is daily while the model is quarterly. Sub-step the overlay and use worst intra-quarter paths.
  - **Definitions:** agencies differ (DBRS excludes repo used to "optimize" exposure; Moody's nets nettable repo and derivatives). Compute all of them.

---

## 8. Risks, pitfalls and limitations
- **Liquidity spirals:** leverage plus illiquidity plus a mandated payout is the textbook loss/margin spiral (Brunnermeier-Pedersen; Harvard 2008; UK LDI 2022). The joint stress is the binding test, not single-factor stresses.
- **Forecast optimism:** strategy-group forecasts and distribution timing have historically been too optimistic (deck memo corpus). Leverage multiplies that error. Shrink $\hat\mu$ toward underwritten-vs-actual realized gaps.
- **Hidden leverage:** GP NAV facilities, sub-lines, recallable distributions and portfolio-company debt raise effective leverage without ADIC's decision.
- **Wrong-way risk:** tail-hedge counterparties or dealers retrench exactly when they are needed (Archegos, dealer balance-sheet limits). Equity financing spiked to ~200bp over fed funds even in non-crisis June 2026.
- **Rate regime:** rising policy rates (Sep 2026 hike) and a 10y above 5% raise both funding costs and refinancing risk. Floating-rate NAV loans reprice immediately.
- **Model limits:** the Monte Carlo above is stylized (two assets, two regimes, assumed parameters). Its numbers illustrate trade-offs and are not forecasts. The ruin formula assumes GBM, continuous withdrawals and an infinite horizon.
- **Governance:** leverage creep under target pressure, the "target-chasing" failure the deck already guards against. Treat leverage limits as Tier 1 constraints, not Tier 2 preferences.
- **Regulatory and market structure:** the US Treasury clearing mandate and changes to bank balance-sheet rules may alter repo and futures funding. Timelines were not verified in this pass.

## 9. Open questions
1. What is ADIC's legal capacity to borrow (own name, via a parent such as an MDGH-style issuer, or guaranteed), and at what rating? Is there an owner limit on recourse debt?
2. Is the 5–10% distribution computed on current, trailing or smoothed NAV? Who controls discretion within the band, and can it be used countercyclically?
3. How much of the DPI decline is structural (longer holds, CV-led exits) and how much cyclical? This decides between borrowing and adjusting (tax-smoothing logic).
4. What look-through leverage exists in ADIC's PE book (GP NAV facilities, sub-lines, portfolio-company leverage)?
5. What are the overlay's CSA terms, eligible collateral and IM models, and how correlated are tail-hedge payoffs with ADIC's margin calls?
6. Which secondary capacity and price impact apply to ADIC-sized portfolios in stress (US$2–10bn tranches)?
7. Unverified in this pass: HOOPP, NZ Super, GIC and Dutch pension leverage specifics; the CPP F2026 leverage ratios; the CME and Mubadala pricing points; the Gorton-Metrick haircut levels.
8. How should the IC's exchange rate between P(10%) and P(floor breach) be elicited, and how often re-elicited?

## 10. References
*[V] = checked this session against the primary page or document (or a search excerpt where noted); [K] = domain knowledge, not re-checked.*

**Theory and methods**
- Ang, A., Papanikolaou, D., Westerfield, M. (2014). Portfolio Choice with Illiquid Assets. *Management Science* 60(11): 2737–2761. NBER WP 19436. https://www.nber.org/papers/w19436 [V]
- Asness, C., Frazzini, A., Pedersen, L. H. (2012). Leverage Aversion and Risk Parity. *Financial Analysts Journal* 68(1): 47–59. https://www.aqr.com/Insights/Research/Journal-Article/Leverage-Aversion-and-Risk-Parity [V]
- Brunnermeier, M., Pedersen, L. H. (2009). Market Liquidity and Funding Liquidity. *Review of Financial Studies* 22(6): 2201–2238. https://www.princeton.edu/~markus/research/papers/Mkt_Fun_Liquidity.pdf [V]
- Brown, J., Dimmock, S., Kang, J.-K., Weisbenner, S. (2014). How University Endowments Respond to Financial Market Shocks: Evidence and Implications. *American Economic Review* 104(3): 931–962. https://doi.org/10.1257/aer.104.3.931 [V]. Working-paper version: NBER WP 15861 (2010, revised 2012; first circulated as "Why I Lost My Secretary: The Effect of Endowment Shocks on University Operations").
- Dimmock, S., Wang, N., Yang, J. (2024). The Endowment Model and Modern Portfolio Theory. *Management Science* 70(3): 1554–1579. https://www.nber.org/papers/w25559 [V]
- Frazzini, A., Pedersen, L. H. (2014). Betting Against Beta. *Journal of Financial Economics* 111(1): 1–25. https://www.nber.org/papers/w16601 [V]
- Gorton, G., Metrick, A. (2012). Securitized Banking and the Run on Repo. *JFE* 104(3): 425–451. https://www.nber.org/papers/w15223 [V]. Also: Gorton, G., Metrick, A. (2010). Haircuts. Federal Reserve Bank of St. Louis *Review* 92(6): 507–520 (Nov/Dec 2010). DOI 10.20955/r.92.507-20. Working-paper version: NBER WP 15273 (2009), https://www.nber.org/papers/w15273 [V]
- Grossman, S., Zhou, Z. (1993). Optimal Investment Strategies for Controlling Drawdowns. *Mathematical Finance* 3(3): 241–276. https://ideas.repec.org/a/bla/mathfi/v3y1993i3p241-276.html [V]
- Kelly, J. L. (1956). A New Interpretation of Information Rate. *Bell System Technical Journal* 35(4): 917–926; summary at https://en.wikipedia.org/wiki/Kelly_criterion [V]. Cited for the log-growth criterion only: the continuous-time leverage and growth formulas in Section 2.2 are not in this paper.
- Sorensen, M., Wang, N., Yang, J. (2014). Valuing Private Equity. *RFS* 27(7): 1977–2021. https://www.nber.org/papers/w19612 [V]
- Agarwal, S., Driscoll, J., Laibson, D. (2013). Optimal Mortgage Refinancing: A Closed-Form Solution. *JMCB* 45: 591–622. https://www.nber.org/papers/w13487 [V]
- Boyd, S. et al. (2017). Multi-Period Trading via Convex Optimization. arXiv:1705.00109 (also *Foundations and Trends in Optimization* [K]). https://arxiv.org/abs/1705.00109 [V]
- Merton, R. C. (1971). Optimum Consumption and Portfolio Rules in a Continuous-Time Model. *JET* 3(4): 373–413. DOI 10.1016/0022-0531(71)90038-X (issue and pages confirmed via Crossref, 2026-10-18). [K]
- MacLean, L., Thorp, E., Ziemba, W. (eds.) (2011). *The Kelly Capital Growth Investment Criterion: Theory and Practice*. World Scientific. DOI 10.1142/7598. [K]
- Dufresne, D. (1990). The distribution of a perpetuity, with applications to risk theory and pension funding. *Scandinavian Actuarial Journal* 1990: 39–79. [K]
- Milevsky, M., Robinson, C. (2000). Self-annuitization and ruin in retirement. *North American Actuarial Journal* 4(4): 112–124. [K]
- Barro, R. (1979). On the Determination of the Public Debt. *Journal of Political Economy* 87(5, Part 1): 940–971. DOI 10.1086/260807 (confirmed via Crossref, 2026-10-18). [K]
- Geanakoplos, J. (2010). The Leverage Cycle. *NBER Macroeconomics Annual 2009* 24(1): 1–66. DOI 10.1086/648285 (Crossref, 2026-10-18; pages were previously given as 1–65, and the volume's next item begins on p. 67). [K]
- Adrian, T., Shin, H. S. (2010). Liquidity and Leverage. *Journal of Financial Intermediation* 19(3): 418–437. [K]
- Gârleanu, N., Pedersen, L. H. (2011). Margin-Based Asset Pricing and Deviations from the Law of One Price. *RFS* 24(6): 1980–2022. [K]
- Shleifer, A., Vishny, R. (2011). Fire Sales in Finance and Macroeconomics. *JEP* 25(1): 29–48. [K]
- Stafford, E. (2022). Replicating Private Equity with Value Investing, Homemade Leverage, and Hold-to-Maturity Accounting. *RFS* 35(1): 299–342. DOI 10.1093/rfs/hhab020 (volume, issue and pages confirmed via Crossref, 2026-10-18; online 2021). (SSRN 2720479 blocked in this session.) [K]
- Takahashi, D., Alexander, S. (2002). Illiquid Alternative Asset Fund Modeling. *Journal of Portfolio Management* 28(2): 90–100. [K]
- Getmansky, M., Lo, A., Makarov, I. (2004). An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns. *JFE* 74(3): 529–609. DOI 10.1016/j.jfineco.2004.04.001 (confirmed via Crossref, 2026-10-18). [K]
- Rockafellar, R. T., Uryasev, S. (2000). Optimization of Conditional Value-at-Risk. *Journal of Risk* 2(3): 21–41. [K]
- Cariño, D. et al. (1994). The Russell–Yasuda Kasai Model. *Interfaces* 24(1): 29–49. [K]
- Pereira, M., Pinto, L. (1991). Multi-stage stochastic optimization applied to energy planning. *Mathematical Programming* 52: 359–375. [K]
- Ben-Tal, A., Goryashko, A., Guslitzer, E., Nemirovski, A. (2004). Adjustable robust solutions of uncertain linear programs. *Mathematical Programming* 99: 351–376. [K]
- Calafiore, G., Campi, M. (2006). The scenario approach to robust control design. *IEEE TAC* 51(5): 742–753. [K]
- Ames, A. et al. (2017). Control Barrier Function Based Quadratic Programs for Safety Critical Systems. *IEEE TAC* 62(8): 3861–3876. [K]
- Mayne, D., Seron, M., Raković, S. (2005). Robust model predictive control of constrained linear systems with bounded disturbances. *Automatica* 41(2): 219–224. [K]
- Dowson, O., Kapelevich, L. (2021). SDDP.jl. *INFORMS Journal on Computing* 33(1): 27–33. [K]
- Basel Committee (2013). Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools. https://www.bis.org/publ/bcbs238.htm [V page; haircut details K]

**Regulators, peers and markets**
- Bank of England (2023). Bank staff paper: LDI minimum resilience. https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/bank-staff-paper-ldi-minimum-resilience [V]
- Financial Stability Board (10 Dec 2024). Liquidity Preparedness for Margin and Collateral Calls: Final report. https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/ [V]
- Federal Reserve (16 Sep 2026). FOMC statement. https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm [V]
- Federal Reserve Bank of New York. SOFR data API. https://markets.newyorkfed.org/api/rates/secured/sofr/last/5.json [V]
- U.S. Treasury. Daily par yield curve, Oct 2026. https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610 [V]
- Morningstar DBRS (18 Sep 2025). Credit Rating Report: CPP Investments & CPPIB Capital. https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-DBRS-Rating-Report-091825.pdf.pdf [V]
- CPP Investments (20/21 May 2026). Net Assets Total $793.3 Billion at 2026 Fiscal Year End. https://ca.finance.yahoo.com/news/cpp-investments-net-assets-total-100000452.html [V]
- CPP Investments (2025). F2025 Annual Report. https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-F2025-Annual-Report-English.pdf [via search excerpt]
- Moody's Ratings (20 Jul 2026). Ontario Teachers' Pension Plan Board: Update to credit analysis. https://www.otpp.com/content/dam/otpp/documents/1-home/about/investors-relations/Credit_Opinion-Ontario-Teachers-Pension-Plan-20Jul2026-PBC_1490754.pdf [V]
- OTPP (2026). Ontario Teachers' announces positive 2025 results. https://otpp.com/en-ca/about-us/news-and-insights/2026/ontario-teachers-announces-positive-2025-results/ [V]
- NBIM. Investment mandate – Government Pension Fund Global (amended 9 Dec 2025). https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/ [V]
- Finadium (13 May 2024), summarizing the Bank of Canada FSR on pension repo. https://finadium.com/?p=140368 [V, secondary]
- Temasek (2026). Investor Presentation 2026. https://www.temasek.com.sg/content/dam/temasek-corporate/our-financials/investor-library/investor-presentation/Temasek%20Investor%20Presentation%202026_EN.pdf [via search excerpt; direct fetch 403]
- Mubadala. Investors overview. https://www.mubadala.com/en/investors/overview [V]
- Emirates NBD Research (22 Jan 2026). PIF 2036 USD sukuk. https://www.emiratesnbdresearch.com/en/articles/pif-2036-usd-sukuk [V]
- Zawya (2026). Saudi PIF raises $7bln in 3-tranche bond sale. https://www.zawya.com/en/capital-markets/bonds/saudi-pif-raises-7bln-in-3-tranche-bond-sale-orderbook-tops-238bln-q5qhbejk [V, partial]; AGBI (May 2026) https://www.agbi.com/finance/2026/05/saudi-arabias-pif-raises-record-7bn-in-debt/ [via search excerpt]
- Enterprise AM (17 Oct 2025). Mubadala bond (T+55). https://enterpriseam.com/uae/2025/10/17/this-morning-mubadala-to-tap-debt-markets-again-this-month-reuters-poll-positive-on-uae-growth-this-year/ [via search excerpt; direct fetch 403]
- Harvard Magazine (Dec 2008). Harvard Borrows $2.5 Billion: The Costs and Rationale. https://www.harvardmagazine.com/print/3822?page=all [V]
- The Harvard Crimson (8 Apr 2025). Harvard April 2025 bond sale. https://www.thecrimson.com/article/2025/4/8/april-2025-bond-sale [V]
- Semafor (26 Aug 2025). Universities are borrowing more. https://www.semafor.com/article/08/26/2025/universities-are-borrowing-more-to-make-up-for-trumps-funding-cuts [V]
- Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf [V]
- ILPA (2024). NAV-Based Facilities: Guidance for LPs and GPs. https://ilpa.org/wp-content/uploads/2024/07/ILPA-Guidance-on-NAV-Facilities-2024.pdf [V]
- Rede Partners (23 Jun 2026). NAV financing report 2026. https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026 [V]
- AllianceBernstein (2026). NAV Loans: Flexibility for Private Equity When Holding Periods Extend. https://www.alliancebernstein.com/us/en-us/investments/insights/investment-insights/nav-loans-flexibility-for-private-equity-when-holding-periods-extend.html [via search excerpt]
- D. E. Shaw (c. Jan 2025). Imbalance Sheet: Supply, Demand, and S&P 500 Financing. https://www.deshaw.com/library/imbalance-sheet [V]
- CME Group (2026). Funding the U.S. Equity Market to New Heights. https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html [via search excerpt; direct fetch timed out]
- Reuters via Kitco (9 Jul 2026). US markets brace for renewed funding pressure as leverage rises. https://www.kitco.com/news/off-the-wire/2026-07-09/us-markets-brace-renewed-funding-pressure-leverage-rises [V]
- GIC. Our Investment Framework. https://www.gic.com.sg/our-investment-framework/ [V: no leverage disclosure]
- NZ Super Fund. How we invest. https://www.nzsuperfund.nz/how-we-invest/ [V: no leverage disclosure]

## Citation corrections (2026-10-18)

Sources: literature audit (`research/literature/00_LITERATURE_SYNTHESIS.md` Sections 2.2 and 2.5; `research/literature/06_leverage.lit.md` Sections 1–2). Metadata confirmed via Crossref on 2026-10-18.
- Section 2.2, log-growth formula: tag "[K: Merton 1971; Kelly 1956]" now credits Merton (1971) with the continuous-time formula and Kelly (1956) with the log-growth criterion only (the verification log's attribution caveat, upheld by the literature check).
- Section 2.2, Kelly leverage and maximum growth: tag "[V: Wikipedia summary of Kelly 1956]" replaced by the continuous-time log-utility result (Merton 1971). Kelly (1956) does not contain these formulas.
- Section 10, Brown, Dimmock, Kang & Weisbenner (2014): subtitle ": Evidence and Implications" added; the NBER w15861 link replaced by the AER DOI 10.1257/aer.104.3.931, with w15861 kept as the working-paper version (audit Section 2.5).
- Section 10, Gorton & Metrick, *Haircuts*: published version added, FRB St. Louis *Review* 92(6): 507–520 (2010), DOI 10.20955/r.92.507-20; NBER WP 15273 kept as the working paper (audit Section 2.2, item 5).
- Section 10, Kelly (1956): note added that it is cited for the log-growth criterion only.
- Section 10, MacLean, Thorp & Ziemba (2011): subtitle ": Theory and Practice" and DOI 10.1142/7598 added.
- Section 10, Merton (1971): *JET* 3(4): 373–413 confirmed (the issue was unconfirmed); DOI 10.1016/0022-0531(71)90038-X added.
- Section 10, Barro (1979): issue given as 87(5, Part 1) per Crossref (was 87(5), unconfirmed); DOI 10.1086/260807 added.
- Section 10, Geanakoplos (2010): pages 1–65 changed to 1–66 per Crossref; DOI 10.1086/648285 added.
- Section 10, Stafford (2022): DOI 10.1093/rfs/hhab020 added and 35(1): 299–342 confirmed (the literature check had found the DOI only in a search excerpt).
- Section 10, Getmansky, Lo & Makarov (2004): DOI 10.1016/j.jfineco.2004.04.001 added.
- No change needed: no Broadie–Glasserman–Kou barrier statistic or shift appears in this dossier, and none of the works in the 2026-10-18 re-checks (topics 10, 11, 13, 14 and G3) is cited here.
