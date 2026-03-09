import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# 🌄 Food background + login card style
page_bg = """
<style>

/* Background image */
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1490818387583-1baba5e638af");
background-size: cover;
background-position: center;
}

/* Remove header background */
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

/* Center login card */
.block-container{
max-width: 400px;
margin-top: 100px;
background-color: rgba(255,255,255,0.9);
padding: 2rem;
border-radius: 15px;
box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🔐 Login")

st.write("Welcome to **AI Food Calorie Calculator** 🍔")

username = st.text_input("👤 Username")
password = st.text_input("🔑 Password", type="password")

if st.button("🚀 Login"):

    if username and password:
        st.session_state["logged_in"] = True
        st.success("Login successful!")

        st.switch_page("pages/Calorie_app.py")

    else:
        st.error("Please enter username and password")