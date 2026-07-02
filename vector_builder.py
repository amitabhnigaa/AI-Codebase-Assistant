import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import FAISS
from embeddings import get_embedding


SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".php",
    ".rb",
    ".xml",
    ".html",
    ".css",
    ".properties",
    ".json",
    ".sql",
    ".yml",
    ".yaml",
    ".md"
}


IGNORE_DIRS = {
    ".git",
    "target",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
    "bin",
    "out",
    ".mvn",
    ".gradle",
    "venv",
    ".venv",
    "coverage",
    ".pytest_cache"
}


def build_vector_db(folder_path):

    docs = []

    for root, dirs, files in os.walk(folder_path):

        # Skip unnecessary folders
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            path = os.path.join(root, file)

            try:

                loader = TextLoader(
                    path,
                    encoding="utf-8"
                )

                loaded_docs = loader.load()

                for doc in loaded_docs:
                    doc.metadata["source"] = path

                docs.extend(loaded_docs)

            except Exception:
                continue

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150
    )

    documents = splitter.split_documents(docs)

    embedding = get_embedding()

    db = FAISS.from_documents(
        documents,
        embedding
    )

    db.save_local("vectorstore")