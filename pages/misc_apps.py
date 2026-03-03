import streamlit as st
import streamlit.components.v1 as components

ollama_page = st.Page("pages/ollama_models.py")

st.set_page_config(page_title="Misc Apps", layout="wide")

st.markdown("""
<style>
.block-container { max-width: 1600px; padding-left: 2rem; padding-right: 2rem; margin: auto; }
.stContainer { background-color: rgba(13,17,23,0.85); border-radius: 12px; padding: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("Misc Apps")

st.markdown("""
### Check out these other things:
""")

st.page_link(ollama_page, label="List Ollama model info", icon="🤖")
