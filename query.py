from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import ollama

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embedding,
    allow_dangerous_deserialization=True
)

while True:

    question = input("Ask: ")

    docs = db.similarity_search(
        question,
        k=1
    )

    context = ""

    for doc in docs:
        context += doc.page_content

    prompt = f"""
    Code:

    {context}

    Question:
    {question}

    Explain clearly.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\n")
    print(response["message"]["content"])
    print("\n")