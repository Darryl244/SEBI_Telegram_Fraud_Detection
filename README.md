# 📊 SEBI Telegram Risk Analysis

## 📌 Overview  
This project analyzes **Telegram groups related to stock market trading/investment calls**, focusing on identifying **high-risk and potentially fraudulent activities**.  

It combines:  
- 📥 **Scraped Telegram messages**  
- 🏛 **SEBI registries** (Investment Advisors & Research Analysts)  
- ⚡ **Text preprocessing, clustering & risk classification**  
- 📊 **Dashboards & interactive visualizations**  

The pipeline helps detect **unregistered advisors, scammy promotions, and risky trading schemes** — aiding **SEBI surveillance & investor protection**.  

---


## ⚙️ Installation  
Create & activate virtual environment:

bash
Copy code
conda create -n sebi_env python=3.10 -y
conda activate sebi_env
Install dependencies:

bash
Copy code
pip install -r requirements.txt

Pipeline Workflow
flowchart TD
    A[Preprocessing & Cleaning] --> B[Raw Telegram Data]
    B --> C[Candidate Matching with SEBI Registry]
    C --> D[Message Clustering & Templates]
    D --> E[Risk Labeling: High / Medium / Low]
    E --> F[Dashboard + Alerts + Reports]

Steps:
Registry Cleaning → normalize SEBI IA/RA registries

Preprocessing → clean Telegram messages (normalize, remove noise).

Candidate Matching → check Telegram users against SEBI records.

Clustering → group similar message templates (BUY/SELL calls, promos).

Risk Labeling → assign risk scores & labels.

Visualization & Reporting →  PDF reports, network graph

🚨 Alerts

Run the alerts script:

python alerts.py


Generates:

data/reports/alerts_feed.csv → latest high-risk messages

Integrated in dashboard under Alerts Feed.

📊 Dashboard

Run the interactive dashboard:

streamlit run app.py

Features:

Overview → metrics, risk distribution, top clusters

Cluster Explorer → inspect message clusters

Candidate Explorer → analyze per-candidate risk profile

Alerts Feed → live table of recent high-risk messages

📈 Example Outputs

📌 Cluster Network Graph (HTML FILE)


📌 Risk Summary Report (PDF)


🛡️ Use Case

Designed for SEBI regulators and investigators to:

Monitor Telegram activity in near real-time

Detect high-risk advisories and fraudulent promotions

Verify advisors against SEBI registry

Build evidence-based case files (messages, clusters, alerts)
