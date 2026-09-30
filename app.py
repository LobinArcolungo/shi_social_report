import streamlit as st
from leaderboard import parse_chat_file, build_month_leaderboard
from pathlib import Path
import base64

st.set_page_config(
    page_title="💩 Leaderboard",
    layout="wide"
)

# ---------- Background ----------
background = Path("assets/background.jpg")

if background.exists():
    with open(background, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        .month-box {{
            background: rgba(0,40,80,0.85);
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            color:white;
        }}

        div.stButton > button {{
            width:100%;
            border-radius:999px;
            background:#2F80ED;
            color:white;
            border:none;
            padding:10px;
            font-weight:bold;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("💩 Poo Leaderboard")

st.write("Upload your WhatsApp export file")

uploaded_file = st.file_uploader(
    "Choose a chat file",
    type=["txt"]
)

if uploaded_file:

    stats, months = parse_chat_file(uploaded_file)

    st.subheader("Available Months")

    months = sorted(months, reverse=True)

    for year, month, label in months:

        with st.expander(label):

            output = build_month_leaderboard(
                stats,
                year,
                month
            )

            st.code(output)