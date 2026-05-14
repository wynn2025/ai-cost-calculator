#!/usr/bin/env python3
"""AI Programming Cost Comparator v2.0"""
import sys, argparse
from datetime import datetime

TOOLS = [
    {"name":"Cursor Pro","cat":"AI IDE","mo":152,"yr":1520,"free":"Limited","rate":9.2,"best":"Full-stack"},
    {"name":"GitHub Copilot","cat":"IDE Plugin","mo":76,"yr":760,"free":"Students free","rate":8.8,"best":"VS Code"},
    {"name":"Claude Code Max","cat":"Terminal AI","mo":1440,"yr":14400,"free":"Limited","rate":9.5,"best":"Complex"},
    {"name":"Claude Code Pro","cat":"Terminal AI","mo":144,"yr":1440,"free":"Limited","rate":9.0,"best":"Daily"},
    {"name":"Windsurf Pro","cat":"AI IDE","mo":105,"yr":1050,"free":"Limited","rate":8.5,"best":"Light dev"},
    {"name":"Augment Code","cat":"IDE Plugin","mo":0,"yr":0,"free":"YES","rate":8.0,"best":"Budget"},
    {"name":"Codeium Free","cat":"IDE Plugin","mo":0,"yr":0,"free":"YES","rate":7.8,"best":"Beginners"},
    {"name":"Trae ByteDance","cat":"AI IDE","mo":0,"yr":0,"free":"YES","rate":8.2,"best":"CN users"},
    {"name":"DeepSeek API","cat":"API","mo":15,"yr":180,"free":"Pay-per-use","rate":9.0,"best":"Terminal"},
    {"name":"DS+Claude Combo","cat":"Combo","mo":22,"yr":264,"free":"Pay-per-use","rate":9.3,"best":"Best value"},
    {"name":"Amazon Q Dev","cat":"IDE Plugin","mo":0,"yr":0,"free":"YES","rate":7.5,"best":"AWS"},
]

BUNDLES = [
    {"name":"Zero Cost","tools":"Augment+Codeium","mo":0,"yr":0},
    {"name":"Minimal","tools":"DeepSeek API+Codeium","mo":15,"yr":180},
    {"name":"Best Value","tools":"DS+Claude+Trae","mo":22,"yr":264},
    {"name":"Professional","tools":"Cursor Pro+DeepSeek API","mo":167,"yr":1700},
    {"name":"Flagship","tools":"Claude Code Pro+Copilot","mo":220,"yr":2200},
]

def compare_all():
    print()
    print("=" * 90)
    print("  AI Programming Tools Cost Comparison (2026-05)")
    print("=" * 90)
    print("  {:<22} {:<12} {:>8} {:>8} {:<14} {:>6} {:<14}".format("Tool","Type","Monthly","Annual","Free?","Rate","Best"))
    print("  " + "-" * 86)
    for t in sorted(TOOLS, key=lambda x: x["mo"]):
        print("  {:<22} {:<12} {:>7}  {:>7}  {:<14} {:>5.1f}  {:<14}".format(t["name"],t["cat"],t["mo"],t["yr"],t["free"],t["rate"],t["best"]))
    print()

def show_bundles():
    print()
    for b in BUNDLES:
        print("  {:<14} {:>5} CNY/mo | {:>5} CNY/yr  ({})".format(b["name"],b["mo"],b["yr"],b["tools"]))
    print()

def budget_plan(budget):
    print("  Budget: {} CNY/month".format(budget))
    ok = [t for t in TOOLS if t["mo"] <= budget]
    for t in sorted(ok, key=lambda x: -x["rate"]):
        tag = " [FREE]" if t["mo"] == 0 else " [{} CNY]".format(t["mo"])
        print("  {:.1f} | {}{} - {}".format(t["rate"],t["name"],tag,t["best"]))
    print()

def export_md(fname="ai_cost_comparison.md"):
    L2 = ["# AI Programming Tools Cost Comparison 2026", "", "> Updated: " + datetime.now().strftime("%Y-%m-%d"), ""]
    L2.append("## Comparison Table")
    L2.append("")
    L2.append("| Tool | Type | Monthly | Annual | Free | Rating | Best For |")
    L2.append("|------|------|---------|--------|------|--------|----------|")
    for t in sorted(TOOLS, key=lambda x: x["mo"]):
        L2.append("| {} | {} | {} | {} | {} | {} | {} |".format(t["name"],t["cat"],t["mo"],t["yr"],t["free"],t["rate"],t["best"]))
    L2.extend(["", "## Bundles", "", "| Bundle | Monthly | Annual |", "|--------|---------|--------|"])
    for b in BUNDLES:
        L2.append("| {} | {} | {} |".format(b["name"],b["mo"],b["yr"]))
    L2.extend(["", "## Tips", "", "1. DeepSeek API 15/mo = 10x cheaper than Claude", "2. DS+Claude combo 22/mo = best value", ""])
    c = chr(10).join(L2)
    with open(fname, "w", encoding="utf-8") as f: f.write(c)
    print("  Exported: {} ({} chars)".format(fname, len(c)))

def export_csv(fname="ai_cost_comparison.csv"):
    L2 = ["Tool,Type,Monthly_CNY,Annual_CNY,Free,Rating,Best_For"]
    for t in TOOLS:
        L2.append("{},{},{},{},{},{},{}".format(t["name"],t["cat"],t["mo"],t["yr"],t["free"],t["rate"],t["best"]))
    c = chr(10).join(L2)
    with open(fname, "w", encoding="utf-8") as f: f.write(c)
    print("  Exported: {} ({} chars)".format(fname, len(c)))

def main():
    p = argparse.ArgumentParser(description="AI Cost Comparator v2.0")
    p.add_argument("--compare", action="store_true")
    p.add_argument("--bundles", action="store_true")
    p.add_argument("--export", choices=["md","csv"])
    p.add_argument("--budget", type=int)
    p.add_argument("--tool", type=str)
    p.add_argument("-o", type=str)
    a = p.parse_args()
    if a.compare: compare_all()
    elif a.bundles: show_bundles()
    elif a.export == "md": export_md(a.o or "ai_cost_comparison.md")
    elif a.export == "csv": export_csv(a.o or "ai_cost_comparison.csv")
    elif a.tool:
        for t in TOOLS:
            if a.tool.lower() in t["name"].lower():
                print("  {} | {}/mo | {}/yr | {}/10 | {}".format(t["name"],t["mo"],t["yr"],t["rate"],t["best"]))
    elif a.budget is not None: budget_plan(a.budget)
    else:
        compare_all()
        show_bundles()

if __name__ == "__main__": main()