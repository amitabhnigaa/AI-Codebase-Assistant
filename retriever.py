import streamlit as st

from langchain_community.vectorstores import FAISS
from embeddings import get_embedding


class CodeRetriever:

    def __init__(self):

        embedding = get_embedding()

        self.db = FAISS.load_local(
            "vectorstore",
            embedding,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, question, k=3):

        return self.db.similarity_search(
            question,
            k=k
        )


@st.cache_resource
def get_retriever():

    return CodeRetriever()