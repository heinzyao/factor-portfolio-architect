# Theory Grounding

Each theory is written with its **dependency** stated — the condition it needs to work. Dependencies are what let you evaluate a proposed change: a modification is good or bad largely according to whether it strengthens or undermines the mechanism the portfolio relies on.

## Fama-French factors (+ momentum)

Expected returns load on market, size, value, profitability, and investment, with momentum as a well-documented addition outside the original model.

Practical points that matter for construction:

- **Value + profitability together** screens out "cheap junk" — the value premium is substantially stronger among profitable firms. Funds built this way (the Avantis and DFA families) are not interchangeable with a plain price-to-book screen.
- **Value and momentum are negatively correlated.** This is the single most useful pairing in factor construction: their drawdowns tend not to coincide, so the combination has a materially better information ratio than either alone. Pairing them is usually a genuine free lunch rather than a bet.
- **Momentum carries crash risk.** Momentum's worst episodes come at sharp reversals off market bottoms (2009 is the canonical case), when the short side rockets and the long side lags. A momentum sleeve needs something that performs in a violent recovery.
- **Factor premia are long-horizon.** Decade-long droughts are within historical norms. A ten-year horizon is roughly the minimum at which factor tilts are a reasonable bet, and framing them as reliable over shorter windows is overselling.

**Dependency:** factor premia persist and the investor holds through the drought. Changes that reduce factor *diversity* (stacking two momentum sleeves, or two small-value sleeves) weaken this more than they appear to, because they concentrate the drought risk.

## Shannon's Demon / volatility harvesting

Geometric return is approximately arithmetic return minus half the variance:

```
g ≈ μ − σ²/2
```

That subtracted term is volatility drag. Rebalancing between volatile, imperfectly correlated sleeves mechanically sells the winner and buys the laggard, converting part of the drag into a **rebalancing bonus**. Shannon's original demonstration used a stock with zero expected drift and cash, rebalanced to 50/50, producing positive compound growth from pure volatility.

**The bonus is maximized when:**
- Sleeve volatility is **high** — low-volatility sleeves have little to harvest.
- Cross-correlation is **low or negative** — this is the binding constraint in practice.
- Expected returns are **similar** — a sleeve that persistently outruns the others turns rebalancing into a drag on return, since you keep selling the winner.
- Returns exhibit **mean reversion** rather than long trends.

**Rebalancing frequency:** semiannual captures most of the available bonus while limiting turnover and tax friction. More frequent rebalancing raises costs and can cut into momentum-driven trends; much less frequent lets allocations drift far enough that the harvest is lost. There is no universal optimum — it depends on the mean-reversion horizon of the sleeves.

**Dependency:** low cross-correlation between sleeves. This is the mechanism to check whenever a holding is swapped. A replacement that is a better fund but more correlated to the rest of the portfolio makes the design *worse*. This is counterintuitive and worth stating explicitly to users, because fund-quality intuitions push the other way.

## Taleb's barbell

Combine an extreme-safety allocation with a small high-convexity allocation, deliberately avoiding the "mediocre middle" of moderate-risk assets. The logic is that risk in the middle is poorly compensated and poorly understood, while the extremes are legible: you know the floor on the safe side and accept capped losses with uncapped upside on the aggressive side.

In practice the safe leg is short-to-long Treasuries and the aggressive leg is concentrated equity or long-duration convexity. Long-duration Treasury STRIPS are interesting because they can serve as the *convex* leg — their payoff in a rate collapse is highly asymmetric.

**Dependency:** the safe leg is actually safe. This broke in 2022, when long Treasuries fell more than 30% and provided no floor at all. A barbell with a duration-heavy safe leg is implicitly a bet against an inflation shock.

## Risk parity / All-Weather

Equalize risk contribution rather than capital across assets mapped to a four-quadrant growth/inflation framework:

| | Inflation rising | Inflation falling |
|---|---|---|
| **Growth rising** | Commodities, gold, EM equity | Equities, corporate credit |
| **Growth falling** | Gold, inflation-linked bonds | Long Treasuries, nominal bonds |

Each quadrant needs coverage, because the framework's premise is that you cannot reliably forecast which one you'll get.

Note that capital weights and risk weights diverge sharply: a 20% allocation to 24-year-duration STRIPS contributes far more risk than 20% to short bonds. Always reason in risk-contribution terms, and say so when the user is thinking in capital terms.

**Dependency:** the stock-bond correlation stays negative. When inflation runs high (empirically above roughly 5%), stock-bond correlation turns positive and the two main sleeves fall together — 2022 being the clean example. This is precisely why gold earns a place as an independent third diversifier: it is not conditional on the same correlation regime.

## Hybrids

Real designs blend these, and the blend is usually where the interest lies. Common combinations:

- **Factor core + convex hedge** — Fama-French equity sleeves with a small long-duration and gold allocation as the barbell's safe leg.
- **Risk-parity/Shannon hybrid** — sleeves chosen for mutual low correlation *and* individually high volatility, so the parity structure also maximizes the harvest. Volatility becomes a feature rather than something to minimize, which reverses the usual intuition about "risky" holdings.
- **Momentum-value parity** — the negatively correlated factor pair, risk-balanced against a ballast sleeve.

When a portfolio is a hybrid, name which mechanism is primary. Change-evaluation needs a primary mechanism to judge against, and hybrids without a stated priority tend to get evaluated incoherently.
