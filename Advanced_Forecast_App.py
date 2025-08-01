
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Advanced AI Forecast Bot", layout="wide")
st.title("📊 Advanced AI Forecast Bot (24-Month Forecast)")

# --- Load Historical Data ---
@st.cache_data
def load_data():
    return pd.read_excel("AI Bot Training Example.xlsx", sheet_name='June-25')

df = load_data()
df['Month'] = pd.to_datetime(df['Month'])
df = df[df['Month'] <= "2025-03-31"]
df.sort_values(['Part No', 'Month'], inplace=True)
df['Fiscal_Year'] = df['Month'].apply(lambda d: f"{d.year}-{d.year+1}" if d.month >= 4 else f"{d.year-1}-{d.year}")
df['Month_Num'] = df['Month'].dt.month

# --- Inflation & Tariff Factors (adjustable) ---
inflation_rate = 0.03  # 3% annual inflation
tariff_factor = 1.02   # 2% impact from tariff

# --- Calculate CAGR ---
annual_totals = df.groupby(['Part No','Fiscal_Year'])['Actual Lifting Qty'].sum().unstack(fill_value=0)
def compute_cagr(start, end):
    return ((end / start)**(1/1) - 1) if start > 0 else 0
cagr_df = pd.DataFrame(index=annual_totals.index)
cagr_df['CAGR'] = [min(compute_cagr(annual_totals.loc[idx,'2023-2024'], annual_totals.loc[idx,'2024-2025']), 1.5)
                   for idx in annual_totals.index]

# --- Absolute Parts ---
last_date = df['Month'].max()
recent_8 = df[df['Month'] >= (last_date - pd.DateOffset(months=8))]
absolute_parts = recent_8.groupby('Part No')['Actual Lifting Qty'].sum()
absolute_parts = absolute_parts[absolute_parts == 0].index.tolist()

# --- Monthly Averages & Segmentation ---
monthly_avg = df[df['Fiscal_Year']=='2024-2025'].groupby(['Part No','Month_Num'])['Actual Lifting Qty'].mean()
part_segments = df[['Part No','Usage','Supplying Country']].drop_duplicates()

# --- Holiday Calendar ---
holiday_months = {'2025-10':0.8, '2026-11':0.8}
def holiday_adjustment(date):
    key = f"{date.year}-{str(date.month).zfill(2)}"
    return holiday_months.get(key,1.0)

# --- Backlog Logic ---
df['Backlog'] = (df['Firm Schedule Qty'] - df['Actual Lifting Qty']).apply(lambda x: x if x>0 else 0)
backlog_uplift = {}
for _, row in df.iterrows():
    if row['Backlog']>0:
        m1=row['Month']+relativedelta(months=1)
        m2=row['Month']+relativedelta(months=2)
        backlog_uplift[(row['Part No'],m1)] = backlog_uplift.get((row['Part No'],m1),0)+(row['Backlog']*0.6)
        backlog_uplift[(row['Part No'],m2)] = backlog_uplift.get((row['Part No'],m2),0)+(row['Backlog']*0.4)

# --- Forecast Logic ---
forecast_months=pd.date_range(start='2025-04-01',end='2027-03-01',freq='MS')
forecast_data=[]
volatility_scores={}

for part_no in df['Part No'].unique():
    cagr=cagr_df.loc[part_no]['CAGR'] if part_no in cagr_df.index else 0
    hist= df[df['Part No']==part_no]['Actual Lifting Qty']
    volatility_scores[part_no]=hist.pct_change().abs().mean()*100

    for m in forecast_months:
        years_since=(m.year-2025)+((m.month-4)/12)
        base_qty=monthly_avg.get((part_no,m.month),0)
        forecast_val=base_qty*((1+cagr)**years_since)
        forecast_val*= (1+inflation_rate) * tariff_factor
        forecast_val*= holiday_adjustment(m)
        forecast_val+= backlog_uplift.get((part_no,m),0)

        if part_no in absolute_parts: forecast_val=0
        if part_no==7500000831 and m>=pd.to_datetime('2025-07-01'): forecast_val=0

        forecast_data.append({
            'Part No':part_no,
            'Month':m,
            'Usage':part_segments[part_segments['Part No']==part_no]['Usage'].values[0],
            'Supplying Country':part_segments[part_segments['Part No']==part_no]['Supplying Country'].values[0],
            'Forecasted Qty':round(forecast_val),
            'Volatility Score (%)':round(volatility_scores[part_no],2)
        })

forecast_df=pd.DataFrame(forecast_data)

# --- Streamlit UI ---
tab1,tab2,tab3=st.tabs(["Single Part Forecast","All Parts Forecast","Download Forecast"])

with tab1:
    part_list=sorted(forecast_df['Part No'].unique())
    selected_part=st.selectbox("Select Part No:",part_list)
    part_data=forecast_df[forecast_df['Part No']==selected_part]
    st.write(f"### Forecast for Part: {selected_part}")
    st.dataframe(part_data)

    fig,ax=plt.subplots()
    hist_data=df[df['Part No']==selected_part]
    ax.plot(hist_data['Month'],hist_data['Actual Lifting Qty'],label="Historical Actual")
    ax.plot(part_data['Month'],part_data['Forecasted Qty'],'--',label="Forecasted")
    ax.legend(); ax.set_xlabel("Month"); ax.set_ylabel("Quantity")
    st.pyplot(fig)

with tab2:
    st.write("### Forecast (All Parts with Segmentation & Confidence Scores)")
    st.dataframe(forecast_df)

with tab3:
    st.download_button("📥 Download Full Forecast",
                       data=forecast_df.to_csv(index=False),
                       file_name="Advanced_24_Month_Forecast.csv",
                       mime="text/csv")
