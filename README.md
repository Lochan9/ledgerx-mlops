# 🧾 LedgerX – AI-Powered Invoice Intelligence Platform  
### MLOps: Data Pipeline Submission

---

## 📘 Overview
This repository contains the **LedgerX Data Pipeline**, the foundation of our AI-powered invoice-processing MLOps platform.  
The pipeline is fully reproducible, container-ready, and version-controlled using **Git + DVC**, orchestrated with **Airflow**, validated via **Great Expectations**, and tested using **pytest**.

## Team Members
- Jash Bhavesh Shah
- Lochan Enugula
- Samruddhi Bansod
- Rutuja Jadhav
- Nirali Hirpara
- Deep Bhanushali

### Core Features
- 🔄 **Automated data ingestion** from Roboflow datasets  
- 🧩 **Preprocessing** – resize, normalization, blur detection, checksum generation  
- ✅ **Validation** – schema + quality checks using Great Expectations  
- 🧱 **Data versioning** – tracked with DVC  
- 🪶 **Airflow orchestration** – 8-stage DAG workflow  
- 🧪 **Unit testing** – automated pytest suite  
- ⚙️ **CI/CD** – GitHub Actions integration  

---

## 📊 Dataset Summary
- **Total Documents** : 6279  
- **Train** : 4395 (70 %)  
- **Validation** : 942 (15 %)  
- **Test** : 942 (15 %)

### 📈 Quality Metrics
- **Average Quality Score :** 0.601  
- **Blur Rate :** 1.99 %

### ⚙️ Components
- Data ingestion from 2 Roboflow datasets  
- Preprocessing with quality assessment  
- Stratified train/val/test splitting  
- DVC version control  
- Airflow orchestration  

---

## ⚙️ Environment Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Lochan9/ledgerx-mlops.git
cd ledgerx-mlops
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Windows → venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Roboflow API Key
```bash
export ROBOFLOW_API_KEY="your_api_key_here"
```

---

## 🚀 Running the Pipeline

### 🧠 Run End-to-End in Python
```bash
python -c "from src.data_pipeline import DataPipeline; pipeline = DataPipeline(); pipeline.run_pipeline()"
```

### 🪶 Run with Airflow
```bash
airflow standalone
```
Then open [http://localhost:8080](http://localhost:8080) → enable **ledgerx_data_pipeline**.  
> DAG flow : check → verify → preprocess → split → validate → test → data card → DVC add  

### 🧪 Run Unit Tests
```bash
pytest -v tests/test_pipeline.py
```

---

## 🗂️ Repository Structure
```
ledgerx-mlops/
├── data/
│   ├── raw/                     # Roboflow datasets (2 sources)
│   ├── processed/               # Preprocessed images + metadata
│   └── splits/                  # Train/Val/Test CSVs
│
├── src/
│   └── data_pipeline.py         # Core LedgerX Data Pipeline class
│
├── airflow_dags/
│   └── ledgerx_data_pipeline_dag.py   # 8-task Airflow DAG
│
├── tests/
│   └── test_pipeline.py         # Unit tests for pipeline and validation
│
├── scripts/
│   ├── setup_great_expectations.py    # Schema & data validation
│   ├── generate_eda.py                # EDA + profiling reports
│   ├── benchmark_performance.py       # Stage benchmarking & throughput
│   └── validate_pipeline.py           # Automated validation logic
│
├── config/
│   └── pipeline_config.yaml      # Central YAML configuration file
│
├── reports/
│   ├── performance_report.json   # Throughput + system metrics
│   ├── data_profile_report.html  # ydata-profiling output
│   └── eda_visualizations.png    # Generated EDA visuals
│
├── docs/
│   ├── ARCHITECTURE.md           # System & Git architecture diagrams
│   ├── SETUP.md                  # Environment & setup instructions
│   └── CONTRIBUTING.md           # Developer workflow & code standards
│
├── .github/workflows/ci-cd.yml   # GitHub Actions for CI/CD pipeline
├── .dvc/                         # DVC internal cache & config
├── Dockerfile                    # FastAPI container image definition
├── docker-compose.yml            # API service orchestration
├── requirements.txt              # Python dependencies (pinned)
├── pipeline.log                  # Runtime log of data pipeline
└── README.md                     # Project overview + execution guide
```

---

## 🔁 Reproducibility & DVC Tracking

### Add Data to DVC
```bash
dvc add data/processed
dvc add data/splits
git add data/processed.dvc data/splits.dvc .dvc/config .gitignore
git commit -m "Add DVC tracking for data pipeline"
```

### Restore Versioned Data
```bash
dvc pull
```

DVC ensures **immutable, shareable dataset states** so anyone can clone the repo, pull versioned data, and rerun the pipeline identically.

---

## 🧩 Validation & Testing
- **Great Expectations** validates schema, column order, value ranges, and duplicates.  
- **Pytest** checks config, metadata, and data-split integrity.  
- **CI/CD** workflow (`.github/workflows/ci-cd.yml`) runs lint + tests + validation on every push.

---

## 🧠 Performance Metrics
| Stage | Duration (s) | Records Processed | Throughput (records/s) |
|-------|--------------:|------------------:|-----------------------:|
| Data Ingestion | 45.2 | 6279 | 139.0 |
| Preprocessing | 850.0 | 6279 | 7.38 |
| Splitting | 8.5 | 6279 | 738.7 |
| Validation | 3.2 | 6279 | 1 962.2 |

> **Insight:** Preprocessing (~850 s) is the bottleneck; planned optimization via multiprocessing.

---

## 🎯 Reproducibility Summary
- All parameters in `config/pipeline_config.yaml`  
- Deterministic splits (`random_seed = 42`)  
- DVC-tracked datasets  
- CI/CD ensures consistent runs across environments  

---

