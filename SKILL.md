---
name: factor-portfolio-architect
description: Build and stress-test multi-factor ETF portfolios under hard construction constraints, using Fama-French factors, Shannon's Demon volatility harvesting, Taleb's barbell, and risk parity / All-Weather. Produces constraint-checked portfolio sets, ranked recommendations, drawdown-focused and post-modern metrics (Martin, Sterling, Treynor, Omega, Sortino, CVaR), 30-year historical regime backtests via index proxies, and forward scenario simulations. Also evaluates proposed changes to an existing portfolio — ticker swaps, weight shifts, duration or metals choices. Use this skill whenever the user asks to design, compare, rank, backtest, or modify an investment portfolio of tickers or ETFs, mentions factor investing, risk parity, volatility harvesting, barbell strategies, rebalancing bonuses, downside risk or post-modern portfolio theory, or asks "is portfolio A better than B" / "should I swap X for Y" / "what if I change this weight" — even if they don't name any of these theories explicitly.
---

# Factor Portfolio Architect

Design constraint-bound multi-factor portfolios and evaluate changes to them, with honest separation between genuine risk-adjusted improvements and directional macro bets.

Repo and bilingual overview: <https://github.com/heinzyao/factor-portfolio-architect#readme>

## Two modes

Read the request and pick the mode. Most conversations start in Mode A and then live in Mode B for many turns — the follow-up questions are usually where the real value is, so don't treat them as afterthoughts.

**Mode A — Construct.** The user wants a set of portfolios built from a ticker universe under constraints. Full workflow below.

**Mode B — Evaluate a change.** The user proposes a swap, a weight shift, or asks "is this better?" about a portfolio already on the table. Skip straight to [Evaluating a change](#evaluating-a-change). Do not rebuild everything — answer the actual question.

## Core stance

Three habits separate a useful answer from a plausible-sounding one:

**Distinguish risk-adjusted improvement from directional bet.** Most proposed changes are not free upgrades — they shift the portfolio's exposure toward one macro outcome and away from another. Say which. "This helps in stagflation and hurts in a deflationary recession; you're expressing a view" is more useful than a verdict with no axis. When a change is genuinely lateral, say that too, rather than manufacturing a preference.

**Respect the design's own logic.** If the portfolio is built to harvest volatility through low sleeve correlation, then a change that raises correlation is bad *for this design* even if the new holding is a better fund in isolation. Judge changes against the stated mechanism, not against generic quality.

**Keep the estimate honest about its provenance.** Most factor ETFs have short live histories. Everything historical is proxy-reconstructed and everything forward is a model output. Label estimates as estimates, in the tables, not just in a footer.

## Mode A: Construct

### 1. Parse constraints into a checklist

Extract every hard constraint before designing anything. Typical ones: max ticker count, exactly-one-per-asset-class rules, weight granularity (multiples of 5), minimum distinct factors, excluded benchmark, horizon, risk tolerance, rebalancing frequency. Write them down and validate against them mechanically — see `scripts/check_constraints.py`. A beautiful portfolio that violates a stated rule is a failed answer, and constraint violations are embarrassing precisely because they're checkable.

### 2. Research the current state

Portfolio design is macro-contingent, so gather before building:
- Each candidate ticker's mandate, expense ratio, duration or composition, and factor loadings. Do not rely on memory for expense ratios, durations, or country weights — these change.
- Current macro: policy rate path, inflation trajectory, term premium and long yields, valuation levels (CAPE, forward P/E), the stock-bond correlation regime, gold's level and trend.
- Forward capital market assumptions from several houses (JPMorgan LTCMA, GMO, Research Affiliates, Vanguard, BlackRock, Invesco). Note whether figures are real or nominal and over what horizon — mixing these silently is a common error.

### 3. Design for span, not just quality

When asked for N portfolios, make them genuinely distinct in *character*, not N variations on one idea. Span the range from aggressive growth/momentum through balanced factor barbells to defensive risk-parity designs. Vary the within-class choices (which Treasury duration, which metals vehicle) and have a reason for each — the reason is the interesting part.

Give each portfolio a name and an explicit theory tag so the user can reason about the set.

### 4. Rank and justify the top few

For each top pick, cover: why these tickers, why these weights, how the theories combine, which macro scenarios it's built for, and how the rebalancing frequency interacts with the design's mechanism. Rank order should reflect the user's stated risk tolerance, not the highest expected return. Estimated metrics should include the downside set — see `references/pmpt.md` for MAR choice, Sortino, UPR and CVaR, and for when an optimizer cross-check is worth running against a hand-built design.

### 5. Historical regimes and forward scenarios

Both tables. See `references/regimes.md` for the regime set and proxy mapping, and `references/scenarios.md` for the forward scenario framework. The regime table's job is to show *where the design loses* — a table where the recommendation wins everywhere is a sign the analysis is flattering itself.

## Evaluating a change

This is Mode B, and it has its own shape. The user has a portfolio and proposes a modification.

1. **State the delta precisely.** "That's AVEM 15→20, EDV 20→15 — a 5-point shift from long duration into EM." Naming the actual change prevents both parties from arguing past each other.

2. **Check constraints still hold.** A swap can silently break a one-per-class or ticker-count rule. Also flag if the proposed ticker was outside the user's stated universe — that's a real departure worth naming, not a technicality.

3. **Quantify what moves and what doesn't.** Use a two-column before/after table. Include the estimation error: if the change moves volatility by 0.2pp and your estimates carry ±2pp of uncertainty, say so plainly rather than presenting spurious precision. Many weight tweaks are inside the noise, and telling the user that is the honest answer. Check the higher moments too, not just volatility: a swap that leaves σ flat while pushing skew from −0.4 to −1.1 has changed the portfolio materially (`references/pmpt.md`).

4. **Test against the design's mechanism.** For a volatility-harvesting design, the question is what happens to sleeve correlation and the rebalancing bonus. For a barbell, it's whether convexity survives. For risk parity, it's the four-quadrant coverage. Name the mechanism and check it.

5. **Scenario table.** Which named scenarios does the change help, which does it hurt. Look for ironies — a change made to avoid a risk sometimes concentrates it elsewhere (excluding one country to dodge geopolitical risk while concentrating into that region's supply chain).

6. **Cost, tax, and friction.** Expense ratio deltas, and tax treatment where it differs materially by wrapper (commodity grantor trusts taxed as collectibles, Treasury interest state-tax-exempt). Note when the answer differs between taxable and tax-advantaged accounts — it often flips the recommendation.

7. **Bottom line with flip conditions.** Give a verdict, then state the observable thresholds that would reverse it. Flip conditions are what make the answer durable after the macro moves.

If the change is worse but the user's underlying goal is sound, offer the better way to achieve the same goal within their constraints. "If you want more EM, fund it from the momentum sleeve rather than from duration" is more useful than a flat no.

## Output format

Table-driven and concise. Dense tables, minimal prose padding. Users asking for this kind of analysis are usually comparing many things at once, and prose buries the comparison.

Standard structure for a full build:

```
## TL;DR                      — verdict and top picks, a few bullets
## Key Findings               — numbered, each a claim with a number attached
## Ticker Fundamentals        — table
## Theory Grounding           — brief, only what the rationale actually uses
## The N Portfolios           — one comparison table, all constraints visible
## Top 3 Ranked               — rationale per pick + estimated metrics table
## Historical Regimes         — table, regimes as rows
## Forward Scenarios          — table with probability weights
## Recommendations            — numbered, including flip thresholds
## Caveats                    — short-history funds, estimate provenance, not advice
```

For a Mode B evaluation, compress hard: verdict, before/after table, scenario table, bottom line, caveats. A weight-swap question does not need a full report, and returning one signals you didn't read the question.

Include a brief note that this is educational analysis rather than personalized investment advice. Keep it to a line — repeated disclaimers dilute the actual reasoning.

## Reference files

- `references/metrics.md` — Martin, Sterling, Treynor, Omega: formulas, what each captures, how to estimate them from proxies and how to present them honestly.
- `references/theories.md` — Fama-French factors, Shannon's Demon / volatility harvesting, Taleb barbell, risk parity / All-Weather. Includes what conditions each strategy depends on, which is what makes change-evaluation possible.
- `references/regimes.md` — the 30-year regime set, long-history proxies for short-lived ETFs, and guidance on building the regime table.
- `references/pmpt.md` — post-modern portfolio theory: downside deviation and MAR selection, Sortino and Upside Potential Ratio, skew/kurtosis, Cornish-Fisher modified VaR and CVaR, and the robust optimizers (mean-semivariance, CVaR-LP, resampling, shrinkage, HRP) with guidance on when they're worth running.
- `references/scenarios.md` — forward scenario framework, probability weighting, and how to keep scenario returns internally consistent.

## Validation script

Run `python scripts/check_constraints.py <portfolios.json>` to verify every portfolio against the hard constraints. It checks ticker count, weight sum, weight granularity, non-positive weights, universe membership, one-per-class rules, factor diversity, and benchmark exclusion. Write the portfolio set to JSON as you design it and validate before presenting — catching a violation in the draft is free, catching it after presenting is not. The script prints a per-portfolio pass/fail table; see the docstring for the input schema.

One-per-class and factor-diversity degrade to *skipped* when the JSON omits the `classes` / `factors` maps, so supply both whenever those constraints are in play. The script says `passed the checks that ran` rather than `passed all checks` when anything was skipped, and lists the skipped checks above that line — read the verdict wording, not just the PASS rows.
