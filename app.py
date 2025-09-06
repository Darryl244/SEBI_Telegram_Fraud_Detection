import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# === Load Data ===
@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), "data", "processed")
    report_dir = os.path.join(os.path.dirname(__file__), "data", "reports")

    messages_file = os.path.join(base_dir, "messages_with_clusters_v2.csv")
    clusters_file = os.path.join(base_dir, "cluster_summary_v2.csv")
    alerts_file = os.path.join(report_dir, "alerts_feed.csv")

    # Load CSVs
    messages = pd.read_csv(messages_file, low_memory=False)
    clusters = pd.read_csv(clusters_file, low_memory=False)
    alerts = pd.read_csv(alerts_file, low_memory=False) if os.path.exists(alerts_file) else pd.DataFrame()

    # Process fields
    if "date" in messages.columns:
        messages["date"] = pd.to_datetime(messages["date"], errors="coerce")
    messages["risk_label"] = messages["risk_label"].astype(str)
    messages["candidate_name_norm_simple"] = messages["candidate_name_norm_simple"].astype(str).fillna("unknown")

    return messages, clusters, alerts

messages, clusters, alerts = load_data()

# === Sidebar ===
st.sidebar.title("📊 SEBI Risk Dashboard")
view = st.sidebar.radio("Choose View:", ["Overview", "Cluster Explorer", "Candidate Explorer", "Alerts Feed"])

# === Export Helpers ===
def export_csv(df, filename="export.csv"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export CSV", csv, filename, "text/csv")

def export_pdf(df, filename="export.pdf", title="Exported Data"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Heading1"]), Spacer(1, 12)]
    for _, row in df.iterrows():
        elements.append(Paragraph(str(row.to_dict()), styles["Normal"]))
        elements.append(Spacer(1, 6))
    doc.build(elements)
    st.download_button("⬇️ Export PDF", buffer.getvalue(), filename, "application/pdf")

# === Overview ===
if view == "Overview":
    st.title("📊 SEBI Telegram Risk Dashboard — Overview")
    st.metric("Total Messages", len(messages))
    st.metric("Candidates", messages["candidate_name_norm_simple"].nunique())
    st.metric("Clusters", len(clusters))

    # Risk distribution pie
    if "risk_label" in messages.columns:
        risk_counts = messages["risk_label"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(risk_counts, labels=risk_counts.index, autopct="%1.1f%%")
        ax.set_title("Risk Distribution")
        st.pyplot(fig)

    # High risk over time
    if "date" in messages.columns:
        daily = messages[messages["risk_label"] == "high"].groupby(messages["date"].dt.date).size()
        if not daily.empty:
            st.line_chart(daily, use_container_width=True)

    st.subheader("Top High-Risk Clusters")
    if "high_ratio" in clusters.columns:
        top_clusters = clusters.sort_values("high_ratio", ascending=False).head(15)
        st.dataframe(top_clusters)
        export_csv(top_clusters, "top_clusters.csv")
        export_pdf(top_clusters, "top_clusters.pdf", "Top High-Risk Clusters")

# === Cluster Explorer ===
elif view == "Cluster Explorer":
    st.title("🔍 Cluster Explorer")

    cluster_id = st.number_input("Enter Cluster ID",
                                 min_value=int(clusters["cluster_id"].min()),
                                 max_value=int(clusters["cluster_id"].max()), step=1)

    cluster_row = clusters[clusters["cluster_id"] == cluster_id]
    if cluster_row.empty:
        st.warning("Cluster not found.")
    else:
        row = cluster_row.iloc[0]
        st.write(f"**Messages:** {row['n_messages']} | **High risk ratio:** {row['high_ratio']:.2f}")
        st.write("**Canonical Template:**", row["canonical_template"])
        st.write("**Example Message:**", row["example_message"])

        # Filter messages
        cluster_msgs = messages[messages["cluster_id"] == cluster_id]
        risk_filter = st.multiselect("Filter by Risk", ["high", "medium", "low"])
        if risk_filter:
            cluster_msgs = cluster_msgs[cluster_msgs["risk_label"].isin(risk_filter)]

        keyword = st.text_input("Search text in messages")
        if keyword:
            cluster_msgs = cluster_msgs[cluster_msgs["text"].str.contains(keyword, case=False, na=False)]

        st.dataframe(cluster_msgs[["message_id", "date", "text",
                                   "candidate_name_norm_simple", "risk_label", "heuristic_score"]])

        export_csv(cluster_msgs, f"cluster_{cluster_id}.csv")
        export_pdf(cluster_msgs, f"cluster_{cluster_id}.pdf", f"Cluster {cluster_id} Messages")

# === Candidate Explorer ===
elif view == "Candidate Explorer":
    st.title("👤 Candidate Explorer")

    candidate_filter = st.text_input("Filter candidate names (contains)")
    candidate_list = messages["candidate_name_norm_simple"].unique()
    if candidate_filter:
        candidate_list = [c for c in candidate_list if candidate_filter.lower() in c.lower()]

    if len(candidate_list) == 0:
        st.warning("No candidates found.")
    else:
        candidate = st.selectbox("Select candidate", candidate_list)
        cand_msgs = messages[messages["candidate_name_norm_simple"] == candidate]

        st.write(f"**Candidate:** {candidate}")
        st.write(f"**Total msgs:** {len(cand_msgs)} | High: {(cand_msgs['risk_label']=='high').sum()} | "
                 f"Medium: {(cand_msgs['risk_label']=='medium').sum()} | Low: {(cand_msgs['risk_label']=='low').sum()}")

        cand_clusters = clusters[clusters["cluster_id"].isin(cand_msgs["cluster_id"].unique())]
        st.write("**Clusters containing this candidate**")
        st.dataframe(cand_clusters)

        risk_filter = st.multiselect("Filter by Risk", ["high", "medium", "low"])
        if risk_filter:
            cand_msgs = cand_msgs[cand_msgs["risk_label"].isin(risk_filter)]

        keyword = st.text_input("Search text in candidate's messages")
        if keyword:
            cand_msgs = cand_msgs[cand_msgs["text"].str.contains(keyword, case=False, na=False)]

        st.write("**Sample messages**")
        st.dataframe(cand_msgs[["message_id", "date", "text", "risk_label", "heuristic_score"]].head(50))

        export_csv(cand_msgs, f"candidate_{candidate}.csv")
        export_pdf(cand_msgs, f"candidate_{candidate}.pdf", f"Messages for {candidate}")

# === Alerts Feed ===
elif view == "Alerts Feed":
    st.title("🚨 Alerts Feed — Recent High-Risk Messages")
    if alerts.empty:
        st.info("No alerts file found or no high-risk messages yet.")
    else:
        st.dataframe(alerts[["date", "candidate_name_norm_simple", "text", "heuristic_score"]])
        export_csv(alerts, "alerts_feed.csv")
        export_pdf(alerts, "alerts_feed.pdf", "High-Risk Alerts Feed")
