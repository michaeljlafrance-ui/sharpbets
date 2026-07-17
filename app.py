import streamlit as st
import requests
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="MLB Sharp Insights", layout="wide")
st.title("⚾ MLB Consensus Dashboard")

# 2. Secure Key Retrieval
# This looks for the secret, but uses a hardcoded fallback so the app won't crash
try:
    API_KEY = st.secrets["RAPIDAPI_KEY"]
except:
    API_KEY = "932206dd22mshf288a41328bab03p12d137jsn9b24ebdfb34c"

URL = "https://the-sharp-edge.p.rapidapi.com/v1/mlb/consensus"

def fetch_data():
    headers = {
        "x-rapidapi-host": "the-sharp-edge.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# 3. Main Interface
if st.button("Load/Refresh MLB Data"):
    with st.spinner('Fetching sharp insights...'):
        raw_data = fetch_data()
        
        if raw_data:
            # Check the structure: some APIs return a list, some return {'data': [...]}
            # This logic handles both cases safely.
            if isinstance(raw_data, dict):
                # If the dict has a 'data' or 'results' key, use that
                if 'data' in raw_data:
                    df = pd.DataFrame(raw_data['data'])
                else:
                    df = pd.DataFrame([raw_data])
            else:
                df = pd.DataFrame(raw_data)
            
            st.success("Data successfully loaded!")
            st.dataframe(df, use_container_width=True)
            
            # CSV Download Button
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "mlb_consensus.csv", "text/csv")
        else:
            st.warning("No data found. Check if the API endpoint is correct.")
