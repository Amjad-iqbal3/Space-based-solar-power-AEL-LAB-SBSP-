# -*- coding: utf-8 -*-
"""
================================================================================
SBSP LEO --- JOURNAL VERSION  (IEEE TVT extension)  --  CONSOLIDATED PLOTTER

Single plotting module that produces every figure in the manuscript:

  Per-policy figures (4) -- one figure-set per allocator policy per scenario:
    Fig 1 : RF Budget, Delivered DC Power, and end-to-end WPT efficiency
            over 24 h, with peak Delivered annotated by arrow and text.
    Fig 2 : Per-station demand vs. mean delivered power (24-h average).
    Fig 3 : Per-station received RF power density at the rectenna.
            Reference lines: 10 W/m^2 (ICNIRP public limit -- the binding
            threshold under the journal scenario) and 100 W/m^2 (rectenna
            rated PD).
    Fig 4 : Per-station operational rectenna efficiency, against the
            static design band (eta_min ... eta_peak).

  Cross-policy comparison figures (Section IV, A-G) -- four allocator
  policies side-by-side at a fixed scenario:
    Comp A : headline metrics bar chart (delivered / Jain / worst-DMR)
    Comp B : per-station grouped bars (delivered kW, 8 stations x 4 policies)
    Comp C : 24-h time series of total delivered MW, four-colour overlay
    Comp D : visibility histogram (scenario-level, # of visible GS per sat-step)
    Comp E : RF capacity utilisation stacked bars (panel -> delivered/loss/discard)
    Comp F : per-station demand-met fraction, 8 x 4 grouped bars
    Comp G : demand sensitivity scan over multiple scenarios (gap-to-LP vs demand)

  Sensitivity sweep figures (Section V) -- 4 altitudes x 3 constellation
  sizes x 4 policies = 48 runs:
    Sens A : total delivered vs altitude, faceted by constellation size
    Sens B : gap-to-LP vs altitude, faceted by constellation size
    Sens C : 2x2 heatmap grid (delivered / Jain / gap / multi-visibility)
    Sens D : Jain index vs altitude, faceted by constellation size

Requires SBSP_env.py (journal-version patches applied:
European cluster, ICNIRP 10 W/m^2 cap, two-tier allocator with
redistribution, lp_optimal benchmark mode).
================================================================================
"""

# ============================================================
# Step 1 --- import the simulation model
# ============================================================
SBSP_MODULE_NAME = "SBSP_env"

import importlib, sys, os, time, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe

try:
    sbsp = importlib.import_module(SBSP_MODULE_NAME)
    SimParams      = sbsp.SimParams
    SBSPSimulation = sbsp.SBSPSimulation
    WPTChannel     = sbsp.WPTChannel
    RE_M           = sbsp.RE_M
    print(f"  Imported '{SBSP_MODULE_NAME}.py' successfully")
except ModuleNotFoundError:
    print(f"\n  Could not import '{SBSP_MODULE_NAME}'. Ensure the .py file is on PYTHONPATH.\n")
    sys.exit(1)

# ============================================================
# Step 2: Simulation settings
# ============================================================
DURATION_HOURS = 24.0
ALLOC_MODE     = "greedy"          # "greedy" | "prop_fair" | "min_demand"
OUTPUT_DIR     = "./sbsp_figures"

# ============================================================
# Step 3: Figure style
# ============================================================
DPI        = 600
FIG_FORMAT = ["pdf"]   # PDF only (vector, IEEE camera-ready ready)

# ---- Centralized font sizes (consistent across all four figures) ----
# Change a value here and every figure picks it up. Sizes were chosen
# to maximize readability on a printed two-column IEEE page while
# keeping x-axis station labels legible at 35° rotation.
FONT_AXIS_LABEL    = 18    # x-axis and y-axis label text  ("Ground Station", "Power [kW]")
FONT_TICK          = 15    # numeric tick labels on both axes
FONT_GS_NAME       = 15    # city names on the x-axis (35° rotated)
FONT_LEGEND        = 13    # legend entries
FONT_BAR_VALUE     = 12    # numeric value labels above bars
FONT_NO_SERVICE    = 13    # red italic "no service" callout
FONT_PEAK_CALLOUT  = 13    # boxed text for Fig 1 peak callout

PALETTE = {
    # ---- IEEE white-background palette ----
    "bg"    : "#ffffff",   # figure background: pure white for print/publication
    "ax_bg" : "#ffffff",   # axes background: white (no panel tint)
    "grid"  : "#bcc1cb",   # medium grey gridlines, mid-contrast against white
    "text"  : "#1a1a1a",   # near-black text, mid-weight (avoid pure black eye strain)
    # Accent colors retained but darkened slightly so they read on white.
    "cyan"  : "#0091a7",   # data-series 1 (was light cyan)
    "orange": "#d96c00",   # data-series 2 (deeper orange)
    "green" : "#2e8b3d",   # data-series 3 (forest green)
    "amber" : "#c79100",   # bar accent (deep amber)
    "red"   : "#c62828",   # threshold/warning (deep red)
    "purple": "#8e44ad",   # data-series 4 (royal purple)
    "teal"  : "#00695c",   # data-series 5 (deep teal)
    "blue"  : "#1565c0",   # data-series 6 (deep blue)
}

GS_COLORS = [
    PALETTE["cyan"],   PALETTE["orange"], PALETTE["green"],
    PALETTE["amber"],  PALETTE["red"],    PALETTE["purple"],
    PALETTE["teal"],   PALETTE["blue"],
]

# ---- Policy palette for cross-policy comparison figures ----
# Four distinct hues chosen to be (a) distinguishable on a WHITE background,
# (b) keep the existing GS_COLORS palette free for per-station figures,
# (c) high-contrast for grouped-bar charts where stations + policies stack.
# These are slightly desaturated from pure web hues so they read well in
# print without overpowering text.
POLICY_COLOR = {
    "greedy"    : "#e08c00",   # amber  (greedy = "grab the best")
    "prop_fair" : "#1d72b8",   # blue   (water-filling distribution)
    "min_demand": "#3a9b3a",   # green  (demand-aware floor)
    "lp_optimal": "#a445b2",   # purple (centralised benchmark, visually distinct)
}
POLICY_LABEL = {
    "greedy"    : "Greedy",
    "prop_fair" : "PF",
    "min_demand": "CO-DC",
    "lp_optimal": "LP upper bound",
}
POLICY_ORDER     = ["greedy", "prop_fair", "min_demand", "lp_optimal"]
HEURISTIC_ORDER  = ["greedy", "prop_fair", "min_demand"]


def apply_style():
    plt.rcParams.update({
        "font.family"      : "DejaVu Sans",
        "font.size"        : FONT_TICK,
        "axes.facecolor"   : PALETTE["ax_bg"],
        "figure.facecolor" : PALETTE["bg"],
        "text.color"       : PALETTE["text"],
        "axes.labelcolor"  : PALETTE["text"],
        "xtick.color"      : PALETTE["text"],
        "ytick.color"      : PALETTE["text"],
        "xtick.labelsize"  : FONT_TICK,
        "ytick.labelsize"  : FONT_TICK,
        "axes.edgecolor"   : "#4a4f5a",     # darker than gridlines, frames the panel
        "axes.linewidth"   : 0.9,
        "axes.grid"        : True,
        "grid.color"       : PALETTE["grid"],
        "grid.linewidth"   : 0.5,
        "grid.alpha"       : 0.6,
        "axes.titlepad"    : 8,
        "axes.titlesize"   : FONT_AXIS_LABEL,
        "axes.titleweight" : "bold",
        "axes.labelsize"   : FONT_AXIS_LABEL,
        "legend.fontsize"  : FONT_LEGEND,
        "legend.framealpha": 0.92,
        "legend.edgecolor" : "#888888",
        "legend.facecolor" : "#ffffff",
        "lines.linewidth"  : 2.0,
        "savefig.dpi"      : DPI,
        "savefig.bbox"     : "tight",
        "savefig.facecolor": PALETTE["bg"],
        "savefig.edgecolor": "none",
    })


def save_fig(fig, stem):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    saved = []
    for fmt in FIG_FORMAT:
        path = os.path.join(OUTPUT_DIR, f"{stem}.{fmt}")
        fig.savefig(path, format=fmt, dpi=DPI,
                    facecolor=PALETTE["bg"], edgecolor="none", bbox_inches="tight")
        saved.append(path)
        print(f"  [SAVED]  {path}")
    return saved


# ============================================================
# Step 4: Run the simulation, aggregate per-station statistics
# ============================================================
def run_simulation(duration_hours, alloc_mode):
    """
    Run a 24-h SBSP simulation under a single allocator policy and aggregate
    the per-station statistics needed by all four figures. Returns the live
    `sim` object plus pre-computed mean delivered, peak/mean PD, and
    operational rectenna efficiency.
    """
    params            = SimParams()
    params.alloc_mode = alloc_mode
    sim               = SBSPSimulation(params)
    dt                = params.dt_s
    n_steps           = int(duration_hours * 3600.0 / dt) + 1
    orbit_steps       = max(int(5550 / dt), 1)

    n_gs           = sim.n_gs
    sum_del_kW     = [0.0] * n_gs
    sum_pd_W_m2    = [0.0] * n_gs
    peak_pd_W_m2   = [0.0] * n_gs
    sum_eta_op     = [0.0] * n_gs
    eta_op_count   = [0]   * n_gs
    count          = 0

    print(f"\n[SBSP]  Simulation starting  ({alloc_mode.upper()})")
    print(f"        Duration = {duration_hours} h  ({n_steps} steps × {dt} s)")
    print(f"        Sats = {sim.n_sats}  GS = {n_gs}\n")

    t_wall = time.time()
    for i in range(n_steps):
        sim.step()
        count += 1
        for j in range(n_gs):
            kw     = sim.hist["gs_delivered_kW"][j][-1]
            pd     = sim.hist["gs_pd_W_m2"][j][-1]
            eta_op = sim.hist["gs_eta_op_pct"][j][-1]
            sum_del_kW[j]  += kw
            sum_pd_W_m2[j] += pd
            if pd > peak_pd_W_m2[j]:
                peak_pd_W_m2[j] = pd
            if kw > 1e-3:
                sum_eta_op[j]   += eta_op
                eta_op_count[j] += 1

        if i % orbit_steps == 0:
            del_ = sim.hist["delivered_MW"][-1]
            soc  = sim.hist["batt_soc_mean"][-1]
            print(f"  {100.*(i+1)/n_steps:5.1f}%   "
                  f"t={(sim.t_unix - params.t0_unix)/3600.:5.2f}h   "
                  f"delivered={del_:.3f} MW   batt_SOC={soc:.1f}%")

    print(f"\n[SBSP]  Finished in {time.time()-t_wall:.1f} s")

    return {
        "sim":          sim,
        "mean_del_kW":  [s/max(count,1)             for s in sum_del_kW],
        "mean_pd_W_m2": [s/max(count,1)             for s in sum_pd_W_m2],
        "peak_pd_W_m2": list(peak_pd_W_m2),
        "mean_eta_op":  [sum_eta_op[j]/max(eta_op_count[j],1) for j in range(n_gs)],
    }


# ============================================================
# Fig 1 --- RF Budget, Delivered Power, and WPT Efficiency over 24 h
# Two-panel layout. Peak annotated with arrow and clear text label.
# ============================================================
def fig_rf_vs_delivered(sim):
    """
    Two stacked panels sharing the time axis:
        Top    : RF Budget and Delivered DC Power on a shared MW axis.
                 Peak Delivered is annotated with a curved arrow and a
                 boxed text callout placed in the empty area between the
                 Delivered curve and the RF Budget curve. Vertical and
                 horizontal positioning is scale-adaptive.
        Bottom : End-to-end WPT efficiency on its own scale, so the small
                 efficiency signal is not visually crushed by RF Budget.

    Samples are instantaneous (one per 30 s simulation step). No smoothing
    or downsampling. Twinx is avoided because it forced poor scaling at
    24 h.
    """
    apply_style()
    h  = sim.hist
    tv = np.asarray(h["t_hr"],           dtype=float)
    rf = np.asarray(h["rf_budget_MW"],   dtype=float)
    dl = np.asarray(h["delivered_MW"],   dtype=float)
    ef = np.asarray(h["efficiency_pct"], dtype=float)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 6.2), sharex=True,
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.10},
        facecolor=PALETTE["bg"],
    )

    # ----- TOP PANEL: RF Budget + Delivered DC -----
    ax1.fill_between(tv, dl, alpha=0.22, color=PALETTE["cyan"],
                     edgecolor="none", zorder=2)
    ax1.plot(tv, rf, color=PALETTE["orange"], lw=0.8,
             alpha=0.85, label="RF Budget (MW)", zorder=3)
    ax1.plot(tv, dl, color=PALETTE["cyan"], lw=1.1,
             label="Delivered DC (MW)", zorder=4)

    # ----- Peak callout (arrow + boxed text) -----
    if dl.size:
        peak_idx  = int(np.argmax(dl))
        peak_time = float(tv[peak_idx])
        peak_val  = float(dl[peak_idx])
        rf_max    = float(rf.max()) if rf.size else 1.0
        t_max     = float(tv[-1])   if tv.size else 24.0

        # Triangle marker on the peak point
        ax1.plot(peak_time, peak_val, marker="v",
                 color=PALETTE["cyan"], ms=10,
                 mec=PALETTE["text"], mew=0.7, zorder=6,
                 linestyle="None")

        # Place the text in the empty zone above the Delivered curve.
        # Vertical position: about 50% of the way from peak up to RF Budget.
        # Horizontal position: offset to the side opposite the peak's half
        # of the time axis so the text always stays inside the figure.
        text_y = peak_val + 0.50 * (rf_max - peak_val)
        if peak_time < 0.55 * t_max:
            text_x = peak_time + 0.08 * t_max
            ha     = "left"
            rad    = -0.20    # arrow curves down-and-right toward marker
        else:
            text_x = peak_time - 0.08 * t_max
            ha     = "right"
            rad    = 0.20     # arrow curves down-and-left toward marker

        ax1.annotate(
            f"Peak Delivered Power\n{peak_val:.3f} MW  @  t = {peak_time:.2f} h",
            xy=(peak_time, peak_val),
            xytext=(text_x, text_y),
            color=PALETTE["cyan"],
            fontsize=FONT_PEAK_CALLOUT,
            fontweight="bold",
            ha=ha, va="center",
            bbox=dict(boxstyle="round,pad=0.40",
                      facecolor="#e6f4f6",       # very pale cyan tint
                      edgecolor=PALETTE["cyan"],
                      lw=1.2, alpha=0.95),
            arrowprops=dict(arrowstyle="-|>",
                            color=PALETTE["cyan"], lw=1.6,
                            connectionstyle=f"arc3,rad={rad}",
                            shrinkA=4, shrinkB=6),
            zorder=7,
        )

    ax1.set_ylabel("Power  [MW]", labelpad=6)
    ax1.set_ylim(0, max(rf.max() * 1.10, 1.0) if rf.size else 1.0)
    ax1.legend(loc="upper right", ncol=1, framealpha=0.7)
    ax1.tick_params(axis="both", which="both", direction="in", length=4)

    # ----- BOTTOM PANEL: WPT efficiency -----
    ax2.fill_between(tv, ef, alpha=0.18, color=PALETTE["green"],
                     edgecolor="none", zorder=2)
    ax2.plot(tv, ef, color=PALETTE["green"], lw=1.0,
             label="End-to-End WPT \u03B7", zorder=3)

    ax2.set_xlabel("Simulation Time  [hr]", labelpad=6)
    ax2.set_ylabel("WPT \u03B7  [%]", labelpad=6)
    ax2.set_ylim(0, max(ef.max() * 1.15, 1.0) if ef.size else 1.0)
    ax2.legend(loc="upper right", ncol=1, framealpha=0.7)
    ax2.tick_params(axis="both", which="both", direction="in", length=4)

    if tv.size:
        ax2.set_xticks(np.arange(0, tv[-1] + 0.5, 2))
        ax2.set_xlim(tv[0], tv[-1])

    fig.tight_layout()
    save_fig(fig, "fig1_rf_vs_delivered")
    plt.close(fig)


# ============================================================
# Fig 2 --- Per-Station Demand vs Mean Delivered Power
# (Single allocator policy, time-averaged over the full 24 h run)
# ============================================================
def fig_demand_vs_delivered(sim, mean_del_kW):
    """
    Two grouped bars per station:  demand (orange, semi-transparent) and
    mean delivered DC power (per-station color from GS_COLORS). Numeric
    labels are placed above each delivered bar.
    """
    apply_style()
    n         = sim.n_gs
    gs_names  = [g.name           for g in sim.ground_stations]
    demands   = [g.demand_W / 1e3 for g in sim.ground_stations]
    delivered = mean_del_kW

    x = np.arange(n)
    w = 0.35

    fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=PALETTE["bg"])

    ax.bar(x - w/2, demands, w, color=PALETTE["orange"], alpha=0.55,
           label="Demand (kW)", zorder=2, edgecolor="none")
    bars_del = ax.bar(x + w/2, delivered, w,
                      color=[GS_COLORS[j] for j in range(n)], alpha=0.90,
                      label="Mean Delivered (kW)", zorder=3, edgecolor="none")

    label_offset = max(demands) * 0.012
    for rect, val in zip(bars_del, delivered):
        if val > 0:
            ax.text(rect.get_x() + rect.get_width()/2.0,
                    rect.get_height() + label_offset,
                    f"{val:.0f}", ha="center", va="bottom",
                    fontsize=FONT_BAR_VALUE, color=PALETTE["text"])

    ax.set_xticks(x)
    ax.set_xticklabels(gs_names, rotation=35, ha="right", fontsize=FONT_GS_NAME)
    ax.set_xlabel("Ground Station", labelpad=6)
    ax.set_ylabel("Power  [kW]", labelpad=6)
    ax.legend(loc="upper right", ncol=2)
    fig.tight_layout()
    save_fig(fig, "fig2_demand_vs_delivered")
    plt.close(fig)


# ============================================================
# Fig 3 --- Per-Station Received RF Power Density at the Rectenna
# (Replaces the original CNR plot. CNR is a comm-link metric and is
#  inappropriate for a power-transmission link.)
# ============================================================
def fig_received_pd(result):
    """
    Per-station received RF power density at the rectenna [W/m²].
    Two bars per station: 24-h peak (instantaneous) and 24-h mean.
    Two horizontal reference lines mark the enforced exposure and design
    limits:
        * ICNIRP general-public limit  10 W/m²  (the binding threshold
          under the journal scenario, since cluster sites are near
          population centres)
        * Rectenna rated power density 100 W/m²
    Stations with no service across the full 24 h are flagged.
    """
    apply_style()
    sim       = result["sim"]
    n         = sim.n_gs
    gs_names  = [g.name for g in sim.ground_stations]
    mean_pd   = result["mean_pd_W_m2"]
    peak_pd   = result["peak_pd_W_m2"]

    # Floor zeros to a small visible value on log scale so unserved stations
    # remain distinguishable from the y-axis.
    mean_pd_v = [max(v, 1e-3) for v in mean_pd]
    peak_pd_v = [max(v, 1e-3) for v in peak_pd]

    x = np.arange(n)
    w = 0.36

    fig, ax = plt.subplots(figsize=(11, 5.8), facecolor=PALETTE["bg"])

    bars_peak = ax.bar(x - w/2, peak_pd_v, w, color=PALETTE["amber"], alpha=0.92,
                       edgecolor="none", label="Peak (instantaneous)", zorder=3)
    bars_mean = ax.bar(x + w/2, mean_pd_v, w, color=PALETTE["cyan"], alpha=0.92,
                       edgecolor="none", label="Mean  (24-h average)", zorder=3)

    # ----- Reference thresholds (journal version: drop occupational 50 W/m^2) -----
    ax.axhline(10,  color=PALETTE["green"], lw=1.5, ls="--", alpha=0.95,
               label="ICNIRP general-public limit  (10 W/m\u00B2)", zorder=2)
    ax.axhline(100, color=PALETTE["red"],   lw=1.5, ls=":",  alpha=0.95,
               label="Rectenna rated PD  (100 W/m\u00B2)",          zorder=2)

    # ----- Numeric labels on peak bars -----
    for rect, val in zip(bars_peak, peak_pd):
        if val > 1e-3:
            label = f"{val:.2f}" if val < 10 else f"{val:.1f}"
            ax.text(rect.get_x() + rect.get_width()/2,
                    rect.get_height() * 1.18,
                    label, ha="center", va="bottom",
                    fontsize=FONT_BAR_VALUE, color=PALETTE["amber"], fontweight="bold")

    # ----- "no service" annotation for stations with no delivery -----
    for j in range(n):
        if peak_pd[j] < 1e-3:
            ax.text(j, 1.5e-3, "no service",
                    ha="center", va="bottom",
                    fontsize=FONT_NO_SERVICE, color=PALETTE["red"],
                    fontweight="bold", style="italic")

    ax.set_xticks(x)
    ax.set_xticklabels(gs_names, rotation=35, ha="right", fontsize=FONT_GS_NAME)
    ax.set_xlabel("Ground Station", labelpad=6)
    ax.set_ylabel("RF Power Density  [W/m\u00B2]", labelpad=6)
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1e3)   # extra headroom for legend inside plot
    ax.legend(loc="upper right", ncol=2, fontsize=FONT_LEGEND-2,
              framealpha=0.92, columnspacing=1.0)

    fig.tight_layout()
    save_fig(fig, "fig3_received_pd")
    plt.close(fig)


# ============================================================
# Fig 4 --- Per-Station Operational Rectenna Efficiency vs Design Band
# (Replaces the original static-parameter figure. Operational efficiency
#  is the load-dependent value averaged over the actively-served steps
#  in a 24-h run.)
# ============================================================
def fig_rectenna_eff_operational(result):
    """
    Per-station operational rectenna efficiency over the 24-h run, plotted
    against each station's static design band:
        * shaded box      design band, eta_min ... eta_peak
        * cyan circle     eta_peak (provisioned, at 100 W/m² rated PD)
        * purple triangle eta_min  (low-load floor)
        * green bar       operational mean eta (averaged over active steps)

    The takeaway is that operational eta tracks eta_min closely because
    incident power density at LEO is two orders of magnitude below the
    100 W/m² rated PD.
    """
    apply_style()
    sim       = result["sim"]
    n         = sim.n_gs
    gs_names  = [g.name                    for g in sim.ground_stations]
    eta_peak  = [g.rectenna_eff_peak*100.0 for g in sim.ground_stations]
    eta_min   = [g.rectenna_eff_min *100.0 for g in sim.ground_stations]
    eta_op    = result["mean_eta_op"]

    x = np.arange(n)
    fig, ax = plt.subplots(figsize=(11, 5.8), facecolor=PALETTE["bg"])

    # ----- Design band as shaded boxes per station -----
    for xi, lo, hi in zip(x, eta_min, eta_peak):
        ax.fill_betweenx([lo, hi], xi-0.32, xi+0.32,
                         color=PALETTE["cyan"], alpha=0.18, zorder=1)

    # ----- Boundary markers -----
    ax.plot(x, eta_peak, "o", color=PALETTE["cyan"], ms=10,
            mec=PALETTE["text"], mew=0.6, linestyle="None",
            label="\u03B7_peak  (provisioned, at 100 W/m\u00B2)", zorder=4)
    ax.plot(x, eta_min,  "v", color=PALETTE["purple"], ms=10,
            mec=PALETTE["text"], mew=0.6, linestyle="None",
            label="\u03B7_min  (low-load floor)", zorder=4)

    # ----- Operational mean as bars -----
    bars = ax.bar(x, eta_op, 0.42, color=PALETTE["green"], alpha=0.90,
                  edgecolor="none",
                  label="Operational mean \u03B7  (24-h average)", zorder=3)
    for rect, val in zip(bars, eta_op):
        if val > 0.5:
            ax.text(rect.get_x() + rect.get_width()/2, val + 1.2,
                    f"{val:.1f}%", ha="center", va="bottom",
                    fontsize=FONT_BAR_VALUE, color=PALETTE["green"], fontweight="bold")

    # ----- "no service" annotation -----
    for j in range(n):
        if eta_op[j] < 0.5:
            ax.text(j, 5, "no service",
                    ha="center", va="bottom",
                    fontsize=FONT_NO_SERVICE, color=PALETTE["red"],
                    fontweight="bold", style="italic")

    ax.set_xticks(x)
    ax.set_xticklabels(gs_names, rotation=35, ha="right", fontsize=FONT_GS_NAME)
    ax.set_xlabel("Ground Station", labelpad=6)
    ax.set_ylabel("Rectenna Efficiency  [%]", labelpad=6)
    ax.set_ylim(0, 115)   # headroom for inside-plot legend
    ax.legend(loc="upper center", ncol=3, fontsize=FONT_LEGEND-2,
              framealpha=0.92, columnspacing=1.5)

    fig.tight_layout()
    save_fig(fig, "fig4_rectenna_eff_operational")
    plt.close(fig)


# ============================================================
# =========  CROSS-POLICY COMPARISON FIGURES (Section IV)  ===
# ============================================================
# Each function takes one or more `summary` dicts (the per-policy
# summary objects produced by the step drivers) and writes a single
# PDF to OUTPUT_DIR. Callers should:
#     plot_V4.OUTPUT_DIR = '/path/to/comparison/dir'
#     plot_V4.apply_style()
#     plot_V4.fig_compA_headline_metrics(summary)
#     plot_V4.fig_compB_per_station(summary)
#     ... etc.

def _policy_xpos_labels_colors(policies=POLICY_ORDER):
    """Return aligned (xpos, labels, colors) arrays for the policy axis."""
    xpos   = np.arange(len(policies))
    labels = [POLICY_LABEL[p] for p in policies]
    colors = [POLICY_COLOR[p] for p in policies]
    return xpos, labels, colors


def fig_compA_headline_metrics(summary, suptitle_extra=""):
    """
    Comp A : three-panel bar chart of headline metrics across policies.
        left  : Total Mean Delivered (kW)
        mid   : Jain Fairness Index
        right : Worst-Served Demand-Met Ratio

    `summary` is a dict keyed by policy name ('greedy', 'prop_fair',
    'min_demand', 'lp_optimal') with at least the keys:
        'total_mean_kW', 'jain', 'worst_dmr'.
    `suptitle_extra` is appended to the figure suptitle, e.g.
    "(total demand 1500 kW)".
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in summary]
    xpos, labels, colors = _policy_xpos_labels_colors(policies)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), facecolor=PALETTE["bg"])
    fig.subplots_adjust(wspace=0.35)
    panels = [
        ("total_mean_kW", "Total Mean Delivered (kW)",         "{:.0f}"),
        ("jain",          "Jain Fairness Index",               "{:.3f}"),
        ("worst_dmr",     "Worst-Served Demand-Met Ratio",     "{:.3f}"),
    ]
    for ax, (key, title, fmt) in zip(axes, panels):
        vals = [summary[p][key] for p in policies]
        ax.bar(xpos, vals, color=colors, edgecolor="none", width=0.35)
        subplot_names = ["(a)", "(b)", "(c)"]

        for ax, (key, title, fmt), name in zip(axes, panels, subplot_names):

            vals = [summary[p][key] for p in policies]

            ax.bar(xpos, vals, color=colors, edgecolor="none", width=0.35)

    
            ax.text(
                0.5, -0.28,
                f"{name} {title}",
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontsize=12,
                # fontweight="bold"
                )

            ax.set_xticks(xpos)
            ax.set_xticklabels(labels, rotation=20, ha="right",
                       fontsize=FONT_LEGEND-1)

            ax.grid(axis="y", alpha=0.25)

            if "Jain" in title:
                ax.set_ylim(0, 1.10)
            else:
                ax.set_ylim(0, max(vals) * 1.18)

            for x, v in zip(xpos, vals):
                ax.text(
                    x, v + 0.02 * max(vals),
                    fmt.format(v),
                    ha="center",
                    va="bottom",
                    fontsize=FONT_BAR_VALUE,
                    # fontweight="bold"
                    )
        #ax.set_title(title, fontsize=FONT_LEGEND)
        ax.set_xticks(xpos)
        ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=FONT_LEGEND-1)
        ax.grid(axis="y", alpha=0.25)
        
    plt.subplots_adjust(bottom=0.25)
    save_fig(fig, "compA_headline_metrics")
    plt.close(fig)


def fig_compB_per_station(summary, demand_label_color="#1a1a1a"):
    """
    Comp B : per-station 24-h mean delivered, grouped bars
    (8 stations x 4 policies). Demand level drawn as a dashed
    horizontal segment over each station's group.

    `summary[policy]` must include:
        'mean_del_kW' (list of len n_gs),
        'demands_kW'  (list of len n_gs),
        'gs_names'    (list of len n_gs).
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in summary]
    gs_names   = summary[policies[0]]["gs_names"]
    demands_kW = summary[policies[0]]["demands_kW"]
    n_gs = len(gs_names);  n_pol = len(policies)
    bar_w = 0.8 / n_pol
    x = np.arange(n_gs)

    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=PALETTE["bg"])
    for i, p in enumerate(policies):
        offset = (i - (n_pol-1)/2.) * bar_w
        ax.bar(x + offset,
               [summary[p]["mean_del_kW"][j] for j in range(n_gs)],
               bar_w, color=POLICY_COLOR[p], edgecolor="none",
               label=POLICY_LABEL[p])
    for j, d in enumerate(demands_kW):
        ax.hlines(d, x[j]-0.45, x[j]+0.45,
                  colors=demand_label_color, linestyles="--",
                  linewidth=1.4, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(gs_names, rotation=25, ha="right", fontsize=FONT_GS_NAME)
    ax.set_ylabel("24-h Mean Delivered  (kW)")
   # ax.set_title("Per-Station Delivered Power, by Policy  (dashed: station demand)")
    # Legend placed outside the axes (to the right) so it does not occlude
    # the leftmost demand-marker dashes (London / Paris / Frankfurt).
    # ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0),
    #           ncol=1, framealpha=0.95, borderaxespad=0.)
    
    ax.legend(loc="upper right", ncol=1, framealpha=0.95, borderaxespad=0.)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig(fig, "compB_per_station")
    plt.close(fig)


def fig_compC_timeseries(time_series, suptitle_extra=""):
    """
    Comp C : 24-h time series of total delivered MW.

    Because all four policies are driven by the same orbital geometry, their
    absolute delivered-power curves visually overlap. To keep all four
    distinguishable, the figure uses two stacked panels:

        Top    : absolute total delivered DC (MW), all four policies,
                 with distinct linestyles so curves remain readable in
                 greyscale print.
        Bottom : difference vs LP upper bound (MW), heuristics only.
                 Because the heuristics drift below LP at different rates,
                 they SEPARATE clearly in this view -- making the policy
                 ordering visible at every orbital pass.

    `time_series` is a dict keyed by policy name; each value is a tuple
    (t_h_list, del_MW_list). Step drivers populate this with:
        time_series[mode] = (list(sim.hist['t_hr']),
                             list(sim.hist['delivered_MW']))
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in time_series]
    # Per-policy linestyle keeps curves visually distinct even when
    # absolute values overlap.
    LINESTYLE = {
        "greedy"    : "-",
        "prop_fair" : "--",
        "min_demand": "-.",
        "lp_optimal": ":",
    }
    LINEWIDTH = {
        "greedy"    : 1.6,
        "prop_fair" : 1.6,
        "min_demand": 1.6,
        "lp_optimal": 2.2,   # LP slightly heavier as the ceiling reference
    }

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(13, 6.5), sharex=True,
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12},
        facecolor=PALETTE["bg"])

    # ----- TOP: absolute delivered power, four policies overlaid -----
    for p in policies:
        t_h, del_MW = time_series[p]
        ax_top.plot(t_h, del_MW, color=POLICY_COLOR[p],
                    lw=LINEWIDTH[p], linestyle=LINESTYLE[p],
                    label=POLICY_LABEL[p], alpha=0.95)
    ax_top.set_ylabel("Total Delivered DC  [MW]")
   # ax_top.set_title(f"Total Delivered DC over 24 h, by Policy  {suptitle_extra}")
    ax_top.legend(loc="upper right", ncol=4, framealpha=0.95)
    ax_top.grid(alpha=0.3)

    # ----- BOTTOM: difference vs LP upper bound (heuristics only) -----
    if "lp_optimal" in time_series:
        t_lp, del_lp = time_series["lp_optimal"]
        import numpy as _np
        lp_arr = _np.asarray(del_lp)
        for p in [pp for pp in policies if pp != "lp_optimal"]:
            t_h, del_MW = time_series[p]
            # align on shorter length in case of edge-case offset
            n = min(len(del_MW), len(lp_arr))
            diff = (_np.asarray(del_MW[:n]) - lp_arr[:n]) * 1000.0  # to kW
            ax_bot.plot(t_h[:n], diff, color=POLICY_COLOR[p],
                        lw=LINEWIDTH[p], linestyle=LINESTYLE[p],
                        label=POLICY_LABEL[p], alpha=0.95)
        ax_bot.axhline(0, color="#1a1a1a", lw=0.8, alpha=0.5)
        ax_bot.set_ylabel("Delivered \u2212 LP  [kW]")
        ax_bot.set_xlabel("Time  [h]")
        ax_bot.grid(alpha=0.3)
    else:
        # If LP isn't in the run, just label the bottom panel out
        ax_bot.set_xlabel("Time  [h]")
        ax_bot.set_ylabel("(LP not in this run)")

    fig.tight_layout()
    save_fig(fig, "compC_timeseries")
    plt.close(fig)


def fig_compD_visibility_histogram(summary):
    """
    Comp D : histogram of (# visible GS per satellite-step) at the
    scenario level. Uses the visibility_hist counter from any policy
    (it is scenario-driven, not policy-driven). Labels each bar with
    its % of total sat-steps if > 0.3 %.
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in summary]
    vh = summary[policies[0]].get("visibility_hist", [])
    if not vh:
        print("  [WARN] fig_compD: no visibility_hist in summary, skipping")
        return
    total = sum(vh)
    pct = [100.0 * v / max(total, 1) for v in vh]
    fig, ax = plt.subplots(figsize=(11, 4.5), facecolor=PALETTE["bg"])
    xv = np.arange(len(vh))
    ax.bar(xv, pct, width=0.4, color=PALETTE["cyan"], edgecolor="none", alpha=0.92)
    ax.set_xlabel("Number of Visible Ground Stations per Satellite-Step")
    ax.set_ylabel("Fraction of Sat-Steps  (%)")
   # ax.set_title(f"Visibility Histogram  (n_sat_steps = {total:,})")
    ax.grid(axis="y", alpha=0.3)
    ax.set_xticks(xv)
    # Headroom above the tallest bar so the percentage labels stay inside
    # the axis rectangle. 1.12x is enough for a single line of bold text.
    ax.set_ylim(0, max(pct) * 1.12)
    for xx, pp in zip(xv, pct):
        if pp > 0.3:
            ax.text(xx, pp + 0.3, f"{pp:.1f}%",
                    ha="center", va="bottom", fontsize=FONT_BAR_VALUE-1)
    fig.tight_layout()
    save_fig(fig, "compD_visibility_histogram")
    plt.close(fig)


def fig_compE_rf_utilisation(summary, suptitle_extra=""):
    """
    Comp E : RF capacity utilisation stacked bars per policy.
        bottom : delivered DC
        next   : link/conversion loss (transmitted RF - delivered DC)
        next   : discarded (cap fired, no redistribution target)
        top    : unallocated (panel RF that never reached the TX)

    Each bar is normalised to % of panel-generated RF.

    `summary[policy]` must include keys:
        'panel_MJ', 'tx_MJ', 'dc_MJ',
        'discarded_MJ', 'link_loss_MJ', 'unallocated_MJ'.
    The link_loss / unallocated keys are auto-derived if missing.
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in summary]
    # auto-derive missing keys
    for p in policies:
        s = summary[p]
        if "link_loss_MJ" not in s:
            s["link_loss_MJ"]   = max(s["tx_MJ"] - s["dc_MJ"], 0.0)
        if "unallocated_MJ" not in s:
            s["unallocated_MJ"] = max(s["panel_MJ"] - s["tx_MJ"]
                                      - s.get("discarded_MJ", 0.0), 0.0)

    xpos = np.arange(len(policies))
    panel = [summary[p]["panel_MJ"]      for p in policies]
    dcv   = [summary[p]["dc_MJ"]         for p in policies]
    llv   = [summary[p]["link_loss_MJ"]  for p in policies]
    dsv   = [summary[p]["discarded_MJ"]  for p in policies]
    unv   = [summary[p]["unallocated_MJ"]for p in policies]
    def pct_of(num, den):
        return [100.0 * n / max(d, 1e-9) for n, d in zip(num, den)]
    dc_p, ll_p = pct_of(dcv, panel), pct_of(llv, panel)
    ds_p, un_p = pct_of(dsv, panel), pct_of(unv, panel)

    fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=PALETTE["bg"])
    ax.bar(xpos, dc_p, label="Delivered as DC",
           color="#2e8b3d", edgecolor="#3a3f52", linewidth=0.6)
    ax.bar(xpos, ll_p, bottom=dc_p,
           label="Link / conversion loss",
           color="#1d72b8", edgecolor="#3a3f52", linewidth=0.6)
    ax.bar(xpos, ds_p, bottom=[a+b for a, b in zip(dc_p, ll_p)],
           label="Discarded (cap, no redist.)",
           color="#a445b2", edgecolor="#3a3f52", linewidth=0.6)
    ax.bar(xpos, un_p, bottom=[a+b+c for a, b, c in zip(dc_p, ll_p, ds_p)],
           label="Unallocated (no visible GS)",
           color="#b8bcc5", edgecolor="#3a3f52", linewidth=0.6)

    ax.set_xticks(xpos)
    ax.set_xticklabels([POLICY_LABEL[p] for p in policies])
    # Two-line y-axis label keeps text inside the figure margins.
    ax.set_ylabel("% of Panel-Generated RF\n(24-h cumulative)")
    # ax.set_title(f"RF Capacity Utilisation by Policy  "
    #              f"(panel total = {panel[0]:.0f} MJ)  {suptitle_extra}")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, 105)
    for x, d in zip(xpos, dc_p):
        ax.text(x, d/2, f"{d:.1f}%", ha="center", va="center",
                fontsize=FONT_BAR_VALUE, fontweight="bold",
                color="#ffffff")
    fig.tight_layout()
    save_fig(fig, "compE_rf_utilisation")
    plt.close(fig)


def fig_compF_demand_met_fraction(summary, total_demand_kW=None):
    """
    Comp F : per-station demand-met fraction (%), grouped bars
    (8 stations x 4 policies). White dashed line at 100 % = full
    demand met.

    `summary[policy]` must include:
        'dmr_per_station' (list of len n_gs, in [0,1]),
        'gs_names'.
    """
    apply_style()
    policies = [p for p in POLICY_ORDER if p in summary]
    gs_names = summary[policies[0]]["gs_names"]
    n_gs = len(gs_names);  n_pol = len(policies)
    bar_w = 0.8 / n_pol
    x = np.arange(n_gs)

    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=PALETTE["bg"])
    for i, p in enumerate(policies):
        offset = (i - (n_pol-1)/2.) * bar_w
        dmr_pct = [summary[p]["dmr_per_station"][j]*100 for j in range(n_gs)]
        ax.bar(x + offset, dmr_pct, bar_w,
               color=POLICY_COLOR[p], edgecolor="none",
               label=POLICY_LABEL[p])
    ax.axhline(100, color="#1a1a1a", linestyle="--", linewidth=1.4,
               alpha=0.75, label="100 % (full demand met)")
    ax.set_xticks(x)
    ax.set_xticklabels(gs_names, rotation=25, ha="right", fontsize=FONT_GS_NAME)
    ax.set_ylabel("24-h Demand-Met Ratio  (%)")
    title = "Per-Station Demand-Met Fraction, by Policy"
    if total_demand_kW is not None:
        title += f"  (total demand {int(total_demand_kW)} kW)"
   # ax.set_title(title)
    # Legend placed outside the axes (to the right) so the 100% reference
    # line and the bars themselves stay unobstructed at all stations.
    # ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0),
    #           ncol=1, framealpha=0.95, borderaxespad=0.)
    ax.legend(loc="upper right", ncol=1, framealpha=0.95, borderaxespad=0.)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig(fig, "compF_demand_met_fraction")
    plt.close(fig)


def fig_compG_demand_sensitivity(step_summaries):
    """
    Comp G : two-panel demand sensitivity scan over multiple scenarios.
        left  : gap-to-LP vs total demand for each heuristic
        right : total delivered vs total demand for all four policies

    `step_summaries` is a list of tuples:
        [(total_demand_kW, label, summary_dict), ...]
    in ascending demand order. Example:
        [(850., 'Step 4', summary4),
         (1500., 'Step 6', summary6),
         (2500., 'Step 5', summary5)]
    """
    apply_style()
    demands = [d[0] for d in step_summaries]
    labels  = [d[1] for d in step_summaries]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=PALETTE["bg"])

    # left panel: gap to LP, heuristics only
    ax = axes[0]
    for p in HEURISTIC_ORDER:
        gaps = []
        for D, lab, s in step_summaries:
            lp = s["lp_optimal"]["total_mean_kW"]
            gaps.append(100. * (lp - s[p]["total_mean_kW"]) / max(lp, 1e-9))
        ax.plot(demands, gaps, "-o", color=POLICY_COLOR[p], lw=2.4, ms=10,
                label=POLICY_LABEL[p],
                markeredgecolor="#3a3f52", markeredgewidth=1.2)
    ax.set_xlabel("Total Cluster Demand  (kW)")
    ax.set_ylabel("Gap to LP Upper Bound  (%)")
   # ax.set_title("Distance from LP-Optimal vs Demand Level")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(alpha=0.3)
    ax.set_xticks(demands)

    # right panel: absolute delivered, all four policies
    ax = axes[1]
    for p in POLICY_ORDER:
        vals = [s[p]["total_mean_kW"] for _, _, s in step_summaries]
        ax.plot(demands, vals, "-o", color=POLICY_COLOR[p], lw=2.4, ms=10,
                label=POLICY_LABEL[p],
                markeredgecolor="#3a3f52", markeredgewidth=1.2)
    ax.set_xlabel("Total Cluster Demand  (kW)")
    ax.set_ylabel("Total Mean Delivered  (kW)")
  #  ax.set_title("Total Delivered vs Demand Level, by Policy")
    ax.legend(loc="upper left", ncol=2, framealpha=0.9)
    ax.grid(alpha=0.3)
    ax.set_xticks(demands)
    # label each demand point with its source step
    for D, lab, s in step_summaries:
        yvals = [s[p]["total_mean_kW"] for p in POLICY_ORDER]
        ax.annotate(lab, (D, max(yvals)+12), ha="center", va="bottom",
                    fontsize=FONT_BAR_VALUE-1, fontweight="bold",
                    color=PALETTE["text"])

    axes[0].text(
        0.5, -0.28,
        "(a) Distance from LP-Optimal vs. Demand Level",
        transform=axes[0].transAxes, ha="center", va="top", fontsize=14)#,fontweight="bold")

    axes[1].text(
        0.5, -0.28,"(b) Total Delivered vs. Demand Level",
        transform=axes[1].transAxes,ha="center", va="top", fontsize=14)#, fontweight="bold")
    fig.tight_layout()
    save_fig(fig, "compG_demand_sensitivity")
    plt.close(fig)


# ============================================================
# =========  SENSITIVITY-SWEEP FIGURES (Section V)  ==========
# ============================================================
# Each function takes the merged sensitivity grid from Step 7 and
# writes a single PDF. `grid` shape: grid[alt][n_sats][policy] -> metrics.

def _sens_grid_axes(grid):
    altitudes  = sorted(grid.keys())
    sat_totals = sorted(next(iter(grid.values())).keys())
    return altitudes, sat_totals


def fig_sensA_delivered_vs_altitude(grid):
    """
    Sens A : total delivered vs altitude, faceted by constellation size
    (one subplot per n_sats; all four policies on each subplot).
    """
    apply_style()
    altitudes, sat_totals = _sens_grid_axes(grid)
    fig, axes = plt.subplots(1, len(sat_totals), figsize=(15, 4.7),
                              sharey=False, facecolor=PALETTE["bg"])
    if len(sat_totals) == 1:
        axes = [axes]
    for ax, n_total in zip(axes, sat_totals):
        for p in POLICY_ORDER:
            vals = [grid[a][n_total][p]["total_mean_kW"] for a in altitudes]
            ax.plot(altitudes, vals, "-o", color=POLICY_COLOR[p],
                    lw=2.2, ms=9, label=POLICY_LABEL[p],
                    markeredgecolor="#3a3f52", markeredgewidth=1.1)
      #  ax.set_title(f"{n_total} satellites", fontsize=FONT_LEGEND)
        ax.set_xlabel("Altitude  [km]")
        ax.grid(alpha=0.3)
        ax.set_xticks(altitudes)
    axes[0].set_ylabel("Total Mean Delivered  [kW]")
    axes[-1].legend(loc="upper left", fontsize=FONT_LEGEND-2, framealpha=0.9)
    fig.suptitle("Sensitivity: Total Delivered vs Altitude, by Constellation Size & Policy",
                 fontsize=FONT_AXIS_LABEL-2, y=1.03)
    fig.tight_layout()
    save_fig(fig, "sensA_delivered_vs_altitude")
    plt.close(fig)


def fig_sensB_gap_to_LP(grid):
    """
    Sens B : gap-to-LP vs altitude, faceted by constellation size.
    Heuristic policies only (LP is the baseline by construction).
    Y-axis shared across subplots so altitude trends are comparable.
    """
    apply_style()
    altitudes, sat_totals = _sens_grid_axes(grid)
    fig, axes = plt.subplots(1, len(sat_totals), figsize=(15, 4.7),
                              sharey=True, facecolor=PALETTE["bg"])
    if len(sat_totals) == 1:
        axes = [axes]
    for ax, n_total in zip(axes, sat_totals):
        for p in HEURISTIC_ORDER:
            lp_vals  = [grid[a][n_total]["lp_optimal"]["total_mean_kW"] for a in altitudes]
            pol_vals = [grid[a][n_total][p]["total_mean_kW"] for a in altitudes]
            gaps = [100.*(lp-v)/max(lp,1e-9) for lp, v in zip(lp_vals, pol_vals)]
            ax.plot(altitudes, gaps, "-o", color=POLICY_COLOR[p],
                    lw=2.2, ms=9, label=POLICY_LABEL[p],
                    markeredgecolor="#3a3f52", markeredgewidth=1.1)
     #   ax.set_title(f"{n_total} satellites", fontsize=FONT_LEGEND)
        ax.set_xlabel("Altitude  [km]")
        ax.grid(alpha=0.3)
        ax.set_xticks(altitudes)
    axes[0].set_ylabel("Gap to LP Upper Bound  [%]")
    axes[-1].legend(loc="upper left", fontsize=FONT_LEGEND-2, framealpha=0.9)
    fig.suptitle("Sensitivity: Gap to LP vs Altitude, by Constellation Size & Heuristic",
                 fontsize=FONT_AXIS_LABEL-2, y=1.03)
    fig.tight_layout()
    save_fig(fig, "sensB_gap_to_LP")
    plt.close(fig)


def fig_sensC_heatmaps(grid):
    """
    Sens C : 2x2 heatmap grid of min-demand performance across the
    (altitude x n_sats) design space, plus the multi-visibility geometry.
    Min-demand chosen because it is the most informative single policy.

    Panels:
        top-left  : total delivered (kW)        viridis
        top-right : Jain index                  plasma
        bot-left  : gap to LP (%)               inferno_r
        bot-right : multi-visibility (%)        cividis
    """
    apply_style()
    altitudes, sat_totals = _sens_grid_axes(grid)
    n_a, n_s = len(altitudes), len(sat_totals)

    arr_delivered = np.zeros((n_s, n_a))
    arr_jain      = np.zeros((n_s, n_a))
    arr_gap       = np.zeros((n_s, n_a))
    arr_mv        = np.zeros((n_s, n_a))
    for i, alt in enumerate(altitudes):
        for j, n_total in enumerate(sat_totals):
            md = grid[alt][n_total]["min_demand"]
            lp = grid[alt][n_total]["lp_optimal"]
            arr_delivered[j, i] = md["total_mean_kW"]
            arr_jain[j, i]      = md["jain"]
            arr_gap[j, i]       = 100.0 * (lp["total_mean_kW"] - md["total_mean_kW"]) \
                                  / max(lp["total_mean_kW"], 1e-9)
            arr_mv[j, i]        = md["multi_visibility_frac"] * 100

    def heat(ax, values, title, fmt, cmap):
        im = ax.imshow(values, aspect="auto", cmap=cmap, origin="lower")
        ax.set_xticks(range(n_a)); ax.set_xticklabels([f"{a}" for a in altitudes])
        ax.set_yticks(range(n_s)); ax.set_yticklabels([f"{n}" for n in sat_totals])
        ax.set_xlabel("Altitude  [km]"); ax.set_ylabel("# Satellites")
       # ax.set_title(title, fontsize=FONT_LEGEND)
        for j in range(values.shape[0]):
            for i in range(values.shape[1]):
                t = ax.text(i, j, fmt.format(values[j, i]),
                            ha="center", va="center",
                            fontsize=FONT_BAR_VALUE, color="white", fontweight="bold")
                # thin black outline keeps the text readable on any colormap
                t.set_path_effects([
                    mpe.Stroke(linewidth=2.0, foreground="black"),
                    mpe.Normal(),
                ])
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), facecolor=PALETTE["bg"])
    heat(axes[0,0], arr_delivered, "Min-Demand: Total Delivered  [kW]", "{:.0f}", "viridis")
    heat(axes[0,1], arr_jain,      "Min-Demand: Jain Index",            "{:.3f}", "plasma")
    heat(axes[1,0], arr_gap,       "Min-Demand: Gap to LP  [%]",        "{:.2f}", "inferno_r")
    heat(axes[1,1], arr_mv,        "Multi-Visibility Fraction  [%]",    "{:.1f}", "cividis")
    fig.suptitle("Sensitivity Heatmaps  (Min-Demand, Step 6 demand baseline)",
                 fontsize=FONT_AXIS_LABEL-2, y=1.00)
    fig.tight_layout()
    save_fig(fig, "sensC_heatmaps")
    plt.close(fig)


def fig_sensD_jain_vs_altitude(grid, ylim=(0.85, 1.0)):
    """
    Sens D : Jain index vs altitude, faceted by constellation size.
    All four policies overlaid on each subplot.
    """
    apply_style()
    altitudes, sat_totals = _sens_grid_axes(grid)
    fig, axes = plt.subplots(1, len(sat_totals), figsize=(15, 4.7),
                              sharey=True, facecolor=PALETTE["bg"])
    if len(sat_totals) == 1:
        axes = [axes]
    for ax, n_total in zip(axes, sat_totals):
        for p in POLICY_ORDER:
            vals = [grid[a][n_total][p]["jain"] for a in altitudes]
            ax.plot(altitudes, vals, "-o", color=POLICY_COLOR[p],
                    lw=2.2, ms=9, label=POLICY_LABEL[p],
                    markeredgecolor="#3a3f52", markeredgewidth=1.1)
      #  ax.set_title(f"{n_total} satellites", fontsize=FONT_LEGEND)
        ax.set_xlabel("Altitude  [km]")
        ax.grid(alpha=0.3)
        ax.set_xticks(altitudes)
        ax.set_ylim(*ylim)
    axes[0].set_ylabel("Jain Fairness Index")
    axes[-1].legend(loc="lower right", fontsize=FONT_LEGEND-2, framealpha=0.9)
    fig.suptitle("Sensitivity: Jain Index vs Altitude, by Constellation Size & Policy",
                 fontsize=FONT_AXIS_LABEL-2, y=1.03)
    fig.tight_layout()
    save_fig(fig, "sensD_jain_vs_altitude")
    plt.close(fig)


def fig_sens_set(grid):
    """Convenience: build all four sensitivity figures from one grid."""
    fig_sensA_delivered_vs_altitude(grid)
    fig_sensB_gap_to_LP(grid)
    fig_sensC_heatmaps(grid)
    fig_sensD_jain_vs_altitude(grid)


# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print(" The AEL-funded Project, University of Manitoba")
    print("  Conference-ready results for SBSP LEO  (VTC2026-Fall)")
    print("=" * 65)

    result = run_simulation(DURATION_HOURS, ALLOC_MODE)

    print("\n[FIGURES]  Generating figures ...\n")
    apply_style()

    fig_rf_vs_delivered          (result["sim"])
    fig_demand_vs_delivered      (result["sim"], result["mean_del_kW"])
    fig_received_pd              (result)
    fig_rectenna_eff_operational (result)

    print("\n  All figures saved to:", os.path.abspath(OUTPUT_DIR))