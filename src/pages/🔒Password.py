import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import xgboost as xgb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
from zxcvbn import zxcvbn
import re
import os
from collections import Counter


st.set_page_config(
    page_title = "Password-Checker",
    page_icon = "🔒"
)

# Adding line to sidebar
with st.sidebar:
    st.write("")

@st.cache_resource
def load_xgb_model():
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(os.path.abspath("xgb_strength_26052024.json"))
    return xgb_model

# Title of page
st.subheader("Password-Checker 🔒", divider="blue")

# Input for password
password_input = st.text_input("Password 🔒", placeholder="Password...") 
password_btn = st.button("Check")

if password_btn and password_input == "":
    st.error("Enter Password")
    
elif password_btn and password_input != "":
    
    password_analysis = pd.DataFrame({
        "length" :        [len(password_input)],
        "small_letters" : [len(re.findall("[a-z]", password_input))],
        "big_letters" :   [len(re.findall("[A-Z]", password_input))],
        "numbers" :       [len(re.findall("[0-9]", password_input))],
        "special_chars" : [sum([count for char, count in Counter(password_input).items() if char in string.punctuation])],
    })

    password_analysis["percent_small_letters"] = round(password_analysis["small_letters"]/password_analysis["length"], 3)
    password_analysis["percent_big_letters"] =   round(password_analysis["big_letters"]/password_analysis["length"], 3)
    password_analysis["percent_numbers"] =       round(password_analysis["numbers"]/password_analysis["length"], 3)
    password_analysis["percent_special_chars"] = round(password_analysis["special_chars"]/password_analysis["length"], 3)
        
    xgb_model = load_xgb_model()
    password_prediction = xgb_model.predict(password_analysis.copy()) # Prediction from XGB model
    zxcvbn_prediction = zxcvbn(password_input) # Prediction from 'zxcvbn' lib
    
    zxcvbn_password_analysis = password_analysis[["length", "small_letters", "big_letters", "numbers", "special_chars"]].copy()
    zxcvbn_password_analysis["Score"] = zxcvbn_prediction["score"]
    zxcvbn_password_analysis["Best-Time"] = "".join(list(str(round(float(zxcvbn_prediction["crack_times_seconds"]["offline_fast_hashing_1e10_per_second"]), 3)))[:5])+"..."
    
    zxcvbn_password_analysis = zxcvbn_password_analysis.rename(columns={
        "length" :        "Length",
        "small_letters" : "Small-Chars",
        "big_letters" :   "Big-Chars",
        "numbers" :       "Numbers",
        "special_chars" : "Special-Chars",
        
    })
    
    colors_dict = {
        0 : "#ff0000",
        1 : "#ffa500",
        2 : "#ffff00",
        3 : "#90ee90",
        4 : "#add8e6",
    }

    zxcvbn_password_analysis = zxcvbn_password_analysis.style.set_properties(**{"background-color": f"{colors_dict[zxcvbn_prediction["score"]]}"}, subset=["Score"])
    st.data_editor(zxcvbn_password_analysis, use_container_width=True, 
                    hide_index=True, disabled=True)
    
    # ----------------- # 
    
    add_vertical_space(5)
    
    # Angles of arrow on pie chart
    angles_dict = {
        0 : 150,
        1 : 90, 
        2 : 30,  
    } 
    angle_rad = np.deg2rad(angles_dict[password_prediction[0]])
    x = np.cos(angle_rad)
    y = np.sin(angle_rad)
    
    fig, ax = plt.subplots()
    wedge, label = ax.pie([1, 1, 1, 3], labels=["2", "1", "0", "..."], 
                                    colors=["#90ee90", "#ffa500", "#f44336"])
    wedge[-1].set_visible(False)
    label[-1].set_visible(False)
    
    ax.add_artist(plt.Circle((0, 0), 0.7, color='white')) # type: ignore
    
    plt.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(facecolor="gray", shrink=0.08))
    ax.text(0, -0.2, "AI", fontsize=15, ha="center", fontweight="bold", color="pink")
    
    ax.axis("equal")
    st.pyplot(fig)