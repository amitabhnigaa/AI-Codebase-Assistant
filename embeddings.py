import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embedding():

    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )