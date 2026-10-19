export const meta = {
  name: 'adic-tree-demo',
  description: 'Worked multi-period scenario-tree example of the ADIC optimizer: build and solve a small multistage stochastic LP, verify it independently (math + finance), visualize it as an interactive offline page, and write a plain-English walkthrough',
  phases: [
    { title: 'Model', detail: 'build and solve the toy multistage program; export nodes, decisions, duals, outcomes' },
    { title: 'Verify', detail: 'independent re-solve, constraint and dual checks; finance sanity review' },
    { title: 'Fix', detail: 'apply verified corrections and re-run' },
    { title: 'Present', detail: 'interactive tree page and walkthrough document' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const EX = ROOT + '\\examples\\tree_demo'
const SCRIPT = EX + '\\tree_demo.py'
const PARAMS = EX + '\\params.json'
const RESULTS = EX + '\\results.json'
const HTML = ROOT + '\\design\\examples\\Tree_Example.html'
const WALK = ROOT + '\\design\\examples\\TREE_WALKTHROUGH.md'

const COMMON = `PROJECT: the ADIC multi-period portfolio optimizer (folder ${ROOT}). The user (a quant lead at ADIC) said the design documents look "too complicated", "human in the loop" and "subjective", and asked to SEE "the multiperiod tree structure example of how this would work". Your work must show, concretely and with real computed numbers, that the core is an objective multistage stochastic optimization: given inputs and limits, it computes decisions at every node of a scenario tree, the shadow price of liquidity at each node, and probabilities of outcomes. Humans only set limits and approve. Everything is SYNTHETIC (label it so).
Context to read briefly (do not get lost in them): ${ROOT}\\design\\ARCHITECTURE.md §5.1-5.7 (the multi-period problem, objective and tiers, the here-and-now tree program H, Phase I, duals and lambda, Lagrangian scoring) and §4.8 (the SELL/HOLD/REFINANCE/LEVER reading rules and instrument library); ${ROOT}\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md §1A (allocation v2, eight groups, Corporate Finance). Definitions confirmed by the user: REFINANCE = raise cash against a holding without selling it (cash-out; e.g. a NAV loan); LEVER = borrow to add exposure; the owner sets the annual distribution (5-10% of NAV, higher when oil is weak) and it is an exogenous liability that must be paid.
ENVIRONMENT: Windows PowerShell 5.1 (cwd resets each call; absolute paths). Python: ${PY} with numpy, scipy, cvxpy (HiGHS, CLARABEL), highspy, pandas, matplotlib, plotly. No network. Do not touch src/ or tests/ (another build is running there).`

const MODEL_SPEC = `TOY MODEL (keep it small, readable and faithful to the architecture's logic; you may refine the details, but record every parameter in ${PARAMS} with a one-line rationale and, where possible, the research source):
- Units $bn; annual stages t = 0, 1, 2 decisions, t = 3 terminal. Three regimes per year: N (normal), D (PE distribution drought), C (crisis with an oil shock). Start in D (the research's drought posterior is about 0.87). Illustrative transition matrix, e.g. from N: N .70 / D .20 / C .10; from D: N .30 / D .55 / C .15; from C: N .25 / D .35 / C .40. Tree = 1 + 3 + 9 + 27 = 40 nodes, node probabilities = products of transitions (must sum to 1 per stage).
- Balance sheet at t0 (allocation v2, $177bn): Liquid book (public markets + treasury) $71bn; PE-like book (PE funds + co-investment + secondaries) $66bn with unfunded commitments (use about $16-20bn); yield book (private credit + capital solutions + real assets) $40bn paying cash yield. Cash buffer inside the liquid book: track cash/HQLA separately (start about $15bn).
- Regime-dependent exogenous rates (illustrative, label SYNTHETIC; anchor on the research where you can): liquid return (e.g. N +7%, D +4%, C -25%); PE NAV return (N +10%, D +3%, C -20%); PE distribution rate as % of NAV (N ~18%, D ~9%, C ~4%); PE call rate as % of unfunded (N ~30%, D ~29%, C ~35%); yield-book cash yield (N 8%, D 7%, C 5%) and NAV return (N +2%, D 0%, C -10%); owner draw as % of NAV (N 6%, D 7.5%, C 10%: oil weak -> higher draw).
- Decisions at every node (non-anticipative: one decision vector per node): sell liquid (small cost); SELL PE interests in the secondary market at a regime-dependent discount (N 8%, D 15%, C 35%; buyer assumes the matching unfunded); REFINANCE via a NAV loan (cash-out against the PE book; LTV cap e.g. 10% of PE NAV, 5% in C; spread N 4% / D 6% / C 9%); draw or repay a committed revolver (limit e.g. $15bn; availability 100% in N and D, 50% in C per the literature; cost ~5.5%); LEVER = add synthetic liquid exposure financed by borrowing (cap total exposure at 1.30x NAV; financing cost ~0.6% plus initial margin in cash); PE PACING = cut this year's planned new commitments (plan e.g. $5bn a year) at a franchise cost per $ cut (research c^PACE ~ 8.6 cents per $ forgone) and with no liquidity credit for two quarters (approximate within the annual step). Debt balances carry and accrue interest; repayments are allowed.
- Hard constraints at every node (Tier 1A): the owner draw is paid in full; cash/HQLA >= a floor (e.g. 4% of NAV); LTV and revolver availability caps; leverage cap; non-negativity. A Tier-1B-style downside constraint: CVaR of terminal wealth at the 10% level >= a floor (choose a floor that binds in a visible but not absurd way, and report it), written in standard LP form (Rockafellar-Uryasev).
- Objective (Tier 2): maximize the expected value of a concave piecewise-linear utility of terminal wealth (an 8-10 tangent approximation of CRRA gamma=3), so the program stays an LP (never risk-neutral). Terminal wealth = cash + liquid + PE NAV + yield NAV - debt (+ a simple terminal value for unfunded if you need it; explain it).
- Solve with HiGHS (highspy directly, or cvxpy with solver HIGHS), get duals from a basic solution. The liquidity price at node n: lambda_n = dual of node n's cash-balance row divided by node probability, relative to the dual at the root (or the architecture's ell = M/(mu - M) premium if you can derive it cleanly) - say exactly what you report.
- Report per node: id, stage, regime path (e.g. D>C>N), probability, opening state, exogenous flows (owner draw, PE calls and distributions, yield cash), decisions with amounts, an action label per book (SELL / HOLD / REFINANCE / LEVER / PACE-CUT), binding constraints with their shadow prices, and lambda. Summary: expected terminal wealth, terminal wealth distribution, P(10-year-equivalent annual return >= 10% over the 3 years, counting distributions paid), P(any PE fire sale at the crisis discount), P(cash floor binding), CVaR, and a comparison with a naive rule (sell liquid first, never refinance or lever) computed on the same tree.
- Also solve a second case WITHOUT the revolver (consent scenario: no signed facility) and report how decisions and lambda change (the architecture's example: a fund flips between SELL and HOLD depending on whether the revolver is signed).
- Show the MPC idea: after year 1 the realized regime is observed and the program is re-solved from that node; demonstrate by re-solving from one stage-1 node and comparing with the original plan.
Performance: the whole script runs in under 20 seconds. Deterministic.`

const BUILD_SCHEMA = { type: 'object', properties: { script: { type: 'string' }, results: { type: 'string' }, runtime_s: { type: 'number' }, objective: { type: 'number' }, root_decisions: { type: 'array', items: { type: 'string' } }, headline: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['script', 'results', 'runtime_s', 'root_decisions', 'headline'] }
const ISSUE_SCHEMA = { type: 'object', properties: { report_path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'issue', 'fix'] } } }, required: ['report_path', 'verdict', 'issues'] }
const FIX_SCHEMA = { type: 'object', properties: { fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, headline: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['fixed', 'not_fixed', 'headline', 'summary'] }
const PRES_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, summary: { type: 'string' }, qa: { type: 'string' } }, required: ['path', 'summary'] }

phase('Model')
const build = await agent(`${COMMON}

TASK: build and solve the worked example.
${MODEL_SPEC}
OUTPUTS: ${SCRIPT} (self-contained, commented where the finance or math is non-obvious), ${PARAMS}, ${RESULTS} (JSON: meta with SYNTHETIC label and parameters; nodes[] with all per-node fields; edges[]; cases {with_revolver, no_revolver}; mpc_resolve; summary; naive_rule comparison), and ${EX}\\RESULTS.md (a short human-readable summary with the key tables). Run the script and make sure it is deterministic (run twice; identical results). Return the structured output.`, { label: 'model:build', phase: 'Model', schema: BUILD_SCHEMA })
if (!build) { log('Model build failed; stopping.'); return null }
log(`Solved in ${build.runtime_s}s. Root decisions: ${build.root_decisions.join('; ')}`)

phase('Verify')
const [math, fin] = await parallel([
  () => agent(`${COMMON}

TASK: independent MATHEMATICAL VERIFICATION of ${SCRIPT} and ${RESULTS}. Do not trust the author. (1) Re-implement the same LP independently from ${PARAMS} (a different code path: e.g. cvxpy with CLARABEL if the author used highspy, or vice versa) and compare the objective (relative difference <= 1e-6) and the decisions. (2) Check every constraint at every node from the exported numbers (cash balances add up to the cent, owner draw paid, floors, caps, LTV, leverage, non-negativity), probabilities per stage sum to 1, non-anticipativity holds by construction. (3) Check the duals: for 5 nodes add a small amount of cash (e.g. $0.01bn) to the node's cash row, re-solve, and compare the objective change with the reported dual; check sign conventions and the lambda normalization the author reports. (4) Check the CVaR formulation, the PWL utility (concave, tangents correct) and the naive-rule comparison (same tree, same flows). (5) Check the no-revolver case and the MPC re-solve. Write ${EX}\\verify_math.md and return the structured issues.`, { label: 'verify:math', phase: 'Verify', schema: ISSUE_SCHEMA }),
  () => agent(`${COMMON}

TASK: FINANCE SANITY REVIEW of ${RESULTS} and ${EX}\\RESULTS.md as an experienced sovereign-fund CIO/CRO would read them. Are the behaviours sensible and explainable? (e.g. in normal branches hold PE and keep pacing; in the drought sell liquid or draw the revolver before selling PE at a discount; in a crisis with oil weak and the owner draw high, use committed liquidity and REFINANCE before fire-selling PE at a 35% discount; LEVER only when liquidity is slack; lambda highest in crisis branches; the no-revolver case raises lambda and can flip a fund to SELL.) Flag anything that looks wrong, implausible, misleading or unexplained (e.g. an action that only appears because of an end-of-horizon artefact, a parameter far from the research, a utility or CVaR floor that drives absurd results, or numbers presented without the SYNTHETIC label). Check parameters against the research where cited (${ROOT}\\research\\00_SYNTHESIS.md, ${ROOT}\\research\\groups\\01_GROUPS_SYNTHESIS.md). Write ${EX}\\verify_finance.md and return the structured issues.`, { label: 'verify:finance', phase: 'Verify', schema: ISSUE_SCHEMA }),
])
const issues = [...((math && math.issues) || []), ...((fin && fin.issues) || [])]
log(`Verification: ${issues.length} issues (critical ${issues.filter(i => i.severity === 'critical').length}, high ${issues.filter(i => i.severity === 'high').length}).`)

phase('Fix')
const fix = await agent(`${COMMON}

TASK: apply the verified corrections from ${EX}\\verify_math.md and ${EX}\\verify_finance.md to ${SCRIPT} and ${PARAMS}: fix every critical and high issue and the medium ones unless you justify otherwise; re-run; regenerate ${RESULTS} and ${EX}\\RESULTS.md; re-run the independent checks that failed (objective agreement, constraint checks, dual finite differences) and record the results in ${EX}\\RESULTS.md under "Verification". Return the structured output with the final headline findings.`, { label: 'fix', phase: 'Fix', schema: FIX_SCHEMA })

phase('Present')
const [page, walk] = await parallel([
  () => agent(`${COMMON}

TASK: build an interactive, self-contained, offline HTML page ${HTML} that shows the worked tree from ${RESULTS} (read it; never retype numbers by hand: generate the page with a Python script ${EX}\\build_page.py that embeds the JSON). Title "Multi-Period Tree Example". Content:
1. A short header: what this is (a small version of the here-and-now program H), SYNTHETIC label, one-paragraph "how to read".
2. The tree drawn left to right (t0 -> t1 -> t2 -> t3), nodes as boxes coloured by regime (N/D/C, colour-blind-safe, with a legend), edge labels with transition probabilities, node probability shown; each node shows compact action badges per book (SELL / HOLD / REFINANCE / LEVER / PACE-CUT) and a small lambda indicator (heat). The 27 leaves can be shown compactly (e.g. collapsible by stage-1 branch, or a zoomable SVG) so the tree stays readable at 1440px width.
3. Clicking a node opens a side panel: path, probability, opening state, exogenous flows, decisions with amounts, binding constraints and shadow prices, lambda, and a one-line plain-English "why" generated from the numbers (e.g. "Crisis + high owner draw: the revolver is at its 50% availability, so the model refinances $Xbn against the PE book instead of selling PE at a 35% discount; lambda = Y").
4. A toggle between the cases "revolver signed" and "no revolver", highlighting nodes whose decision changes.
5. A summary panel: terminal wealth distribution (a small inline SVG histogram or plotted bars), expected terminal wealth, P(>=10% a year), P(PE fire sale), CVaR, and optimized vs naive rule.
6. An "MPC" panel: the re-solve from one stage-1 node versus the original plan.
Design: CSS tokens on :root with a dark-mode override (prefers-color-scheme guarded by :root:not([data-theme="light"]) and :root[data-theme="dark"]), explicit body background, theme toggle, system fonts, 16px gutters, keyboard-accessible nodes, no external resources. Then render it with headless Edge ("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" --headless=new --disable-gpu --user-data-dir=<a temp folder under ${EX}> --window-size=1440,1400 --screenshot=<png> <file URL>), look at the screenshot with the Read tool, and fix layout problems (overlaps, cut-off text, unreadable tree). Return the structured output with a QA note.`, { label: 'present:page', phase: 'Present', schema: PRES_SCHEMA }),
  () => agent(`${COMMON}

TASK: write ${WALK}, a plain-English walkthrough (2,000-3,500 words) for a sovereign-fund IC audience and the quant lead, using the actual numbers in ${RESULTS} and ${EX}\\RESULTS.md (cite node ids; label SYNTHETIC). Sections:
1. What the tree is: stages, regimes, branching, probabilities (with a small ASCII sketch of the first two stages).
2. What is decided at each node and why decisions are "contingent plans": only the root decision is executed now; the rest are the plan for each future branch, re-solved every quarter (MPC) as reality unfolds.
3. The optimization in words and in compact equations: state transition, cash balance, owner draw as a hard liability, limits, CVaR safety floor, concave utility objective; why it is an LP; non-anticipativity.
4. Walk through three branches (the best, the drought, and the crisis-with-oil-shock path): state, decisions (SELL / HOLD / REFINANCE / LEVER / pacing), binding constraints and the liquidity price lambda.
5. The liquidity price: what lambda means in dollars, why it spikes in the crisis branches, how it becomes Corporate Finance's transfer price, and how it decides SELL vs HOLD for a fund (reservation price vs bid), including the revolver vs no-revolver flip.
6. Probabilities of outcomes: what the tree says and why the production system certifies them on 10,000-50,000 simulated paths instead (the tree is for decisions and prices, the simulator for probabilities).
7. Optimized vs naive rule: what the optimization adds, in dollars.
8. How this scales to the production design: the real tree (24 x 4 x 6 = 576 leaves over 8 periods, six model worlds pooled, eight groups, quarterly re-solve in about 2 minutes on HiGHS), what is the same and what is richer.
9. Where humans and AI agents come in, precisely: humans set the limits and approve; agents never produce numbers; the same inputs always give the same outputs. Address the "subjective" concern directly and honestly.
Return the structured output.`, { label: 'present:walkthrough', phase: 'Present', schema: PRES_SCHEMA }),
])

return { build: { runtime_s: build.runtime_s, root: build.root_decisions }, verification: { math: math && { verdict: math.verdict, n: math.issues.length }, finance: fin && { verdict: fin.verdict, n: fin.issues.length } }, fix, page, walkthrough: walk }
