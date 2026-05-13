# AI API Cost Calculator - LLM API费用计算与对比工具

> 一键对比10+主流大模型API的费用，帮你在AI编程时代选对工具、省大钱。

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 为什么需要这个工具？

ChatGPT、Claude、DeepSeek、Gemini...大模型越来越多，价格差异巨大！
- Claude 4 Opus：$15/M输入token
- DeepSeek-V4：$0.27/M输入token
- **差价55倍！**

用错模型，一年多花几万块。这个工具帮你精确计算、对比各模型费用。

## 功能特点

- **10+模型对比** - DeepSeek/GPT-4o/Claude 4/Gemini 2.5/Qwen3/Llama 4等
- **三种使用频率** - 按小时/每天/每周/每月计算
- **可视化图表** - 自动生成对比柱状图
- **交互模式** - 引导式输入，新手友好
- **快速模式** - 一键输出默认对比
- **JSON导出** - 方便集成到其他工具

## 快速开始

### 安装（图表功能可选）

```bash
pip install matplotlib  # 可选，不要图表也能用
```

### 1. 快速对比

```bash
python main.py --quick
```

输出示例：
```
======================================================================
  API Cost Comparison Report
  Tokens/call: 50,000 | Freq: daily | I/O: 60/40
======================================================================
Model                       Per Call    Monthly       Annual
----------------------------------------------------------------------
DeepSeek-V4 (cache)          $0.0371    $1.11       $13.35
DeepSeek-V4                  $0.1428    $4.28       $51.42
Llama 4 Maverick             $0.1240    $3.72       $44.64
Qwen3-235B                   $0.3100    $9.30      $111.60
Gemini 2.5 Flash             $0.1860    $5.58       $66.96
GPT-4o                       $5.5000  $165.00     $1980.00  <-- CHEAPEST
Claude 4 Sonnet              $9.3000  $279.00     $3348.00
Gemini 2.5 Pro               $4.7500  $142.50     $1710.00
----------------------------------------------------------------------
```

### 2. 自定义参数

```bash
# 每次调用10万token，每周一次
python main.py --tokens 100000 --freq weekly

# 对比所有模型
python main.py --tokens 50000 --freq daily --all --chart

# 指定模型
python main.py --tokens 100000 --freq monthly --models "DeepSeek-V4" "GPT-4o" "Claude 4 Sonnet"
```

## 使用示例

### 示例1：团队月度成本预估

```bash
python main.py --tokens 200000 --freq hourly --chart --output team_cost
```
假设每小时自动调用一次20万token的API，生成年度成本报告和图表。

### 示例2：选出性价比最高的模型

```bash
python main.py --quick --json
```
快速模式+JSON输出，方便脚本化处理。

### 示例3：项目预算规划

```bash
python main.py --tokens 50000 --freq daily --all
```
每日5万token调用量，对比全部10个模型的年度费用。

## 支持的模型

| 模型 | 输入价格/M tokens | 输出价格/M tokens | 上下文 |
|------|-------------------|-------------------|--------|
| DeepSeek-V4 | $0.27 | $1.10 | 128K |
| DeepSeek-V4 (cache) | $0.07 | $0.28 | 128K |
| GPT-4o | $2.50 | $10.00 | 128K |
| GPT-4o-mini | $0.15 | $0.60 | 128K |
| Claude 4 Sonnet | $3.00 | $15.00 | 200K |
| Claude 4 Opus | $15.00 | $75.00 | 200K |
| Gemini 2.5 Pro | $1.25 | $10.00 | 1M |
| Gemini 2.5 Flash | $0.15 | $0.60 | 1M |
| Qwen3-235B | $0.50 | $2.00 | 128K |
| Llama 4 Maverick | $0.20 | $0.80 | 1M |

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--quick` | 快速模式（50K tokens, daily） |
| `--tokens N` | 每次调用的token数量 |
| `--freq` | 调用频率: hourly/daily/weekly/monthly |
| `--chart` | 生成对比图表 |
| `--json` | 导出JSON格式 |
| `--all` | 对比所有模型 |
| `--models` | 指定模型列表 |
| `--output` | 输出文件路径 |

## 定价

**免费版**: 命令行基础功能
**付费版**: 29元（含可视化图表+JSON导出+未来新增模型）

适合：AI应用开发者、技术团队负责人、独立开发者、API重度用户

## 系统要求

- Python 3.6+
- matplotlib（可选，用于图表生成）

## License

MIT License
