import streamlit as st
import json
import pandas as pd
import ollama
from fpdf import FPDF
from pypdf import PdfReader

# 1. Setup Streamlit Page Layout
st.set_page_config(page_title="Local AI Resume Intelligence", layout="wide", page_icon=":material/analytics:")
st.title(":material/lock: 100% Offline Local AI Resume Dashboard")
st.caption("All data is processed strictly on your computer using a Local Llama 3 Model.")

# 2. Project Workflow Sidebar Controls
st.sidebar.header(":material/build: Local Workflow Setup")
st.sidebar.markdown("---")
st.sidebar.info(":material/arrow_right: **Step 1:** Select target profile.")
target_role = st.sidebar.text_input("Target Job Role:", placeholder="e.g., Data Analyst")

st.sidebar.markdown("---")
st.sidebar.info(":material/arrow_right: **Step 2:** Upload resume document.")
uploaded_file = st.sidebar.file_uploader("Upload Resume:", type=["txt", "pdf", "csv"])

# Helper function to generate a truly complete PDF report block safely
def create_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Title Banner
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "OFFLINE CAREER EVALUATION REPORT", ln=True, align='C')
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
    
    # Section: FIXED - Generating Interview Questions Inside PDF Matrix Block
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Generated Interview Preparation Matrix", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Technical Concept Questions --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("technical_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2)
    pdf.ln(3)
        
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Project-Based Probes --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("project_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2)
    pdf.ln(3)
        
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "-- Case Scenario Challenges --", ln=True)
    pdf.set_font("Arial", "", 10)
    for idx, q in enumerate(data.get("scenario_questions", []), 1):
        pdf.multi_cell(190, 5, f"Q{idx}: {q}")
        pdf.ln(2)
        
    return bytes(pdf.output())

# 3. Processing Engine Execution
if uploaded_file and target_role:
    with st.spinner(":material/sync: Local Llama 3 is reading and analyzing the resume offline... Please wait..."):
        try:
            # Accurate local text decoding block
            if uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                parsed_pages = []
                for page in reader.pages:
                    text_content = page.extract_text()
                    if text_content:
                        parsed_pages.append(text_content)
                resume_text = "\n".join(parsed_pages)
            elif uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                resume_text = df.to_string()
            else:
                resume_text = uploaded_file.read().decode("utf-8")

            # PASS 1: Extract Core Profile and Analytics (No huge question generation loads)
            prompt_analysis = f"""
            Analyze this resume text completely against the target role: '{target_role}'.
            Return a valid JSON object with exactly these fields:
            {{
                "candidate_name": "Full name found in resume",
                "candidate_education": "Academic credentials summary list",
                "current_skills": "Skills verified on the resume list",
                "candidate_projects": "Projects summary text",
                "candidate_experience": "Corporate work history summary text",
                "readiness_score": 75,
                "missing_skills": "List mapping technical tools missing for this role",
                "recommended_certs": "Courses and credentials to fix the gap"
            }}
            Resume content:
            {resume_text}
            """

            response_analysis = ollama.generate(model='llama3', prompt=prompt_analysis, format='json')
            data_package = json.loads(response_analysis['response'].strip())
            data_package["target_role"] = target_role

            # PASS 2: Separate lightning-fast background loops to generate the required question counts safely
            prompt_q = f"Based on this target position: '{target_role}', generate a JSON list of exactly 10 technical concept interview questions. Structure your reply exactly like this: {{\"questions\": [\"q1\", \"q2\", \"q3\", \"q4\", \"q5\", \"q6\", \"q7\", \"q8\", \"q9\", \"q10\"]}}"
            resp_tech = ollama.generate(model='llama3', prompt=prompt_q, format='json')
            data_package["technical_questions"] = json.loads(resp_tech['response'].strip()).get("questions", [])

            prompt_p = f"Based on these resume projects: {data_package.get('candidate_projects')}, generate a JSON list of exactly 5 project-based interview questions. Structure exactly like: {{\"questions\": [\"q1\", \"q2\", \"q3\", \"q4\", \"q5\"]}}"
            resp_proj = ollama.generate(model='llama3', prompt=prompt_p, format='json')
            data_package["project_questions"] = json.loads(resp_proj['response'].strip()).get("questions", [])

            prompt_s = f"Based on this role: '{target_role}', generate a JSON list of exactly 5 situational scenario interview questions. Structure exactly like: {{\"questions\": [\"q1\", \"q2\", \"q3\", \"q4\", \"q5\"]}}"
            resp_scen = ollama.generate(model='llama3', prompt=prompt_s, format='json')
            data_package["scenario_questions"] = json.loads(resp_scen['response'].strip()).get("questions", [])

            score_val = data_package.get("readiness_score", 0)
            score_display = f"{score_val}/100"

            # ----------------- UI DISPLAY BLOCKS -----------------
            st.success(":material/check_circle: Offline Analysis & Extraction Complete!")

            # Metric Rows
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(":material/person: Candidate Profile", data_package.get("candidate_name", "Unknown"))
            with m2:
                st.metric(":material/trending_up: Current Readiness Score", score_display)
            with m3:
                st.metric(":material/track_changes: Evaluated Job Matrix", target_role)

            st.markdown("---")

            # Main Grid Layout Split
            left_pane, right_pane = st.columns(2)

            # --- LEFT PANE: HORIZONTAL FOLDER TABS ---
            with left_pane:
                st.subheader(":material/assignment: Candidate Profiles & Credentials")
                
                # Creating 4 clean horizontal folder tabs
                tab_edu, tab_skills, tab_proj, tab_exp = st.tabs([
                    "Education", "Structural Skills", "Extracted Projects", "Work History"
                ])
                
                with tab_edu:
                    st.markdown(data_package.get("candidate_education"))
                with tab_skills:
                    st.markdown(data_package.get("current_skills"))
                with tab_proj:
                    st.markdown(data_package.get("candidate_projects"))
                with tab_exp:
                    st.markdown(data_package.get("candidate_experience"))

            # --- RIGHT PANE: HORIZONTAL FOLDER TABS (FIXED UNDERSCORE ERROR) ---
            with right_pane:
                st.subheader(":material/psychology: AI Analysis & Interview Prep")
                
                # Creating 3 clean horizontal folder tabs to fix the vertical text issues
                tab_gaps, tab_certs, tab_prep = st.tabs([
                    "Skill Gaps", "Recommended Courses", "Interview Questions"
                ])
                
                with tab_gaps:
                    st.markdown(data_package.get("missing_skills"))
                with tab_certs:
                    st.markdown(data_package.get("recommended_certs"))
                with tab_prep:
                    st.markdown("#### Technical Concept Questions")
                    for q in data_package.get("technical_questions", []):
                        st.write(f"- {q}")
                    st.markdown("#### Project Probes")
                    for q in data_package.get("project_questions", []):
                        st.write(f"- {q}")
                    st.markdown("#### Situational Scenario Challenges")
                    for q in data_package.get("scenario_questions", []):
                        st.write(f"- {q}")

            # Export Block
            pdf_bytes = create_pdf_report(data_package)
            st.sidebar.markdown("---")
            # Export Options Block
            st.sidebar.markdown("### :material/download: Export Options")
            st.sidebar.download_button(
                label="Download Analysis Report (PDF)",
                data=pdf_bytes,
                file_name=f"Career_Evaluation_{target_role.replace(' ', '_')}.pdf",
                mime="application/pdf",
                icon=":material/picture_as_pdf:"
            )

        except Exception as e:
            st.error(f"Error during processing: {str(e)}")

else:
    st.info(":material/info: Please enter a Target Job Role and upload a Resume document in the sidebar to run the evaluation engine.")
