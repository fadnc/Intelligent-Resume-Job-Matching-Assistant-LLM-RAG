import streamlit as st
import requests

st.title("Resume Job Matcher")

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd = st.text_area("Paste Job Description")

if st.button("Analyze") and resume and jd:

    files = {"resume": resume}   # IMPORTANT: not resume.getvalue()
    data = {"job_description": jd}

    response = requests.post(
        "http://localhost:8000/analyze",
        files=files,
        data=data
    )

    st.write("Status:", response.status_code)

    try:
        st.json(response.json())
    except:
        st.text(response.text)
