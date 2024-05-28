import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Load the saved model
model_filename = 'best_model.pkl'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Load feature columns used in the model
feature_columns = [
    'Release year', 'Release month', 'Release day', 'Release dayofweek',
    'Release decade', 'Genre_Action', 'Genre_Adventure', 'Genre_Role-playing',
    'Genre_Shooter', 'Developer_XYZ', 'Publisher_ABC', 'Platform_PlayStation 4',
    'Platform_Xbox One', 'Platform_PC', # Add other necessary columns here
]

# Function to preprocess user input
def preprocess_input(user_input):
    # One-hot encoding for categorical features
    categorical_features = ['Genre', 'Developer', 'Publisher', 'Platform']
    user_input_encoded = pd.get_dummies(user_input, columns=categorical_features)

    # Ensure all necessary columns are present
    for col in feature_columns:
        if col not in user_input_encoded.columns:
            user_input_encoded[col] = 0

    return user_input_encoded[feature_columns]

# Streamlit app
st.title("Game Sales Prediction")

release_date = st.date_input("Release Date")
genre = st.text_input("Genre")
developer = st.text_input("Developer")
publisher = st.text_input("Publisher")
platform = st.text_input("Platform")

if st.button("Predict Sales"):
    try:
        release_year = release_date.year
        release_month = release_date.month
        release_day = release_date.day
        release_dayofweek = release_date.weekday()
        release_decade = (release_year // 10) * 10

        # Create a DataFrame with user input
        data = {
            'Release year': [release_year],
            'Release month': [release_month],
            'Release day': [release_day],
            'Release dayofweek': [release_dayofweek],
            'Release decade': [release_decade],
            'Genre': [genre],
            'Developer': [developer],
            'Publisher': [publisher],
            'Platform': [platform],
        }

        user_input = pd.DataFrame(data)
        user_input_processed = preprocess_input(user_input)
        prediction_log = model.predict(user_input_processed)
        prediction = np.expm1(prediction_log)  # Convert from log scale
        predicted_sales = f"{prediction[0]:.2f} million copies"
        
        st.success(f"Predicted Game Sales: {predicted_sales}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    