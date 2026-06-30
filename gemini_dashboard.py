import streamlit as st
import json
import pandas as pd
from google import genai
from google.genai import types
from fpdf import FPDF

# 1. Setup Streamlit Page Layout
st.set_page_config(page_title="Enterprise AI Resume Intelligence", layout="wide")
st.title(" Enterprise AI Resume Intelligence Dashboard")
st.caption("Complete End-to-End Autonomous Talent Processing System")
import streamlit as st
import google.generativeai as genai

# 1. Safely pull key from Streamlit Cloud Secrets or local user input
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input(
        label="Gemini API Authorization",
        type="password",
        placeholder="Enter AI Studio API Key...",
        help="Paste your temporary Gemini API Key here to run the resume analysis workflow."
    )
 # 2. Restored Dynamic Gemini Client Configuration
import google.generativeai as genai

if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input(
        label="Gemini API Authorization",
        type="password",
        placeholder="AIzaSy...",
        help="Paste a free trial Gemini API Key here to run the live resume analysis layout."
    )

if api_key:
    genai.configure(api_key=api_key)
    
    class LegacyCompatibilityBridge:
        def generate_content(self, *args, **kwargs):
            kwargs.pop('model', None)
                        # Correctly flatten nested tuples/lists passed by your downstream analysis code
            passed_items = []
            for arg in args:
                if isinstance(arg, (list, tuple)):
                    passed_items.extend(list(arg))
                else:
                    passed_items.append(arg)

           
                
            cleaned_inputs = []
            for item in passed_items:
                if isinstance(item, dict) and "data" in item:
                    cleaned_inputs.append({"mime_type": "application/pdf", "data": item["data"]})
                elif hasattr(item, 'read'):
                    cleaned_inputs.append({"mime_type": "application/pdf", "data": item.read()})
                               else:
                    cleaned_inputs.append(item)

            try:
                active_model = genai.GenerativeModel("gemini-1.5-flash-latest")
                return active_model.generate_content(cleaned_inputs, **kwargs)
            except Exception as e:
                active_model = genai.GenerativeModel("models/gemini-1.5-flash")
                return active_model.generate_content(cleaned_inputs, **kwargs)

            client = LegacyCompatibilityBridge()
            model = client
else:
    st.sidebar.warning(" API Key Required: Please provide an active Gemini API key in the sidebar.")
    st.info(" Welcome! To test this portfolio app, please paste a temporary Gemini API Key in the sidebar input box.")
    st.stop()

    
# 3. Project Workflow Sidebar Controls
st.sidebar.header(" Project Workflow Setup")
st.sidebar.markdown("---")
st.sidebar.info(" **Step 1:** Select target profile.")
target_role = st.sidebar.text_input(" Target Job Role:", placeholder="e.g., Senior Data Analyst")

st.sidebar.markdown("---")
st.sidebar.info(" **Step 2:** Upload resume document.")
uploaded_file = st.sidebar.file_uploader(" Upload Resume:", type=["txt", "pdf"])

# Helper function to generate a truly complete PDF report block safely
def create_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Title Banner
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AUTONOMOUS CAREER EVALUATION REPORT", ln=True, align='C')
    pdf.ln(5)
    
    # Candidate Summary Box
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 8, "Candidate Name:", 0, 0)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, str(data.get('candidate_name', 'N/A')), ln=True)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 8, "Target Position:", 0, 0)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, str(data.get('target_role', 'N/A')), ln=True)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 8, "Readiness Score:", 0, 0)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"{data.get('readiness_score', 'N/A')}/100", ln=True)
    pdf.ln(5)
    
    # Section: Gaps
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Skill Gap Analysis", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, str(data.get('missing_skills', '')).replace('•', '-'))
    pdf.ln(5)
    
    # Section: Learning recommendations
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Course & Certification Recommendations", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, str(data.get('recommended_certs', '')).replace('•', '-'))
    pdf.ln(5)
    
    # Section: Generated Questions List
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Personalized Interview Preparation Matrix", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Technical Concept Questions --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("technical_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2) # Explicitly breaks line and forces next question downward
    pdf.ln(3)
        
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Project-Based Probes --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("project_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2) # Explicitly breaks line and forces next question downward
    pdf.ln(3)
        
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Case Scenario Challenges --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("scenario_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2) # Explicitly breaks line and forces next question downward
        
    return bytes(pdf.output(), encoding="utf-8")


# 4. Processing Engine Execution
if uploaded_file and target_role:
    with st.spinner(" Executing 8-Step Talent Evaluation Workflow... Please Wait..."):
        try:
            if uploaded_file.type == "application/pdf":
                resume_bytes = uploaded_file.read()
                file_part = types.Part.from_bytes(data=resume_bytes, mime_type="application/pdf")
            else:
                resume_text = uploaded_file.read().decode("utf-8")
                file_part = types.Part.from_text(text=resume_text)

            prompt = f"""
            You are an expert AI Executive Recruiter, Tech Lead, and ATS System.
            Analyze the attached resume against the target role: '{target_role}'.
            
            You MUST return your response as a single, valid JSON object containing exactly these text fields. Do not append any conversational filler outside the JSON.
            
            JSON Structure Requirements:
            {{
                "candidate_name": "Full name found in resume",
                "candidate_education": "Markdown bullet list of academic credentials",
                "current_skills": "Markdown bullet list of skills verified on the resume",
                "candidate_projects": "Markdown text summarizing existing projects",
                "candidate_experience": "Markdown text summarizing corporate history",
                "readiness_score": 75,
                "missing_skills": "Markdown list mapping technical tools missing for this role",
                "recommended_certs": "Markdown text detailing courses and credentials to fix the gap",
                "technical_questions": [
                    "Question 1", "Question 2", "Question 3", "Question 4", "Question 5",
                    "Question 6", "Question 7", "Question 8", "Question 9", "Question 10"
                ],
                "project_questions": [
                    "Question 1", "Question 2", "Question 3", "Question 4", "Question 5"
                ],
                "scenario_questions": [
                    "Question 1", "Question 2", "Question 3", "Question 4", "Question 5"
                ]
            }}
            
            Enforce exactly: 10 Technical Questions, 5 Project-based questions based on their resume projects, and 5 behavioral Scenario-based questions for the role.
            """
            file_bytes = uploaded_file.read()
            pdf_data_package = {
                "mime_type": "application/pdf",
                "data": file_bytes
            }
            response = model.generate_content([pdf_data_package, prompt])

           
          

            
            # Safely strip out markdown formatting fences if added by the LLM
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1)
            if raw_text.endswith("```"):
                raw_text = raw_text.rsplit("```", 1)[0]
            raw_text = raw_text.strip()

            # Decode JSON securely
            data_package = json.loads(raw_text)
            data_package["target_role"] = target_role
            
            score_val = data_package.get("readiness_score", 0)
            score_display = f"{score_val}/100"

            # ----------------- UI DISPLAY BLOCKS -----------------
            st.success(" Workflow Complete! All Intelligence Modules Generated Successfully.")

            # Metric Rows
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(" Candidate Profile Identification", data_package.get("candidate_name"))
            with m2:
                st.metric(" Current Readiness Score", score_display)
            with m3:
                st.metric(" Evaluated Job Matrix", target_role)

            st.markdown("---")

            # Main Grid Layout Split
            left_pane, right_pane = st.columns(2)

            with left_pane:
                st.subheader(" Candidate Profiles & Credentials")
                with st.expander(" Academic Qualifications", expanded=True):
                    st.markdown(data_package.get("candidate_education"))
                with st.expander(" Identified Structural Skills", expanded=True):
                    st.markdown(data_package.get("current_skills"))
                with st.expander(" Extracted Projects", expanded=False):
                    st.markdown(data_package.get("candidate_projects"))
                with st.expander(" Corporate Work History", expanded=False):
                    st.markdown(data_package.get("candidate_experience"))

            with right_pane:
                st.subheader(" Core Skill Gap & Recommendations")
                with st.expander(" Active Skill Gap Analysis", expanded=True):
                    st.markdown(data_package.get("missing_skills"))
                with st.expander(" Learning & Course Recommendations", expanded=True):
                    st.markdown(data_package.get("recommended_certs"))

            st.markdown("---")
            st.subheader(" Personalized Interview Question Generator Engine")
            
            q_tab1, q_tab2, q_tab3 = st.tabs([
                " Technical Concept Benchmarks (10 Questions)",
                " Project-Based Probes (5 Questions)",
                " Case Scenario Challenges (5 Questions)"
            ])

            with q_tab1:
                for idx, q in enumerate(data_package.get("technical_questions", []), 1):
                    st.markdown(f"**Q{idx}:** {q}")
            with q_tab2:
                for idx, q in enumerate(data_package.get("project_questions", []), 1):
                    st.markdown(f"**Q{idx}:** {q}")
            with q_tab3:
                for idx, q in enumerate(data_package.get("scenario_questions", []), 1):
                    st.markdown(f"**Q{idx}:** {q}")

            # ----------------- FIXED COMPLETE EXPORT PIPELINES -----------------
            st.sidebar.markdown("---")
            st.sidebar.header(" Export System Reports")
            
            # 1. Full Structural PDF Exporter
            try:
                pdf_bytes = create_pdf_report(data_package)   
                st.sidebar.download_button(
                    label=" Download Final PDF Report",
                    data=pdf_bytes,
                    file_name=f"{data_package.get('candidate_name', 'Candidate')}_Full_Analysis.pdf",
                    mime="application/pdf"
                )
            except Exception as pdf_err:
                st.sidebar.error(f"PDF compilation error: {pdf_err}")

            # 2. Comprehensive CSV Data Exporter
            all_questions = []
            # 2. Comprehensive CSV Data Exporter
            all_questions = []
            for q in data_package.get("technical_questions", []): 
                all_questions.append({"Section": "Technical", "Content/Question": q})
            for q in data_package.get("project_questions", []): 
                all_questions.append({"Section": "Project-Based", "Content/Question": q})
            for q in data_package.get("scenario_questions", []): 
                all_questions.append({"Section": "Scenario-Based", "Content/Question": q})
            
            if all_questions:
                questions_df = pd.DataFrame(all_questions)
                csv_data = questions_df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button(
                    label="Download Questions Spreadsheet (CSV)",
                    data=csv_data,
                    file_name=f"{data_package.get('candidate_name', 'Candidate')}_Metrics.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Execution Failure: {e}")
            st.info("Check data integrity schema or API availability parameters.")
else:
    st.info(" Complete steps 1 and 2 in the sidebar workflow pane to launch analysis.")
