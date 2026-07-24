import streamlit as st
from datetime import datetime

pages = {
    "Main": [
        st.Page("homepage.py", title="Homepage"),
        st.Page("pages/commit_hall_of_fame.py", title="Commit Hall of Fame"),
        st.Page("pages/misc_apps.py", title="Misc Apps"),
    ]
}

pg = st.navigation(pages)
pg.run()

st.sidebar.write(f"Streamlit version: {st.__version__}")
