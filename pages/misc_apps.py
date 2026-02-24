import streamlit as st
import streamlit.components.v1 as components

ollama_page = st.Page("pages/ollama_models.py")

st.set_page_config(
    page_title="Misc Apps",
    layout="wide"
)

st.title("Misc Apps")

st.markdown("""
### Check out these other things:
""")

# Link to the hidden Ollama models page
st.page_link(ollama_page, label="List Ollama model info", icon="🤖")

# You can add more misc apps here
# st.page_link("pages/another_app.py", label="Another App", icon="📦")
