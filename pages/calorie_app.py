import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import pandas as pd
import re

# Page config
st.set_page_config(page_title="AI Food Calorie Calculator", layout="wide")

# Minimal Modern UI CSS
page_style = """
<style>

/* Remove header background */
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}

/* Center content */
.block-container{
    max-width: 900px;
    margin: auto;
    padding-top: 40px;
    padding-bottom: 40px;
}

/* Title style */
h1{
    text-align:center;
    color:#2c3e50;
    font-weight:700;
}

/* Card style */
.main-card {
    background-color: rgba(255,255,255,0.95);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Title
st.markdown("<h1>🍔 AI Food Calorie Calculator</h1>", unsafe_allow_html=True)

# Start card
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("🍽 Enter Food Details")

food_name = st.text_input("Food Name")

uploaded_image = st.file_uploader(
    "Upload Food Image",
    type=["jpg","jpeg","png"]
)

# Calculate button
if st.button("🚀 Calculate Calories"):

    # FOOD NAME INPUT
    if food_name:

        prompt = f"""
        Give nutrition information for {food_name}.
        Format exactly like this:

        Calories: number kcal
        Protein: number g
        Carbs: number g
        Fat: number g
        """

        response = model.generate_content(prompt)
        result = response.text

        st.success("Nutrition Information")
        st.write(result)

        # Extract calories
        calories_match = re.search(r'calories[^0-9]*(\d+)', result, re.IGNORECASE)
        calories = calories_match.group(1) if calories_match else "N/A"

        st.session_state.history.append({
            "Food Name": food_name,
            "Calories": calories
        })

    # IMAGE INPUT
    elif uploaded_image:

        image = Image.open(uploaded_image)

        st.image(image, caption="Uploaded Food", use_container_width=True)

        prompt = """
        Identify the food in this image and give nutrition in this format:

        Food Name: name
        Calories: number kcal
        Protein: number g
        Carbs: number g
        Fat: number g
        """

        response = model.generate_content([prompt, image])
        result = response.text

        st.success("Nutrition Information")
        st.write(result)

        # Extract food name
        food_match = re.search(r'food name[^a-zA-Z]*([a-zA-Z ]+)', result, re.IGNORECASE)
        food_detected = food_match.group(1) if food_match else "Food Image"

        # Extract calories
        calories_match = re.search(r'calories[^0-9]*(\d+)', result, re.IGNORECASE)
        calories = calories_match.group(1) if calories_match else "N/A"

        st.session_state.history.append({
            "Food Name": food_detected,
            "Calories": calories
        })

    else:
        st.warning("Please enter food name or upload an image.")

# History table
st.subheader("📜 Food History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No foods checked yet.")

# Clear history
if st.button("🗑 Clear History"):
    st.session_state.history = []

# End card
st.markdown("</div>", unsafe_allow_html=True)