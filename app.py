import os
import shutil
import zipfile
import uuid
import streamlit as st

from project_info import get_project_info
from prompts import CHAT_PROMPT

# ---------------- Configuration ---------------- #

st.set_page_config(
    page_title="AI Codebase Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Custom Styling (CSS) ---------------- #

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Modern Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    
    /* KPI Card styling */
    .kpi-container {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .kpi-card {
        flex: 1;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9ca3af;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Custom Badges for Languages */
    .lang-badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
        border-radius: 20px;
        background: rgba(139, 92, 246, 0.12);
        color: #c084fc;
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.2s ease;
    }
    
    .lang-badge:hover {
        background: rgba(139, 92, 246, 0.25);
        color: #e9d5ff;
    }
    
    /* Welcome Banner */
    .welcome-banner {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-left: 5px solid #60a5fa;
        margin-bottom: 24px;
    }
    
    .welcome-banner h3 {
        margin-top: 0;
        color: #60a5fa;
        font-weight: 600;
    }
    
    /* Feature Action Cards in Reports Section */
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-top: 4px solid #60a5fa;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        height: 100%;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
        border-top-color: #a78bfa;
    }
    
    .feature-card h4 {
        margin-top: 0;
        color: #f3f4f6;
    }
    
    .feature-card p {
        font-size: 13px;
        color: #9ca3af;
        line-height: 1.5;
    }
    
    /* Adjust sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Chat message area refinements */
    div.stChatMessage {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 AI Codebase Assistant")

# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_ready" not in st.session_state:
    st.session_state.db_ready = False

if "project_name" not in st.session_state:
    st.session_state.project_name = ""

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "project_info" not in st.session_state:
    st.session_state.project_info = None

# Unique upload directory per user session to prevent concurrency issues
UPLOAD_DIR = os.path.join("uploaded_repos", st.session_state.session_id)

# ---------------- Sidebar Layout ---------------- #

with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0 10px 0;'>
            <h2 style='margin-bottom: 5px; color: #f3f4f6;'>Assistant</h2>
            <span style='font-size: 12px; color: #6b7280; font-weight: 500; letter-spacing: 0.05em;'>VERSION 2.0 • PREMIUM UX</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    st.subheader("🛠 AI Tech Stack")
    st.markdown(
        """
        <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px; margin-bottom: 20px;'>
            <div style='margin-bottom: 8px; font-size: 14px;'>🤖 <b>LLM:</b> Gemini 2.5 Flash</div>
            <div style='margin-bottom: 8px; font-size: 14px;'>🧠 <b>Embeddings:</b> MiniLM-L6-v2</div>
            <div style='font-size: 14px;'>💾 <b>Vector DB:</b> FAISS</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.session_state.project_name:
        st.markdown("### 📁 Active Repository")
        st.markdown(
            f"""
            <div style='background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 12px; font-weight: 600; text-align: center; margin-bottom: 20px; font-size: 14px;'>
                📂 {st.session_state.project_name}
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    
    if st.button("🗑 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------- Main Navigation ---------------- #

tab1, tab2, tab3 = st.tabs([
    "🌐 Codebase Dashboard", 
    "📊 Reports & Insights", 
    "💬 AI Codebase Chat"
])

# ==================== TAB 1: CODEBASE DASHBOARD ====================
with tab1:
    if st.session_state.db_ready:
        st.markdown("## 📊 Active Codebase Health")
        
        # Display Stats via KPIs
        info = st.session_state.project_info or {"files": 0, "languages": []}
        
        col_kpi1, col_kpi2 = st.columns(2)
        with col_kpi1:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Active Project</div>
                    <div class='kpi-value' style='font-size: 24px; padding-top: 6px;'>{st.session_state.project_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_kpi2:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Indexed Files</div>
                    <div class='kpi-value'>{info.get("files", 0)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛠 Detected Languages")
        
        languages = info.get("languages", [])
        if languages:
            badges_html = "".join([f"<span class='lang-badge'>{lang}</span>" for lang in languages])
            st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No supported programming languages detected in the project root directory.")
            
        st.markdown("---")
        
        # Option to swap repository
        with st.expander("🔄 Connect Another Codebase"):
            col_git, col_zip = st.columns(2)
            
            with col_git:
                st.markdown("### 🌐 Import from GitHub")
                github_url = st.text_input(
                    "GitHub Repository URL",
                    placeholder="https://github.com/user/repository",
                    key="github_url_reimport"
                )
                if st.button("Clone & Index Repo", key="btn_git_reimport", use_container_width=True):
                    if github_url.strip() == "":
                        st.warning("Please enter a GitHub repository URL.")
                    else:
                        try:
                            from github_clone import clone_repository
                            from vector_builder import build_vector_db
                            with st.spinner("Cloning repository..."):
                                repo_path = clone_repository(github_url)
                            with st.spinner("Building vector database..."):
                                build_vector_db(repo_path)
                            with st.spinner("Retrieving project details..."):
                                project_info = get_project_info(repo_path)
                                st.session_state["project_info"] = project_info
                                st.session_state.project_name = github_url.rstrip("/").split("/")[-1]
                                st.session_state.db_ready = True
                            st.success("🎉 Repository re-indexed successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                            
            with col_zip:
                st.markdown("### 📁 Upload ZIP File")
                uploaded_file = st.file_uploader(
                    "Upload Codebase (.zip)",
                    type=["zip"],
                    key="zip_uploader_reimport"
                )
                if uploaded_file:
                    with st.spinner("Processing ZIP and building index..."):
                        if os.path.exists(UPLOAD_DIR):
                            shutil.rmtree(UPLOAD_DIR)
                        os.makedirs(UPLOAD_DIR, exist_ok=True)

                        zip_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(zip_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        extract_path = os.path.join(UPLOAD_DIR, "extracted_code")
                        os.makedirs(extract_path, exist_ok=True)

                        with zipfile.ZipFile(zip_path, "r") as zip_ref:
                            for member in zip_ref.infolist():
                                target_path = os.path.abspath(os.path.join(extract_path, member.filename))
                                if target_path.startswith(os.path.abspath(extract_path)):
                                    zip_ref.extract(member, extract_path)

                        from vector_builder import build_vector_db
                        build_vector_db(extract_path)
                        st.session_state.db_ready = True
                        st.session_state.project_name = uploaded_file.name.replace(".zip", "")
                        st.session_state.last_uploaded = uploaded_file.name
                        st.session_state["project_info"] = get_project_info(extract_path)
                    st.success("🎉 Repository re-indexed successfully!")
                    st.rerun()
    else:
        st.markdown(
            """
            <div class='welcome-banner'>
                <h3>👋 Welcome to the AI Codebase Assistant!</h3>
                Provide a GitHub repository link or upload a zipped codebase below. The assistant will parse 
                your files, build vector embeddings locally via FAISS, and set up an intelligent chatbot and automated report environment.
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_git, col_zip = st.columns(2)
        
        with col_git:
            st.markdown("### 🌐 Import from GitHub")
            github_url = st.text_input(
                "GitHub Repository URL",
                placeholder="https://github.com/user/repository",
                key="github_url_first"
            )
            if st.button("Clone & Index Repository", key="btn_git_first", use_container_width=True):
                if github_url.strip() == "":
                    st.warning("Please enter a GitHub repository URL.")
                else:
                    try:
                        from github_clone import clone_repository
                        from vector_builder import build_vector_db
                        
                        with st.spinner("Step 1/3: Cloning repository..."):
                            repo_path = clone_repository(github_url)
                        st.success("✅ Repository cloned")

                        with st.spinner("Step 2/3: Building vector database..."):
                            build_vector_db(repo_path)
                        st.success("✅ Vector database created")

                        with st.spinner("Step 3/3: Loading project details..."):
                            project_info = get_project_info(repo_path)
                            st.session_state["project_info"] = project_info
                            st.session_state.project_name = github_url.rstrip("/").split("/")[-1]
                            st.session_state.db_ready = True
                        st.success("🎉 Codebase ready!")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                        
        with col_zip:
            st.markdown("### 📁 Upload ZIP File")
            uploaded_file = st.file_uploader(
                "Upload Repository (.zip)",
                type=["zip"],
                key="zip_uploader_first"
            )
            if uploaded_file:
                with st.spinner("Extracting and building knowledge base..."):
                    if os.path.exists(UPLOAD_DIR):
                        shutil.rmtree(UPLOAD_DIR)
                    os.makedirs(UPLOAD_DIR, exist_ok=True)

                    zip_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(zip_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    extract_path = os.path.join(UPLOAD_DIR, "extracted_code")
                    os.makedirs(extract_path, exist_ok=True)

                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        for member in zip_ref.infolist():
                            target_path = os.path.abspath(os.path.join(extract_path, member.filename))
                            if target_path.startswith(os.path.abspath(extract_path)):
                                zip_ref.extract(member, extract_path)

                    from vector_builder import build_vector_db
                    build_vector_db(extract_path)
                    st.session_state.db_ready = True
                    st.session_state.project_name = uploaded_file.name.replace(".zip", "")
                    st.session_state.last_uploaded = uploaded_file.name
                    st.session_state["project_info"] = get_project_info(extract_path)
                st.success("🎉 Codebase indexed successfully!")
                st.rerun()

# ==================== TAB 2: REPORTS & INSIGHTS ====================
with tab2:
    if not st.session_state.db_ready:
        st.info("📂 No active codebase loaded. Please import or upload a repository in the **Codebase Dashboard** tab first.")
    else:
        st.markdown("## 📊 Codebase Insight Generators")
        st.write("Extract structural architecture, security diagnostics, and code overviews using Gemini AI.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_rep1, col_rep2, col_rep3 = st.columns(3)
        
        with col_rep1:
            st.markdown(
                """
                <div class='feature-card' style='border-top-color: #60a5fa;'>
                    <h4>📋 Project Summary</h4>
                    <p>Construct a structured overview of the application purpose, tech stacks, framework layouts, and APIs.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Generate Summary", key="run_summary", use_container_width=True):
                with st.spinner("Analyzing codebase files for summary..."):
                    try:
                        from project_summary import generate_project_summary
                        st.session_state["summary"] = generate_project_summary()
                    except Exception as e:
                        st.error(f"Summary Error: {str(e)}")
                        
        with col_rep2:
            st.markdown(
                """
                <div class='feature-card' style='border-top-color: #8b5cf6;'>
                    <h4>🏗 Architecture Review</h4>
                    <p>Map high-level code interactions, backend services, controller lifecycle mappings, and databases.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Generate Architecture", key="run_arch", use_container_width=True):
                with st.spinner("Analyzing request flow and layers..."):
                    try:
                        from architecture import generate_architecture
                        st.session_state["architecture"] = generate_architecture()
                    except Exception as e:
                        st.error(f"Architecture Error: {str(e)}")
                        
        with col_rep3:
            st.markdown(
                """
                <div class='feature-card' style='border-top-color: #10b981;'>
                    <h4>🔒 Security Audit</h4>
                    <p>Examine files for hardcoded environment keys, sanitization limits, input safety, and authentication logic.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Run Security Review", key="run_security", use_container_width=True):
                with st.spinner("Auditing codebase vulnerabilities..."):
                    try:
                        from security import security_review
                        st.session_state["security"] = security_review()
                    except Exception as e:
                        st.error(f"Security Audit Error: {str(e)}")

        st.markdown("---")
        
        # Display Report Results in beautiful expanders
        if "summary" in st.session_state:
            with st.expander("📋 Project Summary Details", expanded=True):
                st.markdown(st.session_state["summary"])
                
        if "architecture" in st.session_state:
            with st.expander("🏗 Architecture & Request Flows", expanded=True):
                st.markdown(st.session_state["architecture"])
                
        if "security" in st.session_state:
            with st.expander("🔒 Codebase Security Diagnostics", expanded=True):
                st.markdown(st.session_state["security"])

# ==================== TAB 3: CODEBASE CHAT ====================
with tab3:
    if not st.session_state.db_ready:
        st.info("📂 No active codebase loaded. Please import or upload a repository in the **Codebase Dashboard** tab first.")
    else:
        st.markdown("## 💬 Interact with your Repository")
        st.write("Ask queries about functions, design configurations, or bugs. Answers are supported by retrieved code blocks.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Render Chat History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if "sources" in msg and msg["sources"]:
                    with st.expander("🔍 Referenced Source Code"):
                        for src in msg["sources"]:
                            st.markdown(f"📄 **{src['file']}**")
                            _, ext = os.path.splitext(src['file'])
                            lang = ext.replace(".", "") if ext else "python"
                            st.code(src["content"], language=lang)
        
        # Input block
        question = st.chat_input("Ask a question about your codebase...")
        
        if question:
            # Render user query instantly
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.write(question)
                
            # Response flow
            with st.chat_message("assistant"):
                with st.spinner("Retrieving codebase snippets..."):
                    from retriever import get_retriever
                    retriever = get_retriever()
                    docs = retriever.retrieve(question, k=3)
                    
                    context = "\n\n".join([doc.page_content for doc in docs])
                    prompt = CHAT_PROMPT.format(context=context, question=question)
                    
                with st.spinner("Formulating AI response..."):
                    try:
                        from llm import ask_gemini
                        answer = ask_gemini(prompt)
                        st.write(answer)
                        
                        # Process sources
                        sources = []
                        for doc in docs:
                            src_path = doc.metadata.get("source", "Unknown File")
                            sources.append({
                                "file": os.path.basename(src_path),
                                "content": doc.page_content
                            })
                            
                        # Save response to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                        
                        # Render inline expander immediately
                        with st.expander("🔍 Referenced Source Code"):
                            for src in sources:
                                st.markdown(f"📄 **{src['file']}**")
                                _, ext = os.path.splitext(src['file'])
                                lang = ext.replace(".", "") if ext else "python"
                                st.code(src["content"], language=lang)
                                
                    except Exception as e:
                        error_msg = f"Gemini Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})