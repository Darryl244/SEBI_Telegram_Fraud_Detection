import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# === Paths ===
base_dir = r"D:\Darryl\Coding\s_p\data"
processed_dir = os.path.join(base_dir, "processed")
reports_dir = os.path.join(base_dir, "reports")

os.makedirs(reports_dir, exist_ok=True)

messages_file = os.path.join(processed_dir, "messages_with_risk_v4.csv")
clusters_file = os.path.join(processed_dir, "cluster_summary_v2.csv")

# === Load Data ===
messages = pd.read_csv(messages_file, low_memory=False)
clusters = pd.read_csv(clusters_file, low_memory=False)

# === Generate plots ===
ts = datetime.now().strftime("%Y%m%d_%H%M")

plot1 = os.path.join(reports_dir, f"risk_distribution_{ts}.png")
plot2 = os.path.join(reports_dir, f"top_clusters_{ts}.png")

# Plot 1: Risk distribution
risk_counts = messages["risk_label"].value_counts()
plt.figure(figsize=(5, 4))
risk_counts.plot(kind="bar", color=["green", "orange", "red"])
plt.title("Risk Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(plot1, dpi=120)
plt.close()

# Plot 2: Top clusters by high ratio
top_clusters = clusters.sort_values("high_ratio", ascending=False).head(10)
plt.figure(figsize=(7, 4))
plt.bar(top_clusters["cluster_id"].astype(str), top_clusters["high_ratio"])
plt.title("Top Clusters by High-Risk Ratio")
plt.xlabel("Cluster ID")
plt.ylabel("High-Risk Ratio")
plt.tight_layout()
plt.savefig(plot2, dpi=120)
plt.close()

# === Build PDF ===
report_file = os.path.join(reports_dir, f"risk_summary_{ts}.pdf")

doc = SimpleDocTemplate(report_file, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

elements.append(Paragraph("SEBI Telegram Risk Report", styles["Title"]))
elements.append(Spacer(1, 12))

# Risk distribution
elements.append(Paragraph("Overall Risk Distribution", styles["Heading2"]))
elements.append(Image(plot1, width=300, height=250))
elements.append(Spacer(1, 12))

# Top clusters
elements.append(Paragraph("Top High-Risk Clusters", styles["Heading2"]))
elements.append(Image(plot2, width=350, height=250))
elements.append(Spacer(1, 12))

# Add some sample high-risk messages
elements.append(Paragraph("Sample High-Risk Messages", styles["Heading2"]))
sample_high = messages[messages["risk_label"] == "high"].head(5)
for _, row in sample_high.iterrows():
    txt = f"<b>{row['candidate_name']}</b> ({row['date']}) - Score {row['heuristic_score']}<br/>{row['text'][:300]}..."
    elements.append(Paragraph(txt, styles["Normal"]))
    elements.append(Spacer(1, 6))

doc.build(elements)
print(f"✅ Report generated: {report_file}")
