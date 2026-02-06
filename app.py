import streamlit as st
import requests
from PIL import Image, ImageDraw
from io import BytesIO

st.set_page_config(layout="wide")

username = "1TSnakers"

def circle_crop_from_url(url, antialias=True):
    # Download image
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    img = Image.open(BytesIO(resp.content)).convert("RGBA")

    # Make square (center crop)
    w, h = img.size
    size = min(w, h)
    left = (w - size) // 2
    top = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))

    # Create mask
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

    # Apply mask
    img.putalpha(mask)
    return img

def get_user_info():
    r = requests.get(f"https://api.github.com/users/{username}")
    return r.json()

user_info = get_user_info()

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1600px;
            padding-left: 0rem;
            padding-right: 0rem;
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
        .stContainer {
            background-color: rgba(13,17,23,0.85);
            border-radius: 12px;
            padding: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


main, profile = st.columns(spec=[0.75, 0.25], border=True)

with profile:
    st.image(circle_crop_from_url(user_info["avatar_url"]))
    st.markdown("## **" + user_info["name"] + "**")
    st.markdown("### **" + username + " · he/him**")
    st.text(user_info["bio"])
    

with main:
    col1, col2 = st.columns(2)
    with col1:
        st.title("Hello! I am Thomas, welcome to my website!")
    with col2:
        st.image("eyy.jpg", width=350)

    st.divider()

    st.image("https://komarev.com/ghpvc/?username=" + username)
    st.image(f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/output/snake-dark.svg")

    L, R = st.columns([0.4, 0.6])
    
    with L:
        st.image(f"https://github-readme-stats-1tsnakers.vercel.app/api/?username={username}&layout=compact&theme=dark&show_icons=true")
        st.image(f"https://github-readme-streak-stats-1tsnakers.vercel.app/?user={username}&theme=dark")
    with R:
        st.image(f"https://github-readme-stats-1tsnakers.vercel.app/api/top-langs/?username={username}&layout=compact&theme=dark")
    
    st.divider()

