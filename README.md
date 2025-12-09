# CST1510 - Multi-Domain Intelligence Platform (Tier 1 - IT Operations)

This repository contains a Tier 1 implementation (IT Operations) for the CST1510 coursework.
It includes:
- Streamlit app with Login and IT Operations dashboard
- SQLite database initialization and migration
- bcrypt-based authentication
- CRUD operations for IT tickets
- Plotly visualizations
- AI assistant integration (OpenAI) helper (requires OPENAI_API_KEY)
- OOP model classes
- Sample data and a 1000-1500 word report (DOCX)

Run:
1. pip install -r requirements.txt
2. python database.py      # creates app.db and loads sample data
3. streamlit run app.py

Note: Set OPENAI_API_KEY as an environment variable to enable AI features.
