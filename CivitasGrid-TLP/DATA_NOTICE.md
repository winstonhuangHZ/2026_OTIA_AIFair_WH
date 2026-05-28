# Data Licensing and Attribution Notice
**CivitasGrid-TLP**

This repository contains both code and dataset artifacts. **Code and dataset are licensed under different terms**.

---

## 2) Code License (MIT)
All source code is licensed under the **MIT License** (see `LICENSE`).

---

## 3) Dataset License (ODbL 1.0)
The dataset files under `datasets/ `are released under ODbL v1.0 (see `LICENSES/ODbL-1.0.txt`), since they contain **derived data from OpenStreetMap**.

---

## 3) Upstream Data Sources & Attribution Requirements

### 3.1 OpenStreetMap (OSM)
- Source: © OpenStreetMap contributors  
- Website: https://www.openstreetmap.org  
- License: ODbL 1.0  
- Used for: road network morphology features (road length by class, intersection counts, etc.)

**Attribution required:**  
> © OpenStreetMap contributors — ODbL 1.0

---

### 3.2 WorldPop
- Source: WorldPop, University of Southampton  
- Website: https://www.worldpop.org  
- License: CC BY 4.0  
- Used for: population density aggregated to grid cells  

See: `LICENSES/CC-BY-4.0.txt`

**Attribution required:**  
> WorldPop — CC BY 4.0 (University of Southampton)

---

### 3.3 VIIRS Nighttime Lights
- Source: NOAA / NASA VIIRS Nighttime Lights products  
- License: open/public data (see product documentation)  
- Used for: annual nighttime lights intensity aggregated to grid cells  

---

## 4) Redistribution Notes (ODbL Share-Alike)
- This repository **does not redistribute raw OSM database dumps**, raw WorldPop rasters, or raw VIIRS rasters.
- The dataset contains **aggregated/derived features** computed from these sources.
- If you publicly release a derivative dataset based on TransLuxPop, you must comply with **ODbL share-alike requirements**, including providing access to the derivative database in a machine-readable form under ODbL (or a compatible license).