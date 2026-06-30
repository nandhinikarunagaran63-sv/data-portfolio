import streamlit as st
import json
import base64
import requests
from fpdf import FPDF

# 1. Setup Streamlit Page Layout
st.set_page_config(page_title="Enterprise AI Resume Intelligence", layout="wide")
st.title(" Enterprise AI Resume Intelligence Dashboard")
st.caption("Complete End-to-End Autonomous Talent Processing System")

# 2. Secure Direct Endpoint Route Setup
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input(
        label="Gemini API Authorization",
        type="password",
        placeholder="Enter your Gemini API key (AIzaSy...)"
    )

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
    st.sidebar.warning("⚠️ API Key Required: Please provide an active Gemini API key in the sidebar.")
    st.info("👋 Welcome! To test this portfolio app, please paste a temporary Gemini API Key in the sidebar input box.")
    st.stop()

if uploaded_file and target_role:
    with st.spinner(" Executing Deep Talent Evaluation Workflow... Please Wait..."):
        try:
            pdf_bytes = uploaded_file.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

            prompt = f"""
            You are an expert AI Executive Recruiter and Technical Lead.
            Analyze the attached resume completely against the target job role: '{target_role}'.
            
            You MUST return a single, valid JSON object containing exactly these fields populated with rich detailed text parsed from the resume context:
            {{
                "candidate_name": "Extract the actual full name of the candidate found in the resume document",
                "target_role": "{target_role}",
                "readiness_score": 85,
                "missing_skills": "Write a highly comprehensive bulleted analysis of specific skills gaps and tools missing compared to the role criteria",
                "recommended_certs": "Recommend explicit professional courses and certifications to fill those exact learning gaps",
                "technical_questions": [Provide a list of EXACTLY 10 distinct, deep technical interview questions based on their gaps],
                "project_questions": [Provide a list of EXACTLY 5 structural, architecture-focused project evaluation questions],
                "scenario_questions": [Provide a list of EXACTLY 5 complex situational or case study assessment questions]
            }}
            """
            
            # The correct un-truncated endpoint string concatenation construction layout
            part_a = "https://googleapis.com"
            part_b = "/v1beta/models/gemini-1.5-flash:generateContent?key="
            api_url = part_a + part_b + str(api_key)
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [
                        {"inlineData": {"mimeType": "application/pdf", "data": base64_pdf}},
                        {"text": prompt}
                    ]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            
            web_response = requests.post(api_url, headers=headers, json=payload)
            response_json = web_response.json()
            
            if "candidates" in response_json:
                raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
                parsed_json = json.loads(raw_text)
            else:
                st.error(f"API Error Response: {response_json}")
                st.stop()
            
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
