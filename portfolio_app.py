import streamlit as st

# -------------------------------------------------------------
# 1. PAGE INITIALIZATION (CLEAN CORPORATE LAYOUT)
# -------------------------------------------------------------
st.set_page_config(
    page_title="NANDHINI | Data Analyst",
    page_icon=":material/badge:",
    layout="centered", # Centered format matches classic web pages perfectly
    initial_sidebar_state="expanded"
)

# Custom text color tweaks to make headers pop cleanly over the cream backdrop
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #1e3a2f !important; /* Elegant deep green-slate for text headers */
    }
    div[data-testid="stVScrollBlock"] > div {
        background-color: #ffffff !important; /* Crisp white content boxes */
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. ACCESS GATEWAY CONTROL (LOGIN PANEL)
# -------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

CORRECT_USERNAME = "Nandhini"
CORRECT_PASSWORD = "Password123"

if not st.session_state["logged_in"]:
    st.markdown("##  Secure Portfolio Gateway")
    st.write("Welcome. This analytics portal is private. Enter authorization keys to proceed.")
    username_input = st.text_input("Username Handle", placeholder="Enter username")
    password_input = st.text_input("Access Key", type="password", placeholder="Enter password")
    if st.button("Verify Credentials"):
        if username_input == CORRECT_USERNAME and password_input == CORRECT_PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Authentication failed. Access Denied.")

# -------------------------------------------------------------
# 3. UNLOCKED PORTFOLIO MAIN INTERFACE
# -------------------------------------------------------------
else:
    # Forest Green Sidebar Deck Configuration
    st.sidebar.markdown("<h3 style='color:white;'>Navigation Menu</h3>", unsafe_allow_html=True)
    menu_selection = st.sidebar.radio(
        "Select Page View:",
        ["Home Matrix", "Core Academic Vector", "Analytics Repositories"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Out and Lock"):
        st.session_state["logged_in"] = False
        st.rerun()

    # -------------------------------------------------------------
    # PAGE 1: HOME MATRIX (ELEGANT HEADER LAYOUT)
    # -------------------------------------------------------------
    if menu_selection == "Home Matrix":
        # Upper Main Title Panel
        st.title("[NANDHINI]")
        st.write("**Data Science & Analytics Intern**")
        st.write("*Postgraduate Candidate | Expected Graduation: 2028*")
        st.write("gmail: nandhinikarunagaran63@gmail.com |  linkedin:https://www.linkedin.com/in/nandhini-karunagaran-81944631a?utm_source=share_via&utm_content=profile&utm_medium=member_android |  GitHub")
        st.markdown("---")

        # Two columns matching the image layout: Green Welcome banner left, Photo right
        col_banner, col_photo = st.columns([2, 1])
        
        with col_banner:
            # We use an HTML block to make a solid corporate background box
            st.markdown(
                "<div style='background-color: #1e3a2f; padding: 30px; border-radius: 6px; color: white;'>"
                "<h2 style='color: white; margin-top:0;'>Welcome.</h2>"
                "<p style='font-size: 16px; line-height: 1.6;'>"
                "I am deeply passionate about solving challenging analytical problems, cleaning complex datasets, "
                "and building predictive data frameworks that translate raw metrics into operational business intelligence."
                "</p>"
                "</div>",
                unsafe_allow_html=True
            )

        with col_photo:
            try:
                # Direct public test image string 
                st.image("https://ibb.co", use_container_width=True)
            except Exception as e:
                st.error("Image loading failed.")

        st.markdown("### Personal Registry Details")
        with st.container():
            st.write("**Current Role:** Corporate Data Science Intern")
            st.write("**Geographic Location Node:** Chennai, Tamil Nadu, India")
            st.write("**Primary Focus Areas:**(Resume parsing, Skill Gaps, Readiness Score, and Interview Questions ")

    # -------------------------------------------------------------
    # PAGE 2: CORE ACADEMIC VECTOR
    # -------------------------------------------------------------
    elif menu_selection == "Core Academic Vector":
        st.title("Education & Core Qualifications")
        st.markdown("---")
        
        with st.container():
            st.markdown("###  University Framework")
            st.subheader("M.sc Computational Statistics and Data Analytics")
            st.write("**Institution Grid Location:** [VELLORE INSTITUTE OF TECHNOLOGY]")
            st.write("**Timeline Lifespan:** 2023 - 2028")
            st.write("**Evaluated Performance Metric:** [CGPA 8.7]")

        with st.container():
            st.markdown("### Programmed Knowledge Architectures")
            
            st.write("**1. Data Cleaning & Automation (Python)**")
            st.caption("Writing clean scripts to automatically format, clean, and process large data files.")
            
            st.write("**2. Database Management & Queries (SQL)**")
            st.caption("Designing clear data tables and writing fast queries to combine and filter business information.")
            
            st.write("**3. Statistical Analysis & Visualization (R Language)**")
            st.caption("Analyzing data distributions, tracking patterns, and creating charts to find business trends.")

       # -------------------------------------------------------------
    # PAGE 3: ANALYTICS REPOSITORIES (INTERACTIVE FOLDER LAYOUT)
    # -------------------------------------------------------------
    elif menu_selection == "Analytics Repositories":
        st.title("Project Workloads & Repositories")
        st.write("Click on a project folder below to open its dashboard, inputs, and outputs.")
        st.markdown("---")
        
        #  FOLDER 1: AI RESUME ANALYZER
        # st.expander acts exactly like a clickable folder that opens up when clicked!
        with st.expander(" Folder: Local AI Resume Analyzer & Interview Generator", expanded=False):
            st.markdown("###  Local AI Resume Analyzer & Interview Generator")
            st.write("**Role Context:** Data Science Intern")
            st.write("**Tools Used:** Python, Streamlit, NLP, Ollama (Local LLM)")
            st.markdown("---")
            
            # Create interactive tabs inside the folder
            tab_summary, tab_inputs, tab_outputs = st.tabs([
                " Project Dashboard & Summary", 
                " Inputs Required", 
                " Outputs Generated"
            ])
            
            # TAB 1: SUMMARY
            with tab_summary:
                st.markdown("####  Live Application Endpoint")
                st.write("Click the button below to launch the live, fully operational AI application in a new window:")
                
                # High-visibility action button that links directly to your deployed dashboard
                st.link_button(
                    label="🔗 Launch Live AI Resume Dashboard", 
                    url="https://streamlit.app", # Replace with your real deployed app link later!
                    type="primary"
                )
                st.markdown("---")
                
                st.markdown("#### Project Workflow Logic")
                st.code(
                    "PROJECT_WORKFLOW = {\n"
                    "    '1. Resume Reading': 'Uses Python and NLP to scan and extract skills from uploaded PDF resumes',\n"
                    "    '2. Skill Gap Finder': 'Compares candidate skills with job descriptions to find missing keywords',\n"
                    "    '3. Readiness Score': 'Calculates a clear matching score showing how prepared the candidate is',\n"
                    "    '4. Local LLM Questions': 'Uses Ollama to securely generate custom interview practice questions locally'\n"
                    "}", language="python"
                )

                st.write("**Project Impact:** Built a completely private, localized AI web application using Streamlit that reviews resumes and generates smart prep questions without uploading data to the cloud.")
            
            # TAB 2: INPUTS REQUIRED
            with tab_inputs:
                st.markdown("#### Expected System Inputs")
                st.write("The application processes the following entry vectors from the user:")
                st.info(" **1. Candidate Resume File:** Uploaded in standard PDF format via the interface.")
                st.info(" **2. Target Job Description:** Copied plain text mapping desired skills and experience.")
                st.info(" **3. Core Model Selection:** Dropdown choosing local Ollama models (e.g., Llama3, Mistral).")
            
            # TAB 3: OUTPUTS GENERATED
            with tab_outputs:
                st.markdown("#### Live System Outputs Generated")
                st.write("The pipeline outputs clear metrics and documents for the evaluator:")
                st.success(" **Readiness Score:** A quantitative percentage matching score generated by the scoring rules.")
                st.success(" **Skill Gap Summary:** A visual list highlighting exact technical skills missing from the resume.")
                st.success(" **Interview Prep Sheet:** 20 context-aware technical, project, and behavioral questions built locally.")

        #  FOLDER 2: PLACEHOLDER FOR ANOTHER PROJECT (To show multiple folders)
        with st.expander(" Folder: Future Data Analytics Project / Capstone", expanded=False):
            st.markdown("###  Second Academic / Internship Project")
            st.write("This folder is reserved for your next project deployment.")
            st.info("You can easily copy the template structure above to display inputs and outputs for your other projects here!")

