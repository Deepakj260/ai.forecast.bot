
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

st.title("AI Forecast Bot: Lifting Quantity Prediction")

st.markdown("Upload your monthly schedule file (Excel format)")
uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['Month'] = pd.to_datetime(df['Month'])
    df.sort_values('Month', inplace=True)

    # Feature engineering
    df['Month_Num'] = df['Month'].dt.month
    df['Year'] = df['Month'].dt.year
    df['Firm_Lag1'] = df['Firm Schedule Qty'].shift(1)
    df['Actual_Lag1'] = df['Actual Lifting Qty'].shift(1)

    df_model = df.dropna()

    features = ['Firm Schedule Qty', 'Firm_Lag1', 'Actual_Lag1', 'Month_Num', 'Year']
    target = 'Actual Lifting Qty'

    X = df_model[features]
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=4)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Prediction for test data
    y_pred = model.predict(X_test)
    test_results = X_test.copy()
    test_results['Actual'] = y_test.values
    test_results['Predicted'] = y_pred
    test_results['Error'] = test_results['Actual'] - test_results['Predicted']

    st.subheader("📊 Forecast Results (Last 4 Months)")
    st.dataframe(test_results.round(2))

    # Upload for future prediction
    st.subheader("📥 Upload Next Month's Firm Schedule for Forecast")
    future_file = st.file_uploader("Upload future schedule (same format)", type="xlsx", key="future")

    if future_file:
        future_df = pd.read_excel(future_file)
        future_df['Month'] = pd.to_datetime(future_df['Month'])
        future_df['Month_Num'] = future_df['Month'].dt.month
        future_df['Year'] = future_df['Month'].dt.year

        # Use last known values for lag features
        last_firm = df['Firm Schedule Qty'].iloc[-1]
        last_actual = df['Actual Lifting Qty'].iloc[-1]
        future_df['Firm_Lag1'] = last_firm
        future_df['Actual_Lag1'] = last_actual

        future_features = future_df[features]
        future_df['Predicted Lifting'] = model.predict(future_features)

        st.subheader("🔮 Predicted Actual Lifting")
        st.dataframe(future_df[['Month', 'Firm Schedule Qty', 'Predicted Lifting']].round(2))
