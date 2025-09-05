import pandas as pd
import os, time, smtplib, requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Config ===
BASE_DIR = r"D:\Darryl\Coding\s_p\data\processed"
REPORT_DIR = r"D:\Darryl\Coding\s_p\data\reports"
messages_file = os.path.join(BASE_DIR, "messages_with_clusters_v2.csv")
alerts_file = os.path.join(REPORT_DIR, "alerts_feed.csv")

# Notification settings
ENABLE_EMAIL = True
ENABLE_SLACK = False

# --- Email Settings (Gmail example) ---
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"   # Generate App Password (NOT your Gmail password)
EMAIL_RECEIVER = "receiver_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- Slack Settings ---
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXXX/XXXX/XXXX"

# Create reports dir
os.makedirs(REPORT_DIR, exist_ok=True)

# Track seen messages
seen_ids = set()

def send_email_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("📧 Email alert sent!")
    except Exception as e:
        print("❌ Email sending failed:", e)

def send_slack_alert(message):
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code == 200:
            print("💬 Slack alert sent!")
        else:
            print("❌ Slack error:", response.text)
    except Exception as e:
        print("❌ Slack sending failed:", e)

def load_messages():
    if not os.path.exists(messages_file):
        print("❌ Messages file not found:", messages_file)
        return pd.DataFrame()
    try:
        return pd.read_csv(messages_file, low_memory=False)
    except Exception as e:
        print("❌ Error loading messages:", e)
        return pd.DataFrame()

def generate_alerts():
    global seen_ids
    df = load_messages()
    if df.empty:
        return pd.DataFrame()

    required_cols = ["message_id", "date", "candidate_name_norm_simple",
                     "text", "risk_label", "heuristic_score", "cluster_id"]
    for col in required_cols:
        if col not in df.columns:
            print(f"❌ Missing column: {col}")
            return pd.DataFrame()

    alerts = df[df["risk_label"].str.lower() == "high"].copy()
    if alerts.empty:
        print("ℹ️ No high-risk messages found this cycle.")
        return pd.DataFrame()

    alerts["date"] = pd.to_datetime(alerts["date"], errors="coerce")
    alerts = alerts.sort_values("date", ascending=False)
    alerts = alerts[["message_id", "date", "candidate_name_norm_simple",
                     "cluster_id", "heuristic_score", "text"]]
    alerts["alert_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_alerts = alerts[~alerts["message_id"].isin(seen_ids)].copy()
    if not new_alerts.empty:
        print(f"🚨 {len(new_alerts)} NEW high-risk alerts detected!")
        for _, row in new_alerts.iterrows():
            msg_preview = str(row["text"])[:200].replace("\n"," ")
            alert_msg = (f"🚨 HIGH-RISK ALERT 🚨\n"
                         f"Candidate: {row['candidate_name_norm_simple']}\n"
                         f"Cluster: {row['cluster_id']} | Score: {row['heuristic_score']}\n"
                         f"Date: {row['date']}\n"
                         f"Message: {msg_preview}...")

            print(alert_msg, "\n")

            # Send notifications
            if ENABLE_EMAIL:
                send_email_alert("🚨 SEBI High-Risk Alert", alert_msg)
            if ENABLE_SLACK:
                send_slack_alert(alert_msg)

        # Save CSV
        if os.path.exists(alerts_file):
            existing = pd.read_csv(alerts_file, low_memory=False)
            alerts_all = pd.concat([existing, new_alerts], ignore_index=True)
        else:
            alerts_all = new_alerts
        alerts_all.to_csv(alerts_file, index=False, encoding="utf-8")
        print(f"✅ Alerts feed updated -> {alerts_file}")

        seen_ids.update(new_alerts["message_id"].tolist())
    else:
        print("✔ No new alerts this cycle.")

    return alerts

if __name__ == "__main__":
    print("🔄 Starting automated fraud-prevention alerts...")
    while True:
        try:
            generate_alerts()
        except Exception as e:
            print("❌ Error in cycle:", e)
        print("⏳ Sleeping 5 minutes...\n")
        time.sleep(300)
