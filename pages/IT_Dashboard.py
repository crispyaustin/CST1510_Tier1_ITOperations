# pages/IT_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from models import ITTicket
from database import db
from ai_helper import get_it_insight_from_ai

def load_tickets_df():
    rows = db.query("SELECT * FROM it_tickets")
    return pd.DataFrame([dict(r) for r in rows])

def main():
    st.title("IT Operations – Service Desk Performance")

    user = st.session_state.get("user", None)
    if not user:
        st.warning("Please login first from the Login page.")
        st.stop()

    st.subheader("Ticket Management")

    tab1, tab2, tab3 = st.tabs(["View & Analyze", "Create / Update Ticket", "AI Assistant"])

    with tab1:
        df = load_tickets_df()
        if df.empty:
            st.info("No tickets found. Use the Create tab to add tickets or load sample data by running database.py.")
        else:
            st.dataframe(df)

            # Tickets per staff
            staff_counts = df.groupby("assigned_to")["ticket_id"].count().reset_index().rename(columns={"ticket_id":"count"})
            fig1 = px.bar(staff_counts, x="assigned_to", y="count", title="Tickets per Staff Member")
            st.plotly_chart(fig1, use_container_width=True)

            status_counts = df.groupby("status")["ticket_id"].count().reset_index().rename(columns={"ticket_id":"count"})
            fig2 = px.bar(status_counts, x="status", y="count", title="Tickets by Status")
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.write("Create or update a ticket.")

        col1, col2 = st.columns(2)
        with col1:
            ticket_id = st.text_input("Ticket ID")
            requester = st.text_input("Requester")
            assigned_to = st.text_input("Assigned To")
            status = st.selectbox("Status", ["Open", "In Progress", "Waiting for User", "Resolved", "Closed"])
        with col2:
            opened_at = st.text_input("Opened At (YYYY-MM-DD)")
            resolved_at = st.text_input("Resolved At (YYYY-MM-DD or empty)")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])

        if st.button("Create Ticket"):
            ITTicket.create(ticket_id, requester, assigned_to, status, opened_at, resolved_at, priority)
            st.success("Ticket created.")
            st.rerun()
        if st.button("Update Ticket"):
            ITTicket.update(ticket_id, requester=requester, assigned_to=assigned_to, status=status,
                            opened_at=opened_at, resolved_at=resolved_at, priority=priority)
            st.success("Ticket updated.")
            st.rerun()
        if st.button("Delete Ticket"):
            ITTicket.delete(ticket_id)
            st.success("Ticket deleted.")
            st.rerun()

    with tab3:
        st.subheader("AI Insight Assistant")
        df = load_tickets_df()
        if df.empty:
            st.info("No ticket data for AI to analyze.")
        else:
            summary = df.groupby(["assigned_to", "status"])["ticket_id"].count().reset_index().rename(columns={"ticket_id":"count"})
            st.write("Aggregated view:")
            st.dataframe(summary)

            summary_text = summary.to_string(index=False)
            if st.button("Generate AI Insight"):
                with st.spinner("Contacting AI..."):
                    insight = get_it_insight_from_ai(summary_text)
                    st.markdown("### AI Recommendation")
                    st.write(insight)

if __name__ == "__main__":
    main()
