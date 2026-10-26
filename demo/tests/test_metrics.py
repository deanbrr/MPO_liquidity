"""Each group's objective as a pass/fail test per path (synthetic simulator output: no data needed)."""
import numpy as np

from tpp import metrics


def test_objective_flags_and_rates():
    m = 6
    o = {"r_lev": np.array([[1.0] * 6, [1.0] * 5 + [1.2], [1.1] * 6, [1.0] * 6, [1.0] * 6, [1.0] * 6]),
         "r_ovc": np.array([[0.5] * 6] * 5 + [[0.5] * 5 + [0.9]]),
         "red": np.array([False, False, False, True, False, False]),
         "twr": np.array([0.11, 0.12, 0.09, 0.15, 0.10, 0.20]),
         "prob": np.ones(m)}
    ref = {"twr": np.array([0.12, 0.08, 0.11, 0.10, 0.12, 0.05])}
    fl = metrics.objective_flags(o, ref, lev_cap=1.15, overcommit=0.8, goal=0.10)
    bs, liq, aa = (fl & metrics.OBJ_BS) > 0, (fl & metrics.OBJ_LIQ) > 0, (fl & metrics.OBJ_AA) > 0
    assert bs.tolist() == [True, False, True, True, True, False]        # leverage 1.2 and overcommitment 0.9 fail
    assert liq.tolist() == [True, True, True, False, True, True]        # a forced private sale fails
    assert aa.tolist() == [True, True, False, True, True, True]         # only losing a target the status quo hit fails
    r = metrics.objective_rates(o, fl, goal=0.10)
    assert abs(r["p_goal"] - 5 / 6) < 1e-12 and abs(r["p_bs"] - 4 / 6) < 1e-12
    assert abs(r["p_liq"] - 5 / 6) < 1e-12 and abs(r["p_aa"] - 5 / 6) < 1e-12
    assert abs(r["p_all"] - 2 / 6) < 1e-12                               # paths 1 and 5 meet everything


def test_status_quo_never_costs_itself_the_target():
    o = {"r_lev": np.ones((3, 6)), "r_ovc": np.full((3, 6), 0.5), "red": np.zeros(3, bool),
         "twr": np.array([0.05, 0.10, 0.15]), "prob": np.ones(3)}
    fl = metrics.objective_flags(o, None, 1.15, 0.8, 0.10)
    assert ((fl & metrics.OBJ_AA) > 0).all()
