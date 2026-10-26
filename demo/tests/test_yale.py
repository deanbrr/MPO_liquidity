"""The Yale-model benchmark's recursions, and the representative paths of the year-by-year view (no data needed)."""
import numpy as np

from tpp import metrics, yale


def test_takahashi_alexander_recursions():
    f = {"rc": [0.25, 0.333, 0.5], "life": 12, "bow": 2.5, "yield": 0.0, "G": 0.10}
    c = yale.fund_curve(f, 12)
    assert abs(c["pic"][1] - 0.25) < 1e-12 and abs(c["pic"][2] - (0.25 + 0.333 * 0.75)) < 1e-12
    assert c["dist"][1] == 0.0                                     # nothing to distribute in year 1
    d2 = (2 / 12) ** 2.5 * c["nav"][1] * 1.10
    assert abs(c["dist"][2] - d2) < 1e-12
    # at the end of the fund's life everything grown is distributed: NAV is only that year's contribution
    c12 = 0.5 * (1 - c["pic"][11])
    assert abs(c["nav"][12] - c12) < 1e-12
    assert all(b >= a - 1e-12 for a, b in zip(c["pic"], c["pic"][1:]))


def test_yield_floor_and_dpi_interpolation():
    f = {"rc": [1.0], "life": 10, "bow": 3.0, "yield": 0.06, "G": 0.08}
    c = yale.fund_curve(f, 3)
    assert abs(c["dist"][2] - c["dist"][1] - 0.06 * c["nav"][1] * 1.08) < 1e-12   # the yield floor binds early
    mid = yale.dpi_at(f, 2.5)
    lo, hi = c["dist"][2] / c["pic"][2], c["dist"][3] / c["pic"][3]
    assert min(lo, hi) - 1e-12 <= mid <= max(lo, hi) + 1e-12


def test_representative_paths():
    n = 50
    rng = np.random.default_rng(1)
    ret = rng.normal(0.08, 0.1, (3 * n, 5))
    out = {"twr": np.exp(np.log1p(ret).mean(1)) - 1, "world": np.repeat(np.arange(3), n), "ret": ret,
           "lcr": np.ones((3 * n, 5)), "macro_y": np.zeros((3 * n, 5), int), "exit_y": np.full((3 * n, 5), 2)}
    for k in ("nav", "reserve", "debt", "lev", "ovc"):
        out[f"r_{k}"] = np.ones((3 * n, 6))
    for k in ("draw", "calls", "dist", "sales", "lr_sold", "rev_draw", "forced"):
        out[f"y_{k}"] = np.zeros((3 * n, 5))
    reps = metrics.rep_paths(out)
    assert len(reps) == 9
    for w in range(3):
        tw = [r["twr"] for r in reps if r["world"] == w]
        assert tw == sorted(tw)                                     # worst 10% <= median <= best 10%
    r = reps[4]
    assert abs(r["cum"][-1] - np.prod(1 + np.array(r["ret"]))) < 1e-12
    assert abs((1 + r["ann"][-1]) ** 5 - r["cum"][-1]) < 1e-9
