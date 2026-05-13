# AI Programming Cost Planner - AI编程成本计算器

> 根据你的编程场景（语言、编码时长、项目类型、预算），推荐最优AI工具组合方案。
> 用 Rich 库做漂亮终端UI，交互式引导，5分钟找到最适合你的AI编程方案。

## 功能特点

- **个性化推荐** - 根据语言/时长/项目/预算匹配最优工具
- **10+ AI工具数据库** - Cursor/Copilot/Claude Code/DeepSeek/Windsurf/GPT-4o等
- **6套预设方案** - 从零成本到土豪方案，总有一款适合你
- **Rich终端UI** - 彩色表格、进度条、面板，终端也能很好看
- **省钱对比** - 自动计算vs最贵方案的节省金额和百分比
- **无Rich也能用** - `--no-rich`降级为纯文本输出

## 快速开始

### 安装依赖

```bash
pip install rich  # 可选，没有也能运行（纯文本模式）
```

### 方式1：交互式引导

```bash
python ai_coding_planner.py
```

回答4个问题，获取个性化推荐。

### 方式2：快速模式

```bash
python ai_coding_planner.py --quick
```

使用默认参数（Python/4h/后端/200元预算）直接输出推荐。

### 方式3：命令行参数

```bash
python ai_coding_planner.py --lang "JavaScript/TypeScript" --hours 4 --project web --budget 200
```

### 方式4：查看所有工具对比

```bash
python ai_coding_planner.py --compare
```

### 方式5：查看所有方案

```bash
python ai_coding_planner.py --plans
```

## 使用示例

### 示例1：Python后端开发者

```bash
python ai_coding_planner.py --lang Python --hours 4 --project backend --budget 200
```

输出：推荐 Cursor Pro + DeepSeek API，月费182元，vs最贵方案省1410元/月。

### 示例2：学生/轻度用户

```bash
python ai_coding_planner.py --lang Python --hours 1 --project script --budget 0
```

输出：推荐 Codeium Free，完全免费，基础补全够用。

### 示例3：全职全栈开发者

```bash
python ai_coding_planner.py --lang "JavaScript/TypeScript" --hours 5 --project fullstack --budget 500
```

输出：推荐重度AI编程方案，Claude Code(DeepSeek)+Cursor，月费174元。

## 支持的AI工具

| 工具 | 类型 | 月费(元) | 代码质量 | 速度 | 性价比 |
|------|------|---------|---------|------|--------|
| Cursor Pro | IDE | 152 | 9/10 | 9/10 | 7/10 |
| GitHub Copilot | IDE | 76 | 8/10 | 8/10 | 8/10 |
| Claude Code (Max) | 订阅 | 1440 | 10/10 | 8/10 | 3/10 |
| Claude Code (DeepSeek方案) | 订阅 | 22 | 8/10 | 8/10 | 10/10 |
| Windsurf | IDE | 107 | 8/10 | 8/10 | 7/10 |
| DeepSeek API | API | 30 | 8/10 | 7/10 | 10/10 |
| GPT-4o API | API | 110 | 9/10 | 8/10 | 6/10 |
| Codeium Free | 免费 | 0 | 6/10 | 7/10 | 10/10 |
| Cline + DeepSeek | 免费 | 15 | 7/10 | 7/10 | 10/10 |
| Gemini 2.5 Pro | API | 89 | 8/10 | 7/10 | 7/10 |

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--lang` | 编程语言 |
| `--hours` | 每天编码时长 (1/2/4/5) |
| `--project` | 项目类型 (web/backend/mobile/data/script/infra/fullstack) |
| `--budget` | 月预算 (CNY) |
| `--compare` | 查看全部工具对比表 |
| `--plans` | 查看所有推荐方案 |
| `--quick` | 快速模式（默认参数） |
| `--no-rich` | 禁用Rich UI，纯文本输出 |

## 系统要求

- Python 3.6+
- rich（可选，用于美化终端输出）

## License

MIT License

## 相关推广

配合CSDN文章《AI编程省钱指南》一起推广，闲鱼上架9.9元。
