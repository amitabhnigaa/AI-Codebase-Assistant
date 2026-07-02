from prompts import SECURITY_PROMPT


def security_review():

    from llm import ask_gemini
    from retriever import get_retriever

    retriever = get_retriever()

    docs = retriever.retrieve(
        "Analyze the project for security vulnerabilities.",
        k=10
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = SECURITY_PROMPT.format(
        context=context
    )

    return ask_gemini(prompt)