import streamlit as st

pg = st.navigation([
    st.Page("explore.py", title="Explore", icon="🔍"),
    st.Page("background.py", title="Background", icon="📖"),
    st.Page("methodology.py", title="Methodology", icon="🔬"),
    st.Page("future_work.py", title="Future Work", icon="💭"),
])

pg.run()