import streamlit as st

pg = st.navigation([
    st.Page("explore.py", title="Explore", icon="🔍"),
])

pg.run()