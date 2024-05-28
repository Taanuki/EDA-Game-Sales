import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    # Modify the path to your dataset
    return pd.read_csv('https://github.com/Taanuki/EDA-Game-Sales/tree/main/EDA-Final-Project/data')

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
    sales_time = data.groupby('Release year')['Total Game copies sold'].sum().reset_index()
    fig2 = px.line(sales_time, x='Release year', y='Total Game copies sold', labels={'Release year': 'Year', 'Total Game copies sold': 'Total Sales'})
    st.plotly_chart(fig2)

    st.write("## Platform Distribution")
    platform_count = data['Platform'].value_counts()
    fig3 = px.pie(platform_count, values=platform_count.values, names=platform_count.index, labels={'index': 'Platform', 'value': 'Count'})
    st.plotly_chart(fig3)

    st.write("## Interactive Scatter Plot")
    st.write("### Sales by Genre and Platform")
    fig4 = px.scatter(data, x='Genre', y='Total Game copies sold', color='Platform', size='Total Game copies sold', hover_data=['Game'])
    st.plotly_chart(fig4)
