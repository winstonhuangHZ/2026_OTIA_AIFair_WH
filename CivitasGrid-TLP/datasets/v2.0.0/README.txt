# CivitasGrid-TLP v2.0.0 — Historical Transportation Dynamics Dataset

## Overview

This release introduces **temporally consistent transportation features** derived from OpenStreetMap historical data via the **ohsome API**, enabling analysis of infrastructure-driven urban dynamics over time.

- Initial grid candidates — **7,500 grids**
- **WorldPop-filtered dataset** — **6,178 grids** *(same as v1.1.0)*
- **Mid Quality (MQ) dataset** — **3,962 grids** *(39,620 grid–year observations)*
- **High Quality (HQ) dataset** — **2,566 grids** *(25,660 grid–year observations)*

> **Key Contribution:** This release introduces **yearly transportation features (2015–2024)** in a grid–year panel format, supporting temporal modeling of infrastructure–population co-evolution.

---

## 🆕 What's New in v2.0.0

### 1. **Temporal Coverage: 2015–2024 for Road Length Features**

Transportation infrastructure is now represented in **long panel format**, with one row per grid–year observation (2015–2024).

For each grid and year, the following road length features are provided:
- `len_mot` (motorway)
- `len_tru` (trunk)
- `len_pri` (primary)
- `len_sec` (secondary)
- `len_ter` (tertiary)
- `len_urb` (urban roads: residential + unclassified + service)

grid_id | year | len_mot | len_tru | len_pri | len_sec | len_ter | len_urb


**Static features (single snapshot):**
- `Intersec` — intersection count (Overpass API, 2026-01-03)
- `Intersec_use` — intersection density (`Intersec / cell_area`)

This enables:
- Year-to-year road network expansion analysis
- Before/after studies of major infrastructure projects
- Temporal feature engineering (lags, growth rates, accelerations)

---

### 2. **Hybrid Data Source: ohsome API + Overpass API**

#### Road Length Features (temporal): **ohsome API**

**Advantages of ohsome API:**
- **Consistent multi-year extraction** from the OSM full-history database
- **Reproducible snapshots** at exact timestamps (e.g., `2015-01-01T00:00:00Z`)
- **Research-oriented infrastructure** maintained by HeiGIT (Heidelberg University)
- **Purpose-built for historical analysis**, avoiding ad-hoc snapshot inconsistencies

**Extraction timestamps:**
2015-01-01T00:00:00Z
2016-01-01T00:00:00Z
...
2024-01-01T00:00:00Z


---

#### Intersection Count (static): **Overpass API**

The ohsome API does not currently support node-level topology queries required for accurate intersection identification. Intersection counting requires:

- Consolidating nearby nodes within a tolerance
- Counting node degree (edges meeting at a point)
- Filtering geometry artifacts

**Solution:** Intersection count (`Intersec`) is extracted as a **single static snapshot** using the same Overpass-based method as in v1.1.0.

**Extraction timestamp:**
2026-01-03 (Overpass API query)


To ensure comparability across grids, we additionally construct:
- `Intersec_use = Intersec / cell_area`

This density-based measure serves as a **time-invariant proxy for average road network complexity**, particularly suitable for cross-grid comparisons.

---

### 3. **Revised Quality Control Criteria**

#### Temporal OSM Completeness Check (Road Length Features)

A grid is considered to have a **valid temporal road feature** if:
feature_value > 0 in at least 70% of years (≥7 out of 10)

No extreme discontinuities (e.g., sudden drop to 0 followed by recovery)


This filters out:
- Grids with sporadic or late OSM mapping
- Inconsistent historical backfills

#### Static Check (Intersection Density)

- `Intersec > 0` in the 2026 snapshot

---

### Combined Quality Thresholds

- **MQ:** ≥3 valid transportation features across {`Intersec`, 6 temporal road types}
- **HQ:** ≥4 valid transportation features across {`Intersec`, 6 temporal road types}

**Result:** Stricter temporal consistency filtering relative to v1.1.0
- MQ: 4,293 → **3,962 grids** (-7.7%)
- HQ: 2,833 → **2,566 grids** (-9.4%)

---

## Dataset Tier Tree (Progressive QC)

```text
CivitasGrid-TLP v2.0.0 (Historical)
└── Initial grid candidates (7500)
    └── WorldPop-filtered (6178)
        ├── Mid Quality / MQ (3962 grids; 39,620 grid–years)
        └── High Quality / HQ (2566 grids; 25,660 grid–years)

---

## Comparison: v1.1.0 (Static) vs v2.0.0 (Hybrid Temporal)

| Aspect | v1.1.0 (Overpass) | v2.0.0 (ohsome + Overpass) |
|--------|-------------------|----------------------------|
| **Temporal Coverage** | Single snapshot (2026-01-03) | 10 yearly snapshots (2015–2024) for road lengths |
| **Data Source** | Overpass API (all features) | ohsome API (road lengths) + Overpass (intersections) |
| **Temporal Features** | 0 | 6 road types × 10 years = 60 |
| **Static Features** | 7 | 1 (`Intersec` only) |
| **Quality Control** | Static completeness check | Temporal consistency (70% rule) + static check |
| **MQ Grid Count** | 4,293 | 3,962 (-7.7%) |
| **HQ Grid Count** | 2,833 | 2,566 (-9.4%) |
| **Use Case** | Cross-sectional regression | Panel regression, time-series modeling |
| **Reproducibility** | Snapshot date-dependent | Exact timestamp control (ohsome), fixed snapshot (Intersec) |

---


## Recommended Usage

### Primary Analysis (HQ dataset recommended)

- **Panel regression** with grid and year fixed effects
- **Dynamic models** of infrastructure-population feedback loops
- **Time-based splits** for temporal generalization (e.g., train on 2015–2020, test on 2021–2024)
- **Difference-in-differences** with real-world infrastructure projects

### Sensitivity Tests (MQ dataset)

- Robustness checks under relaxed quality thresholds
- Coverage-performance tradeoff analysis

### ohsome API Queries (Temporal Road Lengths)

Executed on: **January 25, 2026**  
API version: **ohsome API v1.10.0**  
Endpoint: `https://api.ohsome.org/v1/elements/length`

**Query parameters:**
```json
{
  "bboxes": ",,,",
  "time": "2015-01-01,2016-01-01,...,2024-01-01",
  "filter": "highway in (motorway,trunk,primary,secondary,tertiary,residential,unclassified,service) and type:way"
}