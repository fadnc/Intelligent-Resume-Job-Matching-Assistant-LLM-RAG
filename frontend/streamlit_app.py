import streamlit as st
import requests
import os
from typing import Dict, Any
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with high contrast and accessibility
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1976d2;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        border-left: 6px solid #1976d2;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .skill-tag {
        display: inline-block;
        background-color: #d32f2f;
        color: white;
        padding: 0.4rem 0.9rem;
        border-radius: 16px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .suggestion-item {
        background-color: #fffbeb;
        padding: 1rem;
        border: 1px solid #fbbf24;
        border-left: 4px solid #f59e0b;
        margin: 0.5rem 0;
        border-radius: 6px;
        color: #000;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .suggestion-item strong {
        color: #92400e;
    }
    .bullet-item {
        background-color: #f0fdf4;
        padding: 1.2rem;
        border: 1px solid #86efac;
        border-left: 4px solid #10b981;
        margin: 0.5rem 0;
        border-radius: 6px;
        color: #000;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .bullet-item strong {
        color: #065f46;
    }
    .score-excellent { 
        color: #15803d; 
        font-weight: 800; 
    }
    .score-good { 
        color: #16a34a; 
        font-weight: 800; 
    }
    .score-fair { 
        color: #ca8a04; 
        font-weight: 800; 
    }
    .score-poor { 
        color: #dc2626; 
        font-weight: 800; 
    }
    .info-box {
        background-color: #eff6ff;
        padding: 1rem;
        border: 1px solid #93c5fd;
        border-left: 4px solid #2563eb;
        border-radius: 6px;
        margin: 1rem 0;
        color: #000;
    }
    .info-box strong {
        color: #1e40af;
    }
    .tip-box {
        background-color: #fef3c7;
        padding: 1rem;
        border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b;
        border-radius: 6px;
        margin: 1rem 0;
        color: #000;
    }
    .tip-box strong {
        color: #92400e;
    }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def get_score_color_class(score: int) -> str:
    if score >= 80: return "score-excellent"
    elif score >= 60: return "score-good"
    elif score >= 40: return "score-fair"
    else: return "score-poor"

def get_score_emoji(score: int) -> str:
    if score >= 80: return "🌟"
    elif score >= 60: return "✅"
    elif score >= 40: return "⚠️"
    else: return "❌"

def get_score_feedback(score: int) -> str:
    if score >= 80:
        return "Excellent match! Your resume strongly aligns with this role."
    elif score >= 60:
        return "Good match with room for improvement. Focus on the suggestions below."
    elif score >= 40:
        return "Fair match. Consider the improvements to strengthen your application."
    else:
        return "Significant gap identified. Review missing skills and rewrite key sections."

def export_to_text(result: Dict[Any, Any], resume_name: str, job_desc: str) -> str:
    """Export results to formatted text"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    score = result.get('score', 0)
    
    text = f"""
═══════════════════════════════════════════════════════════
        AI RESUME ANALYSIS REPORT
═══════════════════════════════════════════════════════════

Generated: {timestamp}
Resume: {resume_name}

MATCH SCORE: {score}/100 {get_score_emoji(score)}
{get_score_feedback(score)}

───────────────────────────────────────────────────────────
MISSING SKILLS ({len(result.get('missing_skills', []))})
───────────────────────────────────────────────────────────
"""
    
    for i, skill in enumerate(result.get('missing_skills', []), 1):
        text += f"{i}. {skill}\n"
    
    text += f"""
───────────────────────────────────────────────────────────
IMPROVEMENT SUGGESTIONS ({len(result.get('suggestions', []))})
───────────────────────────────────────────────────────────
"""
    
    for i, suggestion in enumerate(result.get('suggestions', []), 1):
        text += f"{i}. {suggestion}\n"
    
    text += f"""
───────────────────────────────────────────────────────────
OPTIMIZED RESUME BULLETS ({len(result.get('rewritten_bullets', []))})
───────────────────────────────────────────────────────────
"""
    
    for i, bullet in enumerate(result.get('rewritten_bullets', []), 1):
        text += f"\nBullet {i}:\n{bullet}\n"
    
    text += f"""
───────────────────────────────────────────────────────────
JOB DESCRIPTION (excerpt)
───────────────────────────────────────────────────────────
{job_desc[:500]}...

═══════════════════════════════════════════════════════════
"""
    return text

def display_results(result: Dict[Any, Any], resume_name: str = "", job_desc: str = ""):
    """Display analysis results with high contrast"""
    score = result.get('score', 0)
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Score display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        score_class = get_score_color_class(score)
        score_emoji = get_score_emoji(score)
        st.markdown(f"""
            <div class="metric-card">
                <h2 style="margin: 0;">Match Score: <span class="{score_class}">{score}/100 {score_emoji}</span></h2>
                <p style="margin-top: 0.8rem; color: #424242; font-size: 1rem;">
                    {get_score_feedback(score)}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Missing Skills", len(result.get('missing_skills', [])))
    
    with col3:
        st.metric("Suggestions", len(result.get('suggestions', [])))
    
    with col4:
        st.metric("New Bullets", len(result.get('rewritten_bullets', [])))
    
    # Export button
    if resume_name and job_desc:
        export_text = export_to_text(result, resume_name, job_desc)
        st.download_button(
            label="📥 Download Analysis Report",
            data=export_text,
            file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Missing skills
    missing_skills = result.get('missing_skills', [])
    if missing_skills:
        st.markdown("### 🎯 Missing Skills")
        st.markdown("**These skills from the job description are not evident in your resume:**")
        
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in missing_skills])
        st.markdown(f'<div style="margin: 1rem 0;">{skills_html}</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
                💡 <strong>Action Item:</strong> Add these skills to your resume if you have experience with them. 
                Include specific examples or projects demonstrating your proficiency.
            </div>
        """, unsafe_allow_html=True)
    
    # Suggestions
    suggestions = result.get('suggestions', [])
    if suggestions:
        st.markdown("### 💡 Improvement Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"""
                <div class="suggestion-item">
                    <strong>{i}.</strong> {suggestion}
                </div>
            """, unsafe_allow_html=True)
    
    # Rewritten bullets
    bullets = result.get('rewritten_bullets', [])
    if bullets:
        st.markdown("### ✨ Optimized Resume Bullets")
        st.markdown("**Copy and customize these improved bullet points:**")
        
        for i, bullet in enumerate(bullets, 1):
            st.markdown(f"""
                <div class="bullet-item">
                    <strong>Bullet {i}:</strong><br/>
                    {bullet}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
                💡 <strong>Pro Tip:</strong> Customize these bullets with your specific metrics and achievements. 
                Use the STAR method (Situation, Task, Action, Result) for maximum impact.
            </div>
        """, unsafe_allow_html=True)
    
    # Raw JSON
    with st.expander("🔍 View Raw JSON Response"):
        st.json(result)

def save_to_history(resume_name: str, score: int):
    """Save analysis to history"""
    st.session_state.analysis_history.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'resume': resume_name,
        'score': score
    })

# Sidebar
with st.sidebar:
    st.markdown("# 📄 Resume Analyzer")
    
    st.markdown("---")
    st.header("📋 About")
    st.markdown("""
        **Powered by AI & RAG Technology**
        
        This tool analyzes your resume against job descriptions using:
        
        ✅ **Match Scoring** - Objective evaluation  
        🎯 **Gap Analysis** - Missing skills identification  
        💡 **Smart Suggestions** - Actionable improvements  
        ✨ **ATS Optimization** - Resume bullet rewrites
    """)
    
    st.markdown("---")
    st.header("⚙️ Settings")
    
    backend_url = st.text_input("Backend URL", value=BACKEND_URL)
    
    if st.button("🔄 Clear History"):
        st.session_state.analysis_history = []
        st.session_state.analysis_result = None
        st.success("History cleared!")
    
    # Analysis history
    if st.session_state.analysis_history:
        st.markdown("---")
        st.header("📊 Recent Analyses")
        for entry in reversed(st.session_state.analysis_history[-5:]):
            score_emoji = get_score_emoji(entry['score'])
            score_class = get_score_color_class(entry['score'])
            st.markdown(f"""
                **{entry['resume'][:25]}...**  
                {score_emoji} <span class="{score_class}">Score: {entry['score']}/100</span>  
                <small>{entry['timestamp']}</small>
            """, unsafe_allow_html=True)
            st.markdown("---")
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; font-size: 0.85rem; color: #666;">
            <p>Built with Streamlit & FastAPI</p>
            <p>Powered by Groq AI</p>
        </div>
    """, unsafe_allow_html=True)

# Main content
st.title("🤖 AI-Powered Resume Analyzer")
st.markdown("""
    Get instant, AI-powered feedback on your resume. Upload your PDF and paste the job description 
    to receive a detailed analysis with actionable insights.
""")

# Tips section
with st.expander("💡 Tips for Best Results", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            **Resume Tips:**
            - Use a clean, ATS-friendly format
            - Include relevant keywords from the job
            - Quantify achievements with metrics
            - Keep it concise (1-2 pages max)
            - Use strong action verbs
        """)
    
    with col2:
        st.markdown("""
            **Job Description Tips:**
            - Paste the complete job posting
            - Don't edit or summarize content
            - Include all requirements & qualifications
            - More detail = more accurate analysis
            - Copy directly from the source
        """)

# Input section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Upload Resume")
    resume = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"],
        help="Upload your resume in PDF format (Max 10MB)"
    )
    
    if resume:
        st.success(f"✅ **{resume.name}**")
        st.info(f"📦 Size: {resume.size / 1024:.2f} KB")

with col2:
    st.markdown("### 💼 Job Description")
    jd = st.text_area(
        "Paste the complete job posting",
        height=200,
        placeholder="Paste the full job description here...\n\nInclude:\n• Job title\n• Responsibilities\n• Required skills\n• Qualifications\n• Company info",
        help="More detail provides better analysis"
    )
    
    if jd:
        word_count = len(jd.split())
        char_count = len(jd)
        st.info(f"📝 {word_count} words • {char_count} characters")
        
        if word_count < 20:
            st.warning("⚠️ Job description seems short. Add more details for better analysis.")

# Analyze button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    analyze_button = st.button("🚀 Analyze My Resume", use_container_width=True)

# Handle analysis
if analyze_button:
    if not resume:
        st.error("❌ Please upload a resume first!")
    elif not jd:
        st.error("❌ Please paste a job description!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📤 Uploading resume...")
            progress_bar.progress(25)
            
            files = {"resume": resume}
            data = {"job_description": jd}
            
            status_text.text("🔍 Analyzing with AI...")
            progress_bar.progress(60)
            
            response = requests.post(
                f"{backend_url}/analyze",
                files=files,
                data=data,
                timeout=120
            )
            
            progress_bar.progress(90)
            
            if response.status_code == 200:
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                result = response.json()
                st.session_state.analysis_result = result
                
                save_to_history(resume.name, result.get('score', 0))
                
                progress_bar.empty()
                status_text.empty()
                
                st.balloons()
                display_results(result, resume.name, jd)
                
            else:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error: HTTP {response.status_code}")
                with st.expander("📋 Error Details"):
                    st.text(response.text)
                    
        except requests.exceptions.Timeout:
            progress_bar.empty()
            status_text.empty()
            st.error("⏱️ Request timed out. Please try again.")
            st.info("💡 Large resumes may take longer to process.")
            
        except requests.exceptions.ConnectionError:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Cannot connect to backend at {backend_url}")
            st.code("uvicorn backend.app:app --reload", language="bash")
            st.info("Make sure the backend server is running ☝️")
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Unexpected error: {str(e)}")
            with st.expander("📋 Technical Details"):
                st.exception(e)

elif st.session_state.analysis_result:
    st.info("ℹ️ Showing previous result. Analyze again for a fresh report.")
    display_results(st.session_state.analysis_result)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1.5rem;">
        <p style="font-size: 1rem; margin-bottom: 0.5rem;">
            Built using <strong>Streamlit</strong> • <strong>FastAPI</strong> • <strong>Groq AI</strong>
        </p>
        <p style="font-size: 0.85rem; color: #999;">
            Powered by RAG (Retrieval Augmented Generation) Technology
        </p>
    </div>
""", unsafe_allow_html=True)