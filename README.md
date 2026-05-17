# AI Programming Cost Calculator / AI编程成本计算器

> 4个问题找到最省钱的AI编程方案 | 12款工具对比 | 6种省钱套餐

## 功能特色

- **交互式问答**: 4步输入你的使用场景，一键获取最优推荐
- **12款工具对比**: Cursor, Copilot, Claude Code, DeepSeek, Windsurf等全面覆盖
- **6种方案推荐**: 从零成本到专业版，总有一款适合你
- **省钱计算**: 精确计算每月/每年费用，直观展示节省金额
- **双模式运行**: CLI交互模式 + 网页版，随心选择

## 价格数据（2026年5月更新）

| 工具 | 月费(CNY) | 类型 | 性价比 |
|------|-----------|------|--------|
| Codeium Free | 0 | IDE补全 | ★★★★★ |
| Trae (字节) | 0 | AI IDE | ★★★★★ |
| DeepSeek V4 API | ~15 | API | ★★★★★ |
| Claude+DeepSeek方案 | ~22 | 终端编程 | ★★★★★ |
| GitHub Copilot | 76 | IDE补全 | ★★★★ |
| Windsurf | 107 | AI IDE | ★★★★ |
| Cursor Pro | 152 | AI IDE | ★★★★ |
| Claude Code Max | 1440 | 终端Agent | ★★ |

## 使用方法

### 方式一：命令行（交互模式）

```bash
pip install rich  # 可选，增强显示效果
python main.py
```

按提示输入4个问题，即可获得推荐方案。

### 方式二：命令行（快速模式）

```bash
python main.py --quick          # 使用默认参数
python main.py --lang Python --hours 4 --project web --budget 200
python main.py --compare        # 查看所有工具对比
python main.py --plans          # 查看所有套餐方案
```

### 方式三：网页版

直接在浏览器打开 `index.html`，零安装、零依赖、离线可用。

## 推荐套餐

| 套餐 | 月费 | 适合人群 |
|------|------|----------|
| 零成本入门 | 0元 | 学生、轻度用户 |
| 极致性价比 | 45元 | 个人开发者 |
| 专业开发者 | 182元 | 全职开发者 |
| 团队协作 | 500元+ | 企业团队 |

## 文件说明

- `main.py` - 入口文件
- `ai_coding_planner.py` - 主程序（CLI交互+推荐引擎）
- `cost_calculator.py` - API成本计算器
- `index.html` - 网页版（单文件，零依赖）
- `product.json` - 产品元数据

## 系统要求

- Python 3.7+
- 可选: rich (pip install rich) 增强终端显示

## License

MIT License

---
*Updated: May 2026 | Author: AI Tools Workshop*
