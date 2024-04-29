import xgboost as xgb
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Loading up the Regression model we created
model = xgb.XGBRegressor()
model.load_model('xgb_model.json')

# Caching the model for faster loading
@st.cache
def predict(carat, cut, color, clarity, depth, table, x, y, z):
    # Predicting the price of the carat
    if cut == 'Fair':
        cut = 0
    elif cut == 'Good':
        cut = 1
    elif cut == 'Very Good':
        cut = 2
    elif cut == 'Premium':
        cut = 3
    elif cut == 'Ideal':
        cut = 4

    if color == 'J':
        color = 0
    elif color == 'I':
        color = 1
    elif color == 'H':
        color = 2
    elif color == 'G':
        color = 3
    elif color == 'F':
        color = 4
    elif color == 'E':
        color = 5
    elif color == 'D':
        color = 6
    
    if clarity == 'I1':
        clarity = 0
    elif clarity == 'SI2':
        clarity = 1
    elif clarity == 'SI1':
        clarity = 2
    elif clarity == 'VS2':
        clarity = 3
    elif clarity == 'VS1':
        clarity = 4
    elif clarity == 'VVS2':
        clarity = 5
    elif clarity == 'VVS1':
        clarity = 6
    elif clarity == 'IF':
        clarity = 7

    prediction = model.predict(pd.DataFrame([[carat, cut, color, clarity, depth, table, x, y, z]], columns=['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z']))
    return prediction[0]  # Returning the first element of the prediction array

st.title('Diamond Price Predictor')
st.image("https://www.thestreet.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cq_auto:good%2Cw_1200/MTY4NjUwNDYyNTYzNDExNTkx/why-dominion-diamonds-second-trip-to-the-block-may-be-different.png")
st.header('Enter the characteristics of the diamond:')
carat = st.number_input('Carat Weight:', min_value=0.1, max_value=10.0, value=1.0)
cut = st.selectbox('Cut Rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox('Color Rating:', ['J', 'I', 'H', 'G', 'F', 'E', 'D'])
clarity = st.selectbox('Clarity Rating:', ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'])
depth = st.number_input('Diamond Depth Percentage:', min_value=0.1, max_value=100.0, value=1.0)
table = st.number_input('Diamond Table Percentage:', min_value=0.1, max_value=100.0, value=1.0)
x = st.number_input('Diamond Length (X) in mm:', min_value=0.1, max_value=100.0, value=1.0)
y = st.number_input('Diamond Width (Y) in mm:', min_value=0.1, max_value=100.0, value=1.0)
z = st.number_input('Diamond Height (Z) in mm:', min_value=0.1, max_value=100.0, value=1.0)

exchange_rate_usd_to_inr = 84  # Conversion rate from USD to INR

if st.button('Predict Price'):
    price_in_usd = predict(carat, cut, color, clarity, depth, table, x, y, z)
    price_in_inr = price_in_usd * exchange_rate_usd_to_inr
    st.success(f'The predicted price of the diamond is ₹{price_in_inr:.2f} INR')

# Load diamond data for visualization
diamond_data = pd.read_csv("diamonds.csv")

# Display histograms for numeric features
st.subheader('Feature Distributions')
fig = px.histogram(diamond_data, x='carat', title='Carat Distribution', nbins=30, histnorm='density')
st.plotly_chart(fig)

fig = px.histogram(diamond_data, x='depth', title='Depth Distribution', nbins=30, histnorm='density')
st.plotly_chart(fig)

fig = px.histogram(diamond_data, x='table', title='Table Distribution', nbins=30, histnorm='density')
st.plotly_chart(fig)

fig = px.histogram(diamond_data, x='price', title='Price Distribution', nbins=30, histnorm='density')
st.plotly_chart(fig)

# Scatter plot between carat and price
st.subheader('Scatter plot of Carat vs Price')
fig = px.scatter(diamond_data, x='carat', y='price', title='Carat vs Price')
st.plotly_chart(fig)
