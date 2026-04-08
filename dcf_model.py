"""
=============================================================
DCF Financial Model — Python Engine
Author  : El Mahdi Mohtam
Version : 1.0
Date    : 2025
=============================================================
⚠️  SECURITY: Uses FICTITIOUS data only.
    Do NOT replace with real company financials.
=============================================================
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# MODEL ASSUMPTIONS (All fictitious)
# ─────────────────────────────────────────────
ASSUMPTIONS = {
    "company_name":      "IndustroCo SA (FICTITIOUS)",
    "currency":          "MAD",
    "revenue_base":      50_000_000,   # Year 0 revenue
    "revenue_growth":    0.08,         # 8% annual growth
    "ebit_margin":       0.15,         # 15%
    "tax_rate":          0.30,         # 30% (Moroccan IS)
    "capex_pct":         0.05,         # 5% of revenue
    "da_pct":            0.03,         # D&A as % of revenue
    "nwc_change_pct":    0.01,         # Change in NWC as % of revenue
    "wacc":              0.10,         # 10%
    "terminal_growth":   0.02,         # 2% perpetuity growth
    "net_debt":          5_000_000,    # Net debt (fictitious)
    "shares_outstanding": 1_000_000,  # Shares (fictitious)
    "projection_years":  5,
}


def build_income_statement(a: dict) -> pd.DataFrame:
    """Project P&L for N years."""
    years = range(1, a["projection_years"] + 1)
    data = []

    for y in years:
        revenue = a["revenue_base"] * ((1 + a["revenue_growth"]) ** y)
        ebit    = revenue * a["ebit_margin"]
        nopat   = ebit * (1 - a["tax_rate"])
        da      = revenue * a["da_pct"]
        capex   = revenue * a["capex_pct"]
        d_nwc   = revenue * a["nwc_change_pct"]
        fcff    = nopat + da - capex - d_nwc

        data.append({
            "Year":    y,
            "Revenue": round(revenue),
            "EBIT":    round(ebit),
            "NOPAT":   round(nopat),
            "D&A":     round(da),
            "CapEx":   round(capex),
            "ΔNWC":    round(d_nwc),
            "FCFF":    round(fcff),
        })

    return pd.DataFrame(data).set_index("Year")


def calculate_dcf(df: pd.DataFrame, a: dict) -> dict:
    """Discount FCFFs and compute valuation."""
    wacc = a["wacc"]
    g    = a["terminal_growth"]

    # PV of each FCFF
    pv_fcffs = [
        df.loc[y, "FCFF"] / ((1 + wacc) ** y)
        for y in df.index
    ]
    sum_pv_fcff = sum(pv_fcffs)

    # Terminal value (Gordon Growth)
    last_fcff    = df.loc[df.index[-1], "FCFF"]
    terminal_val = last_fcff * (1 + g) / (wacc - g)
    pv_terminal  = terminal_val / ((1 + wacc) ** len(df))

    enterprise_value = sum_pv_fcff + pv_terminal
    equity_value     = enterprise_value - a["net_debt"]
    price_per_share  = equity_value / a["shares_outstanding"]

    return {
        "PV of FCFFs":        round(sum_pv_fcff),
        "Terminal Value":     round(terminal_val),
        "PV Terminal Value":  round(pv_terminal),
        "Enterprise Value":   round(enterprise_value),
        "Net Debt":           a["net_debt"],
        "Equity Value":       round(equity_value),
        "Price Per Share":    round(price_per_share, 2),
        "TV % of EV":         f"{pv_terminal / enterprise_value:.1%}",
    }


def sensitivity_analysis(a: dict, df: pd.DataFrame) -> pd.DataFrame:
    """WACC vs Terminal Growth sensitivity table."""
    wacc_range = [w / 100 for w in range(8, 14)]         # 8% to 13%
    growth_range = [g / 100 for g in range(1, 5)]         # 1% to 4%

    rows = {}
    for wacc in wacc_range:
        row = {}
        for g in growth_range:
            last_fcff = df.loc[df.index[-1], "FCFF"]
            tv = last_fcff * (1 + g) / (wacc - g)
            pv_tv = tv / ((1 + wacc) ** len(df))
            pv_fcffs = sum(df.loc[y, "FCFF"] / ((1 + wacc) ** y) for y in df.index)
            ev = pv_fcffs + pv_tv
            equity = ev - a["net_debt"]
            row[f"g={g:.0%}"] = round(equity / a["shares_outstanding"], 0)
        rows[f"WACC={wacc:.0%}"] = row

    return pd.DataFrame(rows).T


def format_number(n: float) -> str:
    """Format large numbers with M suffix."""
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.2f}M {ASSUMPTIONS['currency']}"
    return f"{n:,.0f} {ASSUMPTIONS['currency']}"


def print_report(df: pd.DataFrame, valuation: dict, sensitivity: pd.DataFrame):
    """Print full DCF report to console."""
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  DCF VALUATION REPORT")
    print(f"  Company : {ASSUMPTIONS['company_name']}")
    print(f"  Date    : 2025")
    print(f"{sep}\n")

    print("📈 PROJECTED FREE CASH FLOWS (FCFF)")
    print("-" * 60)
    print(df[["Revenue", "EBIT", "NOPAT", "FCFF"]].to_string())
    print()

    print("💰 VALUATION SUMMARY")
    print("-" * 60)
    for k, v in valuation.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            print(f"  {k:<25}: {format_number(v)}")
        else:
            print(f"  {k:<25}: {v}")
    print()

    print("🔍 SENSITIVITY — Equity Value per Share (MAD)")
    print("   (WACC vs Terminal Growth Rate)")
    print("-" * 60)
    print(sensitivity.to_string())
    print(f"\n{sep}\n")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    a = ASSUMPTIONS

    df         = build_income_statement(a)
    valuation  = calculate_dcf(df, a)
    sensitivity = sensitivity_analysis(a, df)

    print_report(df, valuation, sensitivity)

    # Optional: export to CSV
    df.to_csv("outputs/projected_fcff.csv")
    pd.DataFrame([valuation]).to_csv("outputs/valuation_summary.csv", index=False)
    sensitivity.to_csv("outputs/sensitivity_table.csv")
    print("✅ Outputs saved to /outputs/")
