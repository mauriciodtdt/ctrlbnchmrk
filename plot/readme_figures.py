#!/usr/bin/env python3
# Generates the result figures shown in the README (light and dark variants).
# Values are the ones reported in the ICSPCS 2019 paper; raw data lives in
# doc/PerformanceTests/.
#
# Usage: python3 plot/readme_figures.py   (requires matplotlib)

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "doc", "results")

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "axis": "#c3c2b7",
        "series": ["#2a78d6", "#eb6834", "#1baf7a"],
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#f0efec", "ink2": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "axis": "#383835",
        "series": ["#3987e5", "#d95926", "#199e70"],
    },
}

# Tests 1 & 2: Cbench, 16 switches / 500 MACs (flows per second)
CBENCH_CTRLS = ["POX", "ODL", "ONOS", "Ryu", "Floodlight", "OpenMUL"]
CBENCH_LATENCY = [1802.2, 28335.38, 37755.46, 3416.99, 47257.7, 84654.71]
CBENCH_THROUGHPUT = [3052.9, 30094.09, 133285.65, 2986.43, 33568.73, 4119437.73]

# Test 3: total network topology discovery time (seconds)
DISC_TOPOS = ["Linear\n100 sw", "Hub & spoke\n55 sw", "Hub & spoke\n105 sw",
              "Spine-leaf\n8×16", "Spine-leaf\n8×32"]
DISC_TIMES = {
    "Ryu":  [27.208604, 13.404433, 5.047115, 2.364551, 1.771187],
    "ODL":  [14.561445, 13.027745, 12.277401, 6.934329, 4.600897],
    "ONOS": [10.104715, 12.313744, 5.760109, 3.490575, 4.242794],
}

# Test 5: topology change detection time, spine-leaf 8x16, mean of 10 runs (seconds)
CHANGE_CTRLS = ["ONOS", "ODL", "Ryu", "Floodlight"]
CHANGE_TIMES = [0.955, 1.981, 4.299, 9.278]

# Test 6: network discovery size, linear topology stable for 5 minutes (switches)
SIZE_CTRLS = ["ONOS", "ODL", "Ryu"]
SIZE_NODES = [700, 600, 500]

FONT = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]


def style(ax, t, grid_axis):
    ax.set_facecolor(t["surface"])
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    if grid_axis == "x":
        ax.spines["left"].set_visible(True)
        ax.spines["left"].set_color(t["axis"])
    else:
        ax.spines["bottom"].set_visible(True)
        ax.spines["bottom"].set_color(t["axis"])
    ax.grid(axis=grid_axis, color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=t["muted"], labelsize=9, length=0)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(t["ink2"])


def title(fig, t, text, sub):
    fig.text(0.02, 0.96, text, color=t["ink"], fontsize=13, fontweight="bold", va="top")
    fig.text(0.02, 0.90, sub, color=t["ink2"], fontsize=9.5, va="top")


def hbar(ax, t, labels, values, fmt, color):
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, height=0.6, color=color)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    pad = max(values) * 0.01
    for yi, v in zip(y, values):
        ax.text(v + pad, yi, fmt(v), va="center", fontsize=8.5, color=t["ink2"])
    ax.set_xlim(0, max(values) * 1.15)


def kflows(v):
    return "%.1fK" % (v / 1e3)


def fig_cbench(t):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.9))
    fig.patch.set_facecolor(t["surface"])
    title(fig, t, "Asynchronous message processing (Cbench)",
          "Flows/sec, 16 emulated switches, 500 MACs. Higher is better.")

    hbar(a1, t, CBENCH_CTRLS, CBENCH_LATENCY, kflows, t["series"][0])
    a1.set_title("Latency mode", loc="left", color=t["ink"], fontsize=10.5)
    a1.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "%dK" % (v / 1e3)))

    # OpenMUL (4.1M flows/s) would flatten every other bar, so it is annotated instead
    ctrls = CBENCH_CTRLS[:-1]
    vals = CBENCH_THROUGHPUT[:-1]
    hbar(a2, t, ctrls, vals, kflows, t["series"][0])
    a2.set_title("Throughput mode", loc="left", color=t["ink"], fontsize=10.5)
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "%dK" % (v / 1e3)))
    a2.text(0.98, 0.04, "OpenMUL: %.2fM flows/s\n(off scale, ~31× ONOS)" % (CBENCH_THROUGHPUT[-1] / 1e6),
            transform=a2.transAxes, ha="right", va="bottom", fontsize=8.5, color=t["ink2"])

    for ax in (a1, a2):
        style(ax, t, "x")
    fig.subplots_adjust(left=0.1, right=0.97, top=0.76, bottom=0.08, wspace=0.35)
    return fig


def fig_discovery(t):
    fig, ax = plt.subplots(figsize=(10, 4.4))
    fig.patch.set_facecolor(t["surface"])
    title(fig, t, "Network topology discovery time",
          "Seconds from first switch discovered to last link discovered (OpenFlow 1.3). Lower is better.")

    n = len(DISC_TIMES)
    width = 0.24
    gap = 0.012
    for i, (ctrl, vals) in enumerate(DISC_TIMES.items()):
        xs = [x + (i - (n - 1) / 2) * width for x in range(len(DISC_TOPOS))]
        ax.bar(xs, vals, width - gap, color=t["series"][i], label=ctrl)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.3, "%.1f" % v, ha="center", fontsize=8, color=t["ink2"])

    ax.set_xticks(range(len(DISC_TOPOS)))
    ax.set_xticklabels(DISC_TOPOS)
    ax.set_ylabel("Seconds", color=t["ink2"], fontsize=9)
    style(ax, t, "y")
    leg = ax.legend(loc="upper right", frameon=False, fontsize=9, ncol=3)
    for txt in leg.get_texts():
        txt.set_color(t["ink"])
    fig.subplots_adjust(left=0.07, right=0.98, top=0.8, bottom=0.14)
    return fig


def fig_resilience_scale(t):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.3))
    fig.patch.set_facecolor(t["surface"])
    title(fig, t, "Change detection and network size",
          "Left: seconds to detect a link failure, spine-leaf 8×16, mean of 10 runs (lower is better).  "
          "Right: largest stable linear network (higher is better).")

    hbar(a1, t, CHANGE_CTRLS, CHANGE_TIMES, lambda v: "%.2f s" % v, t["series"][0])
    a1.set_title("Topology change detection time", loc="left", color=t["ink"], fontsize=10.5)

    hbar(a2, t, SIZE_CTRLS, SIZE_NODES, lambda v: "%d switches" % v, t["series"][0])
    a2.set_title("Network discovery size", loc="left", color=t["ink"], fontsize=10.5)
    a2.set_xlim(0, 900)

    for ax in (a1, a2):
        style(ax, t, "x")
    fig.subplots_adjust(left=0.1, right=0.97, top=0.72, bottom=0.1, wspace=0.35)
    return fig


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    plt.rcParams["font.family"] = FONT
    figures = {"cbench": fig_cbench, "discovery_time": fig_discovery,
               "change_detection_and_size": fig_resilience_scale}
    for mode, t in THEMES.items():
        for name, build in figures.items():
            fig = build(t)
            path = os.path.join(OUT_DIR, "%s_%s.png" % (name, mode))
            fig.savefig(path, dpi=160, facecolor=t["surface"])
            plt.close(fig)
            print(path)


if __name__ == "__main__":
    main()
