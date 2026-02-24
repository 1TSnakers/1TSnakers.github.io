import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
import humanize

st.set_page_config(
    page_title="List Ollama model info",
    layout="wide"
)

st.markdown("""
<style>
.block-container { max-width: 1600px; padding-left: 0rem; padding-right: 0rem; margin: auto; }
.stContainer { background-color: rgba(13,17,23,0.85); border-radius: 12px; padding: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.header("List Ollama model info")

HOST = "https://ollama-search-api.vercel.app"

def is_api_up():
    try:
        r = requests.get(f"{HOST}/ping")
        st.write(f"Error: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        st.write(e)
        return False

namespace = st.text_input(
    "Namespace",
    value="library"
)

do_humanize = st.checkbox("Humanize outputs?")

if st.button("Make list"):
    start_time = time.time()
    
    if not is_api_up():
        st.error("API is not reachable")
    else:
        if not namespace:
            st.warning("Namespace cannot be empty!")
            st.stop()
            
        r = requests.get(f"{HOST}/{namespace}")
        library = r.json()["results"]

        if do_humanize:
            models = [model["model_base_name"] for model in library]
            pull_count = [model["pull_count_str"] for model in library]
            date = [model["last_updated_str"] for model in library]
        else:
            models = [model["model_base_name"] for model in library]
            pull_count = [int(model["pull_count"]) for model in library]
            date = [datetime.fromisoformat(model["last_updated_iso"]) for model in library]

        total_time = time.time() - start_time
        total_time = round(total_time, 3)
        cache_time = datetime.fromisoformat(r.json()["cache_expires_at"]) - datetime.now().astimezone()

        st.write(f"{len(models)} models counted in {total_time} seconds")
        st.write(f"Cache expires in {humanize.naturaldelta(cache_time)}")
        
        df = pd.DataFrame({
            "model": models,
            "pull_count": pull_count,
            "date": date
        })

        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "model": "AI Model",
                "Pulls": "Pulls" if do_humanize else st.column_config.NumberColumn("Pulls"),
                "date": "Last Updated" if do_humanize else st.column_config.DateColumn("Last Updated")
            }
        )