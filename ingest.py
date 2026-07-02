import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

docs = []

for root, dirs, files in os.walk("sample_repo"):

    for file in files:

        if file.endswith(".py"):

            path = os.path.join(root, file)

            loader = TextLoader(path)

            loaded_docs = loader.load()

            for doc in loaded_docs:
              doc.metadata["source"] = file

            docs.extend(loaded_docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = splitter.split_documents(docs)

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = FAISS.from_documents(
    documents,
    embedding
)

db.save_local("vectorstore")

print("Database Created Successfully")