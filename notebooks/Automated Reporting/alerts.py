# alerts.py
# Background script to generate alerts feed for SEBI Risk Dashboard

import pandas as pd
import os
from datetime import datetime

# === File paths ===
BASE_DIR = r"D:\Darryl\Coding\s_p\data\processed"
REPORT_DIR = r"D:\Darryl\Coding\s_p\data\reports"

messages_file = os.path.join(BASE_DIR, "messages_with_clusters_v2.csv")
alerts_file = os.path.join(REPORT_DIR, "alerts_feed.csv")

# Ensure reports folder exists
os.makedirs(REPORT_DIR, exist_ok=True)

# === Load messages ===
df = pd.read_csv(messages_file, low_memory=False)
print(f"Loaded messages: {len(df)}")

# Ensure required cols exist
required_cols = ["message_id", "date", "candidate_name_norm_simple",
                 "text", "risk_label", "heuristic_score", "cluster_id"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# === Flag high-risk messages ===
alerts = df[df["risk_label"].str.lower() == "high"].copy()

# Sort by date (latest first if available)
if "date" in alerts.columns:
    alerts["date"] = pd.to_datetime(alerts["date"], errors="coerce")
    alerts = alerts.sort_values("date", ascending=False)

# Select useful columns
alerts = alerts[[
    "message_id", "date", "candidate_name_norm_simple",
    "cluster_id", "heuristic_score", "text"
]]

# Add run timestamp
alerts["alert_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save alerts feed
alerts.to_csv(alerts_file, index=False, encoding="utf-8")
print(f"✅ Alerts feed saved: {alerts_file}")

# Preview
print("\nSample alerts:")
print(alerts.head(10))
