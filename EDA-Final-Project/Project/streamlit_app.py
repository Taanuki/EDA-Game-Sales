import streamlit as st
from explore_page import show_explore_page
from prediction_page import show_predict_page

# Create a sidebar for navigation
page = st.sidebar.selectbox("Explore Or Predict", ("Explore", "Predict"))

# Display the selected page
if page == "Explore":
    show_explore_page()
else:
    show_predict_page()
