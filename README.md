# 📊 SEBI Telegram Risk Monitoring Dashboard
This project is an **semi-automated risk monitoring system for Telegram investment groups**, designed to detect and analyze **illegal financial advice and scam promotions**. It processes raw Telegram messages, matches senders against official **SEBI IA/RA registries**, clusters repetitive scam patterns, and assigns **risk scores (low/medium/high)**. The system was built to **help SEBI and regulators quickly identify unregistered advisors, track high-risk activities, and generate evidence-ready reports** for investor protection.

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
  PDF/CSV exports and alerts feed for monitoring recent high-risk signals and continuously scans, detects only new high-risk cases, and actively notifies SEBI via Email/Slack in real-time.
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
---
## ⚙️ Technologies & Methods Used  

### **Data Collection & Preprocessing**  
- **Telegram Scraper (Telethon)** – Extracted raw messages, users, and group metadata.  
- **Pandas / NumPy** – Data cleaning, normalization, and feature engineering.  
- **Regex & Unicode Normalization** – Redaction of phone numbers, emails, links, and standardizing text.  

### **Entity Resolution & Matching**  
- **SEBI Registries (IA / RA)** – Investment Advisors & Research Analysts database.  
- **Fuzzy Matching + Normalization** – Candidate name alignment with SEBI registries.  

### **Risk Scoring & Classification**  
- **Heuristic Rule-based Model** – Keyword & pattern detection (e.g., *target, jackpot, account handling*).  
- **Weighted Risk Scoring** – Assigning **Low / Medium / High** labels.  
- *(Optional Future Upgrade)*: Transformer-based models (FinBERT / BERT) for advanced NLP-based risk classification.  

### **Clustering & Template Mining**  
- **Sentence-Transformers (MiniLM-L6-v2)** – Generating semantic embeddings of messages.  
- **FAISS / KMeans** – Clustering similar messages into canonical templates for pattern discovery.  

### **Visualization & Analytics**  
- **Matplotlib** – Risk distribution, timelines, charts.  
- **Pyvis + NetworkX** – Interactive **Candidate ↔ Cluster ↔ Group** networks.  
- **Streamlit Dashboard** – Candidate explorer, cluster explorer, alerts feed.  

### **Reporting**  
- **ReportLab** – Automated PDF report generation (risk summaries, top clusters).  
- **CSV Exports** – For SEBI auditors and investigators.
- **Slack Alerts (via Webhook)**
- **Email Alerts (via SMTP Gmail App Password)**

---
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
