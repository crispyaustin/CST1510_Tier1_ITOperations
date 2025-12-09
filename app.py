# app.py
import streamlit as st
from database import db

db.init_schema()

st.set_page_config(page_title="Multi-Domain Intelligence Platform", layout="wide")

st.title("Multi-Domain Intelligence Platform (Tier 1 - IT Operations)")
st.write("Use the sidebar to navigate. Login first.")

st.sidebar.title("Navigation")
st.sidebar.write("Pages:")
st.sidebar.markdown("- Login")
st.sidebar.markdown("- IT Operations Dashboard")

st.write("Open the pages folder in Streamlit to use the Login and Dashboard pages.")
