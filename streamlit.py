import xgboost as xgb
import streamlit as st
import pandas as pd

# Load the regression model
model = xgb.XGBRegressor()
model.load_model('xgb_model.json')

# Define the prediction function
def predict(carat, cut, color, clarity, depth, table, x, y, z):
    # Map categorical inputs to numerical values
    cut_map = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
    color_map = {'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6}
    clarity_map = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}

    cut = cut_map[cut]
    color = color_map[color]
    clarity = clarity_map[clarity]

    # Prepare data for prediction
    input_data = pd.DataFrame([[carat, cut, color, clarity, depth, table, x, y, z]], 
                              columns=['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z'])

    # Predict the price
    prediction = model.predict(input_data)
    return prediction

# Streamlit UI
st.title('Diamond Price Predictor')
st.image("https://www.thestreet.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cq_auto:good%2Cw_1200/MTY4NjUwNDYyNTYzNDExNTkx/why-dominion-diamonds-second-trip-to-the-block-may-be-different.png")
st.header('Enter the characteristics of the diamond:')

# Inputs
carat = st.number_input('Carat Weight:', min_value=0.1, max_value=10.0, value=1.0)
cut = st.selectbox('Cut Rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox('Color Rating:', ['J', 'I', 'H', 'G', 'F', 'E', 'D'])
clarity = st.selectbox('Clarity Rating:', ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'])
depth = st.number_input('Diamond Depth Percentage:', min_value=50.0, max_value=80.0, value=60.0)
table = st.number_input('Diamond Table Percentage:', min_value=50.0, max_value=80.0, value=60.0)
x = st.number_input('Diamond Length (X) in mm:', min_value=3.0, max_value=20.0, value=5.0)
y = st.number_input('Diamond Width (Y) in mm:', min_value=3.0, max_value=20.0, value=5.0)
z = st.number_input('Diamond Height (Z) in mm:', min_value=2.0, max_value=15.0, value=3.0)

# Prediction Button
if st.button('Predict Price'):
    price = predict(carat, cut, color, clarity, depth, table, x, y, z)
    st.success(f'The predicted price of the diamond is ${price[0]:,.2f} USD')
