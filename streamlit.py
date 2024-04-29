import xgboost as xgb
import streamlit as st
import pandas as pd

# Loading up the Regression model we created
model = xgb.XGBRegressor()
model.load_model('xgb_model.json')

# Caching the model for faster loading
@st.cache
def predict(carat, cut, x, y, z):
    #Predicting the price of the carat
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

    # Assuming default column names for simplicity
    prediction = model.predict(pd.DataFrame([[carat, cut, x, y, z]], columns=['carat', 'cut', 'x', 'y', 'z']))
    return prediction[0]  # Returning the first element of the prediction array

st.title('Diamond Price Predictor')
st.image("https://www.thestreet.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cq_auto:good%2Cw_1200/MTY4NjUwNDYyNTYzNDExNTkx/why-dominion-diamonds-second-trip-to-the-block-may-be-different.png")
st.header('Enter the characteristics of the diamond:')
carat = st.number_input('Carat Weight:', min_value=0.1, max_value=10.0, value=1.0)
cut = st.selectbox('Cut Rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
x = st.number_input('Diamond Length (X) in mm:', min_value=0.1, max_value=100.0, value=1.0)
y = st.number_input('Diamond Width (Y) in mm:', min_value=0.1, max_value=100.0, value=1.0)
z = st.number_input('Diamond Height (Z) in mm:', min_value=0.1, max_value=100.0, value=1.0)

exchange_rate_usd_to_inr = 75  # Conversion rate from USD to INR

if st.button('Predict Price'):
    price_in_usd = predict(carat, cut, x, y, z)
    price_in_inr = price_in_usd * exchange_rate_usd_to_inr
    st.success(f'The predicted price of the diamond is ₹{price_in_inr:.2f} INR')
