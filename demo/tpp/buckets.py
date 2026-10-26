"""The bucket catalog: one bucket per ER strategy row (Department | Vertical | vehicle).

Each bucket names the prototype segment (examples/mpo_v2/params.json book.segments) that supplies its cash-flow
intensities (calls and distributions by age), reported-NAV lag and factor loadings, plus its liquidity tier:
  reserve   cash and Treasury: the liquidity reserve that absorbs every flow (the floor is set on it)
  liquid    sold within a quarter at market (Global Agg, Global Equities, MAO capital)
  semi      hedge funds: quarterly dealing with gates
  private   closed-end funds, co-investments, JVs and SMAs: sold only through the secondary market at a bid
Loadings B are on the prototype's six factors [equity, credit, rates, oil, exit, vol]. They set co-movement and path
risk; each bucket's mean return in each ER world is set separately by its alpha (tpp.paths), so B never moves means.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Bucket:
    id: str
    department: str
    vertical: str
    vehicle: str
    tier: str
    segment: str | None          # prototype segment for cash flows / loadings (None: no private engine)
    label: str
    B: tuple = ()                # override of the segment's loadings
    idio: float | None = None    # bucket-level idiosyncratic vol (diversified across the bucket's holdings)
    bid_key: str | None = None   # prototype bids.rho key (private buckets)
    pe_program: bool = False     # in scope of the PE sell-down program
    notes: str = ""

    @property
    def er_key(self) -> str:
        return f"{self.department} | {self.vertical} | {self.vehicle}"

    @property
    def private(self) -> bool:
        return self.tier == "private"

    @property
    def is_fund(self) -> bool:
        return self.vehicle == "Fund"


PE, SEC, CS, INF, RE = ("Private Equity", "Secondaries", "Capital Solutions",
                        "Global Infrastructure & Natural Resources", "Real Estate")
GE, PM, MAO = "Global Equities Division", "Public Markets", "Multi-Asset Overlay"

CATALOG: list[Bucket] = [
    Bucket("PE_EU_F", PE, "Buyout - EU", "Fund", "private", "pe_buyout", "PE Buyout EU (funds)", idio=0.03, bid_key="fund", pe_program=True),
    Bucket("PE_EU_C", PE, "Buyout - EU", "Co-Invest", "private", "co_deal", "PE Buyout EU (co-invest)", idio=0.05, bid_key="co", pe_program=True),
    Bucket("PE_US_F", PE, "Buyout - US", "Fund", "private", "pe_buyout", "PE Buyout US (funds)", idio=0.03, bid_key="fund", pe_program=True),
    Bucket("PE_US_C", PE, "Buyout - US", "Co-Invest", "private", "co_deal", "PE Buyout US (co-invest)", idio=0.05, bid_key="co", pe_program=True),
    Bucket("PE_VC_F", PE, "Venture Capital", "Fund", "private", "pe_growth", "Venture Capital (funds)", idio=0.05, bid_key="vc", pe_program=True),
    Bucket("PE_VC_C", PE, "Venture Capital", "Co-Invest", "private", "co_deal", "Venture Capital (co-invest)", B=(1.5, 0.2, 0.0, 0.0, 0.04, 0.0), idio=0.08, bid_key="co", pe_program=True),
    Bucket("SEC_LP_F", SEC, "LP Led", "Fund", "private", "sec_fund", "Secondaries LP-led (funds)", idio=0.03, bid_key="fund"),
    Bucket("SEC_LP_C", SEC, "LP Led", "Co-Invest", "private", "sec_portfolio", "Secondaries LP-led (co-invest)", idio=0.04, bid_key="fund"),
    Bucket("SEC_GP_F", SEC, "GP Led", "Fund", "private", "sec_cv", "Secondaries GP-led (funds)", idio=0.05, bid_key="fund"),
    Bucket("SEC_GP_C", SEC, "GP Led", "Co-Invest", "private", "sec_cv", "Secondaries GP-led (co-invest)", idio=0.07, bid_key="fund"),
    Bucket("CS_CR_F", CS, "Credit", "Fund", "private", "cs_credit", "Capital Solutions Credit (funds)", idio=0.02, bid_key="cs"),
    Bucket("CS_CR_C", CS, "Credit", "Co-Invest", "private", "cs_credit", "Capital Solutions Credit (co-invest)", idio=0.03, bid_key="cs"),
    Bucket("CS_INS_F", CS, "Insurance", "Fund", "private", "cs_credit", "Capital Solutions Insurance (funds)", idio=0.03, bid_key="cs"),
    Bucket("CS_INS_C", CS, "Insurance", "Co-Invest", "private", "cs_credit", "Capital Solutions Insurance (co-invest)", idio=0.04, bid_key="cs"),
    Bucket("INF_EU_F", INF, "Europe", "Fund", "private", "ra_infra_fund", "Infra & NR Europe (funds)", idio=0.03, bid_key="ra_lp_infra"),
    Bucket("INF_EU_C", INF, "Europe", "Co-Invest", "private", "ra_infra_direct", "Infra & NR Europe (co-invest)", idio=0.04, bid_key="ra_direct"),
    Bucket("INF_NA_F", INF, "North America", "Fund", "private", "ra_infra_fund", "Infra & NR N. America (funds)", B=(0.55, 0.0, 0.3, 0.15, 0.02, 0.0), idio=0.03, bid_key="ra_lp_infra", notes="oil loading 0.15 for the energy share"),
    Bucket("INF_NA_C", INF, "North America", "Co-Invest", "private", "ra_infra_direct", "Infra & NR N. America (co-invest)", B=(0.45, 0.0, 0.4, 0.15, 0.01, 0.0), idio=0.04, bid_key="ra_direct"),
    Bucket("RE_F", RE, "Global RE", "Fund", "private", "ra_va_re_fund", "Real Estate (funds)", idio=0.03, bid_key="ra_lp_va"),
    Bucket("RE_C", RE, "Global RE", "Co-Invest", "private", "ra_core_re_direct", "Real Estate (co-invest / JV)", idio=0.04, bid_key="ra_direct"),
    Bucket("HF", PM, "Hedge Funds", "Fund", "semi", "hf_multi", "Hedge Funds", idio=0.02),
    Bucket("MAO_INT", MAO, "Internal Equity Active MAO", "Derivatives", "liquid", None, "MAO Internal (capital)", B=(0.2, 0.0, 0.0, 0.0, 0.0, -0.1), idio=0.03),
    Bucket("MAO_EXT", MAO, "External MAO", "Derivatives", "liquid", None, "MAO External (capital)", B=(0.2, 0.0, 0.0, 0.0, 0.0, -0.1), idio=0.04),
    Bucket("GE_GLOBAL", GE, "Global Equity", "Fund", "liquid", "lo_dm_active", "Global Equity", B=(1.0, 0.0, 0.0, 0.0, 0.0, 0.0), idio=0.01),
    Bucket("GE_DM", GE, "Developed Markets", "Fund", "liquid", "lo_dm_core", "Developed Markets Equity", idio=0.005),
    Bucket("GE_EM", GE, "Emerging Markets", "Fund", "liquid", "lo_em", "Emerging Markets Equity", idio=0.02),
    Bucket("TREASURY", "Treasury", "Treasury", "Fund", "reserve", None, "Treasury", B=(0.0, 0.0, 0.6, 0.0, 0.0, 0.0), idio=0.0),
    Bucket("CASH", "Cash", "Cash", "Fund", "reserve", None, "Cash", B=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), idio=0.0),
    Bucket("AGG", "Global Agg", "Global Agg", "Fund", "liquid", "lo_fi", "Global Agg", idio=0.005),
]

BY_ID = {b.id: b for b in CATALOG}
BY_KEY = {b.er_key: b for b in CATALOG}
IDS = [b.id for b in CATALOG]
PRIVATE = [b.id for b in CATALOG if b.private]
RESERVE = [b.id for b in CATALOG if b.tier == "reserve"]
LIQUID_RISK = [b.id for b in CATALOG if b.tier in ("liquid", "semi")]
SLEEVES = ["GE_DM", "GE_EM", "GE_GLOBAL", "AGG", "TREASURY", "CASH", "MAO_INT", "MAO_EXT"]   # filled from total NAV
FUND_BUCKETS = [b.id for b in CATALOG if b.private and b.is_fund]
COINVEST_BUCKETS = [b.id for b in CATALOG if b.private and not b.is_fund]
DEPARTMENTS = [PE, SEC, CS, INF, RE, PM, GE, MAO, "Treasury", "Cash", "Global Agg"]


def bucket_for(department: str, vertical: str, vehicle: str) -> Bucket:
    key = f"{department} | {vertical} | {vehicle}"
    if key in BY_KEY:
        return BY_KEY[key]
    if vehicle == "Co-Invest":          # departments without a co-invest row (Public Markets, GE) use the fund row
        key2 = f"{department} | {vertical} | Fund"
        if key2 in BY_KEY:
            return BY_KEY[key2]
    raise KeyError(f"no ER bucket for {key}")
