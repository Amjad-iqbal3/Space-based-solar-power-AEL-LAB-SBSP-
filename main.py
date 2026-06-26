# -*- coding: utf-8 -*-
"""
================================================================================
run_journal_figures.py  --  SBSP LEO Journal Extension, Section IV figure set

Single-file driver that runs a 24-hour SBSP simulation across all four
allocator policies (greedy / prop_fair / min_demand / lp_optimal) AT
THREE DEMAND LEVELS, and generates every figure in Section IV of the
IEEE TVT submission:

  Per-policy figures (16 PDFs total, 4 per policy, HEADLINE scenario only):
    fig1_rf_vs_delivered           RF budget + delivered DC over 24 h
    fig2_demand_vs_delivered       per-station demand vs mean delivered
    fig3_received_pd               per-station incident RF power density
    fig4_rectenna_eff_operational  per-station operational rectenna eta

  Cross-policy comparison figures (6 PDFs, Section IV set A/B/D/E/F/G):
    compA_headline_metrics         total / Jain / worst-DMR bar chart
    compB_per_station              per-station delivered, grouped bars
    compD_visibility_histogram     # visible GS per sat-step
    compE_rf_utilisation           panel -> delivered/loss/discard stack
    compF_demand_met_fraction      per-station DMR, 8 x 4 grouped bars
    compG_demand_sensitivity       gap-to-LP vs total demand (3 scenarios)

Note: compC (time-series overlay) was dropped from the journal set because
the four policies' delivered-power profiles are nearly identical in the
time domain (orbital geometry dominates); compG replaces it as the sixth
comparison figure with a regime-map view of policy differentiation.

Total: 22 PDFs at IEEE-camera-ready 300 DPI vector quality.

Defaults match the manuscript headline scenario:
  altitude       : 450 km    (-a / --altitude)
  constellation  : 4 planes x 5 sats = 20 sats  (-p / --n_planes, -s / --sats_per_plane)
  duration       : 24 h      (-d / --duration)
  demand scale   : 1.0       (-D / --demand_scale; multiplies the baseline
                              per-station demands in GROUND_STATION_TABLE
                              inside SBSP_env.py)

The baseline per-station demands ship as Phase-1 engineering-pilot scales
(160-360 kW each, 1,800 kW cluster total), sized to representative data-
centre / industrial pilot loads in each European city. To change demands
for one or more cities specifically, edit GROUND_STATION_TABLE directly.
To uniformly scale all demands, use --demand_scale.

The compG demand-sensitivity sweep runs at 0.5x and 1.5x of the headline
demand (e.g. 900 / 1,800 / 2,700 kW at default scale = 1.0). Use
--skip_sensitivity to bypass it (5 comp figures instead of 6, ~3x faster).

Wall clock at defaults:
  Headline only (--skip_sensitivity)            : ~3 minutes
  Headline + compG sensitivity (default)        : ~9 minutes

Requirements: Python 3.10+, numpy, scipy, matplotlib. Files in same
directory as this script:
  SBSP_env.py  (the journal-version patched simulation)
  plot_V4.py              (the consolidated journal-version plotter)

Usage:
    python3 run_journal_figures.py                          # defaults (full 6-figure set)
    python3 run_journal_figures.py --skip_sensitivity       # 5 figures, faster
    python3 run_journal_figures.py -a 550 -p 8 -s 5         # 40 sats at 550 km
    python3 run_journal_figures.py --demand_scale 1.39      # 2,500 kW total headline
    python3 run_journal_figures.py -o ./figures_run01       # custom output dir
================================================================================
"""

import sys, os, types, json, time, argparse


def _shim_tkinter():
    """Allow plot_V4 / sim module imports without a display backend."""
    for mod in ['tkinter', 'tkinter.ttk', 'tkinter.messagebox']:
        sys.modules[mod] = types.ModuleType(mod)
    sys.modules['tkinter'].Tk = type('Tk', (), {})


def parse_args():
    p = argparse.ArgumentParser(
        description='SBSP LEO journal-version figure generator (Section IV).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-a', '--altitude', type=float, default=450.0,
                   help='Orbital altitude [km]')
    p.add_argument('-p', '--n_planes', type=int, default=4,
                   help='Number of orbital planes (Walker delta)')
    p.add_argument('-s', '--sats_per_plane', type=int, default=5,
                   help='Satellites per orbital plane')
    p.add_argument('-d', '--duration', type=float, default=24.0,
                   help='Simulation duration [hours]')
    p.add_argument('-D', '--demand_scale', type=float, default=1.0,
                   help='Uniform multiplier on per-station demands in '
                        'GROUND_STATION_TABLE (baseline total: 1,800 kW)')
    p.add_argument('-o', '--output_dir', type=str,
                   default='./journal_figures',
                   help='Root directory for output figures (created if absent)')
    p.add_argument('-P', '--policies', type=str,
                   default='greedy,prop_fair,min_demand,lp_optimal',
                   help='Comma-separated allocator policies to run')
    p.add_argument('--skip_sensitivity', action='store_true',
                   help='Skip the three-demand sweep used for compG. '
                        'Faster (~3 min vs ~9 min) but produces only 5 comp '
                        'figures (A, B, D, E, F) instead of 6 (adds G).')
    return p.parse_args()


# ------------------------------------------------------------------------------
def main():
    args = parse_args()

    _shim_tkinter()
    import matplotlib
    matplotlib.use('Agg')

    # The script expects SBSP_env.py and plot_V4.py to be on the
    # Python path. The simplest case is they sit next to this file.
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)

    # Force fresh import so any patches / monkey-overrides are reapplied
    # cleanly if the script is invoked twice in one Python session.
    for m in ('SBSP_env', 'plot_V4'):
        if m in sys.modules: del sys.modules[m]

    try:
        import SBSP_env as sbsp
    except ImportError:
        print('\n  ERROR: cannot import SBSP_env.py from', here)
        print('  Place SBSP_env.py next to this script and re-run.\n')
        sys.exit(2)
    try:
        import plot_V4 as pv
    except ImportError:
        print('\n  ERROR: cannot import plot_V4.py from', here)
        print('  Place plot_V4.py next to this script and re-run.\n')
        sys.exit(2)

    # ----- patch overrides for command-line scenario tuning -----
    # demand_scale: multiplies the demand_W of every ground station produced
    # by build_ground_stations(). Applied dynamically (per scenario) below;
    # the CLI flag becomes the multiplier for the HEADLINE scenario only.
    orig_build = sbsp.build_ground_stations

    # current scale, mutated as the script walks through scenarios
    _scale_state = {'value': float(args.demand_scale)}
    def scaled_build():
        gs_list = orig_build()
        s = _scale_state['value']
        if abs(s - 1.0) > 1e-9:
            for g in gs_list:
                g.demand_W *= s
        return gs_list
    sbsp.build_ground_stations = scaled_build

    # altitude, n_planes, sats_per_plane go through plot_V4.run_simulation
    # via a small monkey-patch on SimParams.__init__ defaults. Cleaner than
    # editing run_simulation itself.
    orig_simparams_init = sbsp.SimParams.__init__
    def patched_init(self, *a, **kw):
        kw.setdefault('altitude_km',     args.altitude)
        kw.setdefault('n_planes',        args.n_planes)
        kw.setdefault('sats_per_plane',  args.sats_per_plane)
        orig_simparams_init(self, *a, **kw)
    sbsp.SimParams.__init__ = patched_init

    # ----- verification banner -----
    # measure the baseline total demand at the user-requested scale
    _scale_state['value'] = float(args.demand_scale)
    gs_sample = sbsp.build_ground_stations()
    headline_demand_kW = sum(g.demand_W for g in gs_sample) / 1e3
    prm_sample = sbsp.SimParams()
    n_sats = args.n_planes * args.sats_per_plane

    print('=' * 78)
    print(' SBSP LEO  --  Journal Extension Figure Generator  (Section IV)')
    print('=' * 78)
    print(f"  Altitude              : {args.altitude:>7.1f} km")
    print(f"  Constellation         : {args.n_planes} planes x {args.sats_per_plane}"
          f" sats = {n_sats} sats")
    print(f"  Duration              : {args.duration:>7.1f} h")
    print(f"  Headline demand_scale : {args.demand_scale:>7.3f}x")
    print(f"  Headline total demand : {headline_demand_kW:>7.1f} kW")
    print(f"  ICNIRP cap            : {prm_sample.max_safe_pd_W_m2:>7.1f} W/m^2 (public)")
    print(f"  Policies              : {args.policies}")
    print(f"  Output dir            : {args.output_dir}")
    if args.skip_sensitivity:
        print(f"  Sensitivity sweep     : SKIPPED (compG will not be produced)")
    else:
        print(f"  Sensitivity sweep     : 0.5x / 1.0x / 1.5x of headline demand "
              f"({headline_demand_kW*0.5:.0f} / {headline_demand_kW:.0f} / "
              f"{headline_demand_kW*1.5:.0f} kW)")
    print('=' * 78)

    POLICIES = [p.strip() for p in args.policies.split(',') if p.strip()]
    for p in POLICIES:
        assert p in pv.POLICY_ORDER, \
            f"Unknown policy {p!r}; choices are {pv.POLICY_ORDER}"

    OUT_ROOT = os.path.abspath(args.output_dir)
    os.makedirs(OUT_ROOT, exist_ok=True)
    pv.apply_style()

    # ----- helper: run one demand scenario, return summary dict -----
    def run_one_demand_scenario(scale_factor, label, out_subdir,
                                 do_per_policy_figures):
        """
        Run all POLICIES at a given demand-scale factor. If
        do_per_policy_figures is True, save fig1-fig4 PDFs per policy into
        out_subdir/<policy>/. Always returns a (total_demand_kW, summary,
        time_series) triple suitable for fig_compG_demand_sensitivity.
        """
        _scale_state['value'] = float(args.demand_scale) * float(scale_factor)
        gs_check = sbsp.build_ground_stations()
        scenario_demand_kW = sum(g.demand_W for g in gs_check) / 1e3

        print('\n' + '#' * 78)
        print(f"  SCENARIO  {label}  --  total demand {scenario_demand_kW:.0f} kW "
              f"(scale = {_scale_state['value']:.3f}x)")
        print('#' * 78)

        summary = {}
        time_series = {}
        for mode in POLICIES:
            print('\n' + '-' * 78)
            print(f"  [{label}] policy = {mode.upper()}")
            print('-' * 78)

            if do_per_policy_figures:
                pv.OUTPUT_DIR = os.path.join(out_subdir, mode)
                os.makedirs(pv.OUTPUT_DIR, exist_ok=True)

            t0 = time.time()
            result = pv.run_simulation(args.duration, mode)
            elapsed = time.time() - t0
            print(f"  wall-clock for {mode}: {elapsed:.1f} s")

            if do_per_policy_figures:
                # 4 per-policy figures (only for the headline scenario)
                pv.fig_rf_vs_delivered          (result['sim'])
                pv.fig_demand_vs_delivered      (result['sim'],
                                                 result['mean_del_kW'])
                pv.fig_received_pd              (result)
                pv.fig_rectenna_eff_operational (result)

            sim         = result['sim']
            demands_kW  = [g.demand_W / 1e3 for g in sim.ground_stations]
            mean_del_kW = result['mean_del_kW']
            dmr = [mean_del_kW[i] / max(demands_kW[i], 1e-9)
                   for i in range(len(demands_kW))]
            n   = len(dmr)
            s1  = sum(dmr); s2 = sum(x * x for x in dmr)
            jain = (s1 * s1) / (n * s2) if s2 > 1e-12 else 0.0

            A = sim.allocator
            dt = sim.dt

            summary[mode] = {
                'total_mean_kW':         float(sum(mean_del_kW)),
                'mean_del_kW':           mean_del_kW,
                'demands_kW':            demands_kW,
                'dmr_per_station':       dmr,
                'jain':                  float(jain),
                'worst_dmr':             float(min(dmr) if dmr else 0.0),
                'served_count':          sum(1 for x in mean_del_kW if x > 1e-3),
                'gs_names':              [g.name for g in sim.ground_stations],
                'multi_visibility_frac': A.n_multi_visibility / max(A.n_sat_steps, 1),
                'binding_events_frac':   A.n_binding_events / max(A.n_sat_steps, 1),
                'safety_events_frac':    A.n_safety_binding_events / max(A.n_gs_steps, 1),
                'demand_events_frac':    A.n_demand_binding_events / max(A.n_gs_steps, 1),
                'visibility_hist':       list(A.visibility_hist) if A.visibility_hist else [],
                'panel_MJ':              A.cum_panel_RF      * dt / 1e6,
                'tx_MJ':                 A.cum_tx_RF         * dt / 1e6,
                'dc_MJ':                 A.cum_delivered_DC  * dt / 1e6,
                'discarded_MJ':          A.W_discarded       * dt / 1e6,
                'redistributed_MJ':      A.W_redistributed   * dt / 1e6,
            }
            time_series[mode] = (list(sim.hist['t_hr']),
                                 list(sim.hist['delivered_MW']))
        return scenario_demand_kW, summary, time_series

    # ----- run headline scenario (1.0x) -----
    t_total = time.time()
    headline_demand_kW, summary, time_series = run_one_demand_scenario(
        scale_factor=1.0, label='HEADLINE', out_subdir=OUT_ROOT,
        do_per_policy_figures=True)

    # ----- comparison figures from headline scenario (compA, B, D, E, F) -----
    print('\n' + '-' * 78)
    print('  Building cross-policy comparison figures (Comp A, B, D, E, F) '
          'from HEADLINE scenario ...')
    print('-' * 78)

    pv.OUTPUT_DIR = OUT_ROOT
    suptitle_tag = f"(total demand {headline_demand_kW:.0f} kW, " \
                    f"{n_sats} sats @ {args.altitude:.0f} km)"

    if all(p in summary for p in pv.POLICY_ORDER):
        pv.fig_compA_headline_metrics    (summary, suptitle_extra=suptitle_tag)
        pv.fig_compB_per_station         (summary)
        # NOTE: compC dropped; replaced by compG (demand sensitivity) below.
        pv.fig_compD_visibility_histogram(summary)
        pv.fig_compE_rf_utilisation      (summary)
        pv.fig_compF_demand_met_fraction (summary,
                                          total_demand_kW=headline_demand_kW)
    else:
        missing = set(pv.POLICY_ORDER) - set(summary.keys())
        print(f"  [SKIP] Cross-policy figures require all 4 policies. "
              f"Missing: {sorted(missing)}")

    # ----- save HEADLINE summary.json early, so it survives any later failure -----
    summary_path = os.path.join(OUT_ROOT, 'summary.json')
    with open(summary_path, 'w') as f:
        json.dump({
            'config': {
                'altitude_km'   : args.altitude,
                'n_planes'      : args.n_planes,
                'sats_per_plane': args.sats_per_plane,
                'duration_h'    : args.duration,
                'demand_scale'  : args.demand_scale,
                'policies'      : POLICIES,
                'total_demand_kW': headline_demand_kW,
                'n_sats'        : n_sats,
                'skip_sensitivity': args.skip_sensitivity,
            },
            'results': summary,
        }, f, indent=2, default=str)
    print(f"  [SAVED] headline summary: {summary_path}")

    # ----- compG demand-sensitivity sweep -----
    if not args.skip_sensitivity:
        print('\n' + '-' * 78)
        print('  Running demand-sensitivity scenarios (0.5x and 1.5x) for compG ...')
        print('-' * 78)

        low_demand_dir  = os.path.join(OUT_ROOT, 'scenario_low')
        high_demand_dir = os.path.join(OUT_ROOT, 'scenario_high')
        os.makedirs(low_demand_dir,  exist_ok=True)
        os.makedirs(high_demand_dir, exist_ok=True)

        low_demand_kW, low_summary, _ = run_one_demand_scenario(
            scale_factor=0.5, label='LOW (0.5x)', out_subdir=low_demand_dir,
            do_per_policy_figures=False)

        high_demand_kW, high_summary, _ = run_one_demand_scenario(
            scale_factor=1.5, label='HIGH (1.5x)', out_subdir=high_demand_dir,
            do_per_policy_figures=False)

        # save per-scenario summary JSON for traceability
        for d, s, sub in [(low_demand_kW, low_summary, low_demand_dir),
                          (high_demand_kW, high_summary, high_demand_dir)]:
            with open(os.path.join(sub, 'summary.json'), 'w') as f:
                json.dump({'total_demand_kW': d, 'results': s},
                          f, indent=2, default=str)

        # build the three-point summary list and produce compG
        if all(p in summary      for p in pv.POLICY_ORDER) and \
           all(p in low_summary  for p in pv.POLICY_ORDER) and \
           all(p in high_summary for p in pv.POLICY_ORDER):
            step_summaries = [
                (low_demand_kW,      f'{low_demand_kW:.0f} kW',  low_summary),
                (headline_demand_kW, f'{headline_demand_kW:.0f} kW', summary),
                (high_demand_kW,     f'{high_demand_kW:.0f} kW', high_summary),
            ]
            print('\n' + '-' * 78)
            print('  Building compG_demand_sensitivity from 3-point scan ...')
            print('-' * 78)
            pv.OUTPUT_DIR = OUT_ROOT
            pv.fig_compG_demand_sensitivity(step_summaries)
        else:
            print('  [SKIP] compG requires all 4 policies in all 3 scenarios')

    # ----- print summary table -----
    print('\n' + '=' * 92)
    print(f"  RESULTS SUMMARY  --  total demand {headline_demand_kW:.0f} kW, "
          f"{n_sats} sats @ {args.altitude:.0f} km, {args.duration:.0f} h")
    print('=' * 92)

    w = 14
    pol_names = [p for p in pv.POLICY_ORDER if p in summary]
    header_labels = {'greedy':'GREEDY', 'prop_fair':'PROP_FAIR',
                     'min_demand':'MIN_DEMAND', 'lp_optimal':'LP_OPTIMAL'}
    print(f"  {'Metric':<34}" +
          ''.join(f"{header_labels[p]:>{w}}" for p in pol_names))
    print('  ' + '-' * (34 + w * len(pol_names)))

    def row(label, fmt, key):
        vals = [summary[p][key] for p in pol_names]
        print(f"  {label:<34}" + ''.join(f"{fmt.format(v):>{w}}" for v in vals))

    row('Total mean delivered (kW)',    '{:.1f}', 'total_mean_kW')
    row('Jain fairness index',          '{:.4f}', 'jain')
    row('Worst-served DMR',             '{:.4f}', 'worst_dmr')
    row('Stations served (mean>1W)',    '{:d}',   'served_count')
    print()
    row('Multi-visibility/sat-steps',   '{:.3f}', 'multi_visibility_frac')
    row('Demand-bind/GS-steps',         '{:.3f}', 'demand_events_frac')
    row('Safety-bind/GS-steps',         '{:.5f}', 'safety_events_frac')
    print()
    row('RF redistributed (MJ/24h)',    '{:.1f}', 'redistributed_MJ')
    row('RF discarded (MJ/24h)',        '{:.1f}', 'discarded_MJ')

    # gap-to-LP
    if 'lp_optimal' in summary:
        lp_total = summary['lp_optimal']['total_mean_kW']
        print('\n  Distance from LP upper bound:')
        for m in ['greedy', 'prop_fair', 'min_demand']:
            if m in summary:
                gap = (lp_total - summary[m]['total_mean_kW']) / max(lp_total, 1e-9) * 100.
                print(f"    {m:<12} {summary[m]['total_mean_kW']:7.1f} kW  "
                      f"({gap:5.2f}% below LP)")

    total_wall = time.time() - t_total
    print('\n' + '=' * 92)
    print(f"  Total wall clock     : {total_wall/60.:.1f} min "
          f"({total_wall:.1f} s)")
    print(f"  Figures output dir   : {OUT_ROOT}")
    print(f"  Summary JSON         : {summary_path}")
    print('=' * 92)

    # ----- per-station detail table -----
    if all(p in summary for p in pv.POLICY_ORDER):
        print('\n  Per-station 24-h mean delivered  (kW / % of demand):')
        print('  ' + '-' * 92)
        gs_names = summary['greedy']['gs_names']
        demands_kW = summary['greedy']['demands_kW']
        print(f"  {'Station':<14}{'Demand':>10}  "
              + '  '.join(f"{header_labels[p]:>15}" for p in pv.POLICY_ORDER))
        for i, name in enumerate(gs_names):
            cells = []
            for p in pv.POLICY_ORDER:
                v = summary[p]['mean_del_kW'][i]
                dmr_pct = v / max(demands_kW[i], 1e-9) * 100
                cells.append(f"{v:7.1f} ({dmr_pct:4.1f}%)")
            print(f"  {name:<14}{demands_kW[i]:>10.0f}    " + '  '.join(cells))


if __name__ == '__main__':
    main()
