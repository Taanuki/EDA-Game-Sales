import streamlit as st
import pandas as pd
import plotly.express as px
import re
import os

# Define the input and output directories
input_dir = r'C:\Users\kn010\OneDrive\Documents\Concordia files\Final Project EDA\data'
output_dir = r'C:\Users\kn010\OneDrive\Documents\Concordia files\Final Project EDA\data\Cleaned'

# Define the mapping of filenames to console names
files = {
    "best_selling_video_games_PS2.csvs_sorted.csv": "PlayStation 2",
    "best_selling_video_games_PS3.csvs_sorted.csv": "PlayStation 3",
    "best_selling_video_games_PS4.csvs_sorted.csv": "PlayStation 4",
    "best_selling_video_games_PS5.csvs_sorted.csv": "PlayStation 5",
    "GameCube_best_selling_games.csv": "GameCube",
    "PC_best_selling_games.csv": "PC",
    "Nintendo Switch_best_selling_games.csv": "Nintendo Switch",
    "Wii_best_selling_games.csv": "Wii",
    "Wii U_best_selling_games.csv": "Wii U",
    "Xbox_best_selling_games.csv": "Xbox",
    "Xbox One_best_selling_games.csv": "Xbox One",
    "Xbox 360_best_selling_games.csv": "Xbox 360"
}

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to clean up the 'Total Game copies sold' column
def clean_copies_sold(value):
    # Remove text within square brackets
    cleaned_value = re.sub(r'\[.*?\]', '', value)
    return cleaned_value.strip()

# Function to clean the dataframe
def clean_dataframe(df, console_name):
    # Renaming columns
    df.rename(columns=lambda x: x.replace('[a]', '').replace('(s)', '').replace('total copies sold', 'Copies sold').replace('Total Game copies sold', 'Copies sold'), inplace=True)
    
    # Check if 'Copies sold' column exists
    if 'Copies sold' in df.columns:
        # Cleaning the 'Copies sold' column
        df['Copies sold'] = df['Copies sold'].apply(clean_copies_sold)
    
    # Remove any existing 'console_name' columns
    if 'console_name' in df.columns:
        df.drop(columns=['console_name'], inplace=True)
    
    # Add the 'Console_name' column
    df['Console_name'] = console_name
    
    return df

# Function to load and clean data
@st.cache_data
def load_data():
    cleaned_dataframes = []
    
    for file_name, console_name in files.items():
        input_file_path = os.path.join(input_dir, file_name)
        
        # Load the CSV file
        df = pd.read_csv(input_file_path)
        
        # Clean the dataframe
        df = clean_dataframe(df, console_name)
        
        # Append the cleaned dataframe to the list
        cleaned_dataframes.append(df)
        
        # Save the cleaned dataframe to a new CSV file
        output_file_path = os.path.join(output_dir, file_name)
        df.to_csv(output_file_path, index=False)
    
    # Concatenate all cleaned dataframes
    full_data = pd.concat(cleaned_dataframes, ignore_index=True)
    return full_data

data = load_data()

def show_explore_page():
    st.title("Data Exploration")

    st.write("## Dataset Overview")
    st.write(data.head())

    st.write("## Summary Statistics")
    st.write(data.describe())

    st.write("## Genre Distribution")
    genre_count = data['Genre'].value_counts()
    fig1 = px.bar(genre_count, x=genre_count.index, y=genre_count.values, labels={'x': 'Genre', 'y': 'Count'})
    st.plotly_chart(fig1)

    st.write("## Sales Over Time")
    sales_time = data.groupby('Release year')['Copies sold'].sum().reset_index()
    fig2 = px.line(sales_time, x='Release year', y='Copies sold', labels={'Release year': 'Year', 'Copies sold': 'Total Sales'})
    st.plotly_chart(fig2)

    st.write("## Platform Distribution")
    platform_count = data['Console_name'].value_counts()
    fig3 = px.pie(platform_count, values=platform_count.values, names=platform_count.index, labels={'index': 'Platform', 'value': 'Count'})
    st.plotly_chart(fig3)

    st.write("## Interactive Scatter Plot")
    fig4 = px.scatter(data, x='Genre', y='Copies sold', color='Console_name', size='Copies sold', hover_data=['Game'])
    st.plotly_chart(fig4)
