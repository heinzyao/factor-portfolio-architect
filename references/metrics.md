# Drawdown-Focused Metrics

Four ratios chosen together because they triangulate on downside behavior rather than symmetric volatility. Sharpe is deliberately absent: it penalizes upside deviation equally and says nothing about how long a drawdown lasted.

## Martin Ratio (Ulcer Performance Index)

```
Martin = (Rp − Rf) / Ulcer Index

Ulcer Index = sqrt( mean( D_i^2 ) )
where D_i = percentage drawdown from running peak at time i
```

Captures **depth and duration together**. Squaring the drawdown series punishes deep drawdowns disproportionately, and averaging over all periods means a shallow drawdown that lasts three years scores worse than a sharp one that recovers in a quarter.

This is the headline metric for long-horizon investors, because the lived experience of a portfolio is mostly time spent underwater, not annualized standard deviation.

## Sterling Ratio

```
Sterling = Rp / mean( annual max drawdowns )
```

A common variant adds 10% to the denominator (`/ (avg MaxDD + 10%)`), originally to avoid flattering managers with short samples. State which convention is in use — the two are not comparable.

Captures **recurring** drawdown pain. Where Martin looks at the whole underwater curve, Sterling asks how bad a typical bad year is. A strategy with one catastrophic year and nine calm ones scores differently under the two, which is why both are worth reporting.

## Treynor Ratio

```
Treynor = (Rp − Rf) / β
```

Return per unit of **systematic** risk. Rewards diversification that lowers beta without sacrificing return, which makes it the natural metric for judging whether a defensive sleeve is earning its place. A negative-beta asset (long Treasuries in a normal regime) improves Treynor mechanically — note that this can flatter a portfolio in exactly the regimes where the negative beta is unreliable.

Treynor assumes beta is meaningful, so it degrades for portfolios with large non-equity sleeves. Report it, but don't lean on it alone for a heavily diversified design.

## Omega Ratio

```
Omega(θ) = ∫[θ,∞] (1 − F(r)) dr  /  ∫[−∞,θ] F(r) dr
```

Probability-weighted gains above threshold θ divided by probability-weighted losses below it. Typically θ = 0 or the risk-free rate.

Uses the **entire return distribution** — all moments, not just the first two. This is what makes it valuable for portfolios holding assets with skew (gold, long-duration STRIPS, momentum strategies with crash risk). Two portfolios with identical mean and variance can have materially different Omega.

## Estimating these from proxies

Most factor ETFs have short live histories, so these metrics almost always come from reconstructed series. Be explicit about the chain:

1. Map each holding to a long-history proxy index (see `regimes.md`).
2. Build the weighted series with the actual rebalancing frequency — rebalancing changes drawdown paths materially, and an unrebalanced backtest of a rebalancing strategy is measuring the wrong thing.
3. Compute the ratios on the reconstructed series.
4. Present as ranges or approximations, not point estimates to two decimals.

## Presenting honestly

Label the table as estimates in the header, not only in a footnote. When comparing two close variants, state the estimation error — if the metrics move by less than the uncertainty in the inputs, the honest finding is "inside the noise," and reporting a winner anyway is false precision.

Ratios also depend on the assumed risk-free rate, which matters more now than during ZIRP. State it.
