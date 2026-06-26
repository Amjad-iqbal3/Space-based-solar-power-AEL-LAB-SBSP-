"""
================================================================================
SATELLITE-BASED SOLAR POWER (SBSP) — LEO SIMULATION
================================================================================
Purpose : The main objective of this work is to Physically simulate an SBSP 
          constellation delivering Wireless Power Transfer via microwave (2.45 GHz) 
          from LEO to ground rectennas.

Acknowledgment : University of Manitoba| Advanced Network and Embedded Systems Lab
          (AEL), supervised by Prof. Peng Hu.
Contributor : Amjad Iqbal, Mustafa Alhassan, Prof. Peng Hu

================================================================================
PARAMETER  DECLARATION
================================================================================
For every parameter that I have taken for this work is basically divided into
three main categories which is verified, estimated and SBSP-Design:

  [verified] ---- These values are traceable to the genuine  exact value is directly traceable to the cited source.
                  

  [estimated]--- These values are derived from the real published range or dataset.
                  I had explained the derivation logic inline. Based on the studies and online help
                  These estimated values are reasonable but NOT a directly quoted number from the paper.

  [SBSP-DESIGN] --- These values are justified by physical reasoning based on the SBSP literature
                  For context please check (ESA SOLARIS / JAXA USEF concept studies).
                  For ESA SOLARIS the details can be seen here:
                  "https://www.esa.int/Enabling_Support/Preparing_for_the_Future/Discovery_and_Preparation/Space-based_solar_power_seeking_ideas_to_make_it_a_reality"
                  For JAXA USEF please visit here "https://humans-in-space.jaxa.jp/en/future/"
================================================================================
                        MAIN REFERENCES
================================================================================
  [B1]   "Wireless Power Transfer via Radiowaves" by Shinohara N. (2014) 
          Wiley-ISTE. ISBN 978-1-84821-605-1.  Chapter 4.

  [C1]   "CASSIOPeiA Solar Power Satellite Antenna Array – Final Breadboard Results." by 
          Buchanan et al. (2025)  IEEE Trans. Antennas Propag. DOI: 10.1109/TAP.2025.xxxxxxx

  [J1]   "A critical review of using the Peukert equation for determining the remaining capacity of
          lead-acid and lithium-ion batteries." BY Doerffel D. & Sharkh S.A. (2006)
          J. Power Sources 155(2):395-400. DOI:10.1016/j.jpowsour.2005.04.030

  [J2]  "Microwave power transmission: Historical milestones and system components." by
          Strassner B. & Chang K. (2013) Proc. IEEE 101(6):1370-1378. doi: 10.1109/JPROC.2013.2246132

  [J3]    "NRLMSISE-00 empirical model of the atmosphere: Statistical comparisons 
            and scientific issues." bY Picone J.M. et al. (2002)
          J. Geophys. Res. Space Phys. 107(A12):1468.
          doi.org/10.1029/2002JA009430
          In this paper the authors describe the NRLMSISE-00 model mathematically.
          However, it does NOT contain a simple lookup table.

  [B2]   "Fundamentals of Astrodynamics and Applications." by Vallado D.A. (2001) 
          4th ed. Microcosm Press / Springer.
          Table 8-4 — exponential atmosphere layers (US Std Atm 1976 fit).

  [R1]  US Standard Atmosphere (1976). NOAA/NASA/USAF.
          Available: https://ntrs.nasa.gov/citations/19770009539

  [B3]  "Astronomical Algorithms." by Meeus J. (1998)  2nd ed.
          Willmann-Bell. Chapter 25 — Solar coordinates..

  [BC1]  "Satellite Orbits." BY Montenbruck O. & Gill E. (2000) Springer. ISBN 978-3-540-67280-7.
          Chapters 3–5 — drag, SRP, J2 perturbations.

  [B4]   "Spacecraft Thermal Control Handbook, Volume I: Fundamental Technologies."
          by Gilmore D.G. ed. (2002) Vol. I. Aerospace Press. Table 2-1 (view factors), OSR properties.

  [Web1]  "IMM-α Concentrator Solar Cell Datasheet." Spectrolab Inc. (2021) 
          https://www.spectrolab.com/photovoltaics.html
          (\u03B7_stc, temp coefficient, absorptance) = eta= \u03B7

  [RO24] E. Rodgers, E. Gertsen, J. Sotudeh, C. Mullins, A. Hernandez, H. N. Le, P. Smith, and N. Joseph,
        “Space-Based Solar Power,” NASA Office of Technology, Policy, and Strategy, Washington, DC, USA, Tech. Rep.
        20230018600, Jan. 2024, NASA Headquarters

  [J5]  "Degradation Modeling and Telemetry-Based Analysis of Solar Cells in LEO
          for Nano- and Pico-Satellites." by A. Kenzhegarayeva (2025). Appl. Sci.
          https://doi.org/10.3390/app15169208

  [PU24]  N. Pucci, M. Prusa, V. Marinov, H. Mardani, N. Buchanan, and P. D. Mitcheson, “High Efficiency 2.496 Ghz
            Class E Power Amplifier for Space Based Solar Power Applications,”
            in 2024 IEEE 23rd International Conference on Micro and Miniature Power Systems, Self-Powered Sensors and
            Energy Autonomous Devices (PowerMEMS). Tonsberg, Norway: IEEE, Nov. 2024, pp. 163–166. [Online]. Available:
            https://ieeexplore.ieee.org/document/10814265/


  [HW25]  Honeywell Aerospace (2025) "Honeywell Launches Next-Generation Reaction Wheel Assembly for Small Satellites.
          https://aerospace.honeywell.com/us/en/about-us/press-release/2025/09/next-gen-reaction-wheel-small-satellites

  [ITU]   ITU-R (2017) "Recommendation P.618-13: Propagation data and
          prediction methods required for the design of Earth-space
          telecommunication systems."
          https://www.itu.int/rec/R-REC-P.618/en

  [ICNIRP] ICNIRP (2020) "Guidelines for limiting exposure to
          electromagnetic fields (100 kHz to 300 GHz)."
          Health Physics 118(5):483-524.
          Occupational limit at 2.45 GHz: 50 W/m². Public: 10 W/m².

  [KL11]  Kopp G. & Lean J.L. (2011) "A new, lower value of total solar
          irradiance: Evidence and climate significance."
          Geophys. Res. Lett. 38:L01706. DOI:10.1029/2010GL045777

  [IERS]  IERS Conventions (2010). IERS Technical Note 36.
          https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn36.html

  [NIST]  NIST CODATA 2018 recommended values.
          https://physics.nist.gov/cuu/Constants/

  [IAU12] IAU (2012) Resolution B2 — Astronomical Unit.
  [IAU15] IAU (2015) Resolution B3 — Solar radius 695,700 km.
  [EGM]   Pavlis N.K. et al. (2012) EGM2008. J. Geophys. Res. 117:B04406.
  [IGRF]  Alken P. et al. (2021) IGRF-13. Earth Planets Space 73:49.
  [TR09]  Trenberth K.E. et al. (2009) Earth's global energy budget.
          BAMS 90(3):311-323.
  [ST15] "The albedo of Earth," by G. L.Stephens et al.,(2015), Rev. Geophys., 
          53, 141–163. doi: 10.1002/2014RG000449.
"""

import numpy as np
import os as _os
import matplotlib
matplotlib.use("Agg" if "DISPLAY" not in _os.environ else "TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
except ImportError:
    FigureCanvasTkAgg = NavigationToolbar2Tk = None
from dataclasses import dataclass, field
from collections import deque
from typing import List, Tuple, Optional
import warnings, math, threading, time, copy, traceback
import tkinter as tk
from tkinter import ttk, messagebox

warnings.filterwarnings("ignore")

# =============================================================================
#               PHYSICAL CONSTANTS
#  All the Physical values are VERIFIED against International Earth Rotation 
#   and Reference Systems Service (IERS) 2010 / NIST CODATA 2018 https://physics.nist.gov/cuu/pdf/wall_2018.pdf / 
#    IAU resolutions (https://drive.google.com/file/d/1V5qT9qwtpgwqwcbOfr28vLQ2rcxAYdjB/view)
# =============================================================================
RE_M   = 6_371_000.0       # Earth mean radius (m)          
RE_KM  = RE_M / 1e3
GM     = 3.986_004_418e14  # Earth grav. parameter (m³/s²)  
J2     = 1.082_63e-3       # Earth 2nd zonal harmonic        
J3     = -2.532e-6         # 3rd zonal harmonic              
J4     = -1.620e-6         # 4th zonal harmonic              
OMEGA_E= 7.292_115_085e-5  # Earth sidereal rotation (rad/s) 
C_LIGHT= 2.997_924_58e8    # Speed of light (m/s)           
STEFAN_BOLTZ = 5.670_374_419e-8  # W/m²/K⁴                  
K_BOLTZ      = 1.380_649e-23     # J/K                       
AU_M         = 1.495_978_707e11  # 1 AU in metres             
SUN_RADIUS_M = 6.957e8           # Solar photospheric radius   
TSI_1AU      = 1_361.0           # Total solar irradiance W/m² 
G0           = 9.80665           # Standard gravity m/s²       
EARTH_ALBEDO = 0.30              # Bond albedo                 
EARTH_IR_W_M2= 237.0             # OLR outgoing LW flux W/m²   
WPT_FREQ_HZ  = 2.45e9           # WPT ISM frequency Hz         
WPT_LAMBDA_M = C_LIGHT / WPT_FREQ_HZ  # 0.12245 m             
EARTH_MAG_DIPOLE_T_M3 = 7.94e15 # Dipole moment m³·T          
SOLAR_LUMINOSITY_W = 4*math.pi*AU_M**2*TSI_1AU  # ~3.828e26 W 


# =============================================================================
#           SIMULATION PARAMETERS 
#   Most of these values are either estimated or based on the SBSP-design Architecture)
# =============================================================================
@dataclass
class SimParams:

    # ------------------------------Constellation ------------------------------
    # We considered the Walker delta constellation for the standard LEO coverage architecture.
    # 4×5 = 20 satellites chosen as a minimum viable SBSP demonstration
    # constellation in [RO24] Table 1 (Rodgers et al. 2024).
    n_planes:       int   = 4       # 
    sats_per_plane: int   = 5       # 
    altitude_km:    float = 450.0   #  450 km chosen as LEO sweet spot:
                                    #   low drag penalty vs. high coverage angle.
                                    #   Starlink operates 540–570 km [public FCC filing].
                                    #   ISS is 408 km. 450 km is a round design choice.
    inc_deg:        float = 53.0    #  53 degree inclination matches Starlink shell 1 inclination
                                    #   and provides coverage to ±53° latitude,
                                    #   covering all 8 ground stations in this scenario.
    eccentricity:   float = 0.0     #  Circular orbit -- standard for LEO SBSP
                                    #   to maintain constant slant range to ground.

    # ------------------------------Apertures ------------------------------
    # TX and RX aperture sizes design for LEO.
    tx_side_m: float = 200.0  # [based on the RO24 3.2 uses 100–500 m TX for LEO SBSP]
    rx_side_m: float = 500.0  # [based on the RO24 3.2 baseline rectenna]

    #-----------------------Solar panel (Spectrolab IMM-α GaAs triple-junction) -------
    panel_area_m2:     float = 5_000.0  # 5000 m² panel area.
                                        #   Justification: 5000 m² × 1361 W/m² × 0.33 ≈ 2.2 MW
                                        #   DC, consistent with MW-class SBSP target.
    panel_areal_kg_m2: float = 1.0      # [According to Web1] Spectrolab IMM-α thin-film
                                        #   GaAs: areal density ~1 kg/m² per datasheet.
    panel_absorptance: float = 0.93     # [Based on the Web1] GaAs 3J front-surface
                                        #   absorptance = 0.93 (Spectrolab datasheet).
    panel_eff_stc:     float = 0.33     # BOL STC efficiency, State-of-practice for space PV
                                        # (NASA 2022, via Rodgers et al. 2024).
    panel_temp_coeff:  float = -0.0028  # [Based on Web1] GaAs 3J Pmax temp coefficient
                                        #   = −0.28%/K = −0.0028/K (Spectrolab datasheet).
    panel_deg_rate: float = 0.010       # Cell efficiency degradation 1%/yr.
                                        #   Engineering estimate for III-V
                                        #   multijunction cells in the LEO
                                        #   radiation environment. Consistent
                                        #   with fluence-based degradation
                                        #   models for GaAs 3J cells: EOL >90%
                                        #   of BOL over 10–15 yr LEO mission
                                        #   (Raya-Armenta 2021, fluence rates).
    panel_cap_J_K_m2:  float = 400.0   #  GaAs panel thermal capacitance.
                                        #   Typical GaAs cell + substrate: ~400 J/K/m².
                                        #   No single paper directly gives this number;
                                        #   it is consistent with lumped-capacitance
                                        #   models in spacecraft thermal textbooks.

    # ------------------------------ Power chain ------------------------------
    dc_rf_eff:    float = 0.85   #[PU24] Pucci et al. 2024:
                                 #   Class-E PA at 2.496 GHz, eta_DC-RF = 85% (Abstract).
    harness_loss: float = 0.008  #  0.8% resistive harness loss.
                                 #   Boeing 702HP class power harness: ~0.5–1.0%
                                 #   (industry rule of thumb, no single public paper).
    mppt_eff_peak: float = 0.985 #  Peak MPPT efficiency 98.5%.
                                 #   Commercial space MPPT (e.g. SunSpace SS-200)
                                 #   achieves 97–99% at rated power. Datasheet not
                                 #   freely available; value is a mid-range estimate.
    mppt_eff_min:  float = 0.920 #  MPPT efficiency at 5% illumination.
                                 #   MPPT efficiency degrades at low input; 92% is
                                 #   a conservative estimate.

    # ------------------------------ Battery (Li-ion NMC) ------------------------------─
    #
    # Design rationale:
    #   Eclipse duration at 450 km: ~35 min per orbit (5550 s period).
    #   Housekeeping load: 500 W.
    #   Energy needed: 500 W × 35 min / 60 = 292 Wh.
    #   With 80% DoD and 95% efficiency: 292 / 0.80 / 0.95 ≈ 384 Wh minimum.
    #   3600 Wh provides comfortable margin for a 5000 m² spacecraft.

    batt_capacity_Wh: float = 3_600.0  # Total capacity of the battery.
    batt_capacity_Ah: float = 75.0     # Batter current I= P/V= 3600 Wh / 48 V = 75 Ah.
    batt_nominal_v:   float = 48.0     #  Voltage= 48 V which is a common bus spacecraft
                                       #   standard (Boeing 702HP heritage).
    batt_dod_limit:   float = 0.80     #  80% max depth of discharge.
                                       #   NMC Li-ion space cells: 80–85% DoD is
                                       #   standard for LEO cycle life >30,000 cycles.
                                     
    batt_charge_eff:  float = 0.95     #  95% charge efficiency for NMC.
                                       #   Typical NMC round-trip: 93–97%. 
    batt_peukert_k:   float = 1.05     # [Based on the — J1] 
                                       #   Peukert exponent k for Li-ion
                                       #   cells ranges 1.01–1.10. k=1.05 is the
                                      
    batt_internal_r:  float = 0.05     #  Internal resistance 50 mΩ.
                                       #   Typical for large-format space NMC cells.
                                       
    batt_ocv_slope:   float = 0.8      #  open circuit voltage (OCV) for the Linear model slope
                                       # (V/SOC). state of charge (SOC)
                                       #   Simplified model: OCV = V_nom + 0.8×(SOC−0.5)
                                       #   giving OCV range 48±0.4 V over usable SOC.
                                       #   This is a modelling convenience, not a
                                       #   measured value from a specific paper.

    # ------------------ WPT rectenna (fleet-level fallback)---------------------
    # Per-station values are overridden in build_ground_stations().
    # Range 70–90% at 2.45 GHz from according to [B1] Chapter 4 and [J2] Table II.
    rectenna_eff_peak: float = 0.85   #  Mid of 80–90% range
                                      #   reported for Schottky rectifiers at 2.45 GHz,
                                      #   full rated power density ~100 W/m².
    rectenna_eff_min:  float = 0.72   #  At 10% rated power density,
                                      #   Shinohara Ch.4 Fig. 4.x shows ~70–75%.
                                      #   0.72 is the mid of that range.

    # ----------------------- Thermal ------------------------ 
    sat_heat_cap_J_K: float = 80_000.0  # Satellite thermal mass.
                                        #   ~1800 kg spacecraft × ~44 J/K/kg average
                                        #   specific heat (Al structure + electronics)
                                        #   ≈ 80,000 J/K. Physical estimate
    radiator_area_m2: float = 300.0     #  Radiator area.
                                       
    radiator_emiss:   float = 0.92      # [B3] Gilmore Vol.I Table 4-1:
                                        #   Optical Solar Reflector (OSR) emissivity
                                        #   ε = 0.91–0.93.==> 0.92.
    radiator_absorb:  float = 0.10      # [ B3] 
                                        #   OSR solar absorptance \alpha= 0.07–0.12.
    
    sat_init_temp_K:  float = 290.0     #  Initial temperature = 290 K
                                        #   (17°C). Reasonable orbital equilibrium
                                        #   start condition
    bus_area_m2:      float = 50.0      #  Bus projected area for solar
                                        
    bus_absorb:       float = 0.15      # [B3] Gilmore Vol.I Table 4-1:
                                        #   MLI (Multi-Layer Insulation) outer surface
                                        #   solar absorptance \alpha = 0.05–0.20.
                                        
    bus_emiss:        float = 0.85      # [B3] 
                                        #   MLI effective emittance 0.01–0.03 (perfect),
                                        #   but partially blanket bus: 0.80–0.90.
                                        

    # ----------------------- Structure / propulsion -----------------------
    bus_dry_mass_kg: float = 800.0   #      Bus dry mass 800 kg.
                                     #  According tp [RO24] LEO SBSP concept: 500–1200 kg
                                    
    isp_s:           float = 220.0   # Hydrazine monopropellant Isp.
                                     #   Aerojet Rocketdyne MR-103 thruster: Isp = 220–229 s
                                     #   (public datasheet).
                                     #   290 s is bipropellant (e.g. MMH/NTO) territory.

    # ----------------------- ADCS -----------------------
    rw_max_momentum:    float = 75.0   #  according to Honeywell HR16-75 reaction
                                       #   wheel momentum capacity = 75 N·m·s
                                
    rw_max_torque:      float = 0.2    #  Honeywell HR16 max torque
                                       #   = 0.20 N·m.
    attitude_bw_hz:     float = 0.1    #  ACS control bandwidth 0.1 Hz.
                                       #   Typical for large flexible spacecraft.

    max_pointing_err_deg: float = 0.005     # 5 mdeg ≈ 87 µrad operational pointing
                                            # tolerance. Su et al. 2024 specifies
                                            # 0.005° as the half-power beam width
                                            # for ~100 m aperture WPT arrays, with
                                            # required pointing accuracy 0.0005°
                                            # (one order tighter). We adopt 0.005°
                                            # as the operational tolerance, which
                                            # at 200 m TX, 450 km nadir slant range
                                            # corresponds to a beam-centroid
                                            # displacement of ~39 m on the ground —
                                            # well within the 250 m rectenna half-width.
                                    
    sun_track_rate_dps: float = 0.1    #  Panel sun-tracking slew rate
                                       #   0.1°/s. Orbital rate at 450 km ≈ 0.065°/s,
                                       #   so 0.1°/s provides margin. 
    # ----------------------- Allocator / simulation time -----------------------
    alloc_mode:     str   = "greedy"           # Software parameter 
    dt_s:           float = 30.0               # Time step 30 s.
                                               #   LEO period ~5550 s --> ~185 steps/orbit.
                                               #   Sufficient resolution for orbital
                                               
    t0_unix:        float = 1_700_000_000.0    #  Simulation epoch.
                                               #   = 2023-11-14 22:13:20 UTC.
                                               #   Arbitrary recent date for sun position.
    mission_age_yr: float = 0.0               # Software parameter

    @property
    def tx_area_m2(self):       return self.tx_side_m ** 2
    @property
    def rx_area_m2(self):       return self.rx_side_m ** 2
    @property
    def max_safe_pd_W_m2(self):
        # ICNIRP (2020) general-public exposure limit at 2.45 GHz = 10 W/m^2.
        # Journal version uses the public limit because rectenna sites in the
        # European Phase-1 cluster sit near population centres rather than
        # behind controlled-access fencing. Occupational limit = 50 W/m^2.
        return 10.0
                      
    @property
    def total_sat_mass_kg(self):
        return self.bus_dry_mass_kg + self.panel_area_m2 * self.panel_areal_kg_m2


# =============================================================================
#                            SUN EPHEMERIS
#                All the chosen coefficients are based on [B3] "
# =============================================================================
def sun_state(t_unix: float) -> Tuple[np.ndarray, float]:
    J2000_UNIX = 946_728_000.0          # 
    T = (t_unix - J2000_UNIX) / 86_400.0 / 36_525.0  # Julian centuries from J2000.0
    # Mean longitude of Sun 
    L0 = math.radians((280.46646 + 36_000.76983 * T) % 360)
    # Mean anomaly of Sun
    M  = math.radians((357.52911 + 35_999.05029 * T - 0.0001537 * T**2) % 360)
    # Equation of centre
    C  = math.radians(
        (1.914602 - 0.004817*T - 0.000014*T**2) * math.sin(M)
        + (0.019993 - 0.000101*T) * math.sin(2*M)
        + 0.000289 * math.sin(3*M))
    sun_lon = L0 + C
    # Obliquity of ecliptic
    eps = math.radians(23.439291 - 0.013004*T - 1.64e-7*T**2)
    # Earth orbital eccentricity 
    e_E  = 0.016708634
    nu_E = M + C
    # Sun-Earth distance in AU 
    R_AU = (1.0*(1.0 - e_E**2)) / (1.0 + e_E*math.cos(nu_E))
    sl   = sun_lon
    # ECI unit vector to Sun
    sun_eci = np.array([math.cos(sl),
                        math.cos(eps)*math.sin(sl),
                        math.sin(eps)*math.sin(sl)])
    return sun_eci / np.linalg.norm(sun_eci), float(R_AU)


def solar_irradiance_W_m2(R_AU: float) -> float:
    return TSI_1AU / (R_AU**2)  


# =============================================================================
#                   ORBITAL MECHANICS
# =============================================================================
class OrbitalMechanics:

    @staticmethod
    def kepler_newton(M_rad, e, tol=1e-12, max_iter=50):
        """Newton-Raphson solver for Kepler's equation."""
        E = M_rad if e < 0.8 else math.pi
        for _ in range(max_iter):
            dE = (M_rad - E + e*math.sin(E)) / (1.0 - e*math.cos(E))
            E += dE
            if abs(dE) < tol: break
        return E

    @staticmethod
    def true_anomaly(M_rad, e):
        """Mean anomaly --> true anomaly. based on BC1]"""
        E  = OrbitalMechanics.kepler_newton(M_rad, e)
        nu = 2.0*math.atan2(math.sqrt(1+e)*math.sin(E/2),
                            math.sqrt(1-e)*math.cos(E/2))
        return nu % (2*math.pi)

    @staticmethod
    def orbital_radius(a_m, e, nu):
        """Orbital radius from conic section. [BC1]"""
        return a_m*(1.0 - e**2) / (1.0 + e*math.cos(nu))

    @staticmethod
    def eci_from_elements(a_m, e, inc, raan, aop, nu):
        """Keplerian elements --> ECI position. [BC1]"""
        r_m = OrbitalMechanics.orbital_radius(a_m, e, nu)
        p = r_m*math.cos(nu);  q = r_m*math.sin(nu)
        ci,si = math.cos(inc), math.sin(inc)
        cr,sr = math.cos(raan),math.sin(raan)
        ca,sa = math.cos(aop), math.sin(aop)
        Rx = cr*ca - sr*sa*ci;  Ry = -cr*sa - sr*ca*ci
        Sx = sr*ca + cr*sa*ci;  Sy = -sr*sa + cr*ca*ci
        Wx = sa*si;             Wy =  ca*si
        return np.array([Rx*p+Ry*q, Sx*p+Sy*q, Wx*p+Wy*q])

    @staticmethod
    def eci_velocity_from_elements(a_m, e, inc, raan, aop, nu):
        """Keplerian elements --> ECI velocity. [ BC1]"""
        p_orb = a_m*(1.0 - e**2)
        h_mag = math.sqrt(GM*p_orb)
        ci,si = math.cos(inc), math.sin(inc)
        cr,sr = math.cos(raan),math.sin(raan)
        ca,sa = math.cos(aop), math.sin(aop)
        v_P = GM/h_mag*(-math.sin(nu))
        v_Q = GM/h_mag*(e + math.cos(nu))
        P_hat = np.array([cr*ca - sr*sa*ci, sr*ca + cr*sa*ci, sa*si])
        Q_hat = np.array([-cr*sa - sr*ca*ci, -sr*sa + cr*ca*ci, ca*si])
        return v_P*P_hat + v_Q*Q_hat

    @staticmethod
    def eci_to_ecef(pos_eci_m, t_unix):
        """ECI --> ECEF rotation. [ BC1]"""
        J2000_UNIX = 946_728_000.0
        theta = OMEGA_E*(t_unix - J2000_UNIX)
        c, s = math.cos(theta), math.sin(theta)
        return np.array([[c,s,0],[-s,c,0],[0,0,1]]) @ pos_eci_m

    @staticmethod
    def ecef_to_latlon(pos_ecef_m):
        """ECEF --> geocentric latitude and longitude. [ BC1 ]"""
        x,y,z = pos_ecef_m
        r_xy = math.sqrt(x**2 + y**2)
        return math.degrees(math.atan2(z,r_xy)), math.degrees(math.atan2(y,x))

    @staticmethod
    def elevation_angle_deg(sat_pos_eci_m, t_unix, gs_lat_deg, gs_lon_deg):
        """Satellite elevation angle at ground station. [BC1 ]"""
        sat_ecef = OrbitalMechanics.eci_to_ecef(sat_pos_eci_m, t_unix)
        lat = math.radians(gs_lat_deg);  lon = math.radians(gs_lon_deg)
        gs_ecef = RE_M*np.array([math.cos(lat)*math.cos(lon),
                                  math.cos(lat)*math.sin(lon), math.sin(lat)])
        diff = sat_ecef - gs_ecef
        up   = gs_ecef / (np.linalg.norm(gs_ecef)+1e-30)
        rng  = np.linalg.norm(diff)
        if rng < 1.0: return 90.0
        return math.degrees(math.asin(max(-1.0, min(1.0, float(np.dot(diff/rng, up))))))

    @staticmethod
    def slant_range_m(sat_pos_eci_m, t_unix, gs_lat_deg, gs_lon_deg):
        """Slant range from satellite to ground station."""
        sat_ecef = OrbitalMechanics.eci_to_ecef(sat_pos_eci_m, t_unix)
        lat = math.radians(gs_lat_deg);  lon = math.radians(gs_lon_deg)
        gs_ecef = RE_M*np.array([math.cos(lat)*math.cos(lon),
                                  math.cos(lat)*math.sin(lon), math.sin(lat)])
        return float(np.linalg.norm(sat_ecef - gs_ecef))

    @staticmethod
    def j2_raan_rate(a_m, e, inc_rad):
        """J2 RAAN drift rate. """
        n = math.sqrt(GM/a_m**3)
        p = a_m*(1-e**2)
        return -1.5*n*J2*(RE_M/p)**2*math.cos(inc_rad)

    @staticmethod
    def j2_aop_rate(a_m, e, inc_rad):
        """J2 argument of perigee drift rate."""
        n = math.sqrt(GM/a_m**3)
        p = a_m*(1-e**2)
        return 0.75*n*J2*(RE_M/p)**2*(5*math.cos(inc_rad)**2 - 1)

    @staticmethod
    def j2_mean_motion_correction(a_m, e, inc_rad):
        """J2- mean motion"""
        n0 = math.sqrt(GM/a_m**3)
        p  = a_m*(1-e**2)
        return n0*(1 + 1.5*J2*(RE_M/p)**2*math.sqrt(1-e**2)*(1 - 1.5*math.sin(inc_rad)**2))

    @staticmethod
    def gauss_da_dt(a_m, e, inc_rad, nu, f_r, f_t):
        """variational equation for semi-major axis."""
        p = a_m*(1-e**2);  h = math.sqrt(GM*p)
        r = p/(1+e*math.cos(nu))
        return (2*a_m**2/h)*(e*math.sin(nu)*f_r + (p/r)*f_t)

    @staticmethod
    def atm_density_kg_m3(alt_km):
        """
        Exponential atmosphere layer model.

        Table format: (base altitude km, base density kg/m³, scale height km)
        """
        # [B2 Table 8-4 / R1 1976]
        table = [
            (0,    1.225,     8.44),
            (25,   4.008e-2,  6.49),
            (30,   1.841e-2,  6.75),
            (40,   3.996e-3,  7.47),
            (50,   1.027e-3,  8.39),
            (60,   3.097e-4,  7.58),
            (70,   8.283e-5,  6.96),
            (80,   1.846e-5,  6.29),
            (90,   3.416e-6,  5.47),
            (100,  5.606e-7,  5.84),
            (110,  9.708e-8,  8.00),
            (120,  2.222e-8, 11.4),
            (150,  2.076e-9, 22.5),
            (200,  2.541e-10,37.5),
            (300,  1.916e-11,72.2),
            (400,  2.803e-12,125.),
            (500,  5.215e-13,196.),
            (600,  1.137e-13,275.),
            (700,  3.070e-14,320.),
            (800,  1.136e-14,350.),
            (900,  5.759e-15,450.),
            (1000, 3.561e-15,500.),
        ]
        if alt_km <= 0:    return table[0][1]
        if alt_km >= 1000: return table[-1][1]*math.exp(-(alt_km-1000)/500.)
        for i in range(len(table)-1):
            if table[i][0] <= alt_km < table[i+1][0]:
                return table[i][1]*math.exp(-(alt_km-table[i][0])/table[i][2])
        return table[-1][1]

    @staticmethod
    def drag_accel_vector(pos_eci_m, vel_eci_m_s, alt_km, mass_kg, Cd, A_cross_m2):
        """Drag acceleration. Cd=2.2 typical for LEO."""
        omega_vec = np.array([0.0, 0.0, OMEGA_E])
        v_rel     = vel_eci_m_s - np.cross(omega_vec, pos_eci_m)
        v_rel_mag = np.linalg.norm(v_rel)
        if v_rel_mag < 1.0: return np.zeros(3)
        rho = OrbitalMechanics.atm_density_kg_m3(alt_km)
        a_drag_mag = 0.5*Cd*rho*A_cross_m2*v_rel_mag**2/mass_kg
        return -a_drag_mag*(v_rel/v_rel_mag)

    @staticmethod
    def srp_accel_vector(sun_unit, panel_area_m2, mass_kg, Cr, R_AU):
        """Solar radiation pressure acceleration.
        Cr=1.3 is a typical reflectivity coefficient for solar panels."""
        P_sr = TSI_1AU/(C_LIGHT*R_AU**2)
        return Cr*P_sr*panel_area_m2/mass_kg*sun_unit

    @staticmethod
    def eclipse_fraction(pos_eci_m, sun_unit, R_AU):
        """
        Penumbra/umbra eclipse model using circular disk intersection.
        Returns 1.0 = full sun, 0.0 = full eclipse, intermediate = penumbra.
        """
        sun_dist_m = R_AU*AU_M
        proj = float(np.dot(pos_eci_m, -sun_unit))
        if proj <= 0: return 1.0
        perp_vec  = pos_eci_m - proj*(-sun_unit)
        perp_dist = np.linalg.norm(perp_vec)
        alpha_sun   = math.asin(SUN_RADIUS_M/sun_dist_m)
        alpha_earth = math.asin(min(1.0, RE_M/max(np.linalg.norm(pos_eci_m), RE_M+1)))
        sep_ang = math.atan2(perp_dist, proj)
        if sep_ang + alpha_sun <= alpha_earth: return 0.0
        if sep_ang >= alpha_sun + alpha_earth: return 1.0
        d, r1, r2 = sep_ang, alpha_sun, alpha_earth
        if d < 1e-12:
            a_overlap = math.pi*min(r1,r2)**2
        else:
            cos1 = max(-1.,min(1.,(d**2+r1**2-r2**2)/(2*d*r1)))
            cos2 = max(-1.,min(1.,(d**2+r2**2-r1**2)/(2*d*r2)))
            theta1 = 2.*math.acos(cos1)
            theta2 = 2.*math.acos(cos2)
            seg1 = 0.5*r1**2*(theta1-math.sin(theta1))
            seg2 = 0.5*r2**2*(theta2-math.sin(theta2))
            a_overlap = seg1 + seg2
        a_sun = math.pi*r1**2
        return max(0., min(1., 1. - a_overlap/max(a_sun,1e-30)))


# =============================================================================
#                                   ATTITUDE MODEL
# =============================================================================
class AttitudeModel:

    @staticmethod
    def orbit_normal_hat(pos_eci_m, vel_eci_m_s):
        h = np.cross(pos_eci_m, vel_eci_m_s)
        return h/(np.linalg.norm(h)+1e-30)

    @staticmethod
    def nadir_hat(pos_eci_m):
        return -pos_eci_m/(np.linalg.norm(pos_eci_m)+1e-30)

    @staticmethod
    def panel_sun_cosine(pos_eci_m, vel_eci_m_s, sun_unit, panel_track_angle_rad):
        h_hat  = AttitudeModel.orbit_normal_hat(pos_eci_m, vel_eci_m_s)
        nadir  = AttitudeModel.nadir_hat(pos_eci_m)
        radial = -nadir
        tang   = np.cross(h_hat, radial)
        tang  /= (np.linalg.norm(tang)+1e-30)
        ca, sa = math.cos(panel_track_angle_rad), math.sin(panel_track_angle_rad)
        panel_normal = ca*radial + sa*tang
        return max(0., float(np.dot(panel_normal, sun_unit)))

    @staticmethod
    def optimal_panel_track_angle(pos_eci_m, vel_eci_m_s, sun_unit):
        h_hat  = AttitudeModel.orbit_normal_hat(pos_eci_m, vel_eci_m_s)
        nadir  = AttitudeModel.nadir_hat(pos_eci_m)
        radial = -nadir
        tang   = np.cross(h_hat, radial)
        tang  /= (np.linalg.norm(tang)+1e-30)
        sun_plane = sun_unit - float(np.dot(sun_unit, h_hat))*h_hat
        mag = np.linalg.norm(sun_plane)
        if mag < 1e-6: return 0.
        sun_plane /= mag
        return math.atan2(float(np.dot(sun_plane, tang)),
                          float(np.dot(sun_plane, radial)))

    @staticmethod
    def tx_aperture_cosine(pos_eci_m, t_unix, gs_ecef_m):
        sat_ecef = OrbitalMechanics.eci_to_ecef(pos_eci_m, t_unix)
        diff = gs_ecef_m - sat_ecef
        rng  = np.linalg.norm(diff)
        if rng < 1.: return 1.
        beam_dir = diff/rng
        nadir    = -sat_ecef/(np.linalg.norm(sat_ecef)+1e-30)
        return max(0., float(np.dot(beam_dir, nadir)))

    @staticmethod
    def gravity_gradient_torque_Nm(pos_eci_m, I_min_kgm2, I_max_kgm2):
        
        r = np.linalg.norm(pos_eci_m)
        return 1.5*GM/r**3*abs(I_max_kgm2-I_min_kgm2)*0.5

    @staticmethod
    def srp_torque_Nm(panel_area_m2, cg_cp_offset_m, R_AU):
       
        P_sr = TSI_1AU/(C_LIGHT*R_AU**2)
        return P_sr*panel_area_m2*cg_cp_offset_m

    @staticmethod
    def magnetic_torque_Nm(pos_eci_m, residual_dipole_Am2=1.0):
        """ residual dipole 1 A·m² ."""
        r = np.linalg.norm(pos_eci_m)
        lat_rad = math.asin(max(-1.,min(1., pos_eci_m[2]/max(r,1.))))
        B_mag = EARTH_MAG_DIPOLE_T_M3/r**3*math.sqrt(1.+3*math.sin(lat_rad)**2)
        return residual_dipole_Am2*B_mag

    @staticmethod
    def aerodynamic_torque_Nm(pos_eci_m, vel_eci_m_s, alt_km,
                               panel_area_m2, cg_cp_aero_offset_m, mass_kg, Cd=2.2):
        """cg_cp_aero_offset=0.3 m """
        omega_vec = np.array([0.,0.,OMEGA_E])
        v_rel     = vel_eci_m_s - np.cross(omega_vec, pos_eci_m)
        v_rel_mag = np.linalg.norm(v_rel)
        rho = OrbitalMechanics.atm_density_kg_m3(alt_km)
        F_drag = 0.5*Cd*rho*panel_area_m2*0.3*v_rel_mag**2
        return F_drag*cg_cp_aero_offset_m

    @staticmethod
    def pointing_error_accumulate(prev_err_rad, total_disturb_Nm,
                                   rw_torque_Nm, I_sat_kgm2, dt_s, bw_hz):
        """Simplified disturbance-rejection model."""
        alpha_d  = total_disturb_Nm / max(I_sat_kgm2, 1e-3)
        alpha_c  = min(rw_torque_Nm, total_disturb_Nm) / max(I_sat_kgm2, 1e-3)
        net_alpha = max(0., alpha_d - alpha_c)
        d_err    = 0.5*net_alpha*dt_s**2
        tau_acs  = 1./(2.*math.pi*max(bw_hz,1e-3))
        err = prev_err_rad + d_err - prev_err_rad*dt_s/(tau_acs + dt_s)
        return max(0., err)


# =============================================================================
#                       PANEL THERMAL  (Lumped capacitance -- transient)
# =============================================================================
class PanelThermal:
    SPACE_TEMP_K = 4.0            #  CMB temperature ~2.73 K; 4 K conservative
    CELL_ALPHA   = 0.93           # [Web1] GaAs 3J absorptance
    CELL_EPS     = 0.87           # [B3] GaAs front emittance ~0.85–0.90
    SUB_EPS      = 0.05           # [B3] Al honeycomb back emittance

    @staticmethod
    def step_temperature(prev_T_K, irr_W_m2, panel_cos, panel_eff, cap_J_K_m2, dt_s):
        """Lumped capacitance thermal step."""
        G_eff = irr_W_m2*max(panel_cos,0.)
        Q_abs = PanelThermal.CELL_ALPHA*G_eff*(1.-max(panel_eff,0.))
        eps_eff = PanelThermal.CELL_EPS + 0.5*PanelThermal.SUB_EPS
        Q_rad   = eps_eff*STEFAN_BOLTZ*(prev_T_K**4 - PanelThermal.SPACE_TEMP_K**4)
        dT = (Q_abs - Q_rad)/max(cap_J_K_m2,1.)*dt_s
        return max(100., min(500., prev_T_K+dT))

    @staticmethod
    def efficiency_at_temp(panel_eff_stc, panel_temp_K, panel_temp_coeff,
                            mission_age_yr=0., deg_rate=0.02):
        """Temperature and degradation correction."""
        T_stc = 301.15  # Standard test condition temperature 28°C = 301.15 K
        eta_t = panel_eff_stc*(1. + panel_temp_coeff*(panel_temp_K - T_stc))
        eta_d = eta_t*(1. - deg_rate)**mission_age_yr
        return max(0., eta_d)


# =============================================================================
#                       TRANSIENT BUS THERMAL MODEL
# =============================================================================
class ThermalModel:
    VIEW_FACTOR_EARTH = 0.40   # View factor to Earth at 450 km altitude ≈ 0.40

    def __init__(self, heat_cap_J_K, rad_area_m2, rad_emiss, rad_absorb,
                 bus_area_m2, bus_absorb, bus_emiss, init_temp_K):
        self.C       = heat_cap_J_K
        self.A_rad   = rad_area_m2
        self.eps_rad = rad_emiss
        self.alpha_rad = rad_absorb
        self.A_bus   = bus_area_m2
        self.alpha_bus = bus_absorb
        self.eps_bus = bus_emiss
        self.T       = init_temp_K

    def step(self, irr_W_m2, illum_frac, sun_cos_bus, Q_dissip_W, dt_s):
        Q_solar     = self.alpha_bus*self.A_bus*irr_W_m2*sun_cos_bus*illum_frac
        Q_albedo    = EARTH_ALBEDO*irr_W_m2*self.A_bus*self.VIEW_FACTOR_EARTH*0.25
        Q_earth_ir  = EARTH_IR_W_M2*self.A_rad*self.eps_rad*self.VIEW_FACTOR_EARTH
        Q_solar_rad = self.alpha_rad*self.A_rad*irr_W_m2*0.15*illum_frac
        Q_in  = Q_solar + Q_albedo + Q_earth_ir + Q_solar_rad + Q_dissip_W
        Q_out = self.eps_rad*STEFAN_BOLTZ*self.A_rad*self.T**4
        dT    = (Q_in - Q_out)/self.C*dt_s
        self.T = max(100., min(500., self.T+dT))
        return self.T

    def max_allowable_dissipation_W(self, T_max_K=370.):
        Q_rad_max = self.eps_rad*STEFAN_BOLTZ*self.A_rad*T_max_K**4
        Q_passive = (EARTH_IR_W_M2*self.A_rad*self.eps_rad*self.VIEW_FACTOR_EARTH
                     + EARTH_ALBEDO*200.*self.A_bus*self.VIEW_FACTOR_EARTH*0.25)
        return max(0., Q_rad_max - Q_passive)


# =============================================================================
#                    BATTERY MODEL  (Li-ion NMC — Peukert model)
# =============================================================================
class BatteryModel:

    def __init__(self, capacity_Wh, capacity_Ah, dod_limit, charge_eff,
                 peukert_k, r_internal, v_nominal, ocv_slope):
        self.cap_Wh  = capacity_Wh
        self.cap_Ah  = capacity_Ah
        self.dod     = dod_limit
        self.eta_chg = charge_eff
        self.k       = peukert_k
        self.R_int   = r_internal
        self.V_nom   = v_nominal
        self.ocv_slope = ocv_slope
        self.soc     = 1.0
        self._min_soc = 1.0 - dod_limit

    @property
    def energy_J(self):   return self.soc*self.cap_Wh*3600.
    @property
    def usable_J(self):   return (self.soc-self._min_soc)*self.cap_Wh*3600.

    def ocv(self):
        return self.V_nom + self.ocv_slope*(self.soc - 0.5)

    def charge(self, P_W, dt_s):
        if P_W <= 0 or self.soc >= 1.: return
        V_oc = self.ocv()
        # Clamp input to the max chargeable power at this OCV. The constant-power
        # quadratic (I^2*R - I*V_oc + P = 0) requires V_oc^2 >= 4*R_int*P_W for a
        # real-current solution; without this clamp, surplus above ~V_oc^2/(4 R)
        # is silently dropped via the negative-discriminant branch, causing the
        # battery to never charge during high-surplus phases.
        P_max = V_oc * V_oc / (4. * self.R_int + 1e-9)
        P_W = min(P_W, P_max)
        disc = V_oc**2 - 4*self.R_int*P_W
        if disc < 0: return
        I = (V_oc - math.sqrt(max(0.,disc)))/(2*self.R_int + 1e-9)
        P_stored = V_oc*I - I**2*self.R_int
        E_in = max(0., P_stored*dt_s*self.eta_chg)
        self.soc = min(1., self.soc + E_in/(self.cap_Wh*3600.))

    def discharge(self, P_requested_W, dt_s):
        if P_requested_W <= 0 or self.soc <= self._min_soc: return 0.
        V_oc   = self.ocv()
        I_disc = P_requested_W/max(V_oc,1.)
        I_1C   = self.cap_Ah
        if I_disc > 0.01:
            pf = (I_1C/I_disc)**(self.k-1.)
            pf = max(0.1, min(pf, 10.))
        else:
            pf = 1.
        usable_Ah = (self.soc-self._min_soc)*self.cap_Ah*pf
        usable_J  = usable_Ah*3600.*V_oc
        E_req_J   = P_requested_W*dt_s
        P_ohmic   = I_disc**2*self.R_int
        fraction  = max(0.,(P_requested_W-P_ohmic))/max(P_requested_W,1e-9)
        E_del_J   = min(E_req_J, usable_J)*fraction
        E_rem_J   = min(E_req_J, usable_J)
        self.soc  = max(self._min_soc, self.soc - E_rem_J/(self.cap_Wh*3600.))
        return E_del_J/max(dt_s,1e-9)


# =============================================================================
#                   ATMOSPHERE MODEL  (ITU-R P.618-13)
#  All equations are formulated according to "https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.618-13-201712-S!!PDF-E.pdf"".
# =============================================================================
class AtmosphereModel:
    FREQ_GHZ = WPT_FREQ_HZ/1e9  # 2.45 GHz

    @staticmethod
    def rain_rate_p01_mm_hr(lat_deg, lon_deg):
        """Rain rate exceeded 0.01% of time."""
        lat = abs(lat_deg)
        if lat < 10:
            lon_fac = 1.+0.3*math.sin(math.radians(lon_deg-30))
            return min(220., 145.*lon_fac)
        elif lat < 20: base = 95.
        elif lat < 30: base = 65.
        elif lat < 40: base = 42.
        elif lat < 50:
            maritime = (abs(lon_deg)>150 or abs(lon_deg)<30 or (-100<lon_deg<-50))
            base = 35. if maritime else 22.
        elif lat < 60: base = 18.
        elif lat < 70: base = 8.
        else: base = 2.
        return base

    @staticmethod
    def specific_rain_attenuation(rain_rate_mm_hr):
        """k and \alpha coefficients at 2.45 GHz."""
        k_H=0.000847; aH=1.207; k_V=0.000631; aV=1.260
        return 0.5*(k_H*rain_rate_mm_hr**aH + k_V*rain_rate_mm_hr**aV)

    @staticmethod
    def effective_path_length_km(gamma_R, elev_deg, lat_deg):
       
        h_R = 3.+(abs(lat_deg)<36)*0.028*(36-abs(lat_deg))*0.36
        el  = math.radians(max(elev_deg,5.))
        if elev_deg >= 5:
            Ls = h_R/math.sin(el)
        else:
            Ls = 2*h_R/(math.sqrt(math.sin(el)**2+2*h_R/RE_KM*1e3)+math.sin(el))
        r = 1./(1.+0.78*math.sqrt(Ls*gamma_R/AtmosphereModel.FREQ_GHZ)
                - 0.38*(1-math.exp(-2*Ls)))
        return min(Ls*r, Ls)

    @staticmethod
    def rain_attenuation_dB(elev_deg, lat_deg, lon_deg, availability):
        
        R001   = AtmosphereModel.rain_rate_p01_mm_hr(lat_deg, lon_deg)
        if R001 < 1e-3: return 0.
        gamma_R = AtmosphereModel.specific_rain_attenuation(R001)
        L_eff  = AtmosphereModel.effective_path_length_km(gamma_R, elev_deg, lat_deg)
        A_001  = gamma_R*L_eff
        prob   = (1.-availability)*100.
        if prob <= 0.: return 0.
        prob   = max(0.01, min(prob, 50.))
        beta   = 0.
        if abs(lat_deg) < 36.:
            if prob >= 1.:
                beta = -0.005*(abs(lat_deg)-36.)
            else:
                beta = (-0.005*(abs(lat_deg)-36.)
                        + 1.8 - 4.25*math.sin(math.pi*prob/0.2))
        exp_v = -(0.655 + 0.033*math.log(max(prob,1e-9))
                  - 0.045*math.log(max(A_001,1e-6))
                  - beta*(1-prob/0.01)*math.sin(math.radians(lat_deg)))
        exp_v = max(-30., min(30., exp_v))
        A = A_001*math.exp(exp_v*math.log(max(prob/0.01,1e-30)))
        return max(0., A)

    @staticmethod
    def gaseous_attenuation_dB(elev_deg):
        
        el_rad = math.radians(max(elev_deg,2.))
        return (0.0068+0.025)/math.sin(el_rad)

    @staticmethod
    def cloud_attenuation_dB(elev_deg, lat_deg):
        
        L_w = max(0., 1.5-0.03*abs(lat_deg))
        Kl  = 0.002
        el_rad = math.radians(max(elev_deg,2.))
        return Kl*L_w/math.sin(el_rad)

    @staticmethod
    def scintillation_dB(elev_deg, lat_deg, availability):
        
        f_corr   = (WPT_FREQ_HZ/1e9/4.)**0.45
        el_rad   = math.radians(max(elev_deg,5.))
        sigma_phi = 3.6e-3*f_corr/math.sin(el_rad)**1.2
        prob_pct  = (1.-availability)*100.
        a_p = (-0.061*math.log10(max(prob_pct,1e-9))**3
               + 0.072*math.log10(max(prob_pct,1e-9))**2
               - 1.71*math.log10(max(prob_pct,1e-9)) + 3.0)
        return a_p*sigma_phi

    @staticmethod
    def total_attenuation_dB(elev_deg, lat_deg, lon_deg, clear_sky_frac):
        if elev_deg <= 0: return 999.
        gas   = AtmosphereModel.gaseous_attenuation_dB(elev_deg)
        rain  = AtmosphereModel.rain_attenuation_dB(elev_deg, lat_deg, lon_deg, clear_sky_frac)
        cloud = AtmosphereModel.cloud_attenuation_dB(elev_deg, lat_deg)
        scint = AtmosphereModel.scintillation_dB(elev_deg, lat_deg, clear_sky_frac)
        return max(0., gas+rain+cloud+scint)

    @staticmethod
    def transmission(elev_deg, lat_deg, lon_deg, clear_sky_frac):
        dB = AtmosphereModel.total_attenuation_dB(elev_deg, lat_deg, lon_deg, clear_sky_frac)
        return 10.**(-dB/10.)


# =============================================================================
#  WPT CHANNEL \u03c4= tau
#  Fresnel/Goubau beam collection:
#  Goubau-Brown form for circular apertures:
#  τ² = A_tx · A_rx / (λ² · R²)
#  η_beam = 1 - exp(-τ²)
#  Ref: Goubau 1961, Brown 1984. Square-aperture approximation
#  follows the same form to within ~3% for our geometry.
# =============================================================================
class WPTChannel:

    @staticmethod
    def fresnel_number(R_m, tx_area_m2):
        r"""Fresnel number F = A_tx / (\Lambda·R)."""
        return tx_area_m2/(WPT_LAMBDA_M*R_m)

    @staticmethod
    def tau_factor(R_m, tx_area_m2, rx_area_m2, tx_cos=1.):
        """Returns τ² = A_tx_eff · A_rx / (λ² R²) for use in η = 1 - exp(-τ²).
            Goubau-Brown form for circular apertures; ~3% accurate for square."""
        A_tx_eff = tx_area_m2 * max(tx_cos, 0.)
        return (A_tx_eff * rx_area_m2) / (WPT_LAMBDA_M**2 * R_m**2)
    @staticmethod
    def beam_collection_efficiency(R_m, tx_area_m2, rx_area_m2, tx_cos=1.):
        """eta_beam = 1 − exp(−tau2)."""

        if tx_area_m2 <= 0 or R_m < 1.: return 0.
        tau_sq = WPTChannel.tau_factor(R_m, tx_area_m2, rx_area_m2, tx_cos)
        return max(0., min(1., 1. - math.exp(-tau_sq)))

    @staticmethod
    def beam_efficiency(pointing_err_az_deg, pointing_err_el_deg, tx_side_m):
        """Sinc² beam efficiency loss from pointing error"""
        theta_az = math.radians(pointing_err_az_deg)
        theta_el = math.radians(pointing_err_el_deg)
        u = math.pi*tx_side_m*math.sin(theta_az)/WPT_LAMBDA_M
        v = math.pi*tx_side_m*math.sin(theta_el)/WPT_LAMBDA_M
        def sinc2(x):
            if abs(x) < 1e-9: return 1.
            return (math.sin(x)/x)**2
        return max(0., sinc2(u)*sinc2(v))

    @staticmethod
    def rectenna_efficiency(P_rx_W, rx_area_m2, eff_peak=0.85, eff_min=0.65):
        """
        Load-dependent rectenna efficiency.
        According to [M14]
        eta rises linearly with power density from eta_min at 0% to eta_peak at 100%
        rated power density (100 W/m²). This is a simplified linear model
        of the nonlinear Schottky diode characteristic.
        """
        PD_rated_W_m2 = 100.
        PD_actual = P_rx_W/max(rx_area_m2, 1.)
        frac = min(1., PD_actual/PD_rated_W_m2)
        return eff_min + (eff_peak-eff_min)*frac

    @staticmethod
    def link_factor(sat_pos_eci_m, vel_eci_m_s, t_unix, gs, params):
        elev = OrbitalMechanics.elevation_angle_deg(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        if elev < 5.: return 0.
        R_m = OrbitalMechanics.slant_range_m(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        if R_m < 1.: return 0.
        tx_cos   = AttitudeModel.tx_aperture_cosine(sat_pos_eci_m, t_unix, gs.ecef_m)
        eta_geo  = WPTChannel.beam_collection_efficiency(
            R_m, params.tx_area_m2, gs.rx_area_m2, tx_cos)
        eta_atm  = AtmosphereModel.transmission(
            elev, gs.lat_deg, gs.lon_deg, gs.clear_sky_frac)
        return max(0., eta_geo*eta_atm)

    @staticmethod
    def max_safe_tx_W(sat_pos_eci_m, t_unix, gs, params):
        elev = OrbitalMechanics.elevation_angle_deg(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        if elev < 5.: return 0.
        R_m = OrbitalMechanics.slant_range_m(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        if R_m < 1.: return 0.
        tx_cos  = AttitudeModel.tx_aperture_cosine(sat_pos_eci_m, t_unix, gs.ecef_m)
        eta_geo = WPTChannel.beam_collection_efficiency(
            R_m, params.tx_area_m2, gs.rx_area_m2, tx_cos)
        if eta_geo < 1e-30: return 0.
        eta_atm = AtmosphereModel.transmission(
            elev, gs.lat_deg, gs.lon_deg, gs.clear_sky_frac)
        eta_total = eta_geo*eta_atm
        if eta_total < 1e-30: return 0.
        P_rx_max = params.max_safe_pd_W_m2*gs.rx_area_m2
        return float(P_rx_max/eta_total)

    @staticmethod
    def cnr_dB(sat_pos_eci_m, t_unix, gs, p_tx_rf_W, params, bw_hz=100e6):
        if p_tx_rf_W < 1e-3: return -99.
        elev  = OrbitalMechanics.elevation_angle_deg(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        R_m   = OrbitalMechanics.slant_range_m(
            sat_pos_eci_m, t_unix, gs.lat_deg, gs.lon_deg)
        tx_cos   = AttitudeModel.tx_aperture_cosine(sat_pos_eci_m, t_unix, gs.ecef_m)
        eta_geo  = WPTChannel.beam_collection_efficiency(
            R_m, params.tx_area_m2, gs.rx_area_m2, tx_cos)
        eta_atm  = AtmosphereModel.transmission(
            elev, gs.lat_deg, gs.lon_deg, gs.clear_sky_frac)
        T_CMB  = 2.73   # [VERIFIED] CMB temperature
        T_gal  = max(3., 10.*(WPT_FREQ_HZ/1e9)**(-2.))  # [ESTIMATED] galactic noise
        atm_dB = AtmosphereModel.total_attenuation_dB(
            elev, gs.lat_deg, gs.lon_deg, gs.clear_sky_frac)
        if atm_dB > 200.: return -99.          # overflow guard
        L_atm  = 10.**(atm_dB/10.)
        T_phys_atm = 270.   # [SBSP-DESIGN] physical atmosphere temperature
        T_atm  = T_phys_atm*(1.-1./max(L_atm,1.))
        T_sky  = (T_CMB+T_gal)/max(L_atm,1.) + T_atm
        T_LNA  = 100.   # [SBSP-DESIGN] LNA noise temperature 100 K
        L_line = 10.**(0.5/10.)
        T_line = 290.
        T_sys  = max(10., T_sky + T_LNA/L_line + T_line*(1.-1./L_line))
        P_rx   = p_tx_rf_W*eta_geo*eta_atm*gs.rectenna_eff_peak
        N_W    = K_BOLTZ*T_sys*bw_hz
        return 10.*math.log10(max(P_rx/N_W, 1e-30))


# =============================================================================
#                                               POWER ALLOCATOR
# =============================================================================
class PowerAllocator:
    """
    Two-tier constellation-level power allocator.

    Inner tier  -- unchanged from the conference version: each satellite
                   independently allocates its RF budget over its visible
                   ground stations according to the selected policy
                   (greedy / prop_fair / min_demand).

    Outer tier  -- enforces two physical constraints at the constellation
                   level after the inner tier has decided:

        (a) Aggregate ICNIRP safety cap at each ground station:
            sum_s (P_tx[s,k] * link_geom[s,k]) / A_rx[k]  <=  PD_safe
            Single-satellite per-link safety caps already enforce this for
            isolated passes; the aggregate cap covers multi-satellite
            coincidence (3-6 satellites simultaneously visible to one GS
            in the regional cluster).

        (b) Demand cap with redistribution at each ground station:
            sum_s (P_tx[s,k] * link[s,k] * rectenna_eff[k])  <=  1.05 * D[k]
            When this binds, the freed RF budget at each contributing
            satellite is redirected via a second inner-tier pass to that
            satellite's other visible, non-saturated ground stations,
            using the same policy. Capacity that previously was discarded
            is now recovered.

    Three diagnostic counters accumulate over a simulation run:
      n_binding_events       : (sat, step) pairs where >=2 GSs are visible
                               and sum of their demands exceeds the
                               satellite's RF budget. Indicates whether the
                               scenario is in capacity-bound regime.
      n_safety_binding_events: (gs, step) pairs where the aggregate ICNIRP
                               cap fires.
      n_demand_binding_events: (gs, step) pairs where the demand cap fires.
      W_redistributed        : total RF that was rescued by redistribution.
      W_discarded            : total RF lost (cap fires + no other visible
                               GS available to redirect to).
    """

    def __init__(self, mode="greedy", two_tier=True, redistribute=True,
                 max_redist_iter=1):
        self.mode = mode
        self.two_tier = bool(two_tier)
        self.redistribute = bool(redistribute)
        self.max_redist_iter = int(max(1, max_redist_iter))

        # diagnostic counters (accumulate across all simulation steps)
        self.n_sat_steps             = 0
        self.n_gs_steps              = 0
        self.n_binding_events        = 0   # capacity-bound: >=2 GS visible AND sum_demands > budget
        self.n_multi_visibility      = 0   # >=2 GS visible (regardless of demand sum)
        self.n_safety_binding_events = 0
        self.n_demand_binding_events = 0
        self.W_freed                 = 0.0
        self.W_redistributed         = 0.0
        self.W_discarded             = 0.0
        # cumulative RF/DC energy trackers (Watts integrated; multiply by dt
        # in the driver to convert to Joules). Used by the RF capacity-
        # utilisation stacked-bar plot.
        self.cum_panel_RF            = 0.0   # total RF panel chain produced
        self.cum_tx_RF               = 0.0   # total RF actually transmitted (post all caps + redistribution)
        self.cum_delivered_DC        = 0.0   # total DC received at rectennas
        # visibility histogram: count[i] = number of sat-steps with exactly i visible GSs
        self.visibility_hist         = None   # lazy-init when we know n_g

    # ----------------------- inner-tier policies (unchanged) ----------------
    @staticmethod
    def _greedy(h, caps, budget):
        idx = np.argsort(h)[::-1]
        alloc_p, rem = np.zeros(len(h)), float(budget)
        for k in idx:
            if rem <= 0 or h[k] < 1e-15: break
            a = min(rem, float(caps[k]));  alloc_p[k] = a;  rem -= a
        return alloc_p

    @staticmethod
    def _prop_fair(h, caps, budget, max_iter=200):
        eps = 1e-12;  h_eff = np.maximum(h, eps)
        if budget < eps: return np.zeros_like(h)
        mu_lo = eps;  mu_hi = float(np.max(h_eff))/eps
        for _ in range(max_iter):
            mu   = 0.5*(mu_lo+mu_hi)
            p_k  = np.minimum(h_eff/mu, caps)
            if np.sum(p_k) > budget: mu_lo = mu
            else:                    mu_hi = mu
            if (mu_hi-mu_lo)/(mu_hi+1e-30) < 1e-8: break
        return np.clip(h_eff/((mu_lo+mu_hi)*0.5), 0., caps)

    @staticmethod
    def _min_demand(h, caps, budget, demands):
        alloc_p = np.zeros(len(h));  rem = float(budget)
        for k in np.argsort(-h):
            if h[k] < 1e-15 or rem <= 0: break
            need = demands[k]/max(h[k],1e-15)
            a = min(rem, float(caps[k]), need);  alloc_p[k] = a;  rem -= a
        return alloc_p

    @staticmethod
    def _lp_optimal(link_matrix, safe_caps, rf_budgets, demands,
                    rectenna_eff_vec, rx_area_vec, max_safe_pd_W_m2):
        """
        Centralized LP upper bound: maximize total delivered DC across
        all (sat, GS) pairs subject to all physical constraints:
          - per-satellite RF budget
          - per-link safety cap (single-satellite max_safe_tx_W)
          - per-GS demand cap (1.05 * demand)
          - per-GS aggregate ICNIRP cap (sum_s P_tx*link <= PD_safe*A_rx)
        Variables: tx[s,k] for s in [n_s], k in [n_g], flattened.
        """
        from scipy.optimize import linprog
        n_s, n_g = link_matrix.shape
        n_var    = n_s * n_g

        h_eff = link_matrix * rectenna_eff_vec[np.newaxis, :]   # (n_s, n_g)
        c = -h_eff.flatten()                                    # minimize -obj

        # constraint 1: per-sat budget
        A_budget = np.zeros((n_s, n_var))
        for s in range(n_s):
            A_budget[s, s*n_g:(s+1)*n_g] = 1.0
        b_budget = np.asarray(rf_budgets, dtype=float)

        # constraint 2: per-GS demand cap (in DC)
        A_demand = np.zeros((n_g, n_var))
        for k in range(n_g):
            for s in range(n_s):
                A_demand[k, s*n_g + k] = link_matrix[s, k] * rectenna_eff_vec[k]
        b_demand = 1.05 * np.asarray(demands, dtype=float)

        # constraint 3: per-GS aggregate ICNIRP cap (in RF)
        # link_matrix already encodes link factor * beam efficiency (geometric)
        rx_area_vec = np.asarray(rx_area_vec, dtype=float) if rx_area_vec is not None \
                      else np.ones(n_g) * 1e9   # disable if not provided
        A_safety = np.zeros((n_g, n_var))
        for k in range(n_g):
            for s in range(n_s):
                A_safety[k, s*n_g + k] = link_matrix[s, k]
        b_safety = max_safe_pd_W_m2 * rx_area_vec

        A_ub = np.vstack([A_budget, A_demand, A_safety])
        b_ub = np.concatenate([b_budget, b_demand, b_safety])

        # bounds: 0 <= tx[s,k] <= safe_caps[s,k]
        safe_caps = np.asarray(safe_caps, dtype=float)
        lb = np.zeros(n_var)
        ub = safe_caps.flatten()
        bounds = list(zip(lb, ub))

        try:
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                          method='highs')
            if res.success:
                return np.maximum(res.x.reshape(n_s, n_g), 0.0)
        except Exception:
            pass
        return np.zeros((n_s, n_g))

    def _policy(self, h, caps, budget, demands):
        if self.mode == "greedy":     return self._greedy(h, caps, budget)
        if self.mode == "prop_fair":  return self._prop_fair(h, caps, budget)
        return self._min_demand(h, caps, budget, demands)

    # ----------------------- two-tier allocate ------------------------------
    def allocate(self, link_matrix, safe_caps, rf_budgets,
                 demands, rectenna_eff_vec,
                 rx_area_vec=None, max_safe_pd_W_m2=10.0):
        n_s, n_g         = link_matrix.shape
        link_matrix      = np.asarray(link_matrix)
        safe_caps        = np.asarray(safe_caps)
        rf_budgets       = np.asarray(rf_budgets, dtype=float)
        demands          = np.asarray(demands, dtype=float)
        rectenna_eff_vec = np.asarray(rectenna_eff_vec, dtype=float)
        tx = np.zeros((n_s, n_g))

        # --- Pass 1: inner-tier per-satellite policy ---
        # initialise visibility histogram lazily (we now know n_g)
        if self.visibility_hist is None or len(self.visibility_hist) != n_g + 1:
            self.visibility_hist = [0] * (n_g + 1)

        # if mode is centralized LP, skip the per-sat policy loop and outer
        # tier; the LP solves the constellation-level allocation in one shot
        if self.mode == "lp_optimal":
            for s in range(n_s):
                if rf_budgets[s] < 0.1: continue
                self.n_sat_steps += 1
                visible    = link_matrix[s] > 1e-12
                n_visible  = int(np.sum(visible))
                self.visibility_hist[n_visible] += 1
                if n_visible >= 2:
                    self.n_multi_visibility += 1
                    if float(np.sum(demands[visible])) > float(rf_budgets[s]):
                        self.n_binding_events += 1
            tx = self._lp_optimal(link_matrix, safe_caps, rf_budgets, demands,
                                  rectenna_eff_vec, rx_area_vec,
                                  max_safe_pd_W_m2)
            rx_dc = self._rx_dc(tx, link_matrix, rectenna_eff_vec)
            self.cum_panel_RF     += float(np.sum(rf_budgets))
            self.cum_tx_RF        += float(np.sum(tx))
            self.cum_delivered_DC += float(np.sum(rx_dc))
            return tx, rx_dc

        for s in range(n_s):
            if rf_budgets[s] < 0.1: continue
            self.n_sat_steps += 1

            visible    = link_matrix[s] > 1e-12
            n_visible  = int(np.sum(visible))
            self.visibility_hist[n_visible] += 1

            if n_visible >= 2:
                self.n_multi_visibility += 1
                if float(np.sum(demands[visible])) > float(rf_budgets[s]):
                    self.n_binding_events += 1

            h    = link_matrix[s] * rectenna_eff_vec
            caps = safe_caps[s]
            tx[s] = self._policy(h, caps, rf_budgets[s], demands)

        # If two-tier disabled, fall back to original post-hoc scaling
        if not self.two_tier:
            rx_dc = self._rx_dc(tx, link_matrix, rectenna_eff_vec)
            for k in range(n_g):
                self.n_gs_steps += 1
                if rx_dc[k] > demands[k]*1.05:
                    scale = demands[k]*1.05/(rx_dc[k]+1e-12)
                    self.W_discarded += float(np.sum(tx[:, k])) * (1.0 - scale)
                    tx[:, k] *= scale;  rx_dc[k] *= scale
                    self.n_demand_binding_events += 1
            self.cum_panel_RF     += float(np.sum(rf_budgets))
            self.cum_tx_RF        += float(np.sum(tx))
            self.cum_delivered_DC += float(np.sum(rx_dc))
            return tx, rx_dc

        # --- Pass 2: aggregate ICNIRP safety cap at each GS ---
        # Aggregate received RF (not DC) at GS k is sum_s tx[s,k]*link_matrix[s,k]
        # (link_matrix already includes link factor + beam_eff; rectenna_eff
        # converts RF -> DC and does not enter the PD constraint).
        if rx_area_vec is not None:
            rx_area_vec = np.asarray(rx_area_vec, dtype=float)
            for k in range(n_g):
                self.n_gs_steps += 1
                rf_at_k = float(np.sum(tx[:, k] * link_matrix[:, k]))
                pd_agg  = rf_at_k / max(rx_area_vec[k], 1e-9)
                if pd_agg > max_safe_pd_W_m2:
                    scale = max_safe_pd_W_m2 / max(pd_agg, 1e-12)
                    freed = float(np.sum(tx[:, k])) * (1.0 - scale)
                    self.W_freed     += freed
                    self.W_discarded += freed   # provisionally; redistribution may rescue
                    tx[:, k] *= scale
                    self.n_safety_binding_events += 1

        # --- Pass 3: demand cap with redistribution ---
        for _iter in range(self.max_redist_iter):
            rx_dc = self._rx_dc(tx, link_matrix, rectenna_eff_vec)

            # identify saturated GSs and per-sat freed budget
            freed_sat    = np.zeros(n_s)
            saturated_gs = np.zeros(n_g, dtype=bool)
            for k in range(n_g):
                if rx_dc[k] > demands[k]*1.05:
                    scale = demands[k]*1.05/(rx_dc[k]+1e-12)
                    freed_k = float(np.sum(tx[:, k])) * (1.0 - scale)
                    for s in range(n_s):
                        freed_sat[s] += tx[s, k] * (1.0 - scale)
                    self.W_freed += freed_k
                    tx[:, k] *= scale
                    rx_dc[k]   *= scale
                    saturated_gs[k] = True
                    self.n_demand_binding_events += 1

            # redistribution: each sat re-allocates its freed budget to its
            # other visible, non-saturated GSs using the SAME policy
            if not self.redistribute or float(np.sum(freed_sat)) < 0.1:
                # no redistribution requested or nothing to redistribute
                self.W_discarded += float(np.sum(freed_sat))
                break

            tx_pre_redist = tx.copy()
            for s in range(n_s):
                if freed_sat[s] < 0.1: continue
                # zero out saturated GSs in this satellite's view
                h_s    = (link_matrix[s] * rectenna_eff_vec).copy()
                caps_s = safe_caps[s].astype(float).copy()
                h_s[saturated_gs]    = 0.0
                caps_s[saturated_gs] = 0.0
                extra = self._policy(h_s, caps_s, freed_sat[s], demands)
                tx[s] += extra
                used  = float(np.sum(extra))
                self.W_redistributed += used
                self.W_discarded     += (freed_sat[s] - used)

            # check if any redistribution happened; if not, exit early
            if np.allclose(tx, tx_pre_redist):
                break

        # final cleanup demand cap (in case redistribution over-fills any GS)
        rx_dc = self._rx_dc(tx, link_matrix, rectenna_eff_vec)
        for k in range(n_g):
            if rx_dc[k] > demands[k]*1.05:
                scale = demands[k]*1.05/(rx_dc[k]+1e-12)
                tx[:, k] *= scale;  rx_dc[k] *= scale

        self.cum_panel_RF     += float(np.sum(rf_budgets))
        self.cum_tx_RF        += float(np.sum(tx))
        self.cum_delivered_DC += float(np.sum(rx_dc))
        return tx, rx_dc

    @staticmethod
    def _rx_dc(tx, link_matrix, rectenna_eff_vec):
        # vectorised: rx_dc[k] = sum_s tx[s,k] * link[s,k] * rectenna_eff[k]
        return (tx * link_matrix).sum(axis=0) * rectenna_eff_vec


# =============================================================================
#                            GROUND STATIONS
# =============================================================================
@dataclass
class GroundStation:
    """
    Per-station rectenna efficiency.

    RECTENNA EFFICIENCY VALUES
    -----------------------------------------
    The per-station eta_peak and eta_min values below are based on the following:

    Base range: eta_peak = 85–90% at 2.45 GHz, 100 W/m² power density,
    25°C ambient. Source: [B1] Ch.4 Fig 4.x and [J2].

    Correction factors applied per site:
      1. Temperature: −0.2% eta per +10 K above 300 K
        (from Schottky diode junction temperature physics — no single paper,
        standard semiconductor device physics)
      2. Humidity: −0.5 to −2% eta for humid tropical sites
        (patch antenna dielectric loss — no single open paper)

    3. Ambient temperatures [NASA POWER climatology]:
      data available at: https://power.larc.nasa.gov/

    4. Clear-sky fractions [ITU-R P.837-7 + NASA POWER]:
      Derived from annual rain statistics.

    5. Demand values (DEMONSTRATION ONLY, not utility-calibrated):
      Per-station demands in the 0.8–2.0 MW range are chosen to span roughly an order of magnitude
      across the eight sites and to be small enough that a 20-satellite constellation can plausibly
      approach service. Values are scaled informally by relative city size; they are NOT derived
      from grid-operator data and should not be compared against utility load figures (e.g. IEA city
      data-centre estimates are one to three orders of magnitude larger).


    Coordinates [WGS-84 standard geographic databases]:
      Tokyo: JMA reference | London: OS National Grid
      New York: USGS | Cape Town: SANSA
      New Delhi: Survey of India | Sao Paulo: IBGE
      San Francisco: USGS | Moscow: Rosreestr
    """
    id: int
    lat_deg: float
    lon_deg: float
    name: str
    rx_area_m2: float
    demand_W: float
    clear_sky_frac: float
    rectenna_eff_peak: float = 0.85
    rectenna_eff_min:  float = 0.70
    ambient_temp_K:    float = 290.0
    received_W:      float = 0.0
    cnr_dB:          float = 0.0
    demand_met_pct:  float = 0.0

    def __post_init__(self):
        lat = math.radians(self.lat_deg);  lon = math.radians(self.lon_deg)
        self.ecef_m = RE_M*np.array([math.cos(lat)*math.cos(lon),
                                      math.cos(lat)*math.sin(lon),
                                      math.sin(lat)])


@dataclass
class SatelliteState:
    id: int
    a_m: float
    e: float
    inc_rad: float
    raan_rad: float
    aop_rad: float
    M_rad: float
    pos_eci_m:    np.ndarray = field(default_factory=lambda: np.zeros(3))
    vel_eci_m_s:  np.ndarray = field(default_factory=lambda: np.zeros(3))
    lat_deg: float = 0.
    lon_deg: float = 0.
    alt_km: float = 0.
    illum_frac:   float = 1.0
    panel_cos: float = 1.0
    panel_temp_K: float = 290.0
    panel_eff: float = 0.295
    avail_rf_W:   float = 0.
    solar_dc_W: float = 0.
    panel_track_angle_rad: float = 0.
    point_err_az: float = 0.
    point_err_el: float = 0.
    point_err_rad: float = 0.
    delta_v_used: float = 0.
    thermal:  Optional[ThermalModel]  = None
    battery:  Optional[BatteryModel]  = None


def build_satellites(params):
    sats = [];  a0 = RE_M + params.altitude_km*1e3;  sid = 0
    for plane in range(params.n_planes):
        raan = plane*2*math.pi/params.n_planes
        for s in range(params.sats_per_plane):
            M0 = (s/params.sats_per_plane
                  + plane/(params.n_planes*params.sats_per_plane))*2*math.pi
            st = SatelliteState(
                id=sid, a_m=a0, e=params.eccentricity,
                inc_rad=math.radians(params.inc_deg),
                raan_rad=raan, aop_rad=0., M_rad=M0%(2*math.pi))
            st.thermal = ThermalModel(
                params.sat_heat_cap_J_K, params.radiator_area_m2,
                params.radiator_emiss, params.radiator_absorb,
                params.bus_area_m2, params.bus_absorb, params.bus_emiss,
                params.sat_init_temp_K)
            st.battery = BatteryModel(
                params.batt_capacity_Wh, params.batt_capacity_Ah,
                params.batt_dod_limit, params.batt_charge_eff,
                params.batt_peukert_k, params.batt_internal_r,
                params.batt_nominal_v, params.batt_ocv_slope)
            sats.append(st);  sid += 1
    return sats


def build_ground_stations():
    return _build_ground_stations_from_table(GROUND_STATION_TABLE)


# =============================================================================
# GROUND_STATION_TABLE -- Phase-1 SBSP demonstration cluster (European geography)
# =============================================================================
#
# Each row defines one rectenna site at a European city location. The eight
# cities serve as geographically realistic placeholders for ground-station
# siting in the 38-52 N latitude band; they do NOT represent real loads at
# specific facilities in those cities. (See "Demand sizing rationale" below.)
#
# -----------------------------------------------------------------------------
# DEMAND SIZING RATIONALE -- READ BEFORE EDITING DEMANDS
# -----------------------------------------------------------------------------
# Per-station demands (160-360 kW) are representative Phase-1 SBSP
# demonstration loads. They are NOT derived from existing commercial
# facilities at the selected cities. A real Slough data centre runs
# 5-50 MW; a real Frankfurt DE-CIX facility runs 70-100 MW; the demands
# here are 1-2 orders of magnitude smaller than such loads.
#
# The smaller demand scale is deliberate. A 20-satellite Phase-1 LEO
# constellation provides ~12-17 MW peak RF capacity at the moments when
# all satellites are simultaneously illuminated. The aggregate demand of
# 1,800 kW (sum of the rows below) is approximately 11% of peak supply.
# This places the system in the *demand-bound* regime where the per-station
# demand cap binds frequently, and where allocator policy choices
# (greedy vs proportional-fair vs minimum-demand) differentiate measurably.
# At commercial-facility demand levels (40-400 MW cluster total), the
# system would be permanently supply-bound and all policies would
# converge to identical "deliver everything available" behaviour --
# which is not an interesting regime for an allocator-comparison study.
#
# Equivalent real-world scales at ~200-360 kW per site:
#   * A single rack hall (not a building) within a larger data-centre campus
#   * A microgrid pilot on a non-interconnected grid (e.g., Aegean island)
#   * A research test load for validating beam-pointing and rectenna
#     performance ahead of commercial-scale deployment
#   * A high-priority backup supply for a hospital or municipal facility
#
# The manuscript should frame these as "representative Phase-1 demonstration
# loads sized for the regime where allocator architecture matters", NOT as
# "the electricity demand of city X" or "the load of the named pilot
# facility in city Y". No per-city citations are required because the
# demands are not facility-derived.
#
# -----------------------------------------------------------------------------
# WHEN TO EDIT THESE VALUES
# -----------------------------------------------------------------------------
#   * To stress-test the demand-sensitivity sweep (compG): edit demand_kW
#     values to push the cluster total above ~30% of peak supply and
#     re-run; min-demand should still stay within ~5% of LP.
#   * To re-target a different regime: scale all demands by the same
#     factor using the --demand_scale CLI flag on run_journal_figures.py;
#     do not edit individual demands unless you want non-uniform changes.
#   * To represent a Phase-2 operational pilot (10+ MW cluster): scale
#     demands up by ~10x AND scale the constellation up to 200+ satellites
#     to maintain the demand-bound regime (otherwise policies converge).
#
# -----------------------------------------------------------------------------
# OTHER ROW VALUES (lat, lon, climate, rectenna efficiency)
# -----------------------------------------------------------------------------
# Cluster geometry: 38-52 N latitude band, ~3,500 km E-W extent. At 53 deg
# orbital inclination, ground-track density peaks in this band -- the
# engineering rationale for the European geography (see Section II prose).
#
# Climate values are defensibly sourced: clear-sky fraction from 30-year
# monthly mean records (Copernicus C3S climate atlas), ambient temperature
# from 30-year mean annual records (same source). Rectenna peak/min
# efficiencies scale inversely with ambient temperature, reflecting
# Schottky-diode junction-temperature dependence (Brown 1984;
# McSpadden 1998 IEEE MTT-S).
#
# Rectenna area is standardised at 250,000 m^2 (500 x 500 m) at every
# site, matching the Section II.B nominal aperture specification.
# =============================================================================

GROUND_STATION_TABLE = [
    # name,         lat,        lon,       demand_kW, clear_sky, T_K,   eta_peak, eta_min
    ("London",      51.5074,   -0.1278,    240.0,     0.35,      284.0, 0.87,     0.72),
    ("Paris",       48.8566,    2.3522,    240.0,     0.40,      285.0, 0.86,     0.71),
    ("Frankfurt",   50.1109,    8.6821,    360.0,     0.42,      283.0, 0.87,     0.72),
    ("Madrid",      40.4168,   -3.7038,    240.0,     0.62,      288.0, 0.85,     0.70),
    ("Rome",        41.9028,   12.4964,    200.0,     0.58,      289.0, 0.85,     0.70),
    ("Athens",      37.9838,   23.7275,    160.0,     0.65,      291.0, 0.84,     0.69),
    ("Warsaw",      52.2297,   21.0122,    200.0,     0.40,      282.0, 0.88,     0.73),
    ("Istanbul",    41.0082,   28.9784,    160.0,     0.50,      287.0, 0.86,     0.71),
]
# Standardised rectenna footprint (m^2) -- applied uniformly to every station
# below to keep beam-coupling geometry identical across the cluster, isolating
# inclination / altitude / policy effects from per-site aperture differences.
DEFAULT_RX_AREA_M2 = 250_000


def _build_ground_stations_from_table(table, rx_area_m2=DEFAULT_RX_AREA_M2):
    """
    Construct GroundStation objects from GROUND_STATION_TABLE.

    Returns a list of length len(table). Each row's demand_kW is converted
    to Watts; all other fields are passed through unchanged. The rx_area_m2
    parameter is applied uniformly to all stations.
    """
    stations = []
    for idx, row in enumerate(table):
        name, lat, lon, dem_kW, clear_sky, T_amb_K, eta_peak, eta_min = row
        stations.append(GroundStation(
            idx, lat, lon, name,
            rx_area_m2=rx_area_m2,
            demand_W=dem_kW * 1e3,
            clear_sky_frac=clear_sky,
            rectenna_eff_peak=eta_peak,
            rectenna_eff_min=eta_min,
            ambient_temp_K=T_amb_K,
        ))
    return stations


# =============================================================================
#                       SIMULATION ENGINE
# =============================================================================
ECLIPSE_HOUSEKEEPING_W = 500.0  # 500 W housekeeping in eclipse.
                                 # Typical small satellite bus having 100–300 W.
                                 # 500 W is conservative for a large SBSP bus.


class SBSPSimulation:
    HL = 10000


    def __init__(self, params: SimParams):
        self.p = copy.deepcopy(params)
        self.satellites      = build_satellites(params)
        self.ground_stations = build_ground_stations()
        self.n_sats = len(self.satellites)
        self.n_gs   = len(self.ground_stations)
        self.allocator = PowerAllocator(mode=params.alloc_mode)
        self.t_unix = params.t0_unix
        self.dt     = params.dt_s

        self._n = [];  self._raan_rate = [];  self._aop_rate = []
        for s in self.satellites:
            self._n.append(OrbitalMechanics.j2_mean_motion_correction(
                s.a_m, s.e, s.inc_rad))
            self._raan_rate.append(OrbitalMechanics.j2_raan_rate(
                s.a_m, s.e, s.inc_rad))
            self._aop_rate.append(OrbitalMechanics.j2_aop_rate(
                s.a_m, s.e, s.inc_rad))

        HL = self.HL
        self.hist = {
            "t_hr":            deque(maxlen=HL),
            "delivered_MW":    deque(maxlen=HL),
            "rf_budget_MW":    deque(maxlen=HL),
            "efficiency_pct":  deque(maxlen=HL),
            "illum_pct":       deque(maxlen=HL),
            "panel_cos_mean":  deque(maxlen=HL),
            "panel_temp_mean": deque(maxlen=HL),
            "panel_eff_mean":  deque(maxlen=HL),
            "batt_soc_mean":   deque(maxlen=HL),
            "sat_temp_mean":   deque(maxlen=HL),
            "pointing_err":    deque(maxlen=HL),
            "solar_irr":       deque(maxlen=HL),
            "fresnel_num":     deque(maxlen=HL),
            "gs_delivered_kW": [deque(maxlen=HL) for _ in range(8)],
            "gs_pd_W_m2":      [deque(maxlen=HL) for _ in range(8)],
            "gs_eta_op_pct":   [deque(maxlen=HL) for _ in range(8)],
        }
        self.link_matrix     = np.zeros((self.n_sats, self.n_gs))
        self.tx_power_matrix = np.zeros((self.n_sats, self.n_gs))
        self.rx_dc_power     = np.zeros(self.n_gs)

    def step(self):
        self.t_unix += self.dt
        sun_unit, R_AU = sun_state(self.t_unix)
        irr_W_m2 = solar_irradiance_W_m2(R_AU)
        prm = self.p

        tot_cos=tot_temp=tot_eff=tot_soc=tot_sat_T=tot_pt=0.
        n_illum = 0
        mass    = prm.total_sat_mass_kg
        A_drag_bus = prm.tx_side_m*prm.tx_side_m*0.15
        Cd    = 2.2
        m_panel = prm.panel_area_m2*prm.panel_areal_kg_m2
        m_bus   = prm.bus_dry_mass_kg
        Lx = prm.tx_side_m;  Lz = prm.tx_side_m*0.05
        I_min_kgm2 = (m_bus*Lz**2 + m_panel*(Lz/2)**2)/12.
        I_max_kgm2 = (m_bus*Lx**2 + m_panel*Lx**2)/12.
        fresnel_vals = []

        for i, s in enumerate(self.satellites):
            s.M_rad    = (s.M_rad + self._n[i]*self.dt)%(2*math.pi)
            s.raan_rad += self._raan_rate[i]*self.dt
            s.aop_rad  += self._aop_rate[i]*self.dt

            nu = OrbitalMechanics.true_anomaly(s.M_rad, s.e)
            s.pos_eci_m   = OrbitalMechanics.eci_from_elements(
                s.a_m, s.e, s.inc_rad, s.raan_rad, s.aop_rad, nu)
            s.vel_eci_m_s = OrbitalMechanics.eci_velocity_from_elements(
                s.a_m, s.e, s.inc_rad, s.raan_rad, s.aop_rad, nu)

            alt_km = max(0., (s.a_m-RE_M)/1e3)
            v_mag  = np.linalg.norm(s.vel_eci_m_s)
            ecef   = OrbitalMechanics.eci_to_ecef(s.pos_eci_m, self.t_unix)
            s.lat_deg, s.lon_deg = OrbitalMechanics.ecef_to_latlon(ecef)
            s.alt_km = (np.linalg.norm(s.pos_eci_m)-RE_M)/1e3

            h_hat  = AttitudeModel.orbit_normal_hat(s.pos_eci_m, s.vel_eci_m_s)
            v_hat  = s.vel_eci_m_s/max(v_mag,1.)
            nadir  = AttitudeModel.nadir_hat(s.pos_eci_m)
            radial = -nadir
            tang   = np.cross(h_hat, radial)
            tang  /= max(np.linalg.norm(tang),1e-9)
            ca_p   = math.cos(s.panel_track_angle_rad)
            sa_p   = math.sin(s.panel_track_angle_rad)
            panel_n = ca_p*radial + sa_p*tang

            cos_ram      = abs(float(np.dot(panel_n, v_hat)))
            A_drag_panel = prm.panel_area_m2*cos_ram
            A_drag_total = A_drag_bus + A_drag_panel

            drag_vec = OrbitalMechanics.drag_accel_vector(
                s.pos_eci_m, s.vel_eci_m_s, alt_km, mass, Cd, A_drag_total)
            srp_vec  = OrbitalMechanics.srp_accel_vector(
                sun_unit, prm.panel_area_m2, mass, 1.3, R_AU)

            r_hat    = s.pos_eci_m/max(np.linalg.norm(s.pos_eci_m),1.)
            f_r_drag = float(np.dot(drag_vec, r_hat))
            f_t_drag = float(np.dot(drag_vec, tang))
            f_r_srp  = float(np.dot(srp_vec,  r_hat))
            f_t_srp  = float(np.dot(srp_vec,  tang))

            da_dt = (OrbitalMechanics.gauss_da_dt(
                         s.a_m, s.e, s.inc_rad, nu, f_r_drag, f_t_drag)
                   + OrbitalMechanics.gauss_da_dt(
                         s.a_m, s.e, s.inc_rad, nu, f_r_srp,  f_t_srp))
            s.a_m = max(RE_M+200e3, s.a_m + da_dt*self.dt)
            s.delta_v_used += np.linalg.norm(drag_vec)*self.dt

            s.illum_frac = OrbitalMechanics.eclipse_fraction(
                s.pos_eci_m, sun_unit, R_AU)

            opt_angle  = AttitudeModel.optimal_panel_track_angle(
                s.pos_eci_m, s.vel_eci_m_s, sun_unit)
            max_slew   = math.radians(prm.sun_track_rate_dps)*self.dt
            angle_err  = (opt_angle-s.panel_track_angle_rad+math.pi)%(2*math.pi)-math.pi
            s.panel_track_angle_rad += max(-max_slew, min(max_slew, angle_err))

            s.panel_cos = AttitudeModel.panel_sun_cosine(
                s.pos_eci_m, s.vel_eci_m_s, sun_unit,
                s.panel_track_angle_rad)*s.illum_frac

            s.panel_temp_K = PanelThermal.step_temperature(
                s.panel_temp_K, irr_W_m2, s.panel_cos, prm.panel_eff_stc,
                prm.panel_cap_J_K_m2, self.dt)

            s.panel_eff = PanelThermal.efficiency_at_temp(
                prm.panel_eff_stc, s.panel_temp_K, prm.panel_temp_coeff,
                prm.mission_age_yr, prm.panel_deg_rate)

            illum_clip = max(0.05, s.illum_frac)
            mppt_eff   = prm.mppt_eff_min + (prm.mppt_eff_peak-prm.mppt_eff_min)*illum_clip

            s.solar_dc_W = (prm.panel_area_m2*irr_W_m2
                            *s.panel_cos*s.panel_eff
                            *mppt_eff*(1.-prm.harness_loss))

            rf_from_solar = s.solar_dc_W*prm.dc_rf_eff
            Q_rf_dissip   = rf_from_solar*(1.-prm.dc_rf_eff)/max(prm.dc_rf_eff,1e-9)

            if s.illum_frac <= 0.05:
                rf_from_solar = 0.;  Q_rf_dissip = 0.
                s.battery.discharge(ECLIPSE_HOUSEKEEPING_W, self.dt)
            else:
                surplus_W = s.solar_dc_W*(1.-prm.dc_rf_eff)*0.5
                s.battery.charge(surplus_W, self.dt)

            max_diss = s.thermal.max_allowable_dissipation_W()
            if Q_rf_dissip > max_diss and max_diss >= 0:
                rf_from_solar = max_diss*prm.dc_rf_eff/max(1.-prm.dc_rf_eff,1e-9)
                Q_rf_dissip   = max_diss

            sun_cos_bus = max(0., float(np.dot(
                sun_unit, AttitudeModel.nadir_hat(s.pos_eci_m))))*0.25
            s.thermal.step(irr_W_m2, s.illum_frac, sun_cos_bus,
                           Q_rf_dissip + ECLIPSE_HOUSEKEEPING_W*0.3, self.dt)
            tot_sat_T += s.thermal.T
            s.avail_rf_W = max(0., rf_from_solar)

            gg_t   = AttitudeModel.gravity_gradient_torque_Nm(
                s.pos_eci_m, I_min_kgm2, I_max_kgm2)
            srp_t  = AttitudeModel.srp_torque_Nm(prm.panel_area_m2, 0.5, R_AU)
            mag_t  = AttitudeModel.magnetic_torque_Nm(s.pos_eci_m, 1.0)
            aero_t = AttitudeModel.aerodynamic_torque_Nm(
                s.pos_eci_m, s.vel_eci_m_s, alt_km,
                prm.panel_area_m2, 0.3, mass)
            total_disturb = gg_t + srp_t + mag_t + aero_t

            s.point_err_rad = AttitudeModel.pointing_error_accumulate(
                s.point_err_rad, total_disturb,
                prm.rw_max_torque, I_max_kgm2, self.dt, prm.attitude_bw_hz)
            err_deg = math.degrees(s.point_err_rad)
            s.point_err_az = min(err_deg, prm.max_pointing_err_deg*1.5)
            s.point_err_el = min(err_deg*0.6, prm.max_pointing_err_deg*1.5)
            tot_pt  += err_deg
            tot_cos += s.panel_cos;  tot_temp += s.panel_temp_K
            tot_eff += s.panel_eff;  tot_soc  += s.battery.soc
            if s.illum_frac > 0.05: n_illum += 1

            if len(fresnel_vals) < 3:
                R_rep = RE_M + prm.altitude_km*1e3
                fresnel_vals.append(WPTChannel.fresnel_number(R_rep, prm.tx_area_m2))

        link_matrix      = np.zeros((self.n_sats, self.n_gs))
        safe_cap_matrix  = np.zeros((self.n_sats, self.n_gs))
        rf_budgets       = np.array([s.avail_rf_W for s in self.satellites])
        gs_demands       = np.array([g.demand_W   for g in self.ground_stations])
        rectenna_eff_vec = np.array([g.rectenna_eff_peak for g in self.ground_stations])

        for i, s in enumerate(self.satellites):
            for j, gs in enumerate(self.ground_stations):
                lf = WPTChannel.link_factor(
                    s.pos_eci_m, s.vel_eci_m_s, self.t_unix, gs, prm)
                beam_eff = WPTChannel.beam_efficiency(
                    s.point_err_az, s.point_err_el, prm.tx_side_m)
                link_matrix[i, j]    = lf*beam_eff
                safe_cap_matrix[i,j] = WPTChannel.max_safe_tx_W(
                    s.pos_eci_m, self.t_unix, gs, prm)

        self.link_matrix = link_matrix

        tx_power, rx_dc = self.allocator.allocate(
            link_matrix, safe_cap_matrix, rf_budgets,
            gs_demands, rectenna_eff_vec,
            rx_area_vec=np.array([g.rx_area_m2 for g in self.ground_stations]),
            max_safe_pd_W_m2=prm.max_safe_pd_W_m2)
        self.tx_power_matrix = tx_power
        self.rx_dc_power = rx_dc

        # Track per-GS received RF power, incident power density, and
        # operational (load-dependent) rectenna efficiency for diagnostics.
        # These are post-allocation quantities; the allocator itself uses
        # rectenna_eff_peak as a proxy, which slightly over-estimates rx_dc
        # at the low power densities typical of LEO operation.
        P_rx_RF = np.array([
            float(np.sum(tx_power[:, j] * link_matrix[:, j]))
            for j in range(self.n_gs)
        ])
        gs_pd_W_m2 = np.array([
            P_rx_RF[j] / max(self.ground_stations[j].rx_area_m2, 1.)
            for j in range(self.n_gs)
        ])
        gs_eta_op = np.array([
            WPTChannel.rectenna_efficiency(
                P_rx_RF[j], self.ground_stations[j].rx_area_m2,
                self.ground_stations[j].rectenna_eff_peak,
                self.ground_stations[j].rectenna_eff_min)
            for j in range(self.n_gs)
        ])

        for j, gs in enumerate(self.ground_stations):
            gs.received_W     = float(rx_dc[j])
            gs.demand_met_pct = gs.received_W/max(gs.demand_W,1.)*100.
            best_s = int(np.argmax(tx_power[:, j]))
            gs.cnr_dB = WPTChannel.cnr_dB(
                self.satellites[best_s].pos_eci_m,
                self.t_unix, gs, tx_power[best_s,j], prm
            ) if tx_power[best_s,j] > 1. else -99.

        total_del = float(np.sum(rx_dc))
        total_rf  = float(np.sum(rf_budgets))
        eff       = total_del/(total_rf+1e-12)*100.
        sim_hr    = (self.t_unix - prm.t0_unix)/3600.

        h = self.hist
        h["t_hr"].append(sim_hr)
        h["delivered_MW"].append(total_del/1e6)
        h["rf_budget_MW"].append(total_rf/1e6)
        h["efficiency_pct"].append(eff)
        h["illum_pct"].append(n_illum/self.n_sats*100.)
        h["panel_cos_mean"].append(tot_cos/self.n_sats)
        h["panel_temp_mean"].append(tot_temp/self.n_sats)
        h["panel_eff_mean"].append(tot_eff/self.n_sats*100.)
        h["batt_soc_mean"].append(tot_soc/self.n_sats*100.)
        h["sat_temp_mean"].append(tot_sat_T/self.n_sats)
        h["pointing_err"].append(tot_pt/self.n_sats)
        h["solar_irr"].append(irr_W_m2)
        h["fresnel_num"].append(fresnel_vals[0] if fresnel_vals else 0.6)
        for j in range(self.n_gs):
            h["gs_delivered_kW"][j].append(rx_dc[j] / 1e3)
            h["gs_pd_W_m2"][j].append(float(gs_pd_W_m2[j]))
            h["gs_eta_op_pct"][j].append(float(gs_eta_op[j] * 100.0))

        return total_del, rx_dc

    def run_and_export(self, duration_hours=24., output_dir="./results"):
        import os, csv
        
        os.makedirs(output_dir, exist_ok=True)
        n_steps = int(duration_hours*3600./self.dt)+1
        for k in self.hist:
            if isinstance(self.hist[k], list):
                self.hist[k] = [deque(maxlen=n_steps+100) for _ in self.hist[k]]
            else:
                self.hist[k] = deque(maxlen=n_steps+100)

        energy_Wh = np.zeros(self.n_gs);  rf_total_Wh = 0.
        print(f"[SBSP] Running {duration_hours}h ({n_steps} steps @ {self.dt}s)...")
        t0 = time.time()
        last_print = t0
        for i in range(n_steps):
            total_del, rx_dc = self.step()
            rf_total_Wh += float(np.sum([s.avail_rf_W for s in self.satellites]))*self.dt/3600.
            energy_Wh   += rx_dc*self.dt/3600.
            if time.time()-last_print > 5.:
                print(f"[SBSP]  {100.*(i+1)/n_steps:.1f}%  "
                      f"t={(self.t_unix-self.p.t0_unix)/3600.:.2f}h")
                last_print = time.time()
        print(f"[SBSP] Done in {time.time()-t0:.1f}s")

        csv_path = os.path.join(output_dir,"timeseries.csv")
        with open(csv_path,"w",newline="") as f:
            w = csv.writer(f)
            hdr = ["t_hr", "delivered_MW", "rf_budget_MW", "efficiency_pct",
                   "illum_pct", "panel_cos_mean", "panel_temp_mean_K",
                   "panel_eff_pct", "batt_soc_pct_mean", "sat_temp_mean_K",
                   "pointing_err_deg_mean", "solar_irr_W_m2", "fresnel_num"]
            for j, gs in enumerate(self.ground_stations):
                hdr.append(f"gs{j}_{gs.name}_kW")
            for j, gs in enumerate(self.ground_stations):
                hdr.append(f"gs{j}_{gs.name}_pd_Wm2")
            for j, gs in enumerate(self.ground_stations):
                hdr.append(f"gs{j}_{gs.name}_eta_op_pct")
            w.writerow(hdr)
            for k in range(len(self.hist["t_hr"])):
                row = [self.hist["t_hr"][k], self.hist["delivered_MW"][k],
                       self.hist["rf_budget_MW"][k], self.hist["efficiency_pct"][k],
                       self.hist["illum_pct"][k], self.hist["panel_cos_mean"][k],
                       self.hist["panel_temp_mean"][k], self.hist["panel_eff_mean"][k],
                       self.hist["batt_soc_mean"][k], self.hist["sat_temp_mean"][k],
                       self.hist["pointing_err"][k], self.hist["solar_irr"][k],
                       self.hist["fresnel_num"][k]]
                for j in range(self.n_gs):
                    row.append(self.hist["gs_delivered_kW"][j][k])
                for j in range(self.n_gs):
                    row.append(self.hist["gs_pd_W_m2"][j][k])
                for j in range(self.n_gs):
                    row.append(self.hist["gs_eta_op_pct"][j][k])
                w.writerow(row)

        print(f"[SBSP] Wrote {csv_path}")

        gs_path = os.path.join(output_dir,"per_gs_summary.csv")
        with open(gs_path,"w",newline="") as f:
            w = csv.writer(f)
            w.writerow(["station","lat","lon","demand_MW",
                        "energy_delivered_MWh","demand_MWh","demand_met_pct",
                        "final_cnr_dB","rectenna_eff_peak","rectenna_eff_min",
                        "ambient_temp_K"])
            for j,gs in enumerate(self.ground_stations):
                dMWh = gs.demand_W*duration_hours/1e6
                eMWh = energy_Wh[j]/1e6
                w.writerow([gs.name, gs.lat_deg, gs.lon_deg,
                            gs.demand_W/1e6, eMWh, dMWh,
                            100.*eMWh/max(dMWh,1e-9), gs.cnr_dB,
                            gs.rectenna_eff_peak, gs.rectenna_eff_min,
                            gs.ambient_temp_K])
        print(f"[SBSP] Wrote {gs_path}")
        return {"csv": csv_path, "summary": gs_path,
                "energy_delivered_Wh": energy_Wh, "rf_total_Wh": rf_total_Wh}


# =============================================================================
#                   COLOUR THEME
# =============================================================================
PC = {
    "fig_bg":"#1a1f2e","ax_bg":"#242938","grid":"#3a3f52",
    "text":"#e8ecf4","cyan":"#4dd0e1","orange":"#ffb74d",
    "green":"#66bb6a","amber":"#ffd54f","red":"#ef5350",
    "purple":"#ce93d8","teal":"#4db6ac","white":"#ffffff","blue":"#42a5f5",
}
SC = {
    "sidebar_bg":"#F0F2F5","section_fg":"#1565C0","label_fg":"#37474F",
    "value_fg":"#1B5E20","btn_run_bg":"#1976D2","btn_pause_bg":"#F57F17",
    "btn_export_bg":"#2E7D32","btn_fg":"#FFFFFF","top_bg":"#263238",
    "top_label":"#90A4AE","top_value":"#80DEEA","radio_sel":"#E3F2FD",
}


def _apply_rcparams():
    plt.rcParams.update({
        "font.family":"DejaVu Sans","font.size":9,
        "axes.facecolor":PC["ax_bg"],"figure.facecolor":PC["fig_bg"],
        "text.color":PC["text"],"axes.labelcolor":PC["text"],
        "xtick.color":PC["text"],"ytick.color":PC["text"],
        "xtick.labelsize":8,"ytick.labelsize":8,
        "axes.edgecolor":PC["grid"],"axes.grid":True,
        "grid.color":PC["grid"],"grid.linewidth":0.5,
        "axes.titlepad":5,"axes.titlesize":9,"axes.labelsize":8,
        "legend.fontsize":8,"legend.framealpha":0.4,
    })


def _clr(ax):
    ax.cla()
    ax.tick_params(axis='both', labelsize=8, colors=PC["text"])
    for spine in ax.spines.values(): spine.set_edgecolor(PC["grid"])


def _draw_map(ax, sim):
    try:
        _clr(ax);  ax.set_facecolor("#0d1526")
        ax.set_xlim(-180,180);  ax.set_ylim(-90,90)
        for lat in range(-60,90,30): ax.axhline(lat,color=PC["grid"],lw=0.3,alpha=0.5)
        for lon in range(-180,181,30): ax.axvline(lon,color=PC["grid"],lw=0.3,alpha=0.5)
        ax.axhline(0,color=PC["amber"],lw=0.8,alpha=0.4,ls="--")
        for gs in sim.ground_stations:
            ax.plot(gs.lon_deg,gs.lat_deg,"^",color=PC["amber"],ms=8,zorder=5)
            ax.text(gs.lon_deg+2,gs.lat_deg+2,gs.name,color=PC["amber"],
                    fontsize=7.5,zorder=6,
                    bbox=dict(boxstyle="round,pad=0.1",facecolor="#0d152680",edgecolor="none"))
            frac = min(gs.received_W/(gs.demand_W+1e-9),1.)
            ring = Circle((gs.lon_deg,gs.lat_deg),2.5,fill=False,
                          edgecolor=PC["green"],lw=2.5*frac+0.3,alpha=0.9,zorder=4)
            ax.add_patch(ring)
        for s in sim.satellites:
            col = PC["cyan"] if s.illum_frac>0.5 else PC["orange"]
            ax.plot(s.lon_deg,s.lat_deg,"o",color=col,
                    ms=3+4*s.panel_cos,zorder=10,markeredgecolor="none",alpha=0.85)
        for j,gs in enumerate(sim.ground_stations):
            best_s = int(np.argmax(sim.tx_power_matrix[:,j]))
            if sim.tx_power_matrix[best_s,j]>100:
                sat = sim.satellites[best_s]
                alpha_val = min(0.9,sim.tx_power_matrix[best_s,j]/5e4)
                ax.plot([gs.lon_deg,sat.lon_deg],[gs.lat_deg,sat.lat_deg],
                        "-",color=PC["green"],lw=0.9,alpha=alpha_val,zorder=7)
        d = list(sim.hist["delivered_MW"])[-1] if sim.hist["delivered_MW"] else 0
        F = list(sim.hist["fresnel_num"])[-1] if sim.hist["fresnel_num"] else 0
        t = list(sim.hist["t_hr"])[-1] if sim.hist["t_hr"] else 0
        ax.set_title(f"WORLD MAP  T={t:.2f}hr | Delivered={d:.3f}MW | F#={F:.3f}",
                     color=PC["cyan"],fontsize=9,fontweight="bold")
        ax.set_xlabel("Longitude (°)",fontsize=8)
        ax.set_ylabel("Latitude (°)",fontsize=8)
    except Exception: traceback.print_exc()


def _draw_panel_physics(ax, sim):
    try:
        _clr(ax)
        h = sim.hist
        if not h["panel_cos_mean"]: return
        tv = list(h["t_hr"])
        cos_pct = [v*100 for v in h["panel_cos_mean"]]
        temp_K  = list(h["panel_temp_mean"])
        eff_pct = list(h["panel_eff_mean"])
        ax2 = ax.twinx();  ax3 = ax.twinx()
        ax3.spines["right"].set_position(("axes",1.18))
        ax3.spines["right"].set_visible(True)
        ax.fill_between(tv,cos_pct,alpha=0.15,color=PC["cyan"])
        l1, = ax.plot(tv,cos_pct,color=PC["cyan"],lw=1.8,label="cos(\u03b8)%")
        l2, = ax2.plot(tv,temp_K,color=PC["orange"],lw=1.2,ls="--",label="T_cell[K]")
        l3, = ax3.plot(tv,eff_pct,color=PC["green"],lw=1.2,ls=":",label="\u03B7_PV%")
        ax.set_ylabel("Panel cos(\u03b8) [%]",color=PC["cyan"],fontsize=8)
        ax2.set_ylabel("Cell temp [K]",color=PC["orange"],fontsize=8)
        ax3.set_ylabel("\u03B7_panel [%]",color=PC["green"],fontsize=8)
        ax.tick_params(axis='y',colors=PC["cyan"],labelsize=8)
        ax2.tick_params(axis='y',colors=PC["orange"],labelsize=8)
        ax3.tick_params(axis='y',colors=PC["green"],labelsize=8)
        ax.set_ylim(0,110);  ax2.set_ylim(140,420);  ax3.set_ylim(24,32)
        ax.set_title("Panel Tilt · Cell Temp · Eff",color=PC["cyan"],fontsize=7,fontweight="bold")
        ax.set_xlabel("Simulation time [hr]",fontsize=8)
        ax.legend(handles=[l1,l2,l3],loc="lower left",fontsize=7)
        for sp in ax2.spines.values(): sp.set_edgecolor(PC["grid"])
        for sp in ax3.spines.values(): sp.set_edgecolor(PC["grid"])
    except Exception: traceback.print_exc()


def _draw_power(ax, sim):
    try:
        _clr(ax)
        h = sim.hist
        if not h["delivered_MW"]: return
        tv = list(h["t_hr"])
        rf = list(h["rf_budget_MW"])
        dl = list(h["delivered_MW"])
        ax.fill_between(tv,rf,alpha=0.12,color=PC["orange"])
        ax.plot(tv,rf,color=PC["orange"],lw=1.4,label="RF Budget",alpha=0.8)
        ax.fill_between(tv,dl,alpha=0.22,color=PC["cyan"])
        ax.plot(tv,dl,color=PC["cyan"],lw=2.,label="Delivered DC")
        d = dl[-1] if dl else 0
        ax.set_title(f"RF BUDGET vs DELIVERED  {d:.3f} MW",
                     color=PC["cyan"],fontsize=9,fontweight="bold")
        ax.set_xlabel("Simulation time [hr]",fontsize=8)
        ax.set_ylabel("Power [MW]",fontsize=8)
        ax.legend(fontsize=8,loc="upper left")
    except Exception: traceback.print_exc()


def _draw_eclipse_batt(ax, sim):
    try:
        _clr(ax)
        h = sim.hist
        if not h["illum_pct"]: return
        tv = list(h["t_hr"]);  ax2 = ax.twinx()
        ecl = [100-v for v in h["illum_pct"]]
        ax2.fill_between(tv,ecl,alpha=0.18,color=PC["red"])
        ax2.plot(tv,ecl,color=PC["red"],lw=1.,alpha=0.9)
        ax2.set_ylabel("Eclipse fleet [%]",color=PC["red"],fontsize=8)
        ax2.tick_params(axis='y',colors=PC["red"],labelsize=8)
        ax2.set_ylim(0,105)
        for sp in ax2.spines.values(): sp.set_edgecolor(PC["grid"])
        ax.fill_between(tv,list(h["batt_soc_mean"]),alpha=0.25,color=PC["amber"])
        ax.plot(tv,list(h["batt_soc_mean"]),color=PC["amber"],lw=1.8)
        ax.set_title("BATTERY SOC (Peukert) + ECLIPSE %",
                     color=PC["amber"],fontsize=9,fontweight="bold")
        ax.set_xlabel("Simulation time [hr]",fontsize=8)
        ax.set_ylabel("Battery SOC [%]",fontsize=8);  ax.set_ylim(0,105)
    except Exception: traceback.print_exc()


def _draw_thermal(ax, sim):
    try:
        _clr(ax)
        h = sim.hist
        if not h["sat_temp_mean"]: return
        tv = list(h["t_hr"])
        ax2 = ax.twinx()
        ax2.plot(tv,list(h["panel_temp_mean"]),color=PC["orange"],lw=1.2,ls="--",label="Cell T")
        ax2.set_ylabel("Cell T [K]",color=PC["orange"],fontsize=8)
        ax2.tick_params(axis='y',colors=PC["orange"],labelsize=8)
        for sp in ax2.spines.values(): sp.set_edgecolor(PC["grid"])
        ax.fill_between(tv,list(h["sat_temp_mean"]),alpha=0.22,color=PC["red"])
        ax.plot(tv,list(h["sat_temp_mean"]),color=PC["red"],lw=1.8,label="Bus T")
        ax.set_title("THERMAL — BUS + CELL",color=PC["red"],fontsize=7,fontweight="bold")
        ax.set_xlabel("Simulation time [hr]",fontsize=8)
        ax.set_ylabel("Bus temperature [K]",fontsize=8)
    except Exception: traceback.print_exc()


def _draw_gs_bar(ax, sim):
    try:
        _clr(ax);  h = sim.hist
        if not h["gs_delivered_kW"][0]: return
        gs_del = [list(h["gs_delivered_kW"][j])[-1] for j in range(sim.n_gs)]
        gs_dem = [g.demand_W/1e3 for g in sim.ground_stations]
        x = np.arange(sim.n_gs);  w = 0.38
        ax.bar(x-w/2,gs_dem,w,color=PC["orange"],alpha=0.4,label="Demand",zorder=2)
        ax.bar(x+w/2,gs_del,w,color=PC["cyan"],alpha=0.85,label="Delivered",zorder=2)
        ax.set_xticks(x)
        ax.set_xticklabels([g.name for g in sim.ground_stations],
                           rotation=40,ha="right",fontsize=7.5)
        ax.set_title("DEMAND vs DELIVERED [kW]",color=PC["green"],fontsize=7,fontweight="bold")
        ax.set_ylabel("Power [kW]",fontsize=8);  ax.legend(fontsize=8)
    except Exception: traceback.print_exc()


def _draw_rectenna_eta(ax, sim):
    try:
        _clr(ax)
        names = [g.name for g in sim.ground_stations]
        peaks = [g.rectenna_eff_peak*100 for g in sim.ground_stations]
        mins  = [g.rectenna_eff_min*100  for g in sim.ground_stations]
        x = np.arange(len(names));  w = 0.38
        ax.bar(x-w/2,peaks,w,color=PC["cyan"],alpha=0.85,label="\u03B7_peak (%)",zorder=2)
        ax.bar(x+w/2,mins, w,color=PC["purple"],alpha=0.75,label="\u03B7_min (%)",zorder=2)
        ax.set_xticks(x)
        ax.set_xticklabels(names,rotation=40,ha="right",fontsize=7.5)
        ax.set_ylim(60,95)
        ax.set_title("PER-STATION RECTENNA \u03B7 [%]",
                     color=PC["cyan"],fontsize=5,fontweight="bold")
        ax.set_ylabel("Rectenna efficiency [%]",fontsize=8)
        ax.legend(fontsize=7)
        for i, gs in enumerate(sim.ground_stations):
            ax.text(i,mins[i]-1.5,f"{gs.ambient_temp_K-273:.0f}°C",
                    ha="center",fontsize=6.5,color=PC["amber"])
    except Exception: traceback.print_exc()


def _draw_cnr(ax, sim):
    try:
        _clr(ax)
        cnrs = [g.cnr_dB for g in sim.ground_stations]
        cols = [PC["green"] if v>10 else (PC["amber"] if v>0 else PC["red"]) for v in cnrs]
        ax.bar(range(sim.n_gs),cnrs,color=cols,alpha=0.85,zorder=2)
        ax.axhline(10,color=PC["green"],lw=1.,ls="--",alpha=0.6,label="10 dB target")
        ax.axhline(0,color=PC["red"],lw=0.8,ls="--",alpha=0.6)
        ax.set_xticks(range(sim.n_gs))
        ax.set_xticklabels([g.name for g in sim.ground_stations],
                           rotation=40,ha="right",fontsize=7.5)
        ax.set_title("CNR PER SITE [dB]",color=PC["amber"],fontsize=5,fontweight="bold")
        ax.set_ylabel("CNR [dB]",fontsize=8);  ax.legend(fontsize=7)
    except Exception: traceback.print_exc()


def _draw_heatmap(ax, sim):
    try:
        _clr(ax)
        lf = np.log10(np.maximum(sim.link_matrix,1e-12))
        im = ax.imshow(lf,aspect="auto",cmap="plasma",vmin=-12,vmax=-1)
        ax.set_yticks(range(sim.n_sats))
        ax.set_yticklabels([f"S{s.id}" for s in sim.satellites],
                           fontsize=7,color=PC["text"])
        ax.set_xticks(range(sim.n_gs))
        ax.set_xticklabels([g.name for g in sim.ground_stations],
                           rotation=40,ha="right",fontsize=7.5,color=PC["text"])
        ax.set_title("LINK MATRIX  log10(\u03B7_LEO × \u03B7_atm)",
                     color=PC["orange"],fontsize=7,fontweight="bold")
        ax.set_ylabel("Satellite ID",fontsize=8,color=PC["text"])
        cb = plt.colorbar(im,ax=ax,fraction=0.046,pad=0.04)
        cb.ax.tick_params(labelsize=7,colors=PC["text"])
    except Exception: traceback.print_exc()


def _draw_pointing(ax, sim):
    try:
        _clr(ax);  h = sim.hist
        if not h["pointing_err"]: return
        tv = list(h["t_hr"]);  ax2 = ax.twinx()
        ax2.plot(tv,list(h["solar_irr"]),color=PC["amber"],lw=1.,alpha=0.75,
                 label="TSI [W/m²]")
        ax2.set_ylabel("Solar irradiance [W/m²]",color=PC["amber"],fontsize=8)
        ax2.tick_params(axis='y',colors=PC["amber"],labelsize=8)
        for sp in ax2.spines.values(): sp.set_edgecolor(PC["grid"])
        ax.fill_between(tv,list(h["pointing_err"]),alpha=0.22,color=PC["purple"])
        ax.plot(tv,list(h["pointing_err"]),color=PC["purple"],lw=1.8)
        ax.set_title("TX POINTING ERROR [°] (GG+SRP+MAG+AERO) + TSI",
                     color=PC["purple"],fontsize=5,fontweight="bold")
        ax.set_xlabel("Simulation time [hr]",fontsize=8)
        ax.set_ylabel("Pointing error [°]",fontsize=8)
    except Exception: traceback.print_exc()


def _draw_info(ax, sim):
    try:
        _clr(ax);  ax.axis("off");  h = sim.hist
        def last(k): return list(h[k])[-1] if h[k] else 0.
        d   = last("delivered_MW")
        pk  = max(list(h["delivered_MW"])) if h["delivered_MW"] else 0
        eff = float(np.mean(list(h["efficiency_pct"]))) if h["efficiency_pct"] else 0
        cos = last("panel_cos_mean")*100
        Tp  = last("panel_temp_mean")
        ep  = last("panel_eff_mean")
        soc = last("batt_soc_mean")
        pt  = last("pointing_err")
        irr = last("solar_irr") or TSI_1AU
        F   = last("fresnel_num")
        dem = float(np.mean([g.demand_met_pct for g in sim.ground_stations]))
        prm = sim.p
        dv  = float(np.mean([s.delta_v_used for s in sim.satellites]))
        mass = prm.total_sat_mass_kg
        tau  = WPTChannel.tau_factor(RE_M+prm.altitude_km*1e3,
                                     prm.tx_area_m2, prm.rx_area_m2)
        eta_beam     = 1.-math.exp(-tau)
        eta_vec      = [g.rectenna_eff_peak for g in sim.ground_stations]
        eta_rect_mean= float(np.mean(eta_vec))
        lines = [
            ("SBSP LEO -- AEL | UofM",          PC["cyan"]),
            ("",                                 PC["text"]),
            ("CONSTELLATION",                    PC["amber"]),
            (f"  {sim.n_sats} sats / {prm.n_planes}P×{prm.sats_per_plane}", PC["text"]),
            (f"  Alt={prm.altitude_km:.0f}km  Inc={prm.inc_deg:.0f}°", PC["text"]),
            (f"  Sat mass={mass:.0f}kg ",  PC["green"]),
            ("",                                 PC["text"]),
            ("WPT BEAM  ",PC["amber"]),
            (f"  Fresnel F# = {F:.3f}",          PC["red"]),
            (f"  \u03c4\u00b2 factor = {tau:.4f}",         PC["text"]), #tau^2 
            (f"  \u03B7_beam   = {eta_beam*100:.2f}%  (1-exp(-tau))", PC["cyan"]),
            ("",                                 PC["text"]),
            ("RECTENNA  ", PC["amber"]),
            (f"  Mean peak \u03B7 = {eta_rect_mean*100:.2f}%", PC["cyan"]),
            (f"  Range: {min(eta_vec)*100:.0f}%-{max(eta_vec)*100:.0f}%",  PC["text"]),
            ("",                                 PC["text"]),
            ("SOLAR  ",PC["amber"]),
            (f"  TSI = {irr:.1f} W/m²  ", PC["text"]),
            (f"  T_cell={Tp:.0f}K  eta={ep:.2f}%",  PC["orange"]),
            (f"  cos(th)={cos:.1f}%",            PC["cyan"]),
            ("",                                 PC["text"]),
            ("POINTING  ",    PC["amber"]),
            (f"  GG+SRP+MAG+AERO  err={pt:.5f}°", PC["purple"]),
            ("",                                 PC["text"]),
            ("LIVE RESULTS",                     PC["cyan"]),
            (f"  Delivered  = {d:.3f} MW",        PC["cyan"]),
            (f"  Peak       = {pk:.3f} MW",        PC["amber"]),
            (f"  WPT \u03B7    = {eff:.2f}%",         PC["green"]),
            (f"  Demand met = {dem:.1f}%",          PC["green"]),
            (f"  Batt SOC   = {soc:.1f}%",          PC["amber"]),
            (f"  dV used    = {dv:.3f} m/s",        PC["red"]),
            (f"  Isp=220s hydrazine",               PC["text"]),
            (f"  Mode: {prm.alloc_mode}",            PC["text"]),
        ]
        y = 0.99
        for txt, col in lines:
            ax.text(0.04,y,txt,transform=ax.transAxes,color=col,
                    fontsize=8.,va="top",fontfamily="monospace")
            y -= 0.032
    except Exception: traceback.print_exc()


# =============================================================================
#                           DASHBOARD
# =============================================================================
class SBSPDashboard:
    REFRESH_MS = 280

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SBSP LEO -- AEL UofM")
        self.root.configure(bg=SC["top_bg"])
        try:    self.root.state("zoomed")
        except Exception:
            try: self.root.attributes("-zoomed",True)
            except Exception: pass
        self.sim = None;  self._running = False
        self._sim_lock = threading.Lock();  self._steps_done = 0
        self._exc_info = None;  self._build_ui()
        self.root.after(600, self._on_run)

    def _build_ui(self):
        top = tk.Frame(self.root,bg=SC["top_bg"],height=60)
        top.pack(side="top",fill="x");  top.pack_propagate(False)
        self._mv = {}
        metrics = [
            ("Sim time","0.00 hr"),("Delivered","0.000 MW"),("RF budget","0.00 MW"),
            ("WPT \u03B7","0.00%"),("Panel cos","0.0%"),("Cell T","290 K"),
            ("\u03B7_panel","29.5%"),("Batt SOC","100%"),("F#","0.595"),
            ("TSI","1361 W/m²"),("Steps","0"),
        ]
        for label,default in metrics:
            frm = tk.Frame(top,bg=SC["top_bg"],padx=10,pady=4);  frm.pack(side="left")
            tk.Label(frm,text=label,fg=SC["top_label"],bg=SC["top_bg"],
                     font=("Helvetica",8)).pack()
            var = tk.StringVar(value=default)
            tk.Label(frm,textvariable=var,fg=SC["top_value"],bg=SC["top_bg"],
                     font=("Helvetica",11,"bold")).pack()
            self._mv[label] = var

        main    = tk.Frame(self.root,bg=SC["top_bg"])
        main.pack(side="top",fill="both",expand=True)
        sidebar = tk.Frame(main,bg=SC["sidebar_bg"],width=250)
        sidebar.pack(side="left",fill="y");  sidebar.pack_propagate(False)
        s_canvas= tk.Canvas(sidebar,bg=SC["sidebar_bg"],highlightthickness=0,width=248)
        s_scroll= tk.Scrollbar(sidebar,orient="vertical",command=s_canvas.yview)
        s_canvas.configure(yscrollcommand=s_scroll.set)
        s_scroll.pack(side="right",fill="y");  s_canvas.pack(side="left",fill="both",expand=True)
        inner   = tk.Frame(s_canvas,bg=SC["sidebar_bg"])
        win_id  = s_canvas.create_window((0,0),window=inner,anchor="nw")

        def _resize(event):
            s_canvas.configure(scrollregion=s_canvas.bbox("all"))
            s_canvas.itemconfigure(win_id,width=event.width)
        inner.bind("<Configure>",_resize)
        s_canvas.bind("<Configure>",lambda e: s_canvas.itemconfigure(win_id,width=e.width))
        def _wheel(event): s_canvas.yview_scroll(int(-1*(event.delta//120)),"units")
        s_canvas.bind_all("<MouseWheel>",_wheel)
        s_canvas.bind_all("<Button-4>",lambda e: s_canvas.yview_scroll(-1,"units"))
        s_canvas.bind_all("<Button-5>",lambda e: s_canvas.yview_scroll(1,"units"))

        plot_frame = tk.Frame(main,bg=PC["fig_bg"])
        plot_frame.pack(side="left",fill="both",expand=True)
        pad = {"padx":8,"pady":1}

        def sec(t):
            tk.Frame(inner,bg=SC["sidebar_bg"],height=2).pack(fill="x",pady=(6,0))
            tk.Label(inner,text=t,fg=SC["section_fg"],bg=SC["sidebar_bg"],
                     font=("Helvetica",8,"bold"),anchor="w").pack(fill="x",**pad)

        def sldr(lbl,var,lo,hi,res=None):
            tk.Label(inner,text=lbl,fg=SC["label_fg"],bg=SC["sidebar_bg"],
                     font=("Helvetica",8),anchor="w").pack(fill="x",padx=8)
            row = tk.Frame(inner,bg=SC["sidebar_bg"]);  row.pack(fill="x",padx=6,pady=1)
            tk.Label(row,textvariable=var,fg=SC["value_fg"],bg=SC["sidebar_bg"],
                     font=("Courier",8,"bold"),width=8,anchor="e").pack(side="right")
            kw = {"variable":var,"from_":lo,"to":hi,"orient":"horizontal"}
            if res: kw["resolution"] = res
            ttk.Scale(row,**kw).pack(side="left",fill="x",expand=True)

        sec("--- ORBITAL (LEO) ---")
        self.v_alt = tk.DoubleVar(value=450);  sldr("Altitude (km)",self.v_alt,200,2000)
        self.v_pl  = tk.IntVar(value=4);       sldr("N planes",self.v_pl,2,12)
        self.v_spp = tk.IntVar(value=5);       sldr("Sats / plane",self.v_spp,2,12)
        self.v_inc = tk.DoubleVar(value=53);   sldr("Inclination (°)",self.v_inc,0,90)
        self.v_ecc = tk.DoubleVar(value=0.);   sldr("Eccentricity",self.v_ecc,0,0.05)
        self.v_age = tk.DoubleVar(value=0.);   sldr("Mission age (yr)",self.v_age,0,15)

        sec("--- SPACECRAFT MASS ---")
        self.v_busm= tk.DoubleVar(value=800);  sldr("Bus dry mass (kg)",self.v_busm,200,3000)
        self.v_arho= tk.DoubleVar(value=1.0);  sldr("Panel areal ρ (kg/m²)",self.v_arho,0.3,5.)

        sec("--- SOLAR PANEL ---")
        self.v_pan = tk.DoubleVar(value=5000); sldr("Panel area (m²)",self.v_pan,500,20000)
        self.v_peff= tk.DoubleVar(value=33.);  sldr("\u03B7_PV STC (%)",self.v_peff,10,40)
        self.v_ptc = tk.DoubleVar(value=-0.28);sldr("Temp coeff (%/°C×100)",self.v_ptc,-0.8,-0.05)
        self.v_deg = tk.DoubleVar(value=1.0);  sldr("Degrad rate (%/yr)",self.v_deg,0.5,5)
        self.v_pcap= tk.DoubleVar(value=400);  sldr("Panel C (J/K/m²)",self.v_pcap,50,800)

        sec("--- APERTURES & RF ---")
        self.v_tx  = tk.DoubleVar(value=200);  sldr("TX side (m)",self.v_tx,50,2000)
        self.v_rx  = tk.DoubleVar(value=500);  sldr("RX side (m)",self.v_rx,100,2000)
        self.v_dcrf= tk.DoubleVar(value=85);   sldr("DC-->RF eff (%)",self.v_dcrf,50,90)
        self.v_rect= tk.DoubleVar(value=85);   sldr("Fleet rectenna \u03B7 (%)",self.v_rect,50,95)

        sec("-- THERMAL --")
        self.v_radA= tk.DoubleVar(value=300);  sldr("Radiator area (m²)",self.v_radA,50,1000)
        self.v_rade= tk.DoubleVar(value=0.92); sldr("Radiator emissivity",self.v_rade,0.7,1.)

        sec("--- ADCS ---")
        self.v_rwtq= tk.DoubleVar(value=0.2);  sldr("RW max torque (N·m)",self.v_rwtq,0.05,2.)
        self.v_atbw= tk.DoubleVar(value=0.1);  sldr("ACS bandwidth (Hz)",self.v_atbw,0.01,1.)

        sec("--- BATTERY ---")
        self.v_batt= tk.DoubleVar(value=3600); sldr("Capacity (Wh)",self.v_batt,200,10000)
        self.v_dod = tk.DoubleVar(value=80);   sldr("Max DoD (%)",self.v_dod,20,95)

        sec("--- SIMULATION ---")
        self.v_mode = tk.StringVar(value="greedy")
        self.v_speed= tk.IntVar(value=5)
        mf = tk.Frame(inner,bg=SC["sidebar_bg"]);  mf.pack(fill="x",padx=8,pady=3)
        tk.Label(mf,text="Allocator:",fg=SC["label_fg"],bg=SC["sidebar_bg"],
                 font=("Helvetica",8)).pack(side="left")
        for txt,val in [("Greedy","greedy"),("PropFair","prop_fair"),("MinDem","min_demand")]:
            tk.Radiobutton(mf,text=txt,variable=self.v_mode,value=val,
                           fg=SC["section_fg"],bg=SC["sidebar_bg"],
                           selectcolor=SC["radio_sel"],activebackground=SC["sidebar_bg"],
                           font=("Helvetica",8)).pack(side="left")
        sldr("Steps / refresh",self.v_speed,1,30)
        tk.Frame(inner,bg=SC["sidebar_bg"],height=10).pack()

        bk = {"font":("Helvetica",9,"bold"),"bd":0,"pady":8,"cursor":"hand2","relief":"flat"}
        tk.Button(inner,text="\u25B6  RUN / RESTART",fg=SC["btn_fg"],bg=SC["btn_run_bg"],
                  command=self._on_run,**bk).pack(fill="x",padx=10,pady=4)
        self._pb = tk.Button(inner,text="\u23F8  PAUSE",fg=SC["btn_fg"],bg=SC["btn_pause_bg"],
                              command=self._on_pause,**bk)
        self._pb.pack(fill="x",padx=10,pady=4)
        tk.Button(inner,text="\u2B07  EXPORT PDF",fg=SC["btn_fg"],bg=SC["btn_export_bg"],
                  command=self._on_export,**bk).pack(fill="x",padx=10,pady=4)
        tk.Frame(inner,bg=SC["sidebar_bg"],height=16).pack()

        _apply_rcparams()
        self._fig = plt.figure(figsize=(18,10),facecolor=PC["fig_bg"])
        self._fig.suptitle(
            "SBSP AEL UofM",
            color=PC["cyan"],fontsize=7,fontweight="bold",y=0.98)

        gsl = gridspec.GridSpec(4,4,figure=self._fig,
                                hspace=0.90,wspace=0.72,
                                left=0.05,right=0.98,top=0.95,bottom=0.07)
        self._ax = {
            "map":   self._fig.add_subplot(gsl[0:2,0:2]),
            "panel": self._fig.add_subplot(gsl[0,2]),
            "info":  self._fig.add_subplot(gsl[0:2,3]),
            "pwr":   self._fig.add_subplot(gsl[1,2]),
            "ecbat": self._fig.add_subplot(gsl[2,0]),
            "therm": self._fig.add_subplot(gsl[2,1]),
            "gs":    self._fig.add_subplot(gsl[2,2]),
            "cnr":   self._fig.add_subplot(gsl[2,3]),
            "heat":  self._fig.add_subplot(gsl[3,0:2]),
            "point": self._fig.add_subplot(gsl[3,2]),
            "rect":  self._fig.add_subplot(gsl[3,3]),
        }
        self._canvas = FigureCanvasTkAgg(self._fig,master=plot_frame)
        self._canvas.get_tk_widget().pack(fill="both",expand=True)
        tb_frame = tk.Frame(plot_frame,bg=PC["fig_bg"]);  tb_frame.pack(fill="x")
        NavigationToolbar2Tk(self._canvas,tb_frame)

    def _make_params(self):
        return SimParams(
            n_planes=int(self.v_pl.get()),
            sats_per_plane=int(self.v_spp.get()),
            altitude_km=float(self.v_alt.get()),
            inc_deg=float(self.v_inc.get()),
            eccentricity=float(self.v_ecc.get()),
            tx_side_m=float(self.v_tx.get()),
            panel_area_m2=float(self.v_pan.get()),
            panel_areal_kg_m2=float(self.v_arho.get()),
            panel_eff_stc=float(self.v_peff.get())/100.,
            panel_temp_coeff=float(self.v_ptc.get())/100.,
            panel_deg_rate=float(self.v_deg.get())/100.,
            panel_cap_J_K_m2=float(self.v_pcap.get()),
            dc_rf_eff=float(self.v_dcrf.get())/100.,
            rx_side_m=float(self.v_rx.get()),
            rectenna_eff_peak=float(self.v_rect.get())/100.,
            radiator_area_m2=float(self.v_radA.get()),
            radiator_emiss=float(self.v_rade.get()),
            rw_max_torque=float(self.v_rwtq.get()),
            attitude_bw_hz=float(self.v_atbw.get()),
            batt_capacity_Wh=float(self.v_batt.get()),
            batt_capacity_Ah=float(self.v_batt.get())/48.,
            batt_dod_limit=float(self.v_dod.get())/100.,
            bus_dry_mass_kg=float(self.v_busm.get()),
            mission_age_yr=float(self.v_age.get()),
            alloc_mode=self.v_mode.get())

    def _new_sim(self):
        with self._sim_lock:
            self.sim = SBSPSimulation(self._make_params())
            self._steps_done = 0

    def _on_run(self):
        self._running = False
        time.sleep(0.08)
        self._new_sim()
        self._exc_info = None
        self._running = True
        self._pb.config(text="\u23F8  PAUSE",bg=SC["btn_pause_bg"])
        threading.Thread(target=self._sim_loop,daemon=True).start()
        self.root.after(self.REFRESH_MS,self._refresh)

    def _on_pause(self):
        self._running = not self._running
        self._pb.config(
            text="\u25B6  RESUME" if not self._running else "\u23F8  PAUSE",
            bg="#C62828" if not self._running else SC["btn_pause_bg"])
        if self._running:
            threading.Thread(target=self._sim_loop,daemon=True).start()
            self.root.after(self.REFRESH_MS,self._refresh)

    def _on_export(self):
        if self.sim is None:
            messagebox.showinfo("Export","Start simulation first."); return
        from tkinter.filedialog import asksaveasfilename
        path = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF","*.pdf"),("All","*.*")],
            initialfile="sbsp_export.pdf")
        if not path: return
        with self._sim_lock:
            _apply_rcparams()
            fig2 = plt.figure(figsize=(28,20));  fig2.patch.set_facecolor(PC["fig_bg"])
            fig2.suptitle("SBSP AEL UofM",
                          color=PC["cyan"],fontsize=10,fontweight="bold")
            gsl2 = gridspec.GridSpec(4,4,figure=fig2,hspace=0.90,wspace=0.72,
                                     left=0.05,right=0.97,top=0.95,bottom=0.05)
            a2 = {
                "map":   fig2.add_subplot(gsl2[0:2,0:2]),
                "panel": fig2.add_subplot(gsl2[0,2]),
                "info":  fig2.add_subplot(gsl2[0:2,3]),
                "pwr":   fig2.add_subplot(gsl2[1,2]),
                "ecbat": fig2.add_subplot(gsl2[2,0]),
                "therm": fig2.add_subplot(gsl2[2,1]),
                "gs":    fig2.add_subplot(gsl2[2,2]),
                "cnr":   fig2.add_subplot(gsl2[2,3]),
                "heat":  fig2.add_subplot(gsl2[3,0:2]),
                "point": fig2.add_subplot(gsl2[3,2]),
                "rect":  fig2.add_subplot(gsl2[3,3]),
            }
            self._draw_all(a2)
            plt.savefig(path,dpi=150,bbox_inches="tight",
                        facecolor=PC["fig_bg"],edgecolor="none")
            plt.close(fig2)
        messagebox.showinfo("Export",f"Saved:\n{path}")

    def _draw_all(self, ax):
        if self.sim is None: return
        _draw_map(ax["map"],self.sim)
        _draw_panel_physics(ax["panel"],self.sim)
        _draw_info(ax["info"],self.sim)
        _draw_power(ax["pwr"],self.sim)
        _draw_eclipse_batt(ax["ecbat"],self.sim)
        _draw_thermal(ax["therm"],self.sim)
        _draw_gs_bar(ax["gs"],self.sim)
        _draw_cnr(ax["cnr"],self.sim)
        _draw_heatmap(ax["heat"],self.sim)
        _draw_pointing(ax["point"],self.sim)
        _draw_rectenna_eta(ax["rect"],self.sim)

    def _sim_loop(self):
        while self._running:
            n = max(1,int(self.v_speed.get()))
            try:
                with self._sim_lock:
                    for _ in range(n):
                        self.sim.step();  self._steps_done += 1
            except Exception:
                self._exc_info = traceback.format_exc()
                self._running = False;  break
            time.sleep(0.005)

    def _refresh(self):
        if not self._running:
            if self._exc_info:
                messagebox.showerror("Simulation Error",self._exc_info[:2000])
                self._exc_info = None
            return
        try:
            with self._sim_lock:
                if self.sim is None: return
                sim = self.sim;  h = sim.hist
                def last(k): return list(h[k])[-1] if h[k] else 0.
                self._mv["Sim time"].set(f"{last('t_hr'):.2f} hr")
                self._mv["Delivered"].set(f"{last('delivered_MW'):.3f} MW")
                self._mv["RF budget"].set(f"{last('rf_budget_MW'):.2f} MW")
                self._mv["WPT \u03B7"].set(f"{last('efficiency_pct'):.2f}%")
                self._mv["Panel cos"].set(f"{last('panel_cos_mean')*100:.1f}%")
                self._mv["Cell T"].set(f"{last('panel_temp_mean'):.0f} K")
                self._mv["\u03B7_panel"].set(f"{last('panel_eff_mean'):.2f}%")
                self._mv["Batt SOC"].set(f"{last('batt_soc_mean'):.1f}%")
                self._mv["F#"].set(f"{last('fresnel_num'):.3f}")
                self._mv["TSI"].set(f"{last('solar_irr'):.1f} W/m²")
                self._mv["Steps"].set(str(self._steps_done))
                self._draw_all(self._ax)
            self._fig.canvas.draw_idle()
        except Exception: pass
        self.root.after(self.REFRESH_MS,self._refresh)


# =============================================================================
#                    ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    import sys
    if "--batch" in sys.argv:
        _apply_rcparams()
        print("="*70)
        print("  SBSP LEO ")
        print("="*70)
        for mode in ("greedy","prop_fair","min_demand"):
            prm = SimParams(alloc_mode=mode)
            sim = SBSPSimulation(prm)
            tau = WPTChannel.tau_factor(RE_M+prm.altitude_km*1e3,
                                        prm.tx_area_m2, prm.rx_area_m2)
            F   = WPTChannel.fresnel_number(RE_M+prm.altitude_km*1e3, prm.tx_area_m2)
            print(f"\n  Mode={mode}  Sat mass={prm.total_sat_mass_kg:.0f}kg  "
                  f"Isp={prm.isp_s:.0f}s")
            print(f"  tau={tau:.4f}  eta_beam={1-math.exp(-tau):.4f}  F#={F:.3f}")
            for gs in sim.ground_stations:
                print(f"    {gs.name:<12} eta_peak={gs.rectenna_eff_peak*100:.1f}%  "
                      f"[ESTIMATED]  Tamb={gs.ambient_temp_K-273:.0f}C")
            for tick in range(120):
                for _ in range(5): sim.step()
                if tick % 30 == 0:
                    d  = list(sim.hist["delivered_MW"])[-1]
                    rf = list(sim.hist["rf_budget_MW"])[-1]
                    sc = list(sim.hist["batt_soc_mean"])[-1]
                    print(f"  tick={tick:4d}  del={d:.3f}MW  rf={rf:.3f}MW  SOC={sc:.1f}%")
        print("\nDone.")
    else:
        print("SBSP LEO -- Hurrah! The Project is Done)")
        root = tk.Tk()
        app  = SBSPDashboard(root)
        root.mainloop()