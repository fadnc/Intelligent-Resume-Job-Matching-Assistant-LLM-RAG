import streamlit as st
import requests

st.title("Resume Job Matcher")

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd = st.text_area("Paste Job Description")

if st.button("Analyze") and resume and jd:

    with st.spinner("Analyzing resume..."):
        files = {
            "resume": ("resume.pdf", resume.getvalue(), "application/pdf")
        }

        data = {
            "job_description": jd
        }

        response = requests.post(
            "http://localhost:8000/analyze",
            files=files,
            data=data
        )
        

    st.json(response.json())
