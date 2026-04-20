DATA FLOW, CRISP-DM & MLOps
===========================

Overview
--------

The **VITA Platform** (*Visionary Industrial Technology Architecture*) integrates
three complementary perspectives:

- **CRISP-DM** – methodological workflow for analytics and forecasting.
- **6C Architecture** – conceptual industrial intelligence framework.
- **MLOps** – operational lifecycle for machine learning in production.

Together, they ensure that VITA is not only research-driven, but also scalable,
auditable, and production-ready.

Integrated Mapping
------------------

+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| CRISP-DM Phase          | 6C Layer           | MLOps Perspective         | VITA Modules / Artifacts                                   |
+=========================+====================+===========================+============================================================+
| Business Understanding  | Configuration      | Experiment tracking       | `dashboard`, docs                                          |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Data Understanding      | Connection         | DataOps (ingestion)       | `services`, `datasets`                                     |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Data Preparation        | Conversion         | DataOps (preprocessing)   | `common`, `algorithms/core`                                |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Modeling                | Cyber              | ModelOps (training)       | `algorithms/lstm`, `algorithms/rc`,                        |
|                         |                    |                           | `algorithms/hybrid_model`, `algorithms/pycaret`            |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Evaluation              | Cognition          | Model validation          | `output_forecasts`, metrics, reports                       |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Deployment              | Configuration      | CI/CD pipelines           | `services` (inference APIs), `dashboard` (visual rollout)  |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+
| Monitoring & Feedback   | Consciousness      | Continuous learning       | `log`, monitoring hooks, retraining triggers               |
+-------------------------+--------------------+---------------------------+------------------------------------------------------------+


End-to-End Flow
---------------

1. **Ingest & Profile** data (`services` → `datasets`).
2. **Prepare & Convert** with `common` and `algorithms/core`.
3. **Model** with `algorithms` (LSTM, RC, Hybrid, PyCaret).
4. **Evaluate** results, save to `output_forecasts`.
5. **Deploy** via `services` APIs and `dashboard`.
6. **Monitor** through `log/`, detect drift, close the loop.
7. **Retrain automatically** (MLOps) when monitoring triggers thresholds.


Implementation Notes
--------------------

- **DataOps** in VITA: ingestion (`services`), datasets, preprocessing (`common`).
- **ModelOps** in VITA: modular algorithms, experiment tracking, forecasts.
- **CI/CD**: Docker-based deployments (`docker-compose.yml`, `Dockerfile`).
- **Monitoring**: `log/` + retraining pipelines close the loop for industrial AI.
