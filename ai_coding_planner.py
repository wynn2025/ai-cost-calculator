#!/usr/bin/env python3
"""
AI Programming Cost Planner - AI编程成本计算器
根据用户使用场景，推荐最优AI工具组合方案并估算月费用。

Author: AI Tools Workshop
Version: 1.0.0
License: MIT
"""

import sys
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.rule import Rule
    from rich.text import Text
    from rich.columns import Columns
    from rich.layout import Layout
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# ============================================================
# 数据定义
# ============================================================

@dataclass
class AITool:
    """AI编程工具"""
    name: str
    category: str  # "ide", "api", "subscription", "free"
    price_cny: float  # 月费(元)
    price_usd: float  # 月费(美元)
    features: List[str]
    languages: List[str]  # 支持的语言，空=全支持
    project_types: List[str]  # 适合的项目类型，空=全适合
    code_quality: int  # 1-10
    speed: int  # 1-10
    cost_efficiency: int  # 1-10
    context_window: str
    description: str

TOOLS_DB = [
    AITool(
        name="Cursor Pro",
        category="ide",
        price_cny=152, price_usd=20,
        features=["智能补全", "代码生成", "代码解释", "多模型切换", "项目级理解"],
        languages=[], project_types=["web", "mobile", "backend", "data", "script"],
        code_quality=9, speed=9, cost_efficiency=7,
        context_window="128K-200K",
        description="最强AI IDE，内置GPT-4o/Claude，Tab补全体验极佳"
    ),
    AITool(
        name="GitHub Copilot",
        category="ide",
        price_cny=76, price_usd=10,
        features=["行内补全", "Chat", "CLI助手", "PR摘要", "企业版可用"],
        languages=[], project_types=["web", "backend", "script", "devops"],
        code_quality=8, speed=8, cost_efficiency=8,
        context_window="128K",
        description="GitHub官方AI助手，与VS Code深度集成，企业首选"
    ),
    AITool(
        name="Claude Code (Max)",
        category="subscription",
        price_cny=1440, price_usd=200,
        features=["终端AI编程", "全项目理解", "自主编辑", "Git集成", "代码审查"],
        languages=[], project_types=["web", "backend", "data", "script", "infra"],
        code_quality=10, speed=8, cost_efficiency=3,
        context_window="200K",
        description="最强自主编程AI，独立完成复杂项目，但价格昂贵"
    ),
    AITool(
        name="Claude Code (DeepSeek方案)",
        category="subscription",
        price_cny=22, price_usd=3,
        features=["终端AI编程", "DeepSeek V4驱动", "成本降17倍", "开源方案"],
        languages=[], project_types=["web", "backend", "data", "script", "infra"],
        code_quality=8, speed=8, cost_efficiency=10,
        context_window="128K",
        description="用DeepSeek V4替代Claude，保留终端AI编程体验，月费仅3美元"
    ),
    AITool(
        name="Windsurf",
        category="ide",
        price_cny=107, price_usd=15,
        features=["AI IDE", "Cascade流", "多文件编辑", "上下文理解"],
        languages=[], project_types=["web", "mobile", "backend", "script"],
        code_quality=8, speed=8, cost_efficiency=7,
        context_window="128K",
        description="Codeium出品AI IDE，Cascade功能适合多文件修改场景"
    ),
    AITool(
        name="DeepSeek API",
        category="api",
        price_cny=30, price_usd=4,
        features=["API调用", "高性价比", "128K上下文", "代码能力强"],
        languages=[], project_types=["backend", "data", "script", "infra"],
        code_quality=8, speed=7, cost_efficiency=10,
        context_window="128K",
        description="性价比最高的代码API，适合自建工具链和自动化"
    ),
    AITool(
        name="GPT-4o API",
        category="api",
        price_cny=110, price_usd=15,
        features=["API调用", "多模态", "生态完善", "文档丰富"],
        languages=[], project_types=["web", "backend", "data", "script"],
        code_quality=9, speed=8, cost_efficiency=6,
        context_window="128K",
        description="OpenAI旗舰API，生态最完善，文档最丰富"
    ),
    AITool(
        name="Codeium Free",
        category="free",
        price_cny=0, price_usd=0,
        features=["免费补全", "Chat", "多语言支持", "VS Code插件"],
        languages=[], project_types=["web", "script", "backend"],
        code_quality=6, speed=7, cost_efficiency=10,
        context_window="32K",
        description="免费AI补全工具，基础功能够用，适合轻度用户"
    ),
    AITool(
        name="Cline + DeepSeek",
        category="free",
        price_cny=15, price_usd=2,
        features=["VS Code插件", "自主编程", "开源", "DeepSeek驱动"],
        languages=[], project_types=["web", "backend", "script"],
        code_quality=7, speed=7, cost_efficiency=10,
        context_window="128K",
        description="开源VS Code插件+DeepSeek API，低成本自主编程方案"
    ),
    AITool(
        name="Gemini 2.5 Pro",
        category="api",
        price_cny=89, price_usd=12,
        features=["超长上下文1M", "代码生成", "多模态", "Google生态"],
        languages=[], project_types=["web", "backend", "data", "infra"],
        code_quality=8, speed=7, cost_efficiency=7,
        context_window="1M",
        description="Google旗舰模型，百万token上下文，适合大型项目分析"
    ),
]

# 方案模板
PLAN_TEMPLATES = [
    {
        "name": "零成本入门方案",
        "target": "学生/个人开发者，偶尔写代码",
        "tools": ["Codeium Free"],
        "total_cny": 0,
        "total_usd": 0,
        "tip": "完全免费，基础补全够用。后续可升级到付费工具。"
    },
    {
        "name": "极致性价比方案",
        "target": "独立开发者，每天编码2-4小时",
        "tools": ["Cline + DeepSeek", "DeepSeek API"],
        "total_cny": 45,
        "total_usd": 6,
        "tip": "开源+DeepSeek API组合，功能接近Cursor，月费不到50元。"
    },
    {
        "name": "专业开发者方案",
        "target": "全职开发者，追求效率",
        "tools": ["Cursor Pro", "DeepSeek API"],
        "total_cny": 182,
        "total_usd": 24,
        "tip": "Cursor处理日常编码，DeepSeek API处理批量/自动化任务。"
    },
    {
        "name": "团队协作方案",
        "target": "3-10人开发团队",
        "tools": ["GitHub Copilot", "DeepSeek API", "GPT-4o API"],
        "total_cny": 196,
        "total_usd": 29,
        "tip": "Copilot统一团队体验，API处理CI/CD和自动化。按人头算。"
    },
    {
        "name": "重度AI编程方案",
        "target": "AI-first开发者，全AI辅助编程",
        "tools": ["Claude Code (DeepSeek方案)", "Cursor Pro"],
        "total_cny": 174,
        "total_usd": 23,
        "tip": "DeepSeek驱动的Claude Code做主力编程，Cursor做快速补全。月费仅23美元！"
    },
    {
        "name": "土豪方案（原版Claude Code）",
        "target": "不差钱，追求极致体验",
        "tools": ["Claude Code (Max)", "Cursor Pro"],
        "total_cny": 1592,
        "total_usd": 220,
        "tip": "最强AI编程组合。但如果换成DeepSeek方案，月省1400元！"
    },
]


# ============================================================
# 核心计算引擎
# ============================================================

PROGRAMMING_LANGUAGES = [
    "Python", "JavaScript/TypeScript", "Java", "Go", "Rust",
    "C/C++", "PHP", "Ruby", "Swift/Kotlin", "其他"
]

PROJECT_TYPES = [
    ("web", "Web前端开发"),
    ("backend", "后端/API开发"),
    ("mobile", "移动端开发"),
    ("data", "数据分析/ML"),
    ("script", "脚本/自动化"),
    ("infra", "基础设施/DevOps"),
    ("fullstack", "全栈开发"),
]

CODING_HOURS_OPTIONS = [
    (1, "不到1小时（轻度）"),
    (2, "1-3小时（中度）"),
    (4, "4-6小时（重度）"),
    (5, "6小时+（全职）"),
]

BUDGET_OPTIONS = [
    (0, "零成本（只用免费工具）"),
    (50, "50元以内（极致省钱）"),
    (200, "50-200元（性价比优先）"),
    (500, "200-500元（体验优先）"),
    (9999, "不限预算（追求最好）"),
]


def match_tools(lang: str, proj_type: str, hours: int, budget: int) -> List[Tuple[AITool, int]]:
    """根据用户场景匹配工具，返回 (工具, 匹配分) 列表"""
    scored = []
    for tool in TOOLS_DB:
        if tool.price_cny > budget > 0:
            continue
        score = 0
        # 编码时长权重
        if hours <= 1:
            score += tool.cost_efficiency * 3
        elif hours <= 3:
            score += (tool.cost_efficiency + tool.code_quality) * 2
        else:
            score += tool.code_quality * 3 + tool.speed * 2
        # 预算匹配
        if budget == 0 and tool.price_cny == 0:
            score += 20
        elif budget <= 50 and tool.price_cny <= 50:
            score += 10
        elif budget <= 200 and tool.price_cny <= 200:
            score += 5
        # 项目类型匹配
        if not tool.project_types or proj_type in tool.project_types:
            score += 10
        # IDE类工具在重度场景加分
        if hours >= 4 and tool.category == "ide":
            score += 5
        scored.append((tool, score))
    scored.sort(key=lambda x: -x[1])
    return scored


def recommend_plans(hours: int, budget: int) -> List[dict]:
    """根据场景推荐方案"""
    plans = []
    for plan in PLAN_TEMPLATES:
        total = sum(t.price_cny for t in TOOLS_DB if t.name in plan["tools"])
        if total <= budget or budget >= 9999:
            plans.append(plan)
    return plans


def calc_savings(plan_name: str) -> dict:
    """计算某方案 vs 最贵方案的节省"""
    target = next((p for p in PLAN_TEMPLATES if p["name"] == plan_name), None)
    luxury = next((p for p in PLAN_TEMPLATES if "土豪" in p["name"]), None)
    if not target or not luxury:
        return {}
    return {
        "vs_luxury_cny": luxury["total_cny"] - target["total_cny"],
        "vs_luxury_pct": round((1 - target["total_cny"] / max(luxury["total_cny"], 1)) * 100, 1),
    }


# ============================================================
# Rich TUI 界面
# ============================================================

def create_console():
    if HAS_RICH:
        return Console()
    return None


def show_banner(console):
    if not console:
        print("=" * 55)
        print("  AI Programming Cost Planner v1.0")
        print("  AI编程成本计算器")
        print("=" * 55)
        return
    console.print()
    console.print(Panel.fit(
        "[bold cyan]AI Programming Cost Planner v1.0[/]\n"
        "[dim]AI编程成本计算器 - 找到最适合你的AI工具方案[/]",
        border_style="cyan",
        padding=(1, 4),
    ))


def show_welcome(console):
    if not console:
        print("\n根据你的编程场景，推荐最优AI工具组合方案。\n")
        return
    console.print()
    console.print(Rule("[bold yellow]开始评估[/]"))
    console.print()
    console.print("[dim]根据你的编程场景，推荐最优AI工具组合方案。[/]")
    console.print("[dim]回答4个问题，获取个性化推荐。[/]")
    console.print()


def interactive_input(console) -> dict:
    """交互式收集用户信息"""
    if not console:
        # Fallback plain input
        print("\n[1/4] 你的主要编程语言:")
        for i, lang in enumerate(PROGRAMMING_LANGUAGES, 1):
            print(f"  {i}. {lang}")
        lang_idx = int(input("选择(1-{}): ".format(len(PROGRAMMING_LANGUAGES)))) - 1
        lang = PROGRAMMING_LANGUAGES[max(0, min(lang_idx, len(PROGRAMMING_LANGUAGES)-1))]

        print("\n[2/4] 每天编码时长:")
        for i, (h, desc) in enumerate(CODING_HOURS_OPTIONS, 1):
            print(f"  {i}. {desc}")
        h_idx = int(input("选择(1-4): ")) - 1
        hours = CODING_HOURS_OPTIONS[max(0, min(h_idx, 3))][0]

        print("\n[3/4] 主要项目类型:")
        for i, (k, desc) in enumerate(PROJECT_TYPES, 1):
            print(f"  {i}. {desc}")
        p_idx = int(input("选择(1-{}): ".format(len(PROJECT_TYPES)))) - 1
        proj = PROJECT_TYPES[max(0, min(p_idx, len(PROJECT_TYPES)-1))][0]

        print("\n[4/4] 月预算:")
        for i, (b, desc) in enumerate(BUDGET_OPTIONS, 1):
            print(f"  {i}. {desc}")
        b_idx = int(input("选择(1-5): ")) - 1
        budget = BUDGET_OPTIONS[max(0, min(b_idx, 4))][0]
        return {"lang": lang, "hours": hours, "project": proj, "budget": budget}

    # Rich interactive mode
    console.print("[bold cyan][1/4] 你的主要编程语言[/]")
    console.print()
    lang_table = Table(show_header=False, box=None, padding=(0, 2))
    lang_table.add_column("No", style="dim")
    lang_table.add_column("Language")
    for i, lang in enumerate(PROGRAMMING_LANGUAGES, 1):
        lang_table.add_row(str(i), lang)
    console.print(lang_table)
    lang_idx = IntPrompt.ask("选择", choices=[str(i) for i in range(1, len(PROGRAMMING_LANGUAGES)+1)], default=1)
    lang = PROGRAMMING_LANGUAGES[lang_idx - 1]

    console.print()
    console.print("[bold cyan][2/4] 每天编码时长[/]")
    console.print()
    for i, (h, desc) in enumerate(CODING_HOURS_OPTIONS, 1):
        console.print(f"  {i}. {desc}")
    h_idx = IntPrompt.ask("选择", choices=["1", "2", "3", "4"], default=2)
    hours = CODING_HOURS_OPTIONS[h_idx - 1][0]

    console.print()
    console.print("[bold cyan][3/4] 主要项目类型[/]")
    console.print()
    for i, (k, desc) in enumerate(PROJECT_TYPES, 1):
        console.print(f"  {i}. {desc}")
    p_idx = IntPrompt.ask("选择", choices=[str(i) for i in range(1, len(PROJECT_TYPES)+1)], default=1)
    proj = PROJECT_TYPES[p_idx - 1][0]

    console.print()
    console.print("[bold cyan][4/4] 月预算[/]")
    console.print()
    for i, (b, desc) in enumerate(BUDGET_OPTIONS, 1):
        console.print(f"  {i}. {desc}")
    b_idx = IntPrompt.ask("选择", choices=["1", "2", "3", "4", "5"], default=3)
    budget = BUDGET_OPTIONS[b_idx - 1][0]

    return {"lang": lang, "hours": hours, "project": proj, "budget": budget}


def show_results(console, profile: dict):
    lang = profile["lang"]
    hours = profile["hours"]
    proj = profile["project"]
    budget = profile["budget"]
    matched = match_tools(lang, proj, hours, budget)
    plans = recommend_plans(hours, budget)

    if not console:
        print("\n" + "=" * 55)
        print("  YOUR AI TOOL RECOMMENDATION")
        print("=" * 55)
        print(f"  Language: {lang} | Hours/day: {hours} | Budget: {budget} CNY/mo")
        print("\n  TOP RECOMMENDED TOOLS:")
        for tool, score in matched[:5]:
            ps = f"{tool.price_cny} CNY/mo" if tool.price_cny > 0 else "FREE"
            print(f"    - {tool.name}: {ps} | Q:{tool.code_quality} S:{tool.speed} V:{tool.cost_efficiency}")
        print("\n  RECOMMENDED PLANS:")
        for plan in plans[:3]:
            print(f"    [{plan['name']}] {plan['total_cny']} CNY/mo ({plan['total_usd']} USD/mo)")
            print(f"      Tools: {', '.join(plan['tools'])}")
            print(f"      {plan['tip']}")
            sav = calc_savings(plan['name'])
            if sav and sav.get('vs_luxury_cny', 0) > 0:
                print(f"      Save vs luxury: {sav['vs_luxury_cny']} CNY/mo ({sav['vs_luxury_pct']}%)")
            print()
        return

    console.print()
    console.print(Rule("[bold green]Your Personalized AI Tool Recommendation[/]"))
    console.print()
    proj_label = next((desc for k, desc in PROJECT_TYPES if k == proj), proj)
    budget_label = next((desc for b, desc in BUDGET_OPTIONS if b == budget), f"{budget}\u5143")
    console.print(Panel(
        f"[bold]Language:[/] {lang}\n[bold]Coding Hours:[/] {hours}h/day\n"
        f"[bold]Project:[/] {proj_label}\n[bold]Budget:[/] {budget_label}",
        title="Your Profile", border_style="blue",
    ))
    console.print()

    tools_table = Table(title="Top 5 Recommended Tools", show_lines=True, header_style="bold magenta")
    tools_table.add_column("Rank", justify="center", width=5)
    tools_table.add_column("Tool", min_width=20)
    tools_table.add_column("Type", justify="center")
    tools_table.add_column("Price/mo", justify="right")
    tools_table.add_column("Quality", justify="center")
    tools_table.add_column("Speed", justify="center")
    tools_table.add_column("Value", justify="center")
    tools_table.add_column("Description", min_width=25)
    for rank, (tool, score) in enumerate(matched[:5], 1):
        ps = f"[green]{tool.price_cny} CNY[/]" if tool.price_cny > 0 else "[bold green]FREE[/]"
        cc = {"ide": "cyan", "api": "yellow", "subscription": "magenta", "free": "green"}
        cat = f"[{cc.get(tool.category, 'white')}]{tool.category}[/]"
        qb = chr(9608) * tool.code_quality + chr(9617) * (10 - tool.code_quality)
        sb = chr(9608) * tool.speed + chr(9617) * (10 - tool.speed)
        vb = chr(9608) * tool.cost_efficiency + chr(9617) * (10 - tool.cost_efficiency)
        tools_table.add_row(str(rank), f"[bold]{tool.name}[/]", cat, ps, qb, sb, vb, f"[dim]{tool.description}[/]")
    console.print(tools_table)
    console.print()

    console.print(Rule("[bold yellow]Recommended Plans[/]"))
    console.print()
    for i, plan in enumerate(plans[:4], 1):
        sav = calc_savings(plan['name'])
        savings_str = ""
        if sav and sav.get('vs_luxury_cny', 0) > 0:
            vlc = sav['vs_luxury_cny']
            vlp = sav['vs_luxury_pct']
            savings_str = f"\n[dim]vs\u6700\u8d35\u65b9\u6848\u7701 [bold green]{vlc}\u5143/\u6708 ({vlp}%)[/][/]"
        tool_details = []
        for tname in plan.get('tools', []):
            t = next((t for t in TOOLS_DB if t.name == tname), None)
            if t:
                tool_details.append(f"  - [bold]{t.name}[/] ({t.price_cny} CNY/mo)")
        panel_content = (
            f"[dim]Target: {plan['target']}[/]\n\n"
            + "\n".join(tool_details)
            + f"\n\n[bold]Total: {plan['total_cny']} CNY/mo ({plan['total_usd']} USD/mo)[/]"
            + f"\n[dim]{plan['tip']}[/]"
            + savings_str
        )
        bc = ["green", "cyan", "blue", "magenta"]
        console.print(Panel(panel_content, title=f"[bold]#{i} {plan['name']}[/]",
                            border_style=bc[(i-1) % len(bc)], padding=(1, 2)))
        console.print()
    if plans:
        cheapest = min(plans, key=lambda p: p['total_cny'])
        console.print(Panel.fit(
            f"[bold green]Best Value:[/] {cheapest['name']} - [bold yellow]{cheapest['total_cny']} CNY/mo[/]\n"
            f"[dim]{cheapest['tip']}[/]",
            title="Conclusion", border_style="green",
        ))


def show_comparison(console):
    """Show all tools comparison table"""
    if not console:
        print("\nAll Tools Comparison:")
        hdr = f"{'Tool':<28} {'Type':<12} {'CNY/mo':>8} {'Quality':>8} {'Speed':>8} {'Value':>8}"
        print(hdr)
        print("-" * 80)
        for t in TOOLS_DB:
            ps = str(t.price_cny) if t.price_cny > 0 else "FREE"
            print(f"{t.name:<28} {t.category:<12} {ps:>8} {t.code_quality:>8} {t.speed:>8} {t.cost_efficiency:>8}")
        return
    table = Table(title="AI Coding Tools Comparison", show_lines=True, header_style="bold")
    table.add_column("Tool", min_width=20)
    table.add_column("Type")
    table.add_column("CNY/mo", justify="right")
    table.add_column("USD/mo", justify="right")
    table.add_column("Quality", justify="center")
    table.add_column("Speed", justify="center")
    table.add_column("Value", justify="center")
    table.add_column("Context")
    for t in TOOLS_DB:
        price = f"[green]{t.price_cny}[/]" if t.price_cny > 0 else "[bold green]FREE[/]"
        table.add_row(t.name, t.category, price, str(t.price_usd),
                      str(t.code_quality), str(t.speed), str(t.cost_efficiency), t.context_window)
    console.print(table)


def show_plans(console):
    """Show all plans"""
    if not console:
        print("\nAll Plans:")
        for plan in PLAN_TEMPLATES:
            print(f"  [{plan['name']}] {plan['total_cny']} CNY/mo")
            print(f"    Tools: {', '.join(plan['tools'])}")
            print(f"    Target: {plan['target']}")
            print(f"    {plan['tip']}\n")
        return
    console.print()
    console.print(Rule("[bold]All Plans Overview[/]"))
    console.print()
    table = Table(show_lines=True, header_style="bold")
    table.add_column("Plan", min_width=20)
    table.add_column("Target", min_width=20)
    table.add_column("Tools", min_width=30)
    table.add_column("CNY/mo", justify="right")
    table.add_column("USD/mo", justify="right")
    for plan in PLAN_TEMPLATES:
        table.add_row(plan['name'], f"[dim]{plan['target']}[/]",
                      ", ".join(plan['tools']),
                      f"[bold yellow]{plan['total_cny']}[/]", f"${plan['total_usd']}")
    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="AI Programming Cost Planner - AI\u7f16\u7a0b\u6210\u672c\u8ba1\u7b97\u5668",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\nExamples:\n  python ai_coding_planner.py                    # Interactive\n  python ai_coding_planner.py --compare          # All tools\n  python ai_coding_planner.py --plans            # All plans\n  python ai_coding_planner.py --quick            # Quick mode\n",
    )
    parser.add_argument("--lang", type=str, help="Programming language")
    parser.add_argument("--hours", type=int, choices=[1, 2, 4, 5], help="Coding hours/day")
    parser.add_argument("--project", type=str,
                        choices=["web", "backend", "mobile", "data", "script", "infra", "fullstack"],
                        help="Project type")
    parser.add_argument("--budget", type=int, help="Monthly budget (CNY)")
    parser.add_argument("--compare", action="store_true", help="Compare all tools")
    parser.add_argument("--plans", action="store_true", help="View all plans")
    parser.add_argument("--quick", action="store_true", help="Quick mode with defaults")
    parser.add_argument("--no-rich", action="store_true", help="Disable Rich UI")

    args = parser.parse_args()

    if args.no_rich:
        global HAS_RICH
        HAS_RICH = False

    console = create_console() if HAS_RICH else None

    if args.compare:
        show_banner(console)
        show_comparison(console)
        return
    if args.plans:
        show_banner(console)
        show_plans(console)
        return

    show_banner(console)

    if args.quick:
        profile = {"lang": "Python", "hours": 4, "project": "backend", "budget": 200}
    elif args.lang and args.hours and args.project and args.budget:
        profile = {"lang": args.lang, "hours": args.hours, "project": args.project, "budget": args.budget}
    else:
        show_welcome(console)
        profile = interactive_input(console)

    show_results(console, profile)


if __name__ == "__main__":
    main()
