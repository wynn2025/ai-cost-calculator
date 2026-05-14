# AI Programming Cost Calculator v2.1

> 11款AI编程工具成本对比 | 5种省钱套餐 | Markdown/CSV导出 | 按预算推荐

## Quick Start

```bash
# Show all tools comparison table
python ai_cost_compare.py --compare

# Show bundle recommendations
python ai_cost_compare.py --bundles

# Export as Markdown
python ai_cost_compare.py --export md

# Export as CSV
python ai_cost_compare.py --export csv

# Budget recommendation (e.g. 100 CNY/month)
python ai_cost_compare.py --budget 100

# Search specific tool
python ai_cost_compare.py --tool Cursor

# Interactive mode (no args)
python ai_cost_compare.py
```

## Compared Tools (11)

| Tool | Monthly (CNY) | Type | Rating |
|------|--------------|------|--------|
| Augment Code | 0 (FREE) | IDE Plugin | 8.0 |
| Codeium Free | 0 (FREE) | IDE Plugin | 7.8 |
| Trae (ByteDance) | 0 (FREE) | AI IDE | 8.2 |
| Amazon Q Developer | 0 (FREE) | IDE Plugin | 7.5 |
| DeepSeek API | 15 | API | 9.0 |
| DS+Claude Combo | 22 | Combo | 9.3 |
| GitHub Copilot | 76 | IDE Plugin | 8.8 |
| Windsurf Pro | 105 | AI IDE | 8.5 |
| Claude Code Pro | 144 | Terminal AI | 9.0 |
| Cursor Pro | 152 | AI IDE | 9.2 |
| Claude Code Max | 1,440 | Terminal AI | 9.5 |

## Bundle Recommendations

| Bundle | Monthly | Annual | Tools |
|--------|---------|--------|-------|
| Zero Cost | 0 | 0 | Augment + Codeium |
| Minimal | 15 | 180 | DeepSeek API + Codeium |
| Best Value | 22 | 264 | DS+Claude Combo + Trae |
| Professional | 167 | 1,700 | Cursor Pro + DeepSeek API |
| Flagship | 220 | 2,200 | Claude Code Pro + Copilot |

## Features

- **Full comparison table**: Side-by-side cost, type, rating, best use case
- **Monthly + Annual pricing**: See both at a glance
- **Markdown export**: One command generates a publishable comparison document
- **CSV export**: For spreadsheets and data analysis
- **Budget planner**: Input your budget, get ranked recommendations
- **Zero dependencies**: Pure Python standard library only

## Also Included

- `ai_coding_planner.py` - Interactive 4-step recommendation wizard
- `cost_calculator.py` - API token cost calculator (DeepSeek/Claude/GPT)

## License

MIT
