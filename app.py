import streamlit as st
import requests
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="MLB Sharp Insights", layout="wide")
st.title("⚾ MLB Consensus Dashboard")

# 2. Use Secrets for Security (See note below)
# Make sure to set this in your Streamlit Cloud 'Secrets' settings
API_KEY = st.secrets["RAPIDAPI_KEY"] 
URL = "https://the-sharp-edge.p.rapidapi.com/v1/mlb/consensus"

def fetch_data():
    headers = {
        "x-rapidapi-host": "the-sharp-edge.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status() # Raises an error for bad status codes
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# 3. Main Logic
if st.button("Load/Refresh MLB Data"):
    with st.spinner('Fetching sharp insights...'):
        raw_data = fetch_data()
        
        if raw_data:
            # If the API returns a dict, wrap it in a list to make it a row
            # If it returns a list, keep it as is
            if isinstance(raw_data, dict):
                # NOTE: If your data is nested (e.g., raw_data['results']), 
                # change this to pd.DataFrame(raw_data['results'])
                df = pd.DataFrame([raw_data])
            else:
                df = pd.DataFrame(raw_data)
            
            # Displaying the dataframe
            st.success("Data loaded successfully!")
            st.dataframe(df, use_container_width=True)
            
            # Download button for CSV
            csv = df.to_csv(index=False)
            st.download_button("Download Data as CSV", csv, "sharp_mlb_data.csv", "text/csv")
        else:
            st.warning("No data returned from API.")
