import streamlit as st
import pandas as pd
import requests
import zipfile
import io
import matplotlib.pyplot as plt

def download_irs_data():
    url = 'https://www.irs.gov/pub/irs-soi/21zpallagi.csv'
    response = requests.get(url)
    with open('21zpallagi.csv', 'wb') as f:
        f.write(response.content)

def load_data():
    df = pd.read_csv('21zpallagi.csv', encoding='latin1')
    return df

# List of ZIP codes in NY-21 (partial, needs full ZIP code list)
ny21_zipcodes = ['12801', '12803', '12901', '12910', '12912', '12913']

st.title("NY-21 Tax Returns by Income Bracket")

if st.button('Load IRS Data'):
    download_irs_data()
    st.success("IRS data downloaded successfully.")

if st.button('Process Data'):
    df = load_data()
    ny21_data = df[df['ZIPCODE'].astype(str).isin(ny21_zipcodes)]
    grouped = ny21_data.groupby(['ZIPCODE', 'agi_stub'])['N1'].sum().reset_index()
    st.write(grouped)

    st.subheader("Visualization")
    for zipcode in ny21_zipcodes:
        data = grouped[grouped['ZIPCODE'] == zipcode]
        plt.figure()
        plt.pie(data['N1'], labels=data['agi_stub'], autopct='%1.1f%%')
        plt.title(f'Income Distribution in ZIP code {zipcode}')
        st.pyplot(plt)
