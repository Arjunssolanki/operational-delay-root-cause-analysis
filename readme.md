# Operational Inefficiency & Delay Root-Cause Analysis (MySQL + Python)

## 📌 Business Case & Objective

Unscheduled supply chain delays erode profitability and breach client Service Level Agreements (SLAs). This project builds an automated database pipeline that connects to a local MySQL instance, extracts shipping metrics using advanced window functions, and applies scientific hypothesis testing to identify whether process delays are systemic bottlenecks or random operational noise.

## 🛠️ Tech Stack & Architecture

- **Database Engine:** MySQL Server (indexed staging tables)
- **Programming Language:** Python 3.x
- **Core Libraries:** Pandas, NumPy, MySQL-Connector-Python
- **Statistical Inference Engine:** SciPy (One-Way ANOVA Testing)

## 📊 Automated Pipeline Flow

1. **Data Ingestion:** Simulates 1,000 corporate shipping records and uses bulk execute methods to safely populate a local MySQL analytics database.
2. **Server-Side Aggregation:** Executes a multi-stage Common Table Expression (CTE) query directly on the MySQL server to compute transit hour deviations and calculate carrier-wide performance baselines using SQL Window Functions (`AVG() OVER`).
3. **Statistical Root-Cause Extraction:** Pulls the processed data framework into Python to execute a One-Way ANOVA test. This mathematically proves whether different route risk classifications generate distinct timeline variances.
4. **BI Export Layer:** Outputs a clean, pre-calculated dataset (`bi_dashboard_input.csv`) customized for instant visualization drop-ins.

## 🚀 Replicating the System Locally

Ensure your local dependencies are satisfied:

```bash
pip install mysql-connector-python pandas numpy scipy
```

Update the `db_config` credentials inside `project.py` with your local database server password, then launch the engine:

```bash
python project.py
```

## 📉 Corporate Analytics Insights

- **Statistical Verification:** If the computed P-value drops below the 0.05 alpha threshold, the variations in operational delays across risk tiers are confirmed to be non-random.
- **Hiring Manager Takeaway:** Demonstrates an advanced understanding of relational database optimization, hybrid data piping, and objective scientific validation over subjective guessing.
