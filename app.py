import streamlit as st
import requests
import pandas as pd

# Page config
st.set_page_config(page_title="MLB Sharp Insights", layout="wide")

st.title("⚾ MLB Consensus Dashboard")

# Your API Credentials
API_KEY = "932206dd22mshf288a41328bab03p12d137jsn9b24ebdfb34c"
URL = "https://the-sharp-edge.p.rapidapi.com/v1/mlb/consensus"

def fetch_data():
    headers = {
        "x-rapidapi-host": "the-sharp-edge.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(URL, headers=headers)
    return response.json()

if st.button("Refresh MLB Data"):
    with st.spinner('Fetching sharp insights...'):
        data = fetch_data()
        # Assuming the API returns a list of games/consensus
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
else:
    st.info("Click the button to load the latest MLB sharp consensus data.")
