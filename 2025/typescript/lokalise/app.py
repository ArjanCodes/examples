import os

import lokalise
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
LOKALISE_API_KEY = os.getenv("LOKALISE_API_KEY")
LOKALISE_PROJECT_ID = os.getenv("LOKALISE_PROJECT_ID")
LANGUAGE = "nl"

DASHBOARD_TITLE = 601816468
LOADING_DATA = 601820456
SHOW_RAW_DATA = 601821173
RAW_DATA = 601822270
DONE = 601822553
NB_PICKUPS_HOUR = 601828483
MAP_ALL_PICKUPS = 601828555


client = lokalise.Client(LOKALISE_API_KEY)


def translate(key_id: int) -> str:
    key = client.key(LOKALISE_PROJECT_ID, key_id)
    if not key.translations:
        return key.key_name["web"]

    for translation in key.translations:
        if translation["language_iso"] == LANGUAGE:
            return translation["translation"]
    # If no translation found, return the first one
    return key.translations[0]["translation"]


st.title(translate(DASHBOARD_TITLE))

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


data_load_state = st.text(translate(LOADING_DATA))
data = load_data(10000)
data_load_state.text(translate(DONE))

if st.checkbox(translate(SHOW_RAW_DATA)):
    st.subheader(translate(RAW_DATA))
    st.write(data)

st.subheader(translate(NB_PICKUPS_HOUR))
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(translate(MAP_ALL_PICKUPS) % hour_to_filter)
st.map(filtered_data)
