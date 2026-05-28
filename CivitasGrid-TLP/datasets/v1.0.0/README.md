# CivitasGrid-TLP Dataset

## Schema Version
**v1.0.0 — initial public release**

CivitasGrid-TLP (TransLuxPop) is a grid-level (30 arcsec to 1 arcmin grids) panel dataset integrating:
- transportation morphology derived from **OpenStreetMap (OSM)**
- **VIIRS nighttime lights** aggregates
- **WorldPop** population density aggregates and dynamics

Each record corresponds to a **(grid_id, year)** observation.

---

## Dataset Categories

Each released version of CivitasGrid-TLP contains **two dataset tiers**:

1. **Raw Data** — direct extraction output (minimal filtering)
2. **HQ Data** — curated high-quality dataset after quality control (recommended)

Both tiers are provided to support:
- maximum transparency (raw)
- reliable benchmarking and modeling (HQ)

---

## Raw Data

Raw data refers to dataset files produced directly by the automated extraction pipeline **without post-filtering**.  

This tier may include:
- grids with missing or incomplete OSM features (e.g., due to Overpass API failure or local OSM incompleteness)
- grids with missing values / nodata in VIIRS or WorldPop rasters
- grids partially overlapping with water bodies or non-urban regions
- rare edge-case failures from raster sampling or network extraction

### Recommended usage
Raw data is mainly intended for:
- pipeline validation and debugging
- reproducibility checks (to verify what was extracted before QC)
- future alternative cleaning criteria
- research on data coverage, bias, and extraction failure modes

### Notes / Warnings
Raw data may contain records that are:
- not suitable for model training without additional filtering
- potentially misleading if used directly in predictive experiments

---

## HQ (High Quality) Data

The HQ dataset is the **recommended benchmark tier** for modeling and evaluation.  
It is obtained by applying a consistent cleaning process to remove grids with insufficient transportation information or invalid remote sensing signals.

### Quality Control Criteria (Grid-Level Filtering)

A grid cell is **removed entirely** (all associated years are dropped) if it meets any of the following conditions:

#### 1) Insufficient valid OpenStreetMap transportation information
A grid is removed if it contains **fewer than 4 valid (non-zero) OSM-derived transportation features**, among the following set:

- `Intersec` (intersection count)
- `len_mot` (motorway length)
- `len_tru` (trunk length)
- `len_pri` (primary road length)
- `len_sec` (secondary road length)
- `len_ter` (tertiary road length)
- `len_urb` (urban roads length; residential/unclassified/service/living_street)

**Definition of valid:**  
A feature is considered valid if its extracted value is **strictly greater than 0**.

**Rationale:**  
Grids with too few valid OSM indicators are often caused by:
- Overpass download failure / timeout
- grids located in sparse-mapped regions
- water-body or non-road-dominated areas  
Such grids can produce biased or unstable ML behavior and reduce generalisation reliability.

---

#### 2) Missing / invalid remote sensing data
A grid is removed if it contains **nodata / invalid values** in either:
- **VIIRS nighttime lights**, or
- **WorldPop population density**

This rule ensures that each grid has consistent time-series signals for learning dynamics such as `dWorldPop` and `dlogVIIRS`.

---

## Data Extraction Timestamp

### OpenStreetMap Extraction
All OSM-derived features were extracted using the Overpass API on:

📅 **December 29, 2025**

Because OpenStreetMap is continuously updated, OSM-derived features may differ if re-extracted at a later date.  
For strict reproducibility, users are encouraged to use the released dataset version rather than re-running the OSM extraction pipeline without controlling for OSM snapshot timing.

---

## Reproducibility Note
The dataset construction pipeline and environment specification are provided in this repository.  
See:
- `code/` for data extraction scripts and notebooks  
- `environment.yml` for dependency pinning  
- `DATA_NOTICE.md` for licensing and attribution  
