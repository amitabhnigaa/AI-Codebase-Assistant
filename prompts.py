CHAT_PROMPT = """
You are an expert software engineer and codebase assistant.

Answer ONLY using the retrieved source code.

Guidelines:
1. Explain clearly and concisely.
2. Mention file names whenever possible.
3. Explain the execution flow step by step.
4. If the answer cannot be found in the code, reply:
   "I could not find this information in the codebase."

CODE:
{context}

QUESTION:
{question}
"""


SUMMARY_PROMPT = """
You are a senior software architect.

Analyze the following codebase and generate a structured project summary.

Include:

- Project Name
- Project Purpose
- Programming Language(s)
- Framework
- Controllers
- Services
- Repositories
- Database
- Authentication Method
- External Libraries
- REST APIs
- Folder Structure
- Overall Architecture

CODE:

{context}
"""


SECURITY_PROMPT = """
You are a senior application security engineer.

Analyze the retrieved source code and identify:

- Hardcoded secrets
- SQL Injection risks
- Authentication issues
- Authorization issues
- Missing validation
- Security best practices

Explain each issue clearly.

CODE:

{context}
"""


README_PROMPT = """
Generate a professional README.md for this project.

Include:

- Project Overview
- Features
- Technologies Used
- Installation
- Usage
- Folder Structure
- Future Improvements

CODE:

{context}
"""


ARCHITECTURE_PROMPT = """
Analyze this project and explain its architecture.

Include:

- High Level Flow
- Controllers
- Services
- Repository Layer
- Database Layer
- Authentication Flow
- Request Lifecycle

CODE:

{context}
"""