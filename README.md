# 📊 SEBI Telegram Risk Monitoring Dashboard


## 🌟 Overview
This project analyzes **Telegram groups** to detect and monitor:
- 🚨 **High-risk financial messages**
- 🛡️ **Unregistered investment advisors & research analysts**
- 📑 **Suspicious trading recommendations**
- 📈 **Pump-and-dump patterns & fake promotions**

The system combines:
- 📥 Scraping Telegram messages  
- 🧹 Preprocessing & text normalization  
- 🔍 Clustering & risk scoring  
- 🗂️ SEBI registry verification (IA + RA)  
- 📊 Interactive dashboards (Streamlit)  
- 🚨 Automated alerts feed  

The goal: assist **SEBI investigators** in monitoring **financial scams, unverified promotions, and risky groups**.

---
## ✨ Key Features

- 📥 **Data Collection**  
  Scraped raw Telegram messages from multiple groups.

- 🧹 **Preprocessing**  
  Cleaned & normalized text (deduplication, regex cleaning, SEBI registry cross-checks).

- 🔗 **Entity Matching**  
  Linked Telegram usernames/messages with SEBI-registered Investment Advisors (IA) and Research Analysts (RA).

- 🧩 **Clustering**  
  Grouped messages into canonical templates for detecting scam patterns.

- ⚖️ **Risk Scoring**  
  Applied heuristics & labels (`high`, `medium`, `low`) to rank suspicious messages.

- 📊 **Interactive Dashboard**  
  Streamlit-based app to explore clusters, candidates, and alerts.

- 🌐 **Network Graphs**  
  Candidate ↔ Cluster ↔ Group visualizations for scam network mapping.

- 📑 **Automated Reports**  
  PDF/CSV exports and alerts feed for monitoring recent high-risk signals.
---

## 🔄 Workflow

```mermaid
flowchart TD
    A[Preprocessing & Cleaning] --> B[Telegram Scraper]
    B --> C[Registry Matching IA-RA]
    C --> D[Clustering & Template Detection]
    D --> E[Risk Scoring & Labeling]
    E --> F[Dashboard & Exploration]
    E --> G[Alerts Feed]
    F --> H[Network Visualization]

````
## ⚙️ Installation

### 🔹 Create Virual Environment (I used Conda)
```bash
conda env create -f environment.yml
conda activate sebi_project
````

### 🔹 Using Pip

```bash
pip install -r requirements.txt
```

---


### 3️⃣ Run Dashboard

```bash
streamlit run app.py
```

🔎 **Dashboard Views**

* **Overview** → Risk distribution, timeline, top clusters
* **Cluster Explorer** → Inspect suspicious clusters
* **Candidate Explorer** → Analyze individual Telegram users
* **Alerts Feed** → Latest high-risk messages

### 4️⃣ Generate Alerts

```bash
python alerts.py
```

---


## 🛡️ Applications

* Detect **fake advisors & pump-and-dump scams**
* Monitor **unregistered financial services promotions**
* Provide **real-time alerts** for SEBI investigators

---

## ✅ Future Work

* Real-time Telegram bot monitoring
* NLP-based classification (BERT/FinBERT)
* Extend coverage to **WhatsApp & Twitter/X**

---
