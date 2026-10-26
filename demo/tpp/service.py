"""Component 5: the platform service (what build_demo.py calls to precompute the stakeholder page).

Loads and classifies the data once; caches the book and the path sets per preference view; persists each group's
settings and latest plan under demo/state (git-ignored: derived from the MSIP-labelled inputs). Every action takes a
progress callback.

Actions
  overview(role)            data stamp, quality report, classification coverage, book, ER and preference returns,
                            underwriting bias, DPI by vintage, PE candidate pool, the lens and the house limits
  evaluate(role)            status quo with and without the PE program, out of sample, under the role's view
  optimize(role)            the role's objective under every house limit, certified out of sample, with the change
                            list, LEVER / REFINANCE labels, shadow prices and holding cards
  compare()                 the IC matrix: status quo, each group's latest plan and the consensus plan on one view
  swap(role, codes, target) sell named holdings and redeploy into an ER bucket: paired change in every metric
"""
from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from pathlib import Path

import numpy as np

from . import book as bookmod
from . import classify, ingest, lp, metrics, paths, plan as planmod, returns, sim, stakeholders as sh, substitution
from .buckets import BY_ID, CATALOG, PRIVATE
from .legacy import DEMO, demo_params, wilson
from .returns import WORLDS


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if np.isfinite(v) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if o is None or isinstance(o, (str, int, bool)):
        return o
    if hasattr(o, "isoformat"):
        return o.isoformat()
    try:
        import pandas as pd
        if o is pd.NA or (isinstance(o, float) and np.isnan(o)):
            return None
    except Exception:
        pass
    return str(o)


class Platform:
    def __init__(self, data_dir: Path | None = None, state_dir: Path | None = None, fund_file: str | None = None,
                 er_file: str | None = None, quick: bool = False):
        self.P = demo_params()
        self.data_dir = Path(data_dir or DEMO / "data")
        self.state_dir = Path(state_dir or DEMO / "state")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.fund_file = Path(fund_file) if fund_file else self.data_dir / "fund_returns.xlsx"
        self.er_file = Path(er_file) if er_file else self.data_dir / "er_strategy_returns.xlsx"
        self.n_lp = int(self.P.get("simulation.n_lp_paths")) if not quick else 60
        self.n_val = int(self.P.get("simulation.n_val_paths")) if not quick else 150
        self.n_oos = int(self.P.get("simulation.n_oos_paths")) if not quick else 300
        self.lock = threading.RLock()
        self._books: dict = {}
        self._paths: dict = {}
        self.load_data()
        self.states = {r: self._load_state(r) for r in sh.ROLES}
        self.ic = self._load_json("ic.json", {"prefs": copy.deepcopy(sh.LENSES["strategy"]["prefs"]) | {"risk_aversion": 3.0},
                                              "stress": "base"})
        self.plans = {r: self._load_json(f"{r}_plan.json", None) for r in sh.ROLES + ["consensus"]}
        self.last = {}

    # ------------------------------------------------------------------ data and state
    def load_data(self):
        P = self.P
        self.er = ingest.load_er(self.er_file)
        funds = ingest.load_funds(self.fund_file)
        live, _ = ingest.live_book(funds, P)
        self.quality = ingest.quality_report(funds, live, P)
        C = classify.Classifier()
        self.classified = C.classify(live)
        self.coverage = classify.coverage(self.classified)
        self.dpi = ingest.dpi_by_vintage(self.classified)
        props = {**ingest.xlsx.doc_properties(self.fund_file), **ingest.xlsx.doc_properties(self.er_file)}
        self.labelled = any("MSIP_Label" in k for k in props)
        self.files = {"fund_file": self.fund_file.name, "er_file": self.er_file.name,
                      "as_of": self.quality["as_of"], "sensitivity_label": self.labelled}
        self._books.clear()
        self._paths.clear()

    def _load_json(self, name, default):
        p = self.state_dir / name
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return default
        return default

    def _save_json(self, name, obj):
        (self.state_dir / name).write_text(json.dumps(jsonable(obj), indent=1), encoding="utf-8")

    def _load_state(self, role):
        st = sh.default_state(role)
        saved = self._load_json(f"{role}.json", None)
        if saved:
            for k in ("prefs", "objective", "stress"):
                if k in saved:
                    st[k] = saved[k]
            st["settings"].update({k: v for k, v in saved.get("settings", {}).items() if k in sh.LENSES[role]["owns"]})
        st["prefs"] = returns.norm_prefs(st["prefs"])
        return st

    def save_state(self, role: str, patch: dict) -> dict:
        with self.lock:
            st = self.states[role] if role in self.states else None
            if role == "ic":
                self.ic["prefs"] = returns.norm_prefs({**self.ic["prefs"], **patch.get("prefs", {})})
                self.ic["stress"] = patch.get("stress", self.ic["stress"])
                self._save_json("ic.json", self.ic)
                return self.ic
            for k in ("objective", "stress"):
                if k in patch:
                    st[k] = patch[k]
            if "prefs" in patch:
                merged = copy.deepcopy(st["prefs"])
                for k, v in patch["prefs"].items():
                    if isinstance(v, dict) and isinstance(merged.get(k), dict):
                        merged[k].update(v)
                    else:
                        merged[k] = v
                st["prefs"] = returns.norm_prefs(merged)
            for k, v in patch.get("settings", {}).items():
                if k in sh.LENSES[role]["owns"]:
                    st["settings"][k] = v
            self._save_json(f"{role}.json", st)
            return st

    def reset_state(self, role: str) -> dict:
        with self.lock:
            self.states[role] = sh.default_state(role)
            self.states[role]["prefs"] = returns.norm_prefs(self.states[role]["prefs"])
            self._save_json(f"{role}.json", self.states[role])
            return self.states[role]

    def house(self) -> dict:
        return sh.house(self.states)

    # ------------------------------------------------------------------ caches
    @staticmethod
    def _key(*objs) -> str:
        return hashlib.sha256(json.dumps(jsonable(objs), sort_keys=True).encode()).hexdigest()[:20]

    BOOK_KEYS = ("total_nav_bn", "sleeve_split", "revolver_drawn0_bn", "term_debt0_bn", "pe_program_total_bn",
                 "goal_rate")

    def book_for(self, prefs: dict, house: dict, extra: dict | None = None):
        rp = {k: prefs[k] for k in ("basis", "weights", "persistence", "uw_debias")}
        bs = {k: house[k] for k in self.BOOK_KEYS if k in house} | (extra or {})
        key = self._key(rp, bs)
        if key not in self._books:
            R = returns.holding_returns(self.classified, self.er, self.P, prefs)
            B = bookmod.build_book(R["holdings"], R["buckets"], self.er, self.P, bs)
            self._books[key] = (B, R)
            if len(self._books) > 12:
                self._books.pop(next(iter(self._books)))
        return key, self._books[key][0], self._books[key][1]

    def paths_for(self, bkey: str, B, kind: str, stress: str, pi, house: dict):
        n = {"lp": self.n_lp, "val": self.n_val}.get(kind, self.n_oos)
        seed = int(self.P.get({"lp": "simulation.seed_lp", "val": "simulation.seed_val"}.get(kind, "simulation.seed_oos")))
        dset = {k: house.get(k) for k in ("draw_mode", "draw_rate")}
        key = self._key(bkey, kind, stress, dset, n)
        if key not in self._paths:
            self._paths[key] = paths.PathSet(B, self.P, n, seed, stress, pi, dset)
            if len(self._paths) > 12:
                self._paths.pop(next(iter(self._paths)))
        S = self._paths[key]
        S.pi = np.asarray(pi, float) / np.sum(pi)
        S.prob = S.pi[S.world] / S.n
        return S

    def view(self, role: str) -> dict:
        if role == "ic":
            return {"prefs": self.ic["prefs"], "stress": self.ic["stress"], "objective": "gbo"}
        st = self.states[role]
        return {"prefs": st["prefs"], "stress": st["stress"], "objective": st["objective"]}

    @staticmethod
    def _pi(prefs):
        return [prefs["scenario_probs"][w] for w in WORLDS]

    # ------------------------------------------------------------------ actions
    def overview(self, role: str) -> dict:
        with self.lock:
            v = self.view(role)
            house = self.house()
            _, B, R = self.book_for(v["prefs"], house)
            bt = R["buckets"]
            pi = R["pi"]
            rows = []
            nav_by_bucket = {}
            for u in B.units:
                nav_by_bucket[u.bucket] = nav_by_bucket.get(u.bucket, 0.0) + u.nav0
            unf_by_bucket = {}
            for u in B.units:
                unf_by_bucket[u.bucket] = unf_by_bucket.get(u.bucket, 0.0) + u.unf0
            for b in CATALOG:
                er_row = R["er"].loc[b.id]
                rows.append({"bucket": b.id, "label": b.label, "department": b.department, "vertical": b.vertical,
                             "vehicle": b.vehicle, "tier": b.tier,
                             "nav_bn": nav_by_bucket.get(b.id, B.liquid.get(b.id, 0.0)),
                             "unfunded_bn": unf_by_bucket.get(b.id, 0.0),
                             "file_nav_bn": B.liquid_src.get(b.id, {}).get("file", nav_by_bucket.get(b.id, 0.0)),
                             "sleeve_bn": B.liquid_src.get(b.id, {}).get("sleeve", 0.0),
                             "pace_sq_bn": B.pacing_sq.get(b.id, 0.0),
                             "er": [float(er_row[w]) for w in WORLDS], "er_flags": er_row["flags"],
                             "exist": [float(bt.loc[b.id, f"exist_{w}"]) for w in WORLDS],
                             "exist_exp": float(bt.loc[b.id, "exist_exp"]), "exist_ce": float(bt.loc[b.id, "exist_ce"]),
                             "new_exp": float(bt.loc[b.id, "new_exp"]), "new_ce": float(bt.loc[b.id, "new_ce"]),
                             "uw_bias": float(R["bias"].loc[b.id, "beta"]), "uw_n": int(R["bias"].loc[b.id, "n_mature"]),
                             "uw_gap": R["bias"].loc[b.id, "median_gap"]})
            pool = [u for u in B.units if u.pe_program and u.part == "tail"]
            h = R["holdings"]
            nav = h["nav_bn"].to_numpy()
            wavg = lambda col: float(np.average(h[col].fillna(0), weights=np.maximum(nav, 1e-12)))
            return jsonable({
                "role": role, "lens": sh.LENSES.get(role, {"title": "Investment Committee",
                                                          "subtitle": "Compares every group's plan on one view"}),
                "objectives": sh.OBJECTIVES, "stresses": paths.STRESSES,
                "state": self.states.get(role, self.ic), "house": house, "owner": sh.SETTING_OWNER,
                "files": self.files, "quality": self.quality, "coverage": {k: v for k, v in self.coverage.items()
                                                                          if k != "by_rule"},
                "book": B.summary(), "notes": B.notes, "buckets": rows, "dpi": self.dpi,
                "returns_summary": {"strategy_base": wavg("S_base"), "pref_exp": wavg("r_exp"), "pref_ce": wavg("r_ce"),
                                    "pi": pi.tolist()},
                "pe_pool": {"exposure_bn": sum(u.exposure0 for u in pool), "nav_bn": sum(u.nav0 for u in pool),
                            "unfunded_bn": sum(u.unf0 for u in pool), "holdings": sum(u.n for u in pool),
                            "program_bn": house["pe_program_total_bn"],
                            "pe_exposure_bn": sum(u.exposure0 for u in B.units if u.pe_program)},
                "plans": {r: (self.plans.get(r) or {}).get("summary") for r in sh.ROLES + ["consensus"]},
            })

    def _sim_settings(self, house):
        return {k: house[k] for k in ("floor_hard", "floor_target", "waterfall", "hf_quarterly_liquidity",
                                       "revolver_signed_bn", "revolver_drawn0_bn", "term_debt0_bn", "navf_ltv_max",
                                       "goal_rate", "rebalance", "maintain_target") if k in house}

    def _status_quo_pair(self, B, S, house, progress):
        sset = self._sim_settings(house)
        sq_prog = planmod.status_quo(B, self.P, house, program=True)
        sq_none = planmod.status_quo(B, self.P, house, program=False)
        progress("simulating the status quo with and without the PE program")
        o1 = sim.simulate(S, sq_prog, self.P, sset)
        o0 = sim.simulate(S, sq_none, self.P, sset)
        g = float(house["goal_rate"])
        return sq_prog, sq_none, o1, o0, metrics.summarize(o1, g), metrics.summarize(o0, g)

    def evaluate(self, role: str, stress: str | None = None, progress=print, house_override: dict | None = None,
                 prefs_override: dict | None = None) -> dict:
        with self.lock:
            v = self._variant_view(role, prefs_override)
            house = {**self.house(), **(house_override or {})}
            stress = stress or v["stress"]
            progress(f"book and returns under the {role} view ({v['prefs']['basis']} basis)")
            bkey, B, R = self.book_for(v["prefs"], house)
            progress(f"scenario paths: {self.n_oos} x 3 worlds, stress '{stress}'")
            S = self.paths_for(bkey, B, "oos", stress, self._pi(v["prefs"]), house)
            sq_prog, sq_none, o1, o0, s1, s0 = self._status_quo_pair(B, S, house, progress)
            d = metrics.paired_delta(o1, o0)
            res = {"role": role, "stress": stress, "status_quo": s1, "no_program": s0, "program_effect": d,
                   "program": substitution.change_list(B, sq_prog, sq_none, S)["pe_program"],
                   "W0": B.W0, "Wstar": B.Wstar}
            self.last[(role, "evaluate")] = res
            return res

    def _variant_view(self, role: str, prefs_override: dict | None) -> dict:
        v = copy.deepcopy(self.view(role if role != "consensus" else "ic"))
        if prefs_override:
            merged = copy.deepcopy(v["prefs"])
            for k, val in prefs_override.items():
                if isinstance(val, dict) and isinstance(merged.get(k), dict):
                    merged[k].update(val)
                else:
                    merged[k] = val
            v["prefs"] = returns.norm_prefs(merged)
        return v

    def optimize(self, role: str, objective: str | None = None, use_house: bool = True, progress=print,
                 persist: bool = True, house_override: dict | None = None, prefs_override: dict | None = None,
                 stress_override: str | None = None, keep_paths: bool = False) -> dict:
        """persist=False runs a variant (overridden limits, preferences or stress) without replacing the group's
        saved plan; keep_paths returns the out-of-sample per-path results of the plan and the status quo."""
        with self.lock:
            v = self._variant_view(role, prefs_override)
            objective = objective or (v["objective"] if role != "consensus" else "gbo")
            house = {**self.house(), **(house_override or {})}
            prefs = v["prefs"]
            stress = stress_override or (v["stress"] if role != "consensus" else self.ic["stress"])
            st_lp = sh.lp_settings(house, prefs, use_house, self.states.get(role, {}).get("settings"))
            progress(f"book and returns ({prefs['basis']} basis, worlds {np.round(self._pi(prefs), 2).tolist()}, "
                     f"risk aversion {prefs['risk_aversion']:g})")
            bkey, B, R = self.book_for(prefs, house)
            progress(f"in-sample scenarios for the LP: {self.n_lp} paths x 3 worlds (stress '{stress}')")
            S_lp = self.paths_for(bkey, B, "lp", stress, self._pi(prefs), house)
            t0 = time.time()
            M = lp.TPPModel(S_lp, self.P, st_lp, log=progress)
            progress(f"LP built: {M.nvar:,} columns, {M.nrow:,} rows, {M.A_mat.nnz:,} nonzeros ({time.time() - t0:.1f}s)")
            sq = planmod.status_quo(B, self.P, house, program=True)
            ev = M.evaluate_plan(sq)
            if ev is None:
                raise RuntimeError("the status quo is infeasible on the in-sample scenarios")
            if house.get("depth_guard", True):
                M.apply_depth_guard(ev["cvar10"], float(house.get("depth_delta", 0.0)))
                progress(f"depth guard: CVaR10 of five-year wealth no worse than the status quo's "
                         f"({ev['cvar10']:.3f} x W0) minus {float(house.get('depth_delta', 0.0)):.2f}")
            fe = float(house.get("forced_eps", 0.0) or 0.0)
            pg = float(house.get("p_goal_min", 0.0) or 0.0)
            M.apply_eps(p_goal_min=(pg if objective != "gbo" and pg > 0 else None), forced_eps=(fe if fe > 0 else None),
                        ret_min=(float(house["ret_min"]) if objective == "liquidity" else None))
            res = lp.solve(M, objective)
            if res.get("x") is None:
                raise RuntimeError("no feasible plan under the current limits: relax a house limit (see the LP log)")
            res, calib = self._calibrate_guards(M, res, objective, sq, ev, house, bkey, B, stress, prefs, progress)
            x = res["x"]
            ins = M.in_sample(x)
            duals = M.duals(x, res.get("y"), res.get("rc"))
            name = "Consensus plan" if role == "consensus" else f"{sh.LENSES[role]['title']} plan"
            plan = M.extract(x, name)
            plan.meta.update({"objective": objective, "label": res.get("label"), "role": role,
                              "prefs": prefs, "stress": stress})
            progress(f"certifying out of sample: {self.n_oos} fresh paths x 3 worlds")
            S = self.paths_for(bkey, B, "oos", stress, self._pi(prefs), house)
            sset = self._sim_settings(house)
            o_pl = sim.simulate(S, plan, self.P, sset)
            o_sq = sim.simulate(S, sq, self.P, sset)
            g = float(house["goal_rate"])
            s_pl, s_sq = metrics.summarize(o_pl, g), metrics.summarize(o_sq, g)
            d = metrics.paired_delta(o_pl, o_sq)
            cl = substitution.change_list(B, plan, sq, S)
            progress("holding cards from the LP's shadow prices")
            cards = substitution.holding_cards(B, duals, prefs, self.P, house, plan)
            counts = cards[cards["card"] != "LIQUID"].groupby("card")["nav_bn"].agg(["size", "sum"]) \
                .to_dict(orient="index")
            summary = {"name": name, "objective": objective, "label": res.get("label"), "p_goal": s_pl["p_goal"],
                       "p_goal_ci": s_pl["p_goal_ci"], "twr_mean": s_pl["twr_mean"], "cvar10": s_pl["cvar10"],
                       "p_red": s_pl["p_red"], "p_revolver": s_pl["p_revolver"], "lcr_min_p5": s_pl["lcr_min_p5"],
                       "d_p_goal": d["d_p_goal"], "d_p_goal_ci": d["d_p_goal_ci"], "stress": stress,
                       "basis": prefs["basis"], "time": time.strftime("%Y-%m-%d %H:%M")}
            out = {"role": role, "objective": objective, "objective_text": sh.OBJECTIVES.get(objective, objective),
                   "label": res.get("label"), "plan": plan.to_dict(), "summary": summary, "metrics": s_pl,
                   "status_quo": s_sq, "delta": d, "in_sample": ins, "change_list": cl, "duals": duals,
                   "card_counts": counts, "solve_log": res["log"], "phi": res.get("phi"), "E_star": res.get("E_star"),
                   "eps": M.eps, "lp_size": {"cols": M.nvar, "rows": M.nrow, "nnz": int(M.A_mat.nnz)},
                   "calibration": calib,
                   "alternatives": substitution.alternatives(B, prefs, self.P, duals),
                   "W0": B.W0, "Wstar": B.Wstar, "use_house": use_house}
            if persist:
                self.plans[role] = {"plan": plan.to_dict(), "summary": summary, "duals": duals}
                self._save_json(f"{role}_plan.json", self.plans[role])
                self.last[(role, "optimize")] = {"cards": cards, "book_key": bkey}
            if keep_paths:
                out["_paths"] = {"plan": o_pl, "status_quo": o_sq}
                out["_cards"] = cards
            return out

    def _calibrate_guards(self, M, res, objective, sq, ev, house, bkey, B, stress, prefs, progress):
        """The house guards must also hold on fresh paths: the plan and the status quo run on the validation set
        (its own seed; never the certification paths). If the plan's worst-10% average of five-year wealth falls
        short of the guard, or its forced-sale probability exceeds the appetite, the LP's guard is tightened by the
        measured gap and the LP re-solved (up to three rounds; an infeasible tightening keeps the last plan)."""
        from .legacy import cvar_lower
        guard = bool(house.get("depth_guard", True))
        fe = float(house.get("forced_eps", 0.0) or 0.0)
        rounds = int(house.get("calibration_rounds", 3))
        calib = []
        if rounds <= 0 or (not guard and fe <= 0):
            return res, calib
        S_val = self.paths_for(bkey, B, "val", stress, self._pi(prefs), house)
        sset = self._sim_settings(house)
        w = S_val.prob / S_val.prob.sum()
        o_sq = sim.simulate(S_val, sq, self.P, sset)
        delta = float(house.get("depth_delta", 0.0))
        ref = cvar_lower((1 + o_sq["twr"]) ** 5, 0.10, w) - delta
        tighten, fe_eff = 0.0, fe
        for it in range(rounds + 1):
            o = sim.simulate(S_val, M.extract(res["x"], "validation"), self.P, sset)
            gap = ref - cvar_lower((1 + o["twr"]) ** 5, 0.10, w) if guard else 0.0
            red = float(w @ o["red"].astype(float))
            calib.append({"round": it, "tail_gap": float(gap), "p_red": red, "tighten": tighten, "forced_eps": fe_eff})
            ok = gap <= 0.002 and (fe <= 0 or red <= fe + 0.002)
            if ok or it == rounds:
                break
            if gap > 0.002:
                tighten += gap
                M.apply_depth_guard(ev["cvar10"], delta - tighten)
            if fe > 0 and red > fe + 0.002:
                fe_eff = max(fe_eff / 2, 0.001)
                M.apply_eps(forced_eps=fe_eff)
            progress(f"validation round {it + 1}: tail short by {gap:.4f}, forced-sale probability {red:.3f}; re-solving")
            new = lp.solve(M, objective)
            if new.get("x") is None:
                calib[-1]["infeasible"] = True
                break
            res = new
        return res, calib

    def holdings(self, role: str) -> dict:
        with self.lock:
            v = self.view(role)
            house = self.house()
            _, B, R = self.book_for(v["prefs"], house)
            pd_ = self.plans.get(role) or {}
            duals = pd_.get("duals")
            plan = planmod.Plan.from_dict(pd_["plan"]) if pd_.get("plan") else None
            cards = substitution.holding_cards(B, duals, v["prefs"], self.P, house, plan)
            return jsonable({"role": role, "has_duals": duals is not None,
                             "rows": substitution.holdings_payload(cards),
                             "alternatives": substitution.alternatives(B, v["prefs"], self.P, duals)})

    def compare(self, include_consensus: bool = True, progress=print, extra_plans: list | None = None) -> dict:
        """Every group's plan, the status quo (with and without the PE program), the consensus plan and any
        extra_plans [(key, Plan, house overrides for its operating rules)] on the IC view, with each group's
        objective tested on every path against the house limits."""
        with self.lock:
            if include_consensus:
                progress("solving the consensus plan: the Strategy objective under every group's limits")
                self.optimize("consensus", "gbo", True, progress=progress)
            v = self.view("ic")
            house = self.house()
            bkey, B, R = self.book_for(v["prefs"], house)
            S = self.paths_for(bkey, B, "oos", v["stress"], self._pi(v["prefs"]), house)
            sset = self._sim_settings(house)
            g = float(house["goal_rate"])
            sq = planmod.status_quo(B, self.P, house, program=True)
            sq0 = planmod.status_quo(B, self.P, house, program=False)
            o_sq = sim.simulate(S, sq, self.P, sset)
            plans = [("status_quo", sq, None), ("no_program", sq0, None)]
            for r in sh.ROLES + ["consensus"]:
                d = self.plans.get(r)
                if d and d.get("plan"):
                    p = planmod.Plan.from_dict(d["plan"])
                    if set(p.sell) - {u.id for u in B.units}:
                        progress(f"{r}: plan units differ from the IC book (different return basis); "
                                 f"its sales are mapped by bucket and part")
                        p.sell = {k: v_ for k, v_ in p.sell.items() if k in {u.id for u in B.units}}
                    plans.append((r, p, None))
            plans += [(k, p, ov) for k, p, ov in (extra_plans or [])]
            rows = []
            for key, p, ov in plans:
                progress(f"IC view: simulating {p.name}")
                o = sim.simulate(S, p, self.P, self._sim_settings({**house, **ov}) if ov else sset)
                s = metrics.summarize(o, g)
                d = metrics.paired_delta(o, o_sq)
                fl = metrics.objective_flags(o, None if key == "status_quo" else o_sq, float(house["lev_cap"]),
                                             float(house["overcommit"]), g)
                cl = substitution.change_list(B, p, sq0, S)
                rows.append({"key": key, "name": p.name, "metrics": _brief(s), "delta": d,
                             "fans": {k: s["fans"][k] for k in ("nav", "reserve", "lev")},
                             "flows": {k: s["flows"][k] for k in ("draw", "dist", "calls", "forced", "rev_draw")},
                             "hist": s["hist"], "r1": cl["r1"], "financing": cl["financing"],
                             "pe_program": cl["pe_program"], "objective": p.meta.get("objective"),
                             "basis": (p.meta.get("prefs") or {}).get("basis"),
                             "objectives": metrics.objective_rates(o, fl, g), "sim_override": ov})
            return {"rows": rows, "view": v, "W0": B.W0, "Wstar": B.Wstar, "house": house}

    def swap(self, role: str, codes: list[str], target: str, progress=print) -> dict:
        with self.lock:
            v = self.view(role)
            house = self.house()
            progress(f"isolating {len(codes)} holdings as a sale unit")
            bkey, B, R = self.book_for(v["prefs"], house, {"swap_codes": sorted(codes)})
            S = self.paths_for(bkey, B, "oos", v["stress"], self._pi(v["prefs"]), house)
            base = planmod.status_quo(B, self.P, house, program=True)
            sw = copy.deepcopy(base)
            sw.name = "Swap"
            proceeds = 0.0
            sold_nav = sold_unf = 0.0
            for k, u in enumerate(B.units):
                if u.part == "swap":
                    sw.sell[u.id] = [1.0, 0.0, 0.0]
                    proceeds += float(S.ubid[0, 0, k] * u.nav0)
                    sold_nav += u.nav0
                    sold_unf += u.unf0
            if target in PRIVATE:
                c = list(sw.commit.get(target, [0.0] * 5))
                c[0] += proceeds
                sw.commit[target] = c
            elif target in sw.liquid:
                sw.liquid[target] = sw.liquid[target] + proceeds
            sset = self._sim_settings(house)
            g = float(house["goal_rate"])
            o_b = sim.simulate(S, base, self.P, sset)
            o_s = sim.simulate(S, sw, self.P, sset)
            sb, ss = metrics.summarize(o_b, g), metrics.summarize(o_s, g)
            return {"role": role, "codes": codes, "target": target, "target_label": BY_ID[target].label,
                    "sold_nav_bn": sold_nav, "sold_unfunded_bn": sold_unf, "proceeds_bn": proceeds,
                    "base": _brief(sb), "swap": _brief(ss), "delta": metrics.paired_delta(o_s, o_b)}


def _brief(s: dict) -> dict:
    keys = ["p_goal", "p_goal_ci", "twr_mean", "twr_q", "cvar10", "cvar5", "cvar1", "p_red", "forced_mean_bn",
            "forced_p99_bn", "p_revolver", "rev_max_p95_bn", "min_reserve_ratio_p5", "lcr_min_p5", "lcr_min_p50",
            "wealth_mean_bn", "shortfall_mean_bn", "by_world", "on_track", "leverage_t0", "debt_t0_bn", "ovc_t0"]
    out = {k: s[k] for k in keys if k in s}
    out["lev_max_p95"] = max(s["fans"]["lev"]["p95"])
    out["debt_p95_bn"] = max(s["fans"]["debt"]["p95"])
    out["ovc_max_p50"] = max(s["fans"]["ovc"]["p50"])
    out["reserve_min_p5_bn"] = min(s["fans"]["reserve"]["p5"])
    return out
