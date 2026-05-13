#!/usr/bin/env python3
"""DeepSeek-V4 API Cost Calculator v1.0 - Compare LLM API costs"""
import argparse, json, os
from datetime import datetime

MODEL_PRICING = {
    "DeepSeek-V4": {"input": 0.27, "output": 1.10, "ctx": "128K"},
    "DeepSeek-V4 (cache)": {"input": 0.07, "output": 0.28, "ctx": "128K"},
    "Claude 4 Sonnet": {"input": 3.00, "output": 15.00, "ctx": "200K"},
    "Claude 4 Opus": {"input": 15.00, "output": 75.00, "ctx": "200K"},
    "GPT-4o": {"input": 2.50, "output": 10.00, "ctx": "128K"},
    "GPT-4o-mini": {"input": 0.15, "output": 0.60, "ctx": "128K"},
    "Gemini 2.5 Pro": {"input": 1.25, "output": 10.00, "ctx": "1M"},
    "Gemini 2.5 Flash": {"input": 0.15, "output": 0.60, "ctx": "1M"},
    "Qwen3-235B": {"input": 0.50, "output": 2.00, "ctx": "128K"},
    "Llama 4 Maverick": {"input": 0.20, "output": 0.80, "ctx": "1M"},
}

DEFAULT_COMPARE = [
    "DeepSeek-V4", "DeepSeek-V4 (cache)",
    "Claude 4 Sonnet", "GPT-4o", "Gemini 2.5 Pro", "Qwen3-235B"
]

FREQ_MAP = {"daily": 30, "weekly": 4, "monthly": 1, "hourly": 720}
IO_RATIO = 0.6

def calc_cost(name, tokens, freq):
    p = MODEL_PRICING[name]
    inp = tokens * IO_RATIO
    out = tokens * (1 - IO_RATIO)
    per_call = inp / 1e6 * p["input"] + out / 1e6 * p["output"]
    mo = per_call * FREQ_MAP.get(freq, 30)
    return {"model": name, "per_call": per_call, "monthly": mo, "annual": mo * 12}


def print_report(results, tokens, freq):
    print()
    print("=" * 70)
    print("  API Cost Comparison Report")
    pct_in = IO_RATIO*100
    pct_out = (1-IO_RATIO)*100
    print("  Tokens/call: {:,} | Freq: {} | I/O: {:.0f}/{:.0f}".format(tokens, freq, pct_in, pct_out))
    print("=" * 70)
    hdr = "{:25s} {:>10s} {:>10s} {:>12s}".format("Model", "Per Call", "Monthly", "Annual")
    print(hdr)
    print("-" * 70)
    cheapest = min(results, key=lambda x: x["monthly"])
    for r in sorted(results, key=lambda x: x["monthly"]):
        tag = " <-- CHEAPEST" if r is cheapest else ""
        line = "{:25s} {:>9s} {:>9s} {:>11s}".format(
            r["model"],
            "${:.4f}".format(r["per_call"]),
            "${:.2f}".format(r["monthly"]),
            "${:.2f}".format(r["annual"]))
        print(line + tag)
    print("-" * 70)
    g4 = next((r for r in results if r["model"] == "GPT-4o"), None)
    if g4:
        for r in results:
            if r["model"] != "GPT-4o":
                s = g4["annual"] - r["annual"]
                pct = s / g4["annual"] * 100 if g4["annual"] > 0 else 0
                print("  {} saves ${:.2f}/yr vs GPT-4o ({:.1f}%)".format(r["model"], s, pct))
    print("=" * 70)
    return cheapest


def generate_chart(results, tokens, freq, outpath=None):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
    except ImportError:
        print("[ERROR] pip install matplotlib")
        return None
    models = [r["model"] for r in results]
    mo = [r["monthly"] for r in results]
    yr = [r["annual"] for r in results]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle("API Cost Comparison\n({}, {} tokens/call)".format(freq, tokens), fontsize=16, fontweight="bold")
    cmap = {"DeepSeek": "#4FC3F7", "Claude": "#AB47BC", "GPT": "#66BB6A",
            "Gemini": "#FFA726", "Qwen": "#EF5350", "Llama": "#78909C"}
    colors = [next((v for k, v in cmap.items() if k in m), "#78909C") for m in models]
    b1 = a1.barh(models, mo, color=colors, edgecolor="white", height=0.6)
    a1.set_xlabel("Monthly (USD)")
    a1.set_title("Monthly Cost")
    a1.xaxis.set_major_formatter(ticker.FormatStrFormatter("${:.1f}".format(1.1)[:-2] + "{:.1f}"))
    for b, v in zip(b1, mo):
        a1.text(b.get_width() + max(mo)*0.02, b.get_y()+b.get_height()/2,
                "${:.2f}".format(v), va="center", fontsize=9)
    b2 = a2.barh(models, yr, color=colors, edgecolor="white", height=0.6)
    a2.set_xlabel("Annual (USD)")
    a2.set_title("Annual Cost")
    a2.xaxis.set_major_formatter(ticker.FormatStrFormatter("{:.0f}"))
    for b, v in zip(b2, yr):
        a2.text(b.get_width() + max(yr)*0.02, b.get_y()+b.get_height()/2,
                "${:.0f}".format(v), va="center", fontsize=9)
    plt.tight_layout()
    if not outpath:
        outpath = "cost_comparison_{}.png".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    plt.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return outpath


def export_json(results, tokens, freq, outpath=None):
    data = {"generated_at": datetime.now().isoformat(),
            "params": {"tokens": tokens, "freq": freq},
            "models": results}
    if not outpath:
        outpath = "cost_report_{}.json".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return outpath

def interactive():
    sep = "~" * 50
    print()
    print(sep)
    print("  DeepSeek-V4 API Cost Calculator v1.0")
    print("  by Hermes AI Team")
    print(sep)
    try:
        raw = input("\n[1/3] Tokens per call (e.g. 50000): ")
        t = int(raw.replace(",", ""))
    except ValueError:
        print("Default: 50,000")
        t = 50000
    f = input("[2/3] Freq (daily/weekly/monthly/hourly) [daily]: ").strip().lower()
    if f not in FREQ_MAP:
        f = "daily"
    ch = input("[3/3] Chart? (y/n) [y]: ").strip().lower()
    return t, f, ch not in ("n", "no")


def main():
    p = argparse.ArgumentParser(description="LLM API Cost Calculator")
    p.add_argument("--tokens", type=int, default=None)
    p.add_argument("--freq", choices=list(FREQ_MAP.keys()), default=None)
    p.add_argument("--chart", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--quick", action="store_true")
    p.add_argument("--models", nargs="+", default=None)
    p.add_argument("--all", action="store_true")
    p.add_argument("--output", type=str, default=None)
    args = p.parse_args()

    if args.quick:
        tokens, freq, chart = 50000, "daily", True
    elif args.tokens:
        tokens, freq, chart = args.tokens, args.freq or "daily", args.chart
    else:
        tokens, freq, chart = interactive()

    if args.all:
        clist = list(MODEL_PRICING.keys())
    elif args.models:
        clist = [m for m in args.models if m in MODEL_PRICING] or DEFAULT_COMPARE
    else:
        clist = DEFAULT_COMPARE

    results = [calc_cost(m, tokens, freq) for m in clist]
    print_report(results, tokens, freq)
    if chart:
        cp = generate_chart(results, tokens, freq, args.output)
        if cp:
            print("[OK] Chart:", cp)
    if args.json:
        jp = export_json(results, tokens, freq, args.output)
        print("[OK] JSON:", jp)

    cheap = min(results, key=lambda x: x["monthly"])
    expensive = max(results, key=lambda x: x["monthly"])
    sav = expensive["annual"] - cheap["annual"]
    print()
    print(">>> {}: ${:.2f}/mo (cheapest)".format(cheap["model"], cheap["monthly"]))
    print(">>> Save up to ${:.2f}/year by choosing wisely!".format(sav))
    print()

if __name__ == "__main__":
    main()
