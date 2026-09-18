# Multi-Provider Grid Power Allocation & Load Balancer — MVP v1

## Goal
Build a working MVP that implements the core control loop: **telemetry → weather → prediction → balance → battery/grid/shed → dispatch → log → dashboard**. Uses simulated telemetry + real weather API + simple ML models + SQLite logging + a live web dashboard.

---

## Project Structure (Full — Stage 1 + Stage 2)

Files marked with `✅` are implemented in MVP v1. Files marked with `⬜` are created as empty placeholders for Stage 2.

```
microgrid_loadbalancer/
│
├── main.py                              ✅  Entry point — starts control loop + dashboard
├── requirements.txt                     ✅  Python dependencies
├── README.md                            ✅  Project overview & setup instructions
│
├── config/                              #  Configuration files
│   ├── default_config.yaml              ✅  System constants (battery limits, grid caps, coords)
│   └── logging_config.yaml              ⬜  Python logging configuration (Stage 2)
│
├── src/                                 #  Core application source code
│   ├── __init__.py                      ✅
│   ├── core/                            #  Control logic & orchestration
│   │   ├── __init__.py                  ✅
│   │   ├── control_loop.py              ✅  Main procedural control loop orchestrator
│   │   ├── balance.py                   ✅  FR-004: Net energy balance computation
│   │   ├── battery.py                   ✅  FR-005: Battery SoC constraint enforcement
│   │   ├── load_shed.py                 ✅  FR-006: Priority-based load throttling
│   │   └── dispatcher.py               ✅  FR-007: Actuator command dispatch (simulated)
│   │
│   ├── ingestion/                       #  Data ingestion layer
│   │   ├── __init__.py                  ✅
│   │   ├── telemetry.py                 ✅  FR-001: Simulated smart meter telemetry
│   │   ├── weather.py                   ✅  FR-002: Open-Meteo weather API client
│   │   └── simulator.py                 ⬜  pymgrid integration adapter (Stage 2)
│   │
│   ├── safety/                          #  Hardware safety constraints
│   │   ├── __init__.py                  ✅
│   │   ├── frequency_guard.py           ⬜  Grid frequency drift protection (Stage 2)
│   │   └── transformer_guard.py         ⬜  Transformer capacity limit monitor (Stage 2)
│   │
│   └── utils/                           #  Shared utilities
│       ├── __init__.py                  ✅
│       └── helpers.py                   ⬜  Common helper functions (Stage 2)
│
├── model/                               #  Machine Learning models
│   ├── __init__.py                      ✅
│   ├── training/                        #  Model training pipelines
│   │   ├── __init__.py                  ✅
│   │   ├── train_solar.py               ✅  Solar generation model training
│   │   ├── train_load.py                ✅  Load demand model training
│   │   └── data_pipeline.py             ✅  Data preprocessing & feature engineering
│   │
│   ├── inference/                       #  Model inference (prediction)
│   │   ├── __init__.py                  ✅
│   │   ├── predict.py                   ✅  predict_solar(), predict_load() functions
│   │   └── model_loader.py              ✅  Model serialization (save/load .pkl)
│   │
│   ├── datasets/                        #  Training data
│   │   ├── synthetic_seed.csv           ✅  Initial synthetic training data (auto-generated)
│   │   └── README.md                    ✅  Dataset schema documentation
│   │
│   └── saved_models/                    #  Serialized trained models
│       └── .gitkeep                     ✅
│
├── db/                                  #  Database layer
│   ├── __init__.py                      ✅
│   ├── schema.py                        ✅  Table definitions & init_database()
│   ├── logger.py                        ✅  FR-008: Audit trail write functions
│   ├── queries.py                       ✅  Read queries for dashboard & analysis
│   └── migrations/                      #  Schema migrations
│       └── .gitkeep                     ⬜  (Stage 2)
│
├── backend/                             #  API server (Flask)
│   ├── __init__.py                      ✅
│   ├── app.py                           ✅  Flask app factory + route registration
│   ├── routes/                          #  Route modules
│   │   ├── __init__.py                  ✅
│   │   ├── api.py                       ✅  REST API endpoints (/api/history, /api/status)
│   │   └── stream.py                    ✅  SSE streaming endpoint (/api/stream)
│   │
│   └── auth/                            #  Authentication (Stage 2 — MFA)
│       ├── __init__.py                  ⬜
│       └── middleware.py                ⬜  Auth middleware placeholder
│
├── frontend/                            #  Web dashboard
│   ├── templates/
│   │   └── index.html                   ✅  Main dashboard page
│   ├── static/
│   │   ├── css/
│   │   │   └── dashboard.css            ✅  Dashboard styles (dark glassmorphism)
│   │   ├── js/
│   │   │   └── dashboard.js             ✅  Dashboard logic (SSE, charts, gauges)
│   │   └── assets/
│   │       └── .gitkeep                 ✅
│
├── hardware/                            #  Hardware interface layer (Stage 2)
│   ├── __init__.py                      ⬜
│   ├── modbus_client.py                 ⬜  Modbus/TCP client for substations
│   ├── pymgrid_adapter.py               ⬜  pymgrid simulation backend
│   └── relay_controller.py              ⬜  Load-shedding relay control
│
├── tests/                               #  Test suite
│   ├── __init__.py                      ✅
│   ├── test_balance.py                  ✅  Unit tests for energy balance
│   ├── test_battery.py                  ✅  Unit tests for battery constraints
│   ├── test_load_shed.py                ✅  Unit tests for load shedding
│   ├── test_control_loop.py             ✅  Integration test for full loop
│   └── test_forecasting.py              ⬜  ML model accuracy tests (Stage 2)
│
├── docs/                                #  Documentation
│   └── srs.md                           ⬜  Software Requirements Specification
│
└── data/                                #  Runtime data (generated at runtime)
    └── .gitkeep                         ✅  (microgrid.db created here at runtime)
```

**Total: ~55 files across 20 directories.** MVP implements ~35 files; ~20 are empty placeholders.

---

## ML Dataset Design

> [!IMPORTANT]
> **This section details the dataset schema, columns, and sources for both ML models.** Review this carefully — we will finalize before training begins.

### Model 1: Solar Generation Forecaster

**Purpose**: Predict solar panel output (kW) for the next 1–6 hours given weather conditions.

#### Training Dataset Schema (`solar_training_data`)

| Column | Type | Unit | Source | Description |
|--------|------|------|--------|-------------|
| `timestamp` | datetime | ISO 8601 | System clock | Observation time |
| `hour_of_day` | int | 0–23 | Derived from timestamp | Hour feature for daily pattern |
| `month` | int | 1–12 | Derived from timestamp | Seasonal variation |
| `day_of_year` | int | 1–366 | Derived from timestamp | Fine-grained seasonal feature |
| `cloud_cover_pct` | float | 0–100% | Open-Meteo API (`cloud_cover`) | Total cloud cover percentage |
| `shortwave_radiation_wm2` | float | W/m² | Open-Meteo API (`shortwave_radiation`) | Global horizontal irradiance |
| `direct_radiation_wm2` | float | W/m² | Open-Meteo API (`direct_radiation`) | Direct beam irradiance |
| `temperature_c` | float | °C | Open-Meteo API (`temperature_2m`) | Ambient temperature (affects panel efficiency) |
| `solar_generation_kw` | float | kW | **Target** — Telemetry / simulator | Actual measured solar output |

#### Feature Engineering
- `sin_hour = sin(2π × hour / 24)` — captures cyclic daily pattern
- `cos_hour = cos(2π × hour / 24)` — complementary cyclic feature
- `sin_month = sin(2π × month / 12)` — captures seasonal cycle
- `clear_sky_index = shortwave_radiation / max_theoretical_radiation` — normalized radiation

#### Data Sources
| Phase | Source | Notes |
|-------|--------|-------|
| **MVP (Seed)** | Synthetic generator | Sinusoidal solar curve + weather-correlated noise. ~365 days × 24h = 8,760 rows |
| **MVP (Runtime)** | Logged telemetry + Open-Meteo | Each control loop cycle adds 1 row. Model retrains every 24h |
| **Stage 2** | Open-Meteo Historical API + real meters | `https://archive-api.open-meteo.com/v1/archive` for backfilling real historical weather |

---

### Model 2: Load Demand Forecaster

**Purpose**: Predict consumer electricity demand (kW) for the next 1–6 hours.

#### Training Dataset Schema (`load_training_data`)

| Column | Type | Unit | Source | Description |
|--------|------|------|--------|-------------|
| `timestamp` | datetime | ISO 8601 | System clock | Observation time |
| `hour_of_day` | int | 0–23 | Derived from timestamp | Hour feature for daily demand curve |
| `day_of_week` | int | 0–6 | Derived from timestamp | Mon=0 to Sun=6 |
| `month` | int | 1–12 | Derived from timestamp | Seasonal variation |
| `is_weekend` | bool | 0/1 | Derived from day_of_week | Weekend flag |
| `is_holiday` | bool | 0/1 | Manual / calendar API | Public holiday flag |
| `temperature_c` | float | °C | Open-Meteo API | Temperature drives HVAC load |
| `load_demand_kw` | float | kW | **Target** — Telemetry / simulator | Actual measured load |

#### Feature Engineering
- `sin_hour = sin(2π × hour / 24)` — cyclic daily pattern
- `cos_hour = cos(2π × hour / 24)`
- `sin_dow = sin(2π × day_of_week / 7)` — weekly cycle
- `temp_squared = temperature_c²` — captures nonlinear HVAC relationship (cold + hot = high load)

#### Data Sources
| Phase | Source | Notes |
|-------|--------|-------|
| **MVP (Seed)** | Synthetic generator | Double-hump load curve (morning 7–9, evening 18–22) + temperature correlation. 8,760 rows |
| **MVP (Runtime)** | Logged telemetry + weather | Continuous accumulation from control loop |
| **Stage 2** | Real smart meter historical data | CSV/API import from utility provider |

---

### ML Training Strategy (MVP)

```
┌─────────────────────────────────────────────────────────┐
│                  MVP Training Pipeline                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SEED PHASE (startup)                                │
│     └─ Generate 8,760 synthetic rows per model          │
│     └─ Save to model/datasets/synthetic_seed.csv        │
│     └─ Train initial GradientBoostingRegressor           │
│     └─ Save to model/saved_models/*.pkl                 │
│                                                         │
│  2. RUNTIME PHASE (continuous)                          │
│     └─ Each control loop cycle logs actual values to DB │
│     └─ Every 24 hours: retrain from DB history          │
│     └─ Hot-swap model files (no restart needed)         │
│                                                         │
│  3. MODEL CHOICE                                        │
│     └─ Algorithm: GradientBoostingRegressor (sklearn)   │
│     └─ Evaluation: MAPE on 20% holdout split            │
│     └─ Target MAPE: ≤ 10%                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Why GradientBoostingRegressor?** It handles nonlinear relationships well (cloud cover ↔ solar output), is fast to train on <10K rows, doesn't require GPU, and runs easily on edge devices (Raspberry Pi). We can upgrade to LightGBM or a neural net in Stage 2 if MAPE exceeds 10%.

---

## Proposed Changes

### Component: Configuration (`config/`)

#### [NEW] `config/default_config.yaml`
System-wide constants:
- Battery: `soc_min: 20`, `soc_max: 90`, `capacity_kwh: 200`, `max_charge_kw: 50`, `max_discharge_kw: 50`
- Grid: `max_import_kw: 100`, `nominal_freq_hz: 50`, `freq_tolerance_hz: 0.8`
- Location: `latitude: 18.52`, `longitude: 73.86` (Pune, India — configurable)
- Timing: `loop_interval_sec: 5`, `weather_poll_sec: 900`
- Database: `db_path: data/microgrid.db`

---

### Component: Data Ingestion (`src/ingestion/`)

#### [NEW] `src/ingestion/telemetry.py`
**FR-001**: Simulates smart meter readings.
- `generate_telemetry(timestamp)` → dict with `solar_kw`, `load_kw`, `voltage`, `current`, `frequency`
- Sinusoidal + noise solar curve peaking at solar noon; double-hump load curve

#### [NEW] `src/ingestion/weather.py`
**FR-002**: Open-Meteo API client.
- `fetch_weather_forecast(lat, lon)` → `{timestamps[], temperature[], cloud_cover[], shortwave_radiation[], direct_radiation[]}`
- 15-minute caching, fallback defaults on API failure

#### [NEW] `src/ingestion/simulator.py`
Empty placeholder for pymgrid integration (Stage 2).

---

### Component: Core Control Logic (`src/core/`)

#### [NEW] `src/core/balance.py`
**FR-004**: `compute_net_balance(solar_kw, load_kw)` → `net_deficit`  
`classify_state(net_deficit, battery_soc, grid_draw)` → system state enum

#### [NEW] `src/core/battery.py`
**FR-005**: `compute_battery_command(net_deficit, soc, capacity, max_charge, max_discharge)` → `battery_cmd_kw`

#### [NEW] `src/core/load_shed.py`
**FR-006**: `compute_load_shed(remaining_deficit, max_grid_import)` → `(grid_cmd_kw, shed_cmd_kw)`

#### [NEW] `src/core/dispatcher.py`
**FR-007**: `dispatch_commands(battery_cmd, grid_cmd, shed_cmd)` → logs to console + DB (simulated actuator)

#### [NEW] `src/core/control_loop.py`
Main orchestrator: sequentially calls ingestion → prediction → balance → battery → shed → dispatch → log

---

### Component: ML Models (`model/`)

#### [NEW] `model/training/data_pipeline.py`
- `generate_synthetic_solar_data(n_days=365)` → DataFrame with all solar schema columns
- `generate_synthetic_load_data(n_days=365)` → DataFrame with all load schema columns
- `prepare_features(df, model_type)` → feature matrix X, target vector y

#### [NEW] `model/training/train_solar.py`
- `train_solar_model(data_path)` → fits GradientBoostingRegressor, saves `.pkl`, prints MAPE

#### [NEW] `model/training/train_load.py`
- `train_load_model(data_path)` → fits GradientBoostingRegressor, saves `.pkl`, prints MAPE

#### [NEW] `model/inference/predict.py`
- `predict_solar(features_dict)` → predicted solar kW
- `predict_load(features_dict)` → predicted load kW

#### [NEW] `model/inference/model_loader.py`
- `save_model(model, path)` / `load_model(path)` — pickle serialization with error handling

#### [NEW] `model/datasets/README.md`
Documents the dataset schema (mirrors the tables above)

---

### Component: Database (`db/`)

#### [NEW] `db/schema.py`
Creates `microgrid_log` table:
```
id | timestamp | solar_kw | load_kw | predicted_solar | predicted_load |
net_deficit | battery_soc | battery_cmd | grid_cmd | shed_cmd | system_state
```

#### [NEW] `db/logger.py`
- `log_step(conn, step_data_dict)` → INSERT one row per control cycle

#### [NEW] `db/queries.py`
- `query_recent_logs(conn, hours=24)` → returns list of dicts for dashboard
- `query_latest_state(conn)` → returns most recent row

---

### Component: Backend API (`backend/`)

#### [NEW] `backend/app.py`
Flask app factory; registers route blueprints; serves frontend static files

#### [NEW] `backend/routes/api.py`
- `GET /api/status` → current system state JSON
- `GET /api/history?hours=24` → historical log data JSON

#### [NEW] `backend/routes/stream.py`
- `GET /api/stream` → SSE endpoint streaming real-time state every 5 seconds

---

### Component: Frontend Dashboard (`frontend/`)

#### [NEW] `frontend/templates/index.html`
Single-page dashboard layout (semantic HTML5)

#### [NEW] `frontend/static/css/dashboard.css`
- Dark theme with deep navy/charcoal background
- Glassmorphism cards with `backdrop-filter: blur`
- CSS custom properties for color palette
- Responsive grid layout
- Animated status indicator pulses
- Google Font: Inter

#### [NEW] `frontend/static/js/dashboard.js`
- `EventSource('/api/stream')` for live updates
- Chart.js time-series chart (predicted vs actual, dual lines)
- Animated gauge/card values with smooth transitions
- Power flow direction indicators
- Event log auto-scroll

---

### Component: Tests (`tests/`)

#### [NEW] `tests/test_balance.py`
Tests for surplus/deficit classification

#### [NEW] `tests/test_battery.py`
Tests that SoC stays within [20%, 90%], charge/discharge rate limits

#### [NEW] `tests/test_load_shed.py`
Tests grid cap at 100kW, shed calculation

#### [NEW] `tests/test_control_loop.py`
Integration test: 20 cycles, verify constraints + logging

---

## Open Questions

> [!IMPORTANT]
> **Location**: MVP defaults to **Pune, India** (18.52°N, 73.86°E). Change?

> [!IMPORTANT]
> **Solar panel capacity**: What rated capacity should the simulated solar array have? Default: **80 kW peak** (typical small microgrid). This affects the synthetic training data curves.

> [!IMPORTANT]
> **ML model review**: I will **pause and notify you** before we start training the models (Step 6 in execution). You'll be able to review the generated synthetic dataset, tweak columns/distributions, and approve before training begins.

---

## Verification Plan

### Automated Tests
```bash
python -m pytest tests/ -v
```
- Battery SoC stays within [20%, 90%] across all scenarios
- Grid draw never exceeds 100 kW
- All log entries written to SQLite
- Each control loop cycle < 500ms

### Manual Verification
- Start: `python main.py` → open `http://localhost:5000`
- Dashboard shows live-updating gauges, status badge, time-series chart
- SQLite file `data/microgrid.db` contains logged records
- Weather API returns real forecast data (verify in logs)
