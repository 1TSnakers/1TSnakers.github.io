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
make language proficiency better
forgot, coded from my phone
gotta fix before deploy
how tf did this get in?
-_-
make refreshing not weird
make github stat image layouts not look like s***
this formating is for a joke""", language=None)

    st.header("1TSnakers/ProgressiveImageLoader")
    st.code("""i mess things up :'(
make image scaling good
""", language=None)

with col2:
    st.header("1TSnakers/OllamaSearchAPI")
    st.code("""f*** this s***
i love debugging
i have no idea what i am doing
cors s***
i test in production""", language=None)

    st.header("1TSnakers/minimax-distillation-project")
    st.code("""add readme and half done teacher dataset
the teacher dataset is unfinished, dont use it in production, or in anything right now for that matter
i have fundamentally misunderstood how git works.
zipped files shouldnt be tracked, what is there to track anyway?
wrong thing copied :(
renamed all of the files to not start with minimax-distillation-project
the main things im using for this, dont worry, this will be added to :)
""", language=None)

st.markdown("---")

st.header("🏅 Best in Show")
st.info("**\"i have fundamentally misunderstood how git works\"** — 1TSnakers/minimax-distillation-project\n\n*Everyone's first confusion with git branches, manifested.*")
