# Forward Scenario Simulation

## Purpose

Point forecasts of ten-year returns are false precision. Scenarios make the *conditionality* explicit — the useful output is not "this portfolio returns 7%" but "this portfolio returns 7% unless X, in which case 3%, and here is how likely X looks." That framing also gives the user something to monitor.

## A workable scenario set

Four to six named scenarios, spanning the growth/inflation quadrants plus the structural stories that actually drive current debate. A reasonable default set:

| Scenario | Character |
|---|---|
| Productivity/AI boom | Strong real growth, contained inflation, continued index concentration |
| Muddle-through | Trend growth, inflation near but slightly above target, no regime break |
| Sticky inflation / stagflation | Inflation persistently above target with weak growth |
| Fiscal dominance / term-premium shock | Deficits force long yields higher regardless of policy rate |
| Mean reversion to non-US leadership | Valuation gaps close, dollar weakens |
| Deflationary bust | Recession, rate collapse, credit stress |

Adjust to the actual macro debate at the time. Add a domain-specific axis when the portfolio has a concentrated exposure that deserves its own treatment — a China re-rating vs stagnation vs geopolitical-event axis for an EM sleeve, for example. These sub-axes often surface the most important finding.

## Assigning probabilities

Probabilities are judgment, and should be labeled as such. Anchor them where possible: inflation swap markets, Fed funds futures, survey-implied recession probabilities, the spread between forecasters' expected returns.

Avoid the two failure modes — a near-uniform distribution that expresses no view, and a dominant base case at 60%+ that makes the exercise decorative. A defensible spread usually has the base case in the 25–35% range.

## Estimating returns per scenario

Build up from components rather than guessing at the portfolio level:

1. Assign each **asset class** a return under the scenario, informed by published capital market assumptions and the scenario's own logic. Long duration is strongly positive in a deflationary bust and strongly negative in a term-premium shock; gold is the mirror image in the inflation scenarios.
2. Weight up to the portfolio return.
3. Sanity-check across scenarios: no portfolio should win every scenario. If one does, the scenarios aren't spanning enough or the return assumptions are being generous where the design is exposed.

Cross-check the whole grid against the published forecasts you gathered. If your muddle-through case is far above the consensus for the constituent asset classes, something is off.

## The probability-weighted line

Report the weighted expectation, but immediately note the dispersion. The weighted number is the least informative cell in the table — it collapses exactly the conditionality the exercise exists to show. Present it as one row, not as the conclusion.

## Presenting

Scenarios as rows, portfolios plus benchmark as columns, probability in the row label. A final row for the probability-weighted expectation.

Then the interpretive line that matters: identify the scenario where the recommended design *loses* to the benchmark, and say what it would cost. Users deserve to know their downside case before committing, and a recommendation that names its own failure mode is far more credible than one that doesn't.

## Limitations to state

- Scenario returns are model outputs conditioned on judgment, not forecasts.
- Published capital market assumptions differ in horizon (7 vs 10 years), basis (real vs nominal), and methodology. Mixing them without adjustment produces incoherent comparisons — convert to a common basis and say which you used.
- Ten-year windows have historically delivered outcomes outside the range of most contemporaneous scenario sets. The spread should be wide.
- Sequence matters for anyone contributing or withdrawing: the same annualized return with different path produces different terminal wealth. Note this when the user's situation involves cash flows.
