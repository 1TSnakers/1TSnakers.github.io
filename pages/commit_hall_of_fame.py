import streamlit as st

st.set_page_config(page_title="Commit Hall of Fame", layout="wide")

st.markdown("""
<style>
.block-container { max-width: 1600px; padding-left: 2rem; padding-right: 2rem; margin: auto; }
.stContainer { background-color: rgba(13,17,23,0.85); border-radius: 12px; padding: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("Commit Message Hall of Fame")

st.markdown("*The best commit messages from 1TSnakers (Thomas McNamee)*\n\nSorry for the curses, coding at 10 pm is horrible.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("1TSnakers/1TSnakers.github.io")
    st.code("""streamlit is autistic
i hate this solution
its not needed
forgot this is here :/
remove whitespace and make it not atrocious to look at without a giant monitor
(and fix buggy joke code)
make language proficiency better""", language=None)

with col2:
    st.header("1TSnakers/OllamaSearchAPI")
    st.code("""f*** this s***
i love debugging
i have no idea what i am doing
cors s***
i test in production""", language=None)

    st.header("1TSnakers/ProgressiveImageLoader")
    st.code("""i mess things up :'(
make image scaling good
""", language=None)

st.markdown("---")

st.header("🏅 Best in Show")
st.info("**\"i have no idea what i am doing\"** — 1TSnakers/OllamaSearchAPI\n\n*Timeless. Relatable. Pure catharsis.*")
