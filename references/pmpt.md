# Post-Modern Portfolio Theory

PMPT is the repair kit for the parts of Markowitz that break on real return series. It matters here because this skill already reports drawdown-focused ratios (`metrics.md`) — PMPT is the framework those ratios belong to, and it supplies the optimization and distribution machinery that the ratios alone don't.

## What PMPT replaces

| MPT assumption | Why it fails | PMPT replacement |
|---|---|---|
| Risk = variance | Penalizes upside equally with downside | Downside deviation below a target return |
| Returns are normal | Real series are left-skewed and fat-tailed | Full distribution; skew and kurtosis carried explicitly |
| One risk-free rate anchors everything | Investors have goals, not a universal anchor | MAR (minimum acceptable return), chosen per investor |
| MVO weights are the answer | Weights are hypersensitive to mean estimates | Robust optimizers: CVaR, resampling, shrinkage, HRP |

The practical consequence for portfolio ranking: **two portfolios with the same Sharpe can differ materially once asymmetry is priced in.** Gold, long-duration STRIPS, momentum and managed-futures sleeves are exactly where this bites, and this skill's universes are full of them.

## Downside deviation

```
DD(MAR) = sqrt( (1/n) * Σ min(r_i − MAR, 0)^2 )
```

Two conventions exist for the denominator: divide by `n` (all periods) or by the count of below-MAR periods only. The first is standard and is what Sortino assumes — the second inflates the figure and is not comparable. **State which you used.** Dividing by below-target count only is a common silent error in published tables.

Semi-variance is `DD^2`. For a symmetric distribution, `DD ≈ σ/√2`, which is a useful sanity check: if a sleeve's DD is far above `σ/√2`, the left tail is doing real work.

## Sortino ratio

```
Sortino(MAR) = (Rp − MAR) / DD(MAR)
```

Sortino ranks by return per unit of *shortfall* risk. It is not a substitute for the four ratios in `metrics.md` — it is the fifth, and it slots in next to Martin:

| Ratio | Question it answers |
|---|---|
| Sortino | How much return per unit of below-target volatility? |
| Martin | How much return per unit of time spent underwater? |
| Omega | How do all gains above θ compare to all losses below it? |

Sortino sees the *dispersion* of bad periods; Martin sees their *persistence*. A portfolio can look good on one and poor on the other, and when they disagree that disagreement is the finding — report both and say which one the user's horizon should weight.

## Upside Potential Ratio

```
UPR(MAR) = E[ max(r − MAR, 0) ] / DD(MAR)
```

Expected upside per unit of downside risk. UPR is the metric that keeps PMPT from collapsing into pure defensiveness: a portfolio can minimize DD by holding cash and score terribly on UPR. Worth reporting whenever a proposed change reduces risk, to check the change didn't simply remove the portfolio's engine.

## Higher moments and tail measures

Skewness and excess kurtosis are reported per sleeve, not just per portfolio — portfolio-level moments hide which holding carries the tail.

**Cornish-Fisher modified VaR** adjusts the normal quantile for skew and kurtosis:

```
z_cf = z + (z²−1)S/6 + (z³−3z)K/24 − (2z³−5z)S²/36
mVaR = μ + z_cf · σ
```

where `S` = skew, `K` = excess kurtosis, `z` = normal quantile (−1.645 at 95%). The expansion degrades when `|S| > 2` or `K > 7`; past that, use the empirical quantile and say so.

**CVaR (expected shortfall)** is the mean loss beyond VaR. Prefer it to VaR throughout: it is coherent (sub-additive, so diversification cannot look harmful), and it says how bad the bad case is rather than only where it starts. Report CVaR at 95% alongside max drawdown in the metrics table.

## Optimization beyond mean-variance

| Method | Use when | Cost |
|---|---|---|
| Mean-semivariance | Asymmetric sleeves, MAR is well-defined | Endogenous cosemivariance matrix; needs iteration |
| CVaR optimization (Rockafellar–Uryasev) | Tail control is the objective | Linear program, easy to solve; hungry for scenario data |
| Resampled efficiency (Michaud) | Estimates are noisy — nearly always | Averaged weights, no closed form, patent-adjacent history |
| Shrinkage covariance (Ledoit–Wolf) | Assets ≫ observations | Biased but far lower variance; nearly free, use by default |
| Hierarchical Risk Parity (López de Prado) | Covariance is near-singular or ill-conditioned | No optimality claim; robust and stable out of sample |

For the constrained, coarse-grained portfolios this skill builds (weights in multiples of 5, ≤ N tickers), **full optimization is usually theater.** The constraint grid dominates the optimizer's precision. Use these methods to *check* a hand-built design — does the CVaR-optimal portfolio sit near ours, or somewhere else entirely? — rather than to generate weights. Say when the optimizer and the design disagree, and why.

## Choosing the MAR

The MAR is not a technicality; it changes rankings. Common choices and what they encode:

- **0%** — nominal capital preservation. Flatters long-duration and gold in low-inflation samples.
- **Inflation (CPI)** — real preservation. The honest default for a long-horizon investor.
- **Risk-free rate** — opportunity cost framing; makes Sortino comparable to Sharpe.
- **Liability or spending rate (e.g. 4%)** — goal-based. Use when the user has stated a withdrawal or funding target.

Ask, or state the assumption in the table header. Where the ranking flips between two plausible MARs, that flip is worth a line in the recommendations — it means the verdict is MAR-contingent, not robust.

## Estimation honesty

Downside metrics use only the below-target subsample, so their **effective sample size is roughly half** the nominal one, and semi-variance estimates carry proportionally more error than variance. Three consequences to respect:

1. Monthly data over 30 years gives ~360 points, perhaps 150 below MAR. Sortino differences under ~0.1 are noise.
2. Skew and kurtosis need far more data than mean and variance; kurtosis estimates from under 10 years are close to meaningless.
3. Everything inherits the proxy chain from `regimes.md`. A Sortino computed on a reconstructed series is an estimate of an estimate — label it as such in the table, not in a footnote.

When a proposed change moves Sortino by less than the estimation error, the honest answer is that the change is inside the noise. That answer is a finding, not a failure.

## Presenting PMPT output

Add to the estimated-metrics table as columns, with the MAR stated in the header: `Sortino (MAR=CPI)`, `DD`, `CVaR 95%`, `Skew`, `UPR`. Keep Martin, Sterling, Treynor and Omega — the set is complementary, not redundant.

In Mode B, PMPT earns its place in step 3 (quantify what moves): a swap that leaves σ unchanged but shifts skew from −0.4 to −1.1 has changed the portfolio materially, and the mean-variance view would have missed it entirely. Lead with that when it happens.
