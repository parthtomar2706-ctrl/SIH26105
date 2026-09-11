#  SIH26105: AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost%20%7C%20Ensemble-orange.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade platform developed for **Smart India Hackathon 2026 (Problem Statement: SIH26105)** sponsored by the **AICTE Cyber Security Cell**. 

This platform converts complex technical security telemetry (vulnerabilities, audit scores, patch ages, and control coverage) into **quantified monetary financial loss exposure ($/₹)** and uses an optimization engine to allocate security budgets for maximum risk reduction.

---

##  Key Features

* **Continuous Financial Risk Quantification:** Replaces qualitative ratings (*Low*, *Medium*, *High*) with continuous monetary loss estimations using log-scaled ML ensemble models.
* **Feature-Engineered Telemetry Scoring:** Calculates vulnerability exposure ratios, threat impact indices, and active control coverage factors in real time.
* **Investment Optimization Engine:** Simulates security upgrade paths (MFA, EDR, Security Training) under strict budget limits to maximize financial risk reduction.
* **Production-Ready REST API:** Powered by FastAPI with automatic OpenAPI/Swagger documentation.
* **Automated Data Profiling:** Includes comprehensive data quality, distribution, and correlation audits generated via `ydata-profiling`.

---

##  System Architecture

```text
  [ Organizational Telemetry ] ---> [ Log-Scaled ML Ensemble ] ---> [ Monetary Loss Forecast ($) ]
  (Patch Age, CVSS, MFA, EDR)      (XGBoost + GB + RF)             
                                                                               |
  [ Budget Constraint ($) ]    ---> [ Knapsack Optimization ]  ---> [ Recommended Control Allocations ]
