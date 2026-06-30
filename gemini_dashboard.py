import streamlit as st
import json
import base64
import google.genai as genai
from google.genai import types
from fpdf import FPDF

# 1. Setup Streamlit Page Layout
st.set_page_config(page_title="Enterprise AI Resume Intelligence", layout="wide")
st.title(" Enterprise AI Resume Intelligence Dashboard")
st.caption("Complete End-to-End Autonomous Talent Processing System")

# 2. Secure Direct Endpoint Route Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

# 3. Project Workflow Sidebar Controls
st.sidebar.header(" Project Workflow Setup")
st.sidebar.markdown("---")
st.sidebar.info(" **Step 1:** Select target profile.")
target_role = st.sidebar.text_input(" Target Job Role:", placeholder="e.g., Senior Data Analyst")

st.sidebar.markdown("---")
st.sidebar.info(" **Step 2:** Upload resume document.")
uploaded_file = st.sidebar.file_uploader(" Upload Resume:", type=["pdf"])

# Helper function to generate a truly complete PDF report block safely
def create_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AUTONOMOUS CAREER EVALUATION REPORT", ln=True, align='C')
    pdf.ln(5)
    
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
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Skill Gap Analysis", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, str(data.get('missing_skills', '')).replace('•', '-'))
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Course & Certification Recommendations", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, str(data.get('recommended_certs', '')).replace('•', '-'))
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Personalized Interview Preparation Matrix", ln=True)
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

# 4. Processing Engine Execution
if not api_key:
    st.sidebar.warning("⚠️ Streamlit Secrets Vault Setup Missing: Please ensure GEMINI_API_KEY is defined in your cloud settings panel.")
    st.stop()

if uploaded_file and target_role:
    with st.spinner(" Executing Deep Talent Evaluation Workflow... Please Wait..."):
        try:
            # Initialize the modern official GenAI client using our secure vault key token
            client = genai.Client(api_key=api_key)
            
            pdf_bytes = uploaded_file.read()

            prompt = f"Analyze this resume against target job role: '{target_role}'."
            
            # Request content using structural type constraints to guarantee clean text handling
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "candidate_name": types.Schema(type=types.Type.STRING),
                            "target_role": types.Schema(type=types.Type.STRING),
                            "readiness_score": types.Schema(type=types.Type.INTEGER),
                            "missing_skills": types.Schema(type=types.Type.STRING),
                            "recommended_certs": types.Schema(type=types.Type.STRING),
                            "technical_questions": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                            "project_questions": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                            "scenario_questions": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                        },
                        required=["candidate_name", "target_role", "readiness_score", "missing_skills", "recommended_certs", "technical_questions", "project_questions", "scenario_questions"]
                    )
                )
            )
            
            parsed_json = json.loads(response.text)
            st.success("🎉 Analysis Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="👤 Candidate Profile Name", value=parsed_json.get('candidate_name', 'Applicant'))
            with col2:
                st.metric(label="🎯 Role Readiness Score", value=f"{parsed_json.get('readiness_score', 75)}/100")
            
            st.markdown("---")
            st.subheader("📋 Target Job Position")
            st.write(parsed_json.get('target_role', target_role))
            
            st.subheader("🔍 Detailed Skill Gap Analysis")
            st.write(parsed_json.get('missing_skills', ''))
            
            st.subheader("🎓 Recommended Courses & Certifications")
            st.write(parsed_json.get('recommended_certs', ''))
            
            st.markdown("---")
            st.subheader("💡 Personalized Interview Preparation Matrix")
            
            st.markdown("### 🛠️ Technical Concept Questions (10 Total)")
            for idx, q in enumerate(parsed_json.get("technical_questions", []), 1):
                st.write(f"**Question {idx}:** {q}")
                
            st.markdown("### 💻 Project-Based Probes (5 Total)")
            for idx, q in enumerate(parsed_json.get("project_questions", []), 1):
                st.write(f"**Question {idx}:** {q}")
                
            st.markdown("### 📊 Case Scenario Challenges (5 Total)")
            for idx, q in enumerate(parsed_json.get("scenario_questions", []), 1):
                st.write(f"**Question {idx}:** {q}")
            
            try:
                final_pdf_bytes = create_pdf_report(parsed_json)
                st.sidebar.markdown("---")
                st.sidebar.download_button(
                    label="📥 Download Final PDF Report",
                    data=final_pdf_bytes,
                    file_name=f"{parsed_json.get('candidate_name', 'Candidate')}_Full_Analysis.pdf",
                    mime="application/pdf"
                )
            except Exception as pdf_err:
                st.sidebar.error(f"PDF compilation error: {pdf_err}")
                
        except Exception as e:
            st.error(f"Execution Failure: {e}")
