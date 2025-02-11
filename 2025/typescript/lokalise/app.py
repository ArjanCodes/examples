import os
import lokalise
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import json
import requests
import zipfile
import io

load_dotenv()
LOKALISE_API_KEY = os.getenv("LOKALISE_API_KEY")
LOKALISE_PROJECT_ID = os.getenv("LOKALISE_PROJECT_ID")
LANGUAGE = "en"

class LokaliseTranslator:
    def __init__(self, api_key: str, project_id: str, language: str) -> None:
        self.client = lokalise.Client(api_key)
        self.project_id = project_id
        self.language = language
        self.translations = self.get_translations()

    def get_translations(self) -> dict[str, str]:
        response = self.client.download_files(self.project_id, {
            "format": "json",
            "original_filenames": True,
            "replace_breaks": False
        })
        translations_url = response["bundle_url"]
        
        # Download and extract the ZIP file
        zip_response = requests.get(translations_url)
        zip_file = zipfile.ZipFile(io.BytesIO(zip_response.content))
        
        # Find the JSON file corresponding to the selected language
        json_filename = f"{self.language}/no_filename.json"
        with zip_file.open(json_filename) as json_file:
            return json.load(json_file)
    
    def __call__(self, key: str) -> str:
        return self.translations.get(key, key)

translator = LokaliseTranslator(LOKALISE_API_KEY, LOKALISE_PROJECT_ID, LANGUAGE)

st.title(translator("dashboard_title"))

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text(translator("loading_data"))
data = load_data(10000)
data_load_state.text(translator("done"))

if st.checkbox(translator("show_raw_data")):
    st.subheader(translator("raw_data"))
    st.write(data)

st.subheader(translator("nb_pickups_hour"))
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(translator("map_all_pickups") % hour_to_filter)
st.map(filtered_data)
