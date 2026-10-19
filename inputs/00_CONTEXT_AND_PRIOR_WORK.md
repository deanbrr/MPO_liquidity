# Project context and prior work

## 1. Client context (as stated by the user, 2026-10-18)

The user is a quantitative / data-science lead at **ADIC**.

- ADIC runs an **endowment-model** portfolio of about **US$177bn**.
- It is **required to distribute 5–10% of the fund every year** to its sovereign owner.
- It has a **10% return target**, nominal absolute USD per the prior deck.
- It is **permitted to use leverage**.
- About **60% of the portfolio is private markets, mostly private equity (PE)**. PE distributions (DPI) have historically been one of the largest sources of cash, but DPI is now **declining**.
- The user wants a **multi-period optimization framework** that supports **robust scenario analysis** and reports **probabilities of outcomes**.
- Each individual strategy or asset should be examinable through a **SELL / HOLD / REFINANCE / LEVER** lens.
- Return data per asset:
  1. **underwritten** return at inception
  2. **current actual** return
  3. the strategy group's **forecast** return
- **What that data looks like** (user-confirmed, 2026-10-18):
  - forecasts are archived every quarter, so a point-in-time history exists;
  - all three series are IRR or multiple (MOIC) per holding, since inception;
  - forecasts come with ranges or cases;
  - everything is net of fees and carry.
- The user also wants to **chat with the model and ask questions** (2026-10-18). See design brief R16.
- ADIC runs a very large **multi-asset overlay of OTC derivatives** with two strategies:
  - **(a) tail-protection hedge**
  - **(b) opportunistic trading strategy** that aims to make money
- The user wants an **agentic architecture** that performs this analysis, and wants the **Investment Committee (IC) to be able to discuss the results**.
- Inspiration paper: *The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery*
  - Authors: Lange, Grillotti, Yamada, Charakorn, Ha (Sakana AI); arXiv:2610.18933v1, 13 Oct 2026; HTML at https://arxiv.org/html/2610.18933v1
  - Pipeline: task drafting → idea generation → planning → sandboxed experiments → result aggregation → baselines and ablations → analysis → report writing.
  - A meta-controller runs parallel research agents, with rubric verification at each stage.
  - Its ablations "suggest that reliable scientific autonomy depends not only on base model capabilities, but also on the cross-agent orchestration layer" (abstract). The base model also matters substantially (§5, §6.3).
  - Paper mechanisms are summarized accurately in `design/00_DESIGN_BRIEF.md` §2 and `research/verification/13_paper_deepread.localcheck.md`.

## 1A. Organization: the eight investment groups (user, 2026-10-18; Real Assets added later the same day)

The user described ADIC's investment organization. The framework's holdings, forecasts, action sets, budgets and IC discussion should map onto these groups.

| # | Group | User's description | Interpretation (status) |
|---|---|---|---|
| 1 | Private Equity (PE) | "allocates to funds" | Primary commitments to third-party PE funds (buyout, growth, venture, sector) as an LP. |
| 2 | Secondaries | "invests in secondary funds and does direct deals"; confirmed as "a hybrid of direct and fund investments" | A hybrid book: (a) LP commitments to third-party secondary funds; (b) direct secondary deals (direct LP-portfolio purchases, GP-led continuation vehicles). **Confirmed by the user.** |
| 3 | Capital Solutions | "does interesting financial deals" | Structured and hybrid capital: preferred and structured equity, holdco / NAV-based and fund financing, GP solutions, asset-backed and special-situations capital. **Confirmed by the user.** |
| 4 | Co-investment | "does direct co investment" | Minority equity co-investments alongside GPs, deal by deal. |
| 5 | Public Markets | "invests in hedge funds and other long only managers" | External hedge funds (multi-strategy, macro, equity long/short, credit, relative value) and long-only equity and fixed-income managers. |
| 6 | Private Credit | "invests in private credit" | Funds and SMAs in direct lending, asset-based finance, mezzanine and opportunistic credit. |
| 7 | Overlay | see §1 | Multi-asset OTC derivatives: tail-protection hedge and opportunistic trading. Also the natural home of synthetic exposure and rebalancing. |
| 8 | Real Assets | "i forgot another group called real assets" (added after the seven-group research) | **Confirmed by the user (2026-10-18):** sectors are real estate, infrastructure, and energy & natural resources (agriculture and timber are excluded). It invests through funds plus co-investments and direct assets or joint ventures. It is part of the ~60% private allocation; the user did not give a size, so the working figure is $18bn (see allocation v2). Energy and natural-resource holdings add oil exposure that is wrong-way with the owner's draw. Research streams G10–G15 are in progress, and design brief §8 holds the interim rules. |

**Treasury is owned by Corporate Finance** (user, 2026-10-18). It is a non-investment function, not one of the eight investment groups.
- **In the framework:** Corporate Finance / Treasury is ADIC's internal bank. It holds the cash and liquidity buffer, so it is the natural owner of:
  - the liquidity gate
  - the contingency funding plan
  - internal liquidity transfer pricing (the bank-FTP analogue)
- **Confirmed by the user:** Corporate Finance also owns:
  - portfolio-level borrowing and leverage facilities
  - overlay collateral (VM/IM) management
  - payment of distributions to the owner

  Corporate Finance therefore runs the whole funding and liability side of the balance sheet. The eight investment groups run the asset side.
- **Design consequences:**
  - Portfolio-level LEVER decisions (facilities, repo, bonds) are Corporate Finance actions. Groups own asset-level SELL / HOLD / REFINANCE / LEVER proposals.
  - Overlay margin is funded from Corporate Finance's collateral pool. The overlay is charged for contingent collateral use and credited for tail-hedge cash inflows in stress.
  - Distribution payments, liquidity buffer, borrowing and collateral all sit with one owner. The optimizer's liquidity shadow prices become Corporate Finance's internal transfer-pricing curve.
- **IC roster:** add a Treasurer / Corporate Finance seat to the shadow IC. It owns the liquidity gate and the contingency funding plan.

### Implications for the framework
These are the orchestrator's initial view, for research and design agents to test.

1. **Groups are the organizational unit; the total portfolio is the decision unit.**
   - Every holding carries a group tag. Holdings, forecasts, actions, budgets and IC discussion roll up by group.
   - Decisions are judged on total-portfolio outcomes.
   - A transfer between two ADIC groups is close to zero-sum and must never count as liquidity raised. Example: the Secondaries group buying a PE-group fund stake.
2. **The "strategy group forecast" is group-specific.** Each group forecasts differently:

   | Group | How it forecasts |
   |---|---|
   | PE | GP projections and look-through models |
   | Co-investment | Deal models |
   | Private Credit | Loss-adjusted yields |
   | Public Markets | Manager alpha expectations |
   | Overlay | Strategy P&L expectations |
   | Real Assets | Asset business plans: yield-on-cost, NOI growth, exit cap rates; appraisal-based marks |

   Estimate bias and credibility per group, and per strategy within each group.
3. **SELL / HOLD / REFINANCE / LEVER means something different in each group.**

   | Holding type | What the lens covers |
   |---|---|
   | PE fund interests | Secondary sale, NAV loan or preferred equity, or slowing new commitments |
   | Hedge funds | Redemption, subject to notice periods, gates and lock-ups |
   | Long-only managers | Physical-to-synthetic replacement through the overlay: keeps exposure, frees cash |
   | Private credit | Loan or fund-interest sales, back-leverage |
   | Co-investments | Single-asset secondary sales, holdco financing |
   | Capital Solutions | Syndication, asset-level financing |
   | Real assets | SELL: asset or stake sales, fund-interest secondaries, open-end redemptions (queues). REFINANCE: cash-out refinancing of asset-level debt, recap, sale-leaseback, JV sell-down. LEVER: acquisition or development debt |
4. **Two groups double as ADIC's market intelligence for its own liquidity actions.**
   - The Secondaries group knows secondary pricing, which feeds SELL.
   - The Capital Solutions group knows NAV-loan and preferred-equity pricing, which feeds REFINANCE.
   - Their quotes are valuable inputs and need conflict-of-interest controls.
5. **Some groups' opportunity sets are richest when ADIC's liquidity is scarcest.**
   - Secondary discounts and structured-capital yields widen in a DPI drought or a crisis.
   - Dry powder therefore has option value, and the shadow price of liquidity must reflect it.
6. **Cash generation differs sharply by group.**
   - Private Credit and Capital Solutions produce contractual cash yield.
   - PE funds and co-investments depend on exits.
   - Secondaries return cash faster than primaries.
   - Public Markets is the main liquidity reservoir, subject to hedge-fund terms.
   - The overlay can be a cash source (tail-hedge monetization) or a cash use (variation margin).
   - Real Assets produce income yield from core real estate and infrastructure, but depend on exits for value-add. Open-end funds can queue or gate redemptions. Asset-level debt brings refinancing risk.

### Action definitions and distribution mechanism (user-confirmed, 2026-10-18)
- **REFINANCE versus LEVER: cash-out versus exposure-up.**
  - **REFINANCE:** raise cash against a holding without selling it, e.g. a NAV loan, preferred equity or a recap.
  - **LEVER:** borrow to *add* exposure or return.
  - **SELL:** dispose of the holding, wholly or partly.
  - **HOLD:** keep it and fund its calls.
- **The owner sets the distribution rate each year.**
  - The sovereign owner's demand falls within 5–10% of the fund and is likely to be higher when oil is weak.
  - ADIC must meet it. It is an **exogenous, stochastic liability**, not a decision variable.
  - Model it as demand D_t = clip(f(oil, fiscal state, regime), 5%, 10%) × NAV, with liability-side wrong-way risk.

### Synthetic data
The user said synthetic returns may be created where needed.
- All synthetic data must be labeled as synthetic in data files, outputs and IC materials.
- It must never be presented as ADIC data.

The working allocation for the synthetic book is an assumption, to be replaced by ADIC figures:

| Bucket | Working NAV ($bn) | % of $177bn |
|---|---|---|
| PE funds (primaries) | 52 | 29.4% |
| Secondaries | 14 | 7.9% |
| Co-investment | 18 | 10.2% |
| Capital Solutions | 8 | 4.5% |
| Private Credit | 14 | 7.9% |
| **Private subtotal** | **106** | **59.9%** |
| Public Markets: hedge funds | 20 | 11.3% |
| Public Markets: long-only | 36 | 20.3% |
| Treasury: cash + IG (owned by Corporate Finance, not an investment group) | 15 | 8.5% |
| **Total** | **177** | **100%** |

**Working allocation v2, with Real Assets** (added 2026-10-18). The user confirmed that Real Assets is part of the ~60% private allocation. The $18bn size is a working assumption. This version supersedes the table above for new work. The seven-group research ran on v1, so its numbers will be re-run.

| Bucket | Working NAV ($bn) | % of $177bn |
|---|---|---|
| PE funds (primaries) | 34 | 19.2% |
| Secondaries | 14 | 7.9% |
| Co-investment | 18 | 10.2% |
| Capital Solutions | 8 | 4.5% |
| Private Credit | 14 | 7.9% |
| Real Assets | 18 | 10.2% |
| **Private subtotal** | **106** | **59.9%** |
| Public Markets: hedge funds | 20 | 11.3% |
| Public Markets: long-only | 36 | 20.3% |
| Treasury: cash + IG (Corporate Finance) | 15 | 8.5% |
| **Total** | **177** | **100%** |

**Unfunded commitments under v2:**
- **Real Assets:** about $4bn (closed-end funds and development).
- **PE:** the user chose the research figure, census v1.1 at $16.4bn, over the earlier $27bn (2026-10-18). Total unfunded is about $27.0bn before Real Assets.
- **Caveat:** census v1.1 was sealed for the $52bn PE-funds bucket. At the v2 bucket of $34bn, the same U/NAV of 0.32 implies about $10.9bn. Re-runs report both figures and flag the choice for the user.

- **Overlay:** sized by notional, not NAV. Working assumption: tens of $bn gross notional across the two strategies, collateralized from treasury.
- **Unfunded commitments:** working assumption ≈ $38bn. Mostly PE funds, plus:
  - secondaries, including deferred payments
  - private credit delayed-draw and revolver commitments
  - Capital Solutions
- **Distributions:** 5–10% of $177bn is about $8.9–17.7bn a year.

## 2. Prior work: deck "Robust Target-Attainment Total Portfolio Approach", v8

The deck is a 10-slide answer to an "ADIC Data Science Lead Case Study". It uses the case-brief numbers, **not** today's portfolio:

| Item | Value |
|---|---|
| Multi-asset NAV | $85bn |
| Liquid ≤30 days | 55% ($46.8bn) |
| Unfunded commitments | $18bn |
| IG + cash floor | 8% |
| Base 12-month capital calls | $6.0bn |

Figures are in `inputs/deck_v8/media/`.

### Slide 1 – Recommendation
Pursue the 10% absolute USD objective only after the robust floor and the liquidity survival gate clear.

- Return-seeking comes from three signals: valuation, opportunity-cost α*, and QDD (quantitative due diligence).
- The state engine conditions risk and liquidity.
- Flow: robust floor and liquidity gate → state + fragility risk conditioning → valuation + α* + QDD return signals → overlay / pacing implementation → IC decision (approve / resize / defer).
- IC output: floor status, Δ probability of hitting 10%, α* versus the funding basket, QDD evidence, drawdown and liquidity shadow costs, overlay margin, and a clear recommendation.

### Slide 2 – Case requirements → peer-informed architecture
Four pillars:

1. **Total Portfolio Approach:** common decision currency, incremental impact, constraint surfacing, dynamic what-if.
2. **QDD:** beta vs skill, leverage, timing, repeatability, downside behaviour, IEC-ready evidence.
3. **Liquidity & stress:** probabilistic cash-flow paths, LCR, survival horizon, breach risk, early warnings.
4. **AI governance:** multi-agent extraction / challenge / synthesis, with deterministic math and human sign-off.

Peer returns chart (realised long-run, annualised USD):

| Peer | Return | Period |
|---|---|---|
| NBIM | 6.6% | since 1998 |
| GIC | 5.7% | 20-yr |
| CPP | 8.3% | 10-yr |
| NACUBO >$5bn endowments | 8.3% | 10-yr |
| Yale | 10.3% | 20-yr |
| NZ Super | 10.0% | 20-yr |

The proposed ADIC stretch is 10%, against a 7% robust floor.

### Slide 3 – Quantitative core: two-tier optimizer (multi-period control, not static SAA)
- **Tier 1: hard robust floor and liquidity survival.**
  - Reject any action if plausible model misspecification pushes the worst-case 5-year annualised return below 7%, or if liquidity survival fails.
  - The gate allows at most a 5% breach probability under misspecification.
  - Hard constraints: IG + cash ≥ 8% of NAV; haircut 30-day liquidity must cover P99 margin plus stressed 12-month net calls.
- **Tier 2: stretch toward 10%, only after Tier 1 clears.**
  - Maximise target-attainment probability and opportunity-cost α*, net of drawdown, liquidity, policy and irreversibility shadow costs.
  - Controls: liquid reallocations, new private commitments, derivative overlays.
- Chart: x = 5-yr P(breach 7% floor) under misspecification; y = expected 5-yr annualised return; colour = liquidity headroom (×LCR).

  | Policy | P(breach) | Expected return | Gate |
  |---|---|---|---|
  | Robust framework | ≈2% | ≈11.6% | passes |
  | Static SAA | ≈3.5% | ≈7.9% | passes |
  | Target-chasing | ≈18% | ≈12.5% | rejected |

### Slide 4 – State + Fragility Engine: risk conditioning, not alpha forecasting
- The engine estimates the current market state, fragility and confidence. It does **not** forecast returns.
- It conditions vol and correlations, private calls and distributions, secondary discounts, overlay margin, and liquidity survival.
- Current lights:

  | Signal | Status | Reading |
  |---|---|---|
  | Macro state | AMBER | late-cycle inflation / policy hold |
  | Market fragility | AMBER | turbulence / absorption elevated, not crisis |
  | Credit stress | RED | private credit sleeve impaired |
  | Mean reversion | GREEN | |
  | Opportunity α* | GREEN | ACWI overlay + selected secondaries clear; broad private credit does not |
  | QDD evidence | AMBER | |
  | Liquidity gate | GREEN | |
  | Overlay capacity | GREEN | |

- Plan:
  - Y1–Y2: hedge, hold and preserve liquidity.
  - Y3: amplify only if valuation, α*, QDD and LCR stay green.
- The engine is based on HMM/HSMM plus fragility indicators (turbulence, absorption ratio).

### Slide 5 – From signals to action
- States: Defense (risk rising + not cheap), Hold/wait (stress high + cheap but falling), Selective add (stress/stagflation + cheap carry), Amplify (recovery + cheap + momentum), Size down (state confidence low).
- All states pass through a **Tier 1 gate**: floor 7%? liquidity? IG + cash 8%? P99 margin?
- Actions: Hedge (futures + freeze pacing), Hold (small dislocation adds only), Amplify (futures + staged commitments).
- **Hedge rule:** fragility ↑ AND (valuation not attractive OR liquidity gate tight) → reduce effective beta via overlay.
- **Amplify rule:** valuation cheap + α* > 0 + QDD supportive + LCR clear + fragility stable/falling → add exposure via overlay.
- Principle: the state conditions risk; valuation, α* and QDD drive return-seeking.

### Slide 6 – 3-year simulation + attribution
- Simulation: 50,000 paths, Student-t (df = 5), regime-conditional vol and correlations, private-asset lag.
- The scenario is a stylised path: oil shock → stagflation → recovery.
- Illustrative asset-class means by year:

  | Asset class | Y1 | Y2 | Y3 | σ Y1 |
  |---|---|---|---|---|
  | Global equities | −10% | +10% | +32% | 25% |
  | Fixed income | +8% | +4% | +10% | 10% |
  | Private equity | −5% | +7% | +20% | 15% |
  | Real assets | +9% | +8% | +12% | 12% |
  | Private credit | −10% | +5% | +12% | 12% |
  | Hedge funds | +5% | +7% | +6% | 8% |

- Results:

  | Policy | Mean | P(≥10%) | P10 | P(DD > 15%) |
  |---|---|---|---|---|
  | Static SAA | 7.3% | 31.7% | −0.3% | 23.9% |
  | Robust framework | 10.8% | 54.6% | +2.8% | 14.3% |
  | Target-chasing | 11.9% | 58.5% | +1.2% | 31.9% |

- Attribution of the +3.5pp uplift:

  | Component | Contribution |
  |---|---|
  | State / fragility protection | +0.5 |
  | Mean-reversion timing | +0.8 |
  | Opportunity-cost α* | +0.8 |
  | QDD / memo-corpus filter | +0.5 |
  | Overlay execution | +1.0 |
  | Liquidity / carry drag | −0.1 |

- Attribution formulas:
  - Simple contribution: RC_{α*,j} ≈ (Capital_j / NAV) × α*_j × (H_j / H)
  - Ablation: ΔR^ann = (W_T^full / W_T^{no α*})^{1/H} − 1
  - Shapley: φ_c(y) = Σ_{S ⊆ C\{c}} |S|!(|C|−|S|−1)!/|C|! · [y(S ∪ {c}) − y(S)]

### Slide 7 – Scenario mechanics: hedge first, then amplify (overlay sizes illustrative)

| Policy | Y1: oil shock + growth stress | Y2: stagflation | Y3: disinflation + recovery |
|---|---|---|---|
| Robust | −8% MSCI ACWI, +8% duration, −4% liquid credit hedge, +2% oil/inflation | −2% ACWI, +4% duration, +1% oil/inflation, +1% opportunistic α | +18% ACWI, +4% duration, +4% credit beta, +1% opportunistic α |
| Target-chasing | no hedge | +20% ACWI, +8% credit beta | +35% ACWI, +12% credit beta |
| Robust contribution | +0.4% | +0.6% | +2.5% |

Gating rule: Y3 amplification is blocked unless valuation, α*, QDD, P99 margin and LCR all clear.

### Slide 8 – Opportunity-cost α* + 18-yr QDD make proposals comparable (TPA heatmap)
- Heatmap columns: portfolio Δ return ($ and annualised %), α* vs funding basket, ΔMCTR, LAR99 consumed, ES95 increase, policy breach risk, QDD confidence, reversibility, robust floor impact, decision.
- Proposals:

  | Proposal | Δ return | α* | ΔMCTR | LAR99 | ES95 | Policy | QDD | Reversibility | Floor | Decision |
  |---|---|---|---|---|---|---|---|---|---|---|
  | A. MSCI ACWI recovery overlay, $3.0bn notional | +$110m / +0.35% ann. | +20bps | +0.3% vol | $0.2bn | +0.4% | green | High | daily | +0.1pp | APPROVE (trigger-based) |
  | B. PE secondary / co-invest, staged ($1.0bn of $3.0bn) | +$850m / +0.45% ann. | +280bps | +0.1% vol | $0.8bn | +0.5% | green | High | 5–7yr | +0.2pp | APPROVE $1.0bn staged |
  | C. Broad private credit blind pool, $1.5bn | +$60m / +0.05% | +60bps | +0.2% | $1.5bn | +0.8% | amber | Low | 7–10yr | −0.6pp | DEFER, re-underwrite |

- Memo-corpus findings:
  - **What worked:** staged secondaries and co-invests with clear downside memos.
  - **What failed:** leverage >6× EBITDA, dependence on multiple expansion, weak downside cases.
  - **Blind spot:** distribution timing was repeatedly too optimistic after spread shocks and exit-window closures.
  - **Action:** approve staged PE secondaries; defer broad private credit; challenge recovery assumptions.

### Slide 9 – IC dashboard (illustrative, 50,000 paths)
- Headline metrics:

  | Metric | Value |
  |---|---|
  | Survival horizon (P50, scenario B) | >36m |
  | 12-month breach risk | 0.6% |
  | P10 LCR | 2.1× |
  | P99 overlay margin | $0.7bn |
  | Base 12m calls | $6.0bn |
  | Floor margin | +2.3% vs 7% floor (1.5σ) |

- Early warnings:

  | Indicator | Status |
  |---|---|
  | State / fragility posterior | AMBER |
  | Distribution / call ratio | GREEN |
  | Secondary discount | AMBER |
  | Margin usage | GREEN |
  | IG + cash floor | GREEN |
  | Private credit defaults | AMBER |

- 36-month liquidity fan: liquid ≤30d stays around $44–50bn, against a ~$6.8bn floor.

### Slide 10 – Multi-agentic system and governance
- Architecture, in five columns:
  1. **Data:** 18-yr IC memos (PDFs, decks, post-mortems); portfolio data (NAVs, cash flows, exposures); market data (prices, factors, macro).
  2. **Extraction:** QDD/Memo agent (LlamaParse + dual-LLM extraction); State/Fragility agent (HMM + turbulence + absorption ratio).
  3. **Analytics:** α* engine (opportunity cost vs factor-funding basket); Liquidity engine (Monte Carlo, regime-switched LCR and PBR); Overlay engine (futures/options sizing, margin and gate check).
  4. **Challenge:** Devil's advocate (target-chasing flag, failure-analogue retrieval).
  5. **Synthesis:** IC synthesis agent (TAS, TAP, gloss, citation-traced memo), then the human IC (approve / resize / defer, with audit trail and override log). A closed loop feeds override + outcome back into the corpus.
- **What prevents target-chasing?** The Tier 1 robust floor is a hard constraint. Any action that breaches the 7% floor, liquidity survival, the model-confidence threshold or the 8% IG + cash floor is rejected, regardless of TAP uplift.
- **AI boundary:** LLMs extract, retrieve, challenge and summarise. Deterministic code runs α*, QDD metrics, Monte Carlo, liquidity tests and overlay margin. The IC retains decision rights.
- Motto: "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."

## 3. Gaps between the prior work and the new requirement (initial assessment)

1. Scaled for $85bn and 55% liquid, whereas the real fund is $177bn with ~60% private. The liquidity picture is far tighter.
2. No asset-level SELL / HOLD / REFINANCE / LEVER decisions. The private book is treated as an aggregate with a lag.
3. The 5–10% distribution requirement is not modelled as an explicit policy, stochastic liability or constraint.
4. Leverage is not modelled as a decision variable, at either the portfolio or the asset level.
5. The PE cash-flow model is thin. There is no explicit, regime-dependent call/distribution model capturing the DPI decline.
6. No fusion of underwritten / actual / forecast returns into calibrated forward beliefs.
7. The tail-protection hedge and the opportunistic trading strategy are not modelled separately. Collateral and margin dynamics are only a P99 number.
8. Multi-period control is a set of hand rules. It is not formally optimised and does not expose shadow prices.
9. IC interaction is limited to a dashboard and a synthesis agent. There is no structured deliberation, view elicitation or live what-if.
