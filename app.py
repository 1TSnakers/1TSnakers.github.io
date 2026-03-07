import streamlit as st
import requests
import humanize
from datetime import datetime

# Fetch last commit from GitHub API
def get_last_commit():
    try:
        url = "https://api.github.com/repos/1TSnakers/1TSnakers.github.io/commits?per_page=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            commit = data[0]["commit"]
            date = datetime.fromisoformat(commit["author"]["date"].replace("Z", "+00:00"))
            relative = humanize.naturalday(date)
            return f"{relative}"
        return "Unable to fetch commit"
    except:
        return "Offline"

pages = {
    "Main": [
        st.Page("homepage.py", title="Homepage"),
        st.Page("pages/commit_hall_of_fame.py", title="Commit Hall of Fame"),
        st.Page("pages/misc_apps.py", title="Misc Apps"),
    ],
    "Misc Apps": [
        st.Page("pages/ollama_models.py", title="List Ollama model info"),
    ]
}

pg = st.navigation(pages)
pg.run()

st.sidebar.write(f"Streamlit version: {st.__version__}")
st.sidebar.write(f"Last commit: {get_last_commit()}")
