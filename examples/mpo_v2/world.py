"""Build one synthetic world: book -> fusion -> tree -> ledger data -> status-quo LP -> optimizer LP
(SYNTHETIC - NOT ADIC DATA). Deterministic given params.json, so the main process and every worker build the same
world independently."""
from __future__ import annotations

import numpy as np

import optim
from book import build_units, make_book
from common import Params
from fusion import fuse
from model import MPOModel
from prep import prepare
from scenarios import Generator, factor_means
from tree import build_tree, finalize_tree


def headline_variant(P: Params) -> dict:
    return {"alpha_dispersion": P.get("truth_model.alpha_dispersion_main"), "bid_info": P.get("truth_model.bid_info_main"),
            "placebo": False}


def base(P: Params, book_seed=None, variant=None):
    """Generator, factor means, units, book, beliefs and the tree (the tree uses the headline book's status-quo
    statistics so every book shares it)."""
    gen = Generator(P)
    Ef, Ef_w = factor_means(gen, P, np.random.default_rng(P.get("seeds.factor_means")))
    units = build_units(P, Ef)
    hv = headline_variant(P)
    book_h = make_book(P, units, P.get("seeds.book"), hv)
    bel_h = fuse(P, units, book_h)
    W0 = sum(u["nav_econ"] for u in units) + P.get("treasury.cash0")
    wts = np.array([u["nav_econ"] for u in units]) / W0
    b_sq = sum(wts[k] * np.asarray(u["B"]) for k, u in enumerate(units))
    a_sq = float(sum(wts[k] * bel_h[k]["alpha_hat"] for k in range(len(units))))
    tr = finalize_tree(P, gen, build_tree(P, gen, np.random.default_rng(P.get("tree.seed")), b_sq, a_sq))
    if book_seed is None:
        book, bel = book_h, bel_h
    else:
        book = make_book(P, units, book_seed, variant or hv)
        bel = fuse(P, units, book)
    return {"gen": gen, "Ef": Ef, "Ef_w": Ef_w, "units": units, "book": book, "beliefs": bel, "tr": tr,
            "b_sq": b_sq, "a_sq": a_sq}


def build(P: Params, log=None, book_seed=None, variant=None, use_beliefs=True, phase1=True):
    w = base(P, book_seed, variant)
    D = prepare(P, w["units"], w["beliefs"], w["book"], w["gen"], w["tr"], use_beliefs=use_beliefs)
    m0 = MPOModel(D, "B0", log=log)
    m0.set_cost(m0.obj_b0())
    x0, y0, rec0 = m0.run("B0: status-quo funding LP (tree readings)")
    if x0 is None:
        raise RuntimeError(f"B0 LP failed: {rec0['status']}")
    b0 = optim.b0_info(m0, x0)
    m = MPOModel(D, "OPT", b0info=b0, log=log)
    ph = optim.phase1(m, log if log is not None else (lambda s: None)) if phase1 else None
    w.update({"D": D, "m0": m0, "x0": x0, "b0": b0, "m": m, "phase1": ph,
              "slack_ub": ph["slack_ub"] if ph else {s: 0.0 for s in optim.SLACKS}})
    return w


def reset_model(w: dict):
    """Fresh HiGHS instance with the base bounds and the Phase I allowances (deterministic task restarts)."""
    m = w["m"]
    m.h = None
    m.highs()
    ph = w["phase1"]
    for s in optim.SLACKS:
        ii = np.atleast_1d(getattr(m, s)).ravel()
        m.set_col_bounds(ii, 0.0, w["slack_ub"][s] if "slack_ub" in w else 0.0)
    return m
