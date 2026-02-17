
from pymongo import MongoClient
import streamlit as st


def get_database():
    """
    Connects to MongoDB Atlas using credentials stored in Streamlit secrets.
    """
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["m3_pediatric_db"]
