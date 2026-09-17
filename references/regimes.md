# Historical Regime Analysis

## Why regimes rather than a single backtest

A single 30-year annualized number hides the thing that matters: a diversified factor portfolio and a cap-weighted global index can produce similar long-run returns while behaving completely differently along the way. Regime decomposition shows *when* a design wins and loses, which is what the user actually needs to decide whether they can hold it.

## The regime set

Roughly 1995–2025, adjust the endpoint to the present:

| Regime | Period | Character |
|---|---|---|
| Tech melt-up | 1995–1999 | US large growth dominant, value crushed |
| Dot-com bust | 2000–2002 | Growth collapses, value and small-value strongly positive |
| Commodity/EM/value boom | 2003–2007 | Broad non-US and value leadership, weak dollar |
| Global Financial Crisis | 2007–2009 | Correlations to 1, Treasuries rally hard, gold resilient |
| Post-GFC ZIRP / US growth | 2009–2019 | US mega-cap growth dominance, factor drought |
| COVID crash and recovery | 2020–2021 | Fastest bear then fastest recovery, gold strong |
| Inflation shock | 2022 | Stocks and bonds fall together, gold roughly flat |
| AI concentration | 2023–2025 | Extreme index concentration, US leadership |

Two of these are non-negotiable for an honest analysis. **2000–2002** is where factor tilts earn their keep. **2022** is where the stock-bond correlation assumption breaks. A regime table omitting either is flattering the design.

## Long-history proxies

Most factor ETFs launched recently, so reconstruct with index or long-lived fund proxies:

| Exposure | Proxy options |
|---|---|
| US large blend | S&P 500 TR |
| US large growth | Russell 1000 Growth, S&P 500 Growth |
| US large value | Russell 1000 Value, Fama-French HML-tilted portfolios |
| US large momentum | MSCI USA Momentum, AQR momentum series, Ken French UMD |
| US small value | Russell 2000 Value, S&P 600 Value, DFSVX (long history) |
| Intl developed small value | MSCI EAFE Small Value, DISVX |
| Emerging markets | MSCI EM (from 1988) |
| EM ex-China | MSCI EM ex-China (shorter; note the limitation) |
| Long Treasuries | Bloomberg US Long Treasury, TLT from 2002, Ibbotson LT Govt earlier |
| Extended duration STRIPS | Bloomberg US Treasury STRIPS 20–30yr |
| Gold | LBMA gold PM fix, GLD from 2004 |
| Precious metals basket | Blend LBMA gold/silver/platinum/palladium at fund weights |
| Global equity benchmark | MSCI ACWI (VT launched 2008, so ACWI covers earlier periods) |

Ken French's data library is the authoritative source for factor return series and covers periods no fund does.

## Building the table

- Rows are regimes, columns are the candidate portfolios plus the benchmark.
- Report annualized return **and** max drawdown per regime. Return alone hides the experience.
- Reconstruct with the actual rebalancing frequency. This matters — the rebalancing bonus only appears in a rebalanced series, so an unrebalanced backtest systematically understates a volatility-harvesting design.
- Approximate figures are fine and honest; spurious precision is not. Round to whole percentage points.

## Interpreting for the user

State the pattern plainly, including the unflattering half. A diversified factor-plus-ballast design will typically lag a cap-weighted global index in US-growth-dominated regimes (1995–99, 2009–19, 2023–25) and outperform in value/EM/crisis regimes (2000–02, GFC, 2022). Over the full period the returns are often comparable with smaller drawdowns.

That pattern is the honest sales pitch and the honest warning simultaneously: the design asks the investor to underperform during long, visible, widely-discussed periods of index leadership. Users who aren't told this in advance tend to abandon the strategy at the worst moment, which converts a reasonable design into a realized loss.

## Data cautions

- Index returns exclude fees and, for some series, taxes on distributions. Live results run below index results.
- Survivorship and backfill bias affect long factor series, generally inflating premia.
- Currency basis matters for international series — state whether figures are USD or local.
- Where sources conflict on a figure (this happens with commodity and gold series in particular), prefer the primary source and note the discrepancy rather than silently picking one.
