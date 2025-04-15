import streamlit as st
from login import loginpage
from dashboard import Dashboard

st.set_page_config(page_title="Human Resource Management", layout="centered")

# Custom styles
st.markdown("""
    <style>
    body {
        background-color: white;
        color: #333;
    }

    .stForm.st-emotion-cache-qcpnpn.e1ttwmlf1 {
        background-color: #000;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .st-emotion-cache-1yiq2ps {
        background-color: rgb(6, 24, 48);
        padding: 20px;
        border-radius: 12px;
    }

    .stTextInput, .stPasswordInput {
        width: 100%;
        height: 40px;
        margin-bottom: 20px;
        font-size: 16px;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        width: 100%;
        height: 50px;
        border-radius: 5px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #45a049;
    }

    .stTitle {
        text-align: center;
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Render login or dashboard based on login state
if st.session_state.logged_in:
    Dashboard()
else:
    loginpage()
