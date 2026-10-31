"""Entry point: names the pages in the sidebar (Builders, For investors)."""
import streamlit as st

pages = st.navigation([
    st.Page("builders.py", title="Builders", icon="🚀", default=True),
    st.Page("pages/2_For_investors.py", title="For investors", icon="💼"),
])
pages.run()
