# Factor Portfolio Architect

**[English](#english) | [繁體中文](#繁體中文)**

---

## English

A Claude Code / Claude.ai **skill** for designing constraint-bound multi-factor ETF portfolios and evaluating changes to them — with an honest separation between genuine risk-adjusted improvements and directional macro bets.

> Educational analysis, not personalized investment advice.

### What it does

- Builds N genuinely distinct portfolios from a ticker universe under hard constraints (ticker count, weight granularity, one-per-asset-class, factor diversity, benchmark exclusion).
- Evaluates a proposed change — a ticker swap, a weight shift, a duration or metals choice — without rebuilding everything.
- Produces drawdown-focused and post-modern metrics: Martin, Sterling, Treynor, Omega, Sortino, UPR, CVaR.
- Runs 30-year historical regime backtests via long-history index proxies, plus forward scenario simulations with probability weights.
- Mechanically validates every portfolio against the stated constraints before presenting.

### Two modes

| Mode | When | Output |
|---|---|---|
| **A — Construct** | "Build me N portfolios from this universe" | Full report: fundamentals, N portfolios, top-3 ranked, regime + scenario tables |
| **B — Evaluate a change** | "Should I swap X for Y?" / "Is A better than B?" | Compressed: verdict, before/after table, scenario table, flip conditions |

Most conversations start in Mode A and then live in Mode B for many turns — the follow-up questions are usually where the real value is.

### Core stance

**Distinguish risk-adjusted improvement from directional bet.** Most proposed changes are not free upgrades; they shift exposure toward one macro outcome and away from another. Say which axis.

**Respect the design's own logic.** If a portfolio is built to harvest volatility through low sleeve correlation, a change that raises correlation is bad *for this design* — even if the new fund is better in isolation.

**Keep the estimate honest about its provenance.** Most factor ETFs have short live histories. Everything historical is proxy-reconstructed, everything forward is a model output. Label estimates as estimates, in the tables.

### Theories used

| Theory | Core mechanism |
|---|---|
| Fama-French factors | Size, value, momentum, profitability, investment premia |
| Shannon's Demon | Rebalancing bonus from low-correlation, high-volatility sleeves |
| Taleb barbell | Extreme safety + extreme convexity, nothing in the middle |
| Risk parity / All-Weather | Equal risk contribution across four macro quadrants |
| Post-modern portfolio theory | Downside deviation, MAR, skew/kurtosis, CVaR, robust optimizers |

### Repository layout

```
SKILL.md                      # The skill itself: workflow, output format, core stance
scripts/check_constraints.py  # Mechanical constraint validator
references/
  metrics.md                  # Martin, Sterling, Treynor, Omega — formulas and honest presentation
  theories.md                 # Factor / Shannon / barbell / risk parity, and what each depends on
  regimes.md                  # 30-year regime set and long-history proxies for short-lived ETFs
  pmpt.md                     # Downside deviation, Sortino, UPR, CVaR, robust optimizers
  scenarios.md                # Forward scenario framework and probability weighting
```

### Installation

Clone into your Claude skills directory:

```bash
git clone https://github.com/heinzyao/factor-portfolio-architect.git \
  ~/.claude/skills/factor-portfolio-architect
```

The skill then triggers automatically whenever you ask Claude to design, compare, rank, backtest, or modify a portfolio of tickers — even without naming any of the theories.

### Constraint validator

```bash
python scripts/check_constraints.py portfolios.json
python scripts/check_constraints.py portfolios.json --quiet   # failures only
```

Checks ticker count, weight sum, weight granularity, one-per-class rules, factor diversity, and benchmark exclusion. Prints a per-portfolio pass/fail table. Input schema is documented in the script's docstring. Requires Python 3 only — no dependencies.

Example input:

```json
{
  "constraints": {
    "max_tickers": 5,
    "weight_multiple": 5,
    "weight_sum": 100,
    "min_distinct_factors": 2,
    "excluded_tickers": ["VT"],
    "one_per_class": ["treasury", "metals"]
  },
  "classes": { "SPMO": "us_large", "AVUV": "us_small", "EDV": "treasury", "GLDM": "metals" },
  "factors": { "SPMO": ["momentum"], "AVUV": ["size", "value", "profitability"] },
  "portfolios": [
    { "name": "Barbell", "weights": { "SPMO": 40, "AVUV": 20, "EDV": 25, "GLDM": 15 } }
  ]
}
```

### Example prompts

- "Build me 8 portfolios from SPMO, AVUV, AVDV, AVEM, EDV, VGIT, GLDM, and DBMF. Max 5 tickers each, weights in multiples of 5, exactly one Treasury and one metals holding."
- "Should I swap EDV for VGLT in portfolio 3?"
- "What happens to the rebalancing bonus if I move 5 points from gold into EM?"

### License

MIT

---

## 繁體中文

一個用於 Claude Code / Claude.ai 的 **skill**，用來在硬性限制下設計多因子 ETF 投資組合，並評估對其所做的調整——誠實地區分「真正的風險調整後改善」與「方向性的總經押注」。

> 本專案為教育性質的分析工具，不構成個人化投資建議。

### 功能

- 在硬性限制下（標的數量、權重級距、每類資產只能選一檔、因子分散度、排除基準指數）從指定的標的池建構出 N 個性格真正不同的投資組合。
- 評估提出的調整——換股、權重移動、存續期或貴金屬載具選擇——而不需要整個重做。
- 產出以回撤為核心的後現代績效指標：Martin、Sterling、Treynor、Omega、Sortino、UPR、CVaR。
- 透過長歷史指數代理，執行 30 年歷史情境回測，並附帶機率加權的前瞻情境模擬。
- 在輸出報告前，用程式機械式地驗證每個組合是否符合所有限制條件。

### 兩種模式

| 模式 | 使用時機 | 產出 |
|---|---|---|
| **A — 建構** | 「從這個標的池幫我建 N 個組合」 | 完整報告：標的基本面、N 個組合、前三名排序、歷史情境與前瞻情境表 |
| **B — 評估調整** | 「我該把 X 換成 Y 嗎？」／「A 比 B 好嗎？」 | 精簡輸出：結論、前後對照表、情境表、翻盤條件 |

多數對話從 Mode A 開始，之後長時間停留在 Mode B——後續的追問通常才是真正價值所在。

### 核心立場

**區分風險調整後改善與方向性押注。** 多數提議的調整不是免費升級，而是把曝險往某個總經結果傾斜、遠離另一個。要說清楚是哪個軸向。

**尊重設計本身的邏輯。** 如果組合是靠低相關性的部位來收割波動度，那麼提高相關性的調整對「這個設計」就是壞的——即使新標的單獨來看更好。

**對估計值的來源保持誠實。** 多數因子 ETF 實際存續期很短。所有歷史數據都是代理重建的，所有前瞻數據都是模型輸出。估計值要在表格中就標示為估計值。

### 使用的理論

| 理論 | 核心機制 |
|---|---|
| Fama-French 因子 | 規模、價值、動能、獲利能力、投資傾向的溢酬 |
| 夏農的惡魔 | 由低相關、高波動部位產生的再平衡紅利 |
| 塔雷伯槓鈴 | 極度安全 + 極度凸性，中間什麼都不放 |
| 風險平價／全天候 | 在四個總經象限間均等分配風險貢獻 |
| 後現代投資組合理論 | 下檔離差、MAR、偏度／峰度、CVaR、穩健最佳化 |

### 專案結構

```
SKILL.md                      # skill 本體：工作流程、輸出格式、核心立場
scripts/check_constraints.py  # 機械式限制條件驗證器
references/
  metrics.md                  # Martin、Sterling、Treynor、Omega——公式與誠實呈現方式
  theories.md                 # 因子／夏農／槓鈴／風險平價，以及各自的成立前提
  regimes.md                  # 30 年情境集合，以及短命 ETF 的長歷史代理標的
  pmpt.md                     # 下檔離差、Sortino、UPR、CVaR、穩健最佳化
  scenarios.md                # 前瞻情境框架與機率加權
```

### 安裝

複製到你的 Claude skills 目錄：

```bash
git clone https://github.com/heinzyao/factor-portfolio-architect.git \
  ~/.claude/skills/factor-portfolio-architect
```

之後只要你請 Claude 設計、比較、排序、回測或調整標的組合，這個 skill 就會自動觸發——即使你沒有提到任何理論名稱。

### 限制條件驗證器

```bash
python scripts/check_constraints.py portfolios.json
python scripts/check_constraints.py portfolios.json --quiet   # 只顯示失敗項
```

檢查標的數量、權重加總、權重級距、每類資產只能選一檔的規則、因子分散度，以及基準指數排除。輸出每個組合的通過／失敗表格。輸入格式定義在腳本的 docstring 中。只需要 Python 3，無任何相依套件。

輸入範例：

```json
{
  "constraints": {
    "max_tickers": 5,
    "weight_multiple": 5,
    "weight_sum": 100,
    "min_distinct_factors": 2,
    "excluded_tickers": ["VT"],
    "one_per_class": ["treasury", "metals"]
  },
  "classes": { "SPMO": "us_large", "AVUV": "us_small", "EDV": "treasury", "GLDM": "metals" },
  "factors": { "SPMO": ["momentum"], "AVUV": ["size", "value", "profitability"] },
  "portfolios": [
    { "name": "Barbell", "weights": { "SPMO": 40, "AVUV": 20, "EDV": 25, "GLDM": 15 } }
  ]
}
```

### 使用範例

- 「用 SPMO、AVUV、AVDV、AVEM、EDV、VGIT、GLDM、DBMF 幫我建 8 個組合。每個最多 5 檔，權重是 5 的倍數，公債和貴金屬各只能選一檔。」
- 「組合 3 的 EDV 換成 VGLT 好嗎？」
- 「如果我把 5 個百分點從黃金移到新興市場，再平衡紅利會怎樣？」

### 授權

MIT
