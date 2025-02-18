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

ny21_zipcodes = ['12028', '12040', '12042', '12045', '12046', '12053', '12057', '12068', '12069', '12070', '12072', '12073', '12074', '12078', '12086', '12095', '12108', '12117', '12118', '12122', '12134', '12139', '12164', '12166', '12167', '12168', '12190', '12194', '12197', '12801', '12803', '12808', '12809', '12810', '12811', '12812', '12814', '12815', '12816', '12817', '12819', '12820', '12821', '12822', '12823', '12824', '12827', '12828', '12831', '12832', '12833', '12834', '12835', '12836', '12837', '12838', '12839', '12841', '12842', '12843']

st.title("NY-21 Tax Returns by Income Bracket")

if st.button('Load IRS Data'):
    download_irs_data()
    st.success("IRS data downloaded successfully.")

if st.button('Process Data'):
    df = load_data()
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
