from prompts import SUMMARY_PROMPT


def generate_project_summary():

    from llm import ask_gemini
    from retriever import get_retriever

    retriever = get_retriever()

    docs = retriever.retrieve(
        "Explain the complete project architecture and project overview.",
        k=10
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = SUMMARY_PROMPT.format(
        context=context
    )

    return ask_gemini(prompt)