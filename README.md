# Summary of the Space-based-solar-power-AEL-LAB-SBSP-
The main purpose of this work is to formulate constellation-level power allocation as a two-tier scheduling problem and evaluate it in a physically grounded, end-end-end simulation of a 20-satellite Walker constellation beaming 2.45 GHz microwave power to an eight-station cluster, with propagation simulated over 24 hours using a coupled orbital, thermal, battery, and wireless power transfer channel model.



---

## Contents
- [System Model](#system-model)
- [Two-Tier Allocator Architecture](#Two-Tier-Allocator-Architecture)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [License](#license)
---

## 1. System Model
The proposed framework consists of a space segment and a ground segment, linked by an maximum power transfer (MPT) chain operating at $2.45 \text{GHz}$. In an example 20-satellite Walker delta constellation, each satellite carries a $5000m^2$ GaAs multi-junction PV array operating at 33\% BOL efficiency. Its output is conditioned by a maximum-power-point-tracking (MPPT) DC–DC converter  ($\eta_{\mathrm{MPPT}} = 96\%$) and buffered by a $3.6\text{kWh}$ lithium-ion battery at 80\% depth of discharge (DoD). It is then converted to microwave power by a Class-E PA target ($\eta_{\mathrm{DC-RF}} = 85$\%) 
and radiated through a $200\\mathrm{m} \times 200\\mathrm{m}$ phased-array transmit aperture. The atmospheric propagation losses are modeled using ITU-R~P.618 at \${2.45}\text{GHz}$, accounting for beam-coupling and attenuation variability as a function of elevation angle and weather for each pass. On a GS, each rectenna site consists of a $500\\mathrm{m} \times 500\\mathrm{m}$ Schottky-diode array rectenna (with a typical efficiency $\eta_{\mathrm{rect}} = 72\text{-}85$)\% 
delivering ${160}-{360} \text{kW}$ to a co-located pilot load, with the cumulative sun-to-load efficiency $\eta_{\mathrm{total}}$ ranging from 14\% - 20\% over a 24-hour operational average.

# Proposed Constellation geometry
The proposed constellation is described by the Walker delta notation $\mathcal{W}(T/P/F)$, where $T = S = 20$ is the total number of satellites, $P = 4$ is the number of equally spaced orbital planes, and $F = 1$ is the phasing parameter that determines the inter-plane mean-anomaly offset. Each plane contains $S/P = 5$ satellites, equally spaced in mean anomaly by $\Delta M = 2\pi/(S/P)$. We place each satellite in a circular orbit at an altitude of $h = \text{450 km}$. Please refer to the ![Proposed Model](C:\Users\iqbala2\Downloads\system_overview_page-0001) for the system model.

---
## 2. Two Tier 
