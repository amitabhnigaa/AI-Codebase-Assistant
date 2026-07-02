from prompts import ARCHITECTURE_PROMPT


def generate_architecture():

    from llm import ask_gemini
    from retriever import get_retriever

    retriever = get_retriever()

    docs = retriever.retrieve(
        "Explain the complete architecture of this project.",
        k=10
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = ARCHITECTURE_PROMPT.format(
        context=context
    )

    return ask_gemini(prompt)