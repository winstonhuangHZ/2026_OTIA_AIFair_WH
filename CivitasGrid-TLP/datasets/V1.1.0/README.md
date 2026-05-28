# CivitasGrid-TLP v1.1.0 —  (Dataset 4)

##  Overview

This release provides multiple dataset tiers derived from a common pool of grid candidates through **progressive grid-level quality control**.

- Initial grid candidates — 7,500 grids
- **WorldPop-filtered dataset** — **6,178 grids**
- **Mid Quality (MQ) dataset** — **4,293 grids**
- **High Quality (HQ) dataset** — **2,833 grids**

> **Important:** Filtering is applied at the **grid level**.  
> Once a grid is removed, **all associated years** `(grid_id, year)` are dropped.

---

## Dataset Tier Tree (Progressive QC)

```text
CivitasGrid-TLP v1.1.0 (Dataset 4)
└── Initial grid candidates (7500)
    └── WorldPop-filtered (6178)
        ├── Mid Quality / MQ (4293)   [>= 3 valid transport blocks]
        └── High Quality / HQ (2833)  [>= 4 valid transport blocks]
```

---

## Filtering Pipeline Diagram (ASCII)

```text
(7500) Initial candidates
   |
   |-- WorldPop QC (remove nodata & low-pop grids)
   v
(6178) WorldPop-filtered
   |
   |-- Transport coverage QC (MQ: >=3 valid blocks)
   v
(4293) Mid Quality (MQ)
   |
   |-- Transport coverage QC (HQ: >=4 valid blocks)
   v
(2833) High Quality (HQ)
```

---

## Grid-Level Filtering Criteria

### 1) WorldPop-based Filtering (Population Validity)

A grid is removed if it satisfies **either** condition:

- contains **WorldPop nodata / invalid values** in any year, **or**
- has **population density < 5 persons/km²** in **any** year

These grids can introduce noise and reduce stability in long-tail dynamics modeling.

---

### 2) Transportation Feature Coverage Filtering (OSM Completeness)

Transportation-related features are defined as:

- `Intersec`
- `len_mot`
- `len_tru`
- `len_pri`
- `len_sec`
- `len_ter`
- `len_urb`

**Definition of valid block:**  
A transportation feature is considered valid if its extracted value is **strictly > 0**.

---

#### Mid Quality (MQ) Dataset Criteria

A grid is removed if it contains **fewer than 3 valid non-zero transportation feature blocks** among the set above.

- **Resulting tier:** **4,293 grids**

---

#### High Quality (HQ) Dataset Criteria

A grid is removed if it contains **fewer than 4 valid non-zero transportation feature blocks** among the set above.

- **Resulting tier:** **2,833 grids**


Grids with insufficient valid transportation indicators may yield unstable ML behavior and reduce generalisation reliability, especially under long-tail regression settings.

---

## Recommended Usage

- **HQ dataset (2833 grids)** is recommended as the **default benchmark tier** for:
  - long-tail regression evaluation
  - MoE gating stability experiments
  - cross-grid generalisation splits
- **MQ dataset (4293 grids)** can be used for:
  - sensitivity tests of QC strictness
  - robustness / coverage tradeoff studies
  
  ---
  
## OpenStreetMap Extraction

All OSM-derived features were extracted using the Overpass API on:

📅 **January 3rd, 2026**

Because OpenStreetMap is continuously updated, OSM-derived features may differ if re-extracted at a later date.  
For strict reproducibility, users are encouraged to use the released dataset version rather than re-running the OSM extraction pipeline without controlling for OSM snapshot timing.
