import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import time
import random

st.set_page_config(
    page_title="1TSnakers Website!",
    layout="wide"
)

username = "1TSnakers"

@st.cache_data
def circle_crop_from_url(url, antialias=True):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content)).convert("RGBA")

    w, h = img.size
    size = min(w, h)
    left = (w - size) // 2
    top = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))

    if antialias:
        scale = 4
        big = size * scale
        mask = Image.new("L", (big, big), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, big, big), fill=255)
        mask = mask.resize((size, size), Image.LANCZOS)
    else:
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

    img.putalpha(mask)
    return img

@st.cache_data
def get_user_info():
    r = requests.get(f"https://api.github.com/users/{username}")
    return r.json()

@st.cache_data
def get_lang_info():
    r = requests.get(f"https://github-languages-api.vercel.app/languages/{username}")
    r = r.json()
    result = {}

    for lang in r["languages"]:
        result[lang["language"]] = lang["percentage"] / 100
    return result


def get_language_colors():
    url = "https://raw.githubusercontent.com/anuraghazra/github-readme-stats/refs/heads/master/src/common/languageColors.json"
    return requests.get(url).json()



user_info = get_user_info()

st.markdown("""
<style>
.block-container { max-width: 1600px; padding-left: 2rem; padding-right: 2rem; margin: auto; }
.stContainer { background-color: rgba(13,17,23,0.85); border-radius: 12px; padding: 1.5rem; }
</style>
""", unsafe_allow_html=True)

cache_bust = int(time.time())

main, profile = st.columns(spec=[0.75, 0.25], border=True)

with profile:
    avatar_url = user_info["avatar_url"] + f"?v={cache_bust}"
    avatar = circle_crop_from_url(avatar_url)
    st.image(avatar)

    with open("jokes.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    components.html(html_code, height=40, scrolling=False)

    st.divider()

    st.markdown(f"## **{user_info['name']}**")
    st.markdown(f"### **{username} · he/him**")
    st.text(user_info["bio"])
    st.divider()

    rand_skill_header = random.choice(["Tech I Actually Use:", "What I Build With:", "Weapons of Choice:", "Current Loadout:"])
    st.subheader(rand_skill_header)

    language_colors = get_language_colors()

    skills = dict(get_lang_info())
    skills["Java"] = 0.0

    for skill, level in skills.items():
        color = language_colors.get(skill, "#888888")
        label = f"**{skill}:** {int(level*100)}%" if level > 0 else f"**{skill}:** 0% (thankfully)"
        st.markdown(label)
        st.markdown(f"""
            <div style="background-color: #333; border-radius: 4px; height: 8px; width: 100%; margin-bottom: 16px;">
                <div style="background-color: {color}; width: {int(level*100)}%; height: 8px; border-radius: 4px;"></div>
            </div>
        """, unsafe_allow_html=True)


theme = "streamlit"

with main:
    col1, col2 = st.columns(2)
    with col1:
        st.title("Hello! I am Thomas, welcome to my website!")
    with col2:
        st.image("eyy.jpg", width=350)

    st.divider()
    
    st.markdown("### 🚀 Artemis 2 Launch Countdown")
    components.html(f"""
    <iframe
        src="https://www.tickcounter.com/countdown/9886762/artemis-ii-launch"
        width="100%"
        height="245"
        frameborder="0"
        allowfullscreen
    >
    </iframe>
    """, height=200, scrolling=False)
    st.caption("First crewed mission around the Moon since 1972 🌙")
    st.divider()

    st.image(f"https://komarev.com/ghpvc/?username={username}&v={cache_bust}")
    st.image("https://hit.yhype.me/github/profile?account_id=162380893")
    st.image(f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/output/snake-dark.svg?v={cache_bust}")

    with st.container(horizontal=True):
        st.image(f"https://github-readme-stats-1tsnakers.vercel.app/api/?username={username}&layout=compact&theme={theme}&show_icons=true&v={cache_bust}")
        st.image(f"https://github-readme-stats-1tsnakers.vercel.app/api/top-langs/?username={username}&layout=donut&theme={theme}&v={cache_bust}")
        st.image(f"https://github-readme-streak-stats-1tsnakers.vercel.app/?user={username}&theme={theme}&v={cache_bust}")

    st.divider()
    st.header("Cool things I made:")

    hall_of_fame_page = st.Page("pages/commit_hall_of_fame.py")
    st.page_link(hall_of_fame_page, label="Commit Message Hall of Fame", icon="🏆")

    pin_columns = st.columns(3)
    pinned = ["minimax-distillation-project","ProgressiveImageLoader", "ollama-for-godot", "1TSnakers.github.io", "godot-games"]
    for repo in range(len(pinned)):
        with pin_columns[repo % 3]:
            st.image(f"https://github-readme-stats-1tsnakers.vercel.app/api/pin/?username={username}&repo={pinned[repo]}&theme={theme}&v={cache_bust}", width=int(1130/3))
