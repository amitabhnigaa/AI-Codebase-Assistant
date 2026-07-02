# 🤖 AI Codebase Assistant

<div align="center">

### AI-powered Repository Analysis using Gemini 2.5 Flash + RAG + FAISS

Analyze any GitHub repository or ZIP project, generate project summaries, architecture diagrams, security reviews, and chat with the codebase using Generative AI.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-red?style=for-the-badge)](https://ai-codebase-assistant-auxgljsrmwgncggieazmwu.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?style=for-the-badge&logo=streamlit)]()
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google)]()
[![LangChain](https://img.shields.io/badge/LangChain-RAG-success?style=for-the-badge)]()
[![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-green?style=for-the-badge)]()

</div>

---

# 🌐 Live Demo

🚀 **Try the application online**

**https://ai-codebase-assistant-auxgljsrmwgncggieazmwu.streamlit.app/**

---

# 📖 Overview

AI Codebase Assistant is an intelligent software engineering assistant that helps developers quickly understand unfamiliar codebases using Retrieval-Augmented Generation (RAG).

Instead of manually reading hundreds of source files, users can upload a ZIP repository or analyze a public GitHub repository. The application indexes the source code using semantic embeddings and enables natural language interaction with the project.

Beyond conversational code exploration, the assistant can automatically generate:

- 📋 Project Summary
- 🏗 Software Architecture
- 🔒 Security Review
- 💬 AI-powered Codebase Chat

The goal is to significantly reduce onboarding time for developers working with new projects.

---

# ✨ Features

## 🌐 Repository Analysis

- Analyze any public GitHub repository
- Upload ZIP repositories
- Automatic repository indexing

## 🤖 AI Assistant

- Chat with any codebase
- Context-aware responses
- Semantic code search

## 📊 Automated Documentation

- Generate project summaries
- Explain architecture
- Security review
- Source code retrieval

## ⚡ Performance

- FAISS Vector Database
- HuggingFace Embeddings
- Gemini 2.5 Flash
- Optimized retrieval pipeline

---
# 🏗 System Architecture

```mermaid
flowchart TD

    A[User]

    A --> B[Streamlit UI]

    B --> C{Repository Source}

    C -->|GitHub URL| D[Clone Repository]

    C -->|ZIP Upload| E[Extract Repository]

    D --> F[Vector Builder]
    E --> F

    F --> G[Chunk Source Code]

    G --> H[Generate Embeddings]

    H --> I[FAISS Vector Database]

    I --> J[Semantic Retriever]

    J --> K[Gemini 2.5 Flash]

    K --> L[Project Summary]

    K --> M[Architecture Analysis]

    K --> N[Security Review]

    K --> O[AI Chat Response]
```

---