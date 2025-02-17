import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

def download_irs_data():
    url = 'https://www.irs.gov/pub/irs-soi/21zpallagi.csv'
    response = requests.get(url)
    with open('21zpallagi.csv', 'wb') as f:
        f.write(response.content)

def load_data():
    df = pd.read_csv('21zpallagi.csv', encoding='latin1')
    return df

ny21_zipcodes = ['12801', '12803', '12901', '12910', '12912', '12913']

st.title("NY-21 Tax Returns by Income Bracket")

if st.button('Load IRS Data'):
    download_irs_data()
    st.success("IRS data downloaded successfully.")

if st.button('Process Data'):
    df = load_data()
    # Use the correct column name 'zipcode'
    try:
        ny21_data = df[df['zipcode'].astype(str).isin(ny21_zipcodes)]
        grouped = ny21_data.groupby(['zipcode', 'agi_stub'])['N1'].sum().reset_index()
        st.write(grouped)

        st.subheader("Visualization")
        for zipcode in ny21_zipcodes:
            data = grouped[grouped['zipcode'] == zipcode]
            plt.figure()
            plt.pie(data['N1'], labels=data['agi_stub'], autopct='%1.1f%%')
            plt.title(f'Income Distribution in ZIP code {zipcode}')
            st.pyplot(plt)
    except KeyError:
        st.error("Error processing data. Please check the dataset and column names.")
