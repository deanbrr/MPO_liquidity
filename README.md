# MPO_liquidity

Multiperiod Optimization in an Endowment Framework.

This repository holds the research, the design and working prototypes for a multi-period, liquidity-aware portfolio optimizer. It is built for a ~$177bn endowment-model sovereign fund with these features:
- the owner sets an annual distribution of 5–10% of NAV;
- the return goal is 10% nominal USD;
- leverage is allowed;
- about 60% of the fund is private markets;
- a large multi-asset OTC derivatives overlay runs a tail hedge and an opportunistic book.

> **All portfolio data in this repository is SYNTHETIC.** It is generated from documented processes for testing and illustration. It is not the fund's data and not a forecast.

## What it does

1. **Data and three-return fusion.** Each holding's underwritten, actual and group-forecast returns, together with market bids, are fused into a calibrated forward belief.
2. **Scenario tree.** Regimes (normal, PE distribution drought, crisis with an oil shock) drive returns, PE calls and distributions, secondary pricing and the owner's oil-linked draw.
3. **Multi-period optimizer.** One linear (or mixed-integer) program decides every node of the tree. It covers SELL / HOLD / ADD / REFINANCE / LEVER per holding, pacing, rebalancing, hedging and funding. The constraints are: pay the owner, keep a liquidity floor, stay within leverage and LTV caps, and keep a red-event limit. Each node also gets a liquidity price λ, the value of $1 of extra cash at that node.
4. **Simulator.** Probabilities of outcomes are measured out of sample on fresh simulated paths.
5. **Reports and chat.** These are interactive pages, and later a read-only analyst that answers questions using engine numbers only.

The engine is deterministic: the same inputs and limits always give the same decisions and numbers. People set the limits and approve the decisions. No language model produces any number.

## Repository map

| Path | Contents |
|---|---|
| `research/` | Multi-disciplinary research: 14 topic dossiers, 15 group dossiers (eight investment groups, including Real Assets), adversarial verification logs, cluster and master syntheses, gap addenda with their calculation scripts, the literature sweep and the citation-fix log. Start with `research/00_SYNTHESIS.md`, then `research/groups/01_GROUPS_SYNTHESIS.md`, `research/groups/02_REAL_ASSETS_SYNTHESIS.md` and `research/00_RESEARCH_SUFFICIENCY.md`. |
| `design/` | The design brief, the full architecture (`ARCHITECTURE.md`), the build specification (`BUILD_SPEC.md`), the slim engine-first design (`SLIM_ARCHITECTURE.md`, in progress), the decision-space specification, the chat-analyst design (`addenda/CHAT_ANALYST.md`), open decisions, the architecture schematic (`schematic/`) and worked examples (`examples/`). |
| `examples/tree_demo/` | A small worked multi-period tree: 3 years, 3 regimes, 40 nodes, solved by HiGHS and independently verified. The interactive page is `design/examples/Tree_Example.html`. |
| `examples/mpo_v2/` | Goal-seeking optimizer prototype over the full decision space, in progress. |
| `src/adic_tpa/`, `tests/` | Production package, build wave 0: data contracts, RNG, numerics, statistics, test kit and registry. |
| `orchestration/` | Scripts used to run the research, design and build workflows. |
| `inputs/` | Project context and prior work. |

## Quick start (Windows, Python 3.12)

```powershell
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -e .
# Worked tree example: solve, then render the interactive page
.venv\Scripts\python.exe examples\tree_demo\tree_demo.py
.venv\Scripts\python.exe -X utf8 examples\tree_demo\render_tree.py
# Tests for the production package
.venv\Scripts\python.exe -m pytest tests -q
```

Solvers: HiGHS (via `highspy` / cvxpy) and CLARABEL. No commercial solver is needed.

## Not included

- **The source paper.** *The Agentic Scientist* (Lange et al., Sakana AI, arXiv:2610.18933) is used as inspiration but not redistributed here. Get it from https://arxiv.org/abs/2610.18933.
- **Large regenerable research artifacts** (each over 5 MB):
  - `research/groups/addenda/gap_04_calcs/g04_shapley_M*_mixB.npz`
  - `g04_main_results.json`
  - `research/addenda/gap_02_calcs/gap02_grid_raw.json`

  Regenerate them with the calculation scripts in the same folders.

## Status (19 October 2026)

- **Research:** complete.
- **Architecture and build specification:** v1.1.
- **Slim engine-first design:** in progress, together with the goal-seeking optimizer prototype.
- **Production build:** wave 0 (foundations).

Open decisions and their working assumptions are listed in `design/OPEN_DECISIONS.md`.

*This is a private repository. It contains organization-specific design material.*
