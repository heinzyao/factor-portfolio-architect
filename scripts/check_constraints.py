#!/usr/bin/env python3
"""
Validate a set of portfolios against hard construction constraints.

Constraint violations are cheap to catch here and expensive to catch after
presenting, so run this on the draft before writing anything up.

Usage:
    python check_constraints.py portfolios.json
    python check_constraints.py portfolios.json --quiet   # only show failures

Input schema (JSON):
{
  "constraints": {
    "max_tickers": 5,
    "weight_multiple": 5,
    "weight_sum": 100,
    "min_distinct_factors": 2,
    "excluded_tickers": ["VT"],
    "one_per_class": ["treasury", "metals"],
    "allowed_universe": ["SPMO", "AVUV", "..."]
  },
  "classes": {
    "SPMO": "us_large", "AVUV": "us_small", "EDV": "treasury",
    "GLDM": "metals", "...": "..."
  },
  "factors": {
    "SPMO": ["momentum"],
    "AVUV": ["size", "value", "profitability"],
    "...": ["..."]
  },
  "portfolios": [
    {
      "name": "Shannon's Demon Vol-Harvest",
      "theory": "risk-parity / Shannon hybrid",
      "holdings": {"SPMO": 30, "AVUV": 20, "AVEM": 15, "EDV": 20, "GLTR": 15}
    }
  ]
}

Only "portfolios" and "holdings" are strictly required; every check whose
supporting data is absent is skipped and reported as such, so a partial
config still gives useful output.
"""

import argparse
import json
import sys
from collections import Counter

# Equity classes -- used to decide which holdings count toward factor diversity.
EQUITY_CLASS_HINTS = ("large", "small", "mid", "intl", "international",
                      "emerging", "em", "equity", "stock")


def is_equity_class(class_name):
    if not class_name:
        return False
    lowered = class_name.lower()
    return any(hint in lowered for hint in EQUITY_CLASS_HINTS)


def check_portfolio(portfolio, constraints, classes, factors):
    """Return (list_of_failures, list_of_skipped_checks) for one portfolio."""
    failures = []
    skipped = []

    holdings = portfolio.get("holdings", {})
    if not holdings:
        return ["no holdings specified"], skipped

    tickers = list(holdings)
    weights = list(holdings.values())

    # --- ticker count ---
    max_tickers = constraints.get("max_tickers")
    if max_tickers is not None and len(tickers) > max_tickers:
        failures.append(
            f"{len(tickers)} tickers exceeds max of {max_tickers}"
        )

    # --- weights sum ---
    target_sum = constraints.get("weight_sum", 100)
    actual_sum = sum(weights)
    if abs(actual_sum - target_sum) > 1e-9:
        failures.append(f"weights sum to {actual_sum}, expected {target_sum}")

    # --- weight granularity ---
    multiple = constraints.get("weight_multiple")
    if multiple:
        offenders = [
            f"{t}={w}" for t, w in holdings.items()
            if abs(w % multiple) > 1e-9
        ]
        if offenders:
            failures.append(
                f"weights not multiples of {multiple}: {', '.join(offenders)}"
            )

    # --- non-positive weights ---
    nonpositive = [f"{t}={w}" for t, w in holdings.items() if w <= 0]
    if nonpositive:
        failures.append(f"non-positive weights: {', '.join(nonpositive)}")

    # --- excluded tickers ---
    excluded = set(constraints.get("excluded_tickers", []))
    hit = excluded.intersection(tickers)
    if hit:
        failures.append(f"contains excluded ticker(s): {', '.join(sorted(hit))}")

    # --- universe membership ---
    universe = constraints.get("allowed_universe")
    if universe:
        outside = [t for t in tickers if t not in set(universe)]
        if outside:
            failures.append(
                f"outside stated universe: {', '.join(sorted(outside))}"
            )

    # --- one-per-class rules ---
    one_per = constraints.get("one_per_class", [])
    if one_per:
        if not classes:
            skipped.append("one_per_class (no 'classes' map provided)")
        else:
            counts = Counter(
                classes.get(t) for t in tickers if classes.get(t)
            )
            unmapped = [t for t in tickers if t not in classes]
            if unmapped:
                skipped.append(
                    f"class checks for unmapped ticker(s): {', '.join(sorted(unmapped))}"
                )
            for required_class in one_per:
                n = counts.get(required_class, 0)
                if n != 1:
                    failures.append(
                        f"expected exactly 1 '{required_class}' holding, found {n}"
                    )

    # --- factor diversity across equity holdings ---
    min_factors = constraints.get("min_distinct_factors")
    if min_factors:
        if not factors:
            skipped.append("min_distinct_factors (no 'factors' map provided)")
        else:
            equity_tickers = [
                t for t in tickers
                if not classes or is_equity_class(classes.get(t))
            ]
            distinct = set()
            for t in equity_tickers:
                distinct.update(factors.get(t, []))
            if len(distinct) < min_factors:
                failures.append(
                    f"only {len(distinct)} distinct equity factor(s) "
                    f"({', '.join(sorted(distinct)) or 'none'}), "
                    f"need {min_factors}"
                )

    return failures, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Validate portfolios against construction constraints."
    )
    parser.add_argument("config", help="path to portfolios JSON")
    parser.add_argument("--quiet", action="store_true",
                        help="only print portfolios that fail")
    args = parser.parse_args()

    try:
        with open(args.config) as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.exit(f"error: file not found: {args.config}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: invalid JSON in {args.config}: {exc}")

    constraints = data.get("constraints", {})
    classes = data.get("classes", {})
    factors = data.get("factors", {})
    portfolios = data.get("portfolios", [])

    if not portfolios:
        sys.exit("error: no portfolios found in config")

    all_skipped = set()
    n_pass = 0
    lines = []

    for i, portfolio in enumerate(portfolios, start=1):
        name = portfolio.get("name", f"portfolio {i}")
        failures, skipped = check_portfolio(
            portfolio, constraints, classes, factors
        )
        all_skipped.update(skipped)

        if failures:
            lines.append(f"FAIL  {name}")
            for f in failures:
                lines.append(f"        - {f}")
        else:
            n_pass += 1
            if not args.quiet:
                holdings = portfolio.get("holdings", {})
                summary = " / ".join(f"{t} {w}" for t, w in holdings.items())
                lines.append(f"PASS  {name}")
                lines.append(f"        {summary}")

    print("\n".join(lines))
    print()

    # Skipped checks go ABOVE the verdict on purpose. Anyone who reads the
    # bottom line and stops there must not be able to mistake a partial run
    # for a complete one — and the verdict itself says which it was.
    if all_skipped:
        print("Skipped checks (missing supporting data):")
        for s in sorted(all_skipped):
            print(f"  - {s}")
        print()

    scope = "the checks that ran" if all_skipped else "all checks"
    print(f"{n_pass}/{len(portfolios)} portfolios passed {scope}.")

    sys.exit(0 if n_pass == len(portfolios) else 1)


if __name__ == "__main__":
    main()
