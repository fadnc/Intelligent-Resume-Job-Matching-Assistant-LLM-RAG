import streamlit as st
import requests
import os
from typing import Dict, Any
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed CSS with proper color contrast and cohesive design
st.markdown("""
    <style>
    /* Root variables for consistent theming */
    :root {
        --primary: #2563eb;
        --primary-light: #3b82f6;
        --primary-dark: #1d4ed8;
        --success: #059669;
        --success-light: #10b981;
        --warning: #d97706;
        --warning-light: #f59e0b;
        --danger: #dc2626;
        --danger-light: #ef4444;
        --text-dark: #111827;
        --text-medium: #374151;
        --text-light: #6b7280;
        --text-muted: #9ca3af;
        --bg-white: #ffffff;
        --bg-gray-50: #f9fafb;
        --bg-gray-100: #f3f4f6;
        --border-light: #e5e7eb;
        --border-medium: #d1d5db;
    }
    
    .main {
        padding: 1.5rem 2rem;
    }
    
    /* Header with better gradient */
    .header-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1d4ed8 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(30, 64, 175, 0.25);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    .header-container p {
        margin: 0.75rem 0 0 0;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
    }
    
    /* Button styles */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: #ffffff !important;
        padding: 0.875rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Score card */
    .score-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #2563eb, #3b82f6, #2563eb);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-color: #d1d5db;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }
    
    /* Skill tags - softer orange/amber instead of harsh red */
    .skill-tag {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(234, 88, 12, 0.25);
        transition: all 0.2s ease;
        cursor: default;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(234, 88, 12, 0.35);
    }
    
    .skill-tag::before {
        content: '⚠';
        margin-right: 0.5rem;
        font-size: 0.75rem;
    }
    
    /* Suggestion items - warm amber tones */
    .suggestion-item {
        background: #fffbeb;
        padding: 1.25rem;
        border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b;
        margin: 0.75rem 0;
        border-radius: 10px;
        color: #92400e;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.1);
        transition: all 0.2s ease;
    }
    
    .suggestion-item:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }
    
    .suggestion-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        background: #f59e0b;
        color: #ffffff;
        border-radius: 50%;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.75rem;
    }
    
    /* Bullet items - green tones */
    .bullet-item {
        background: #f0fdf4;
        padding: 1.25rem;
        border: 1px solid #86efac;
        border-left: 4px solid #22c55e;
        margin: 0.75rem 0;
        border-radius: 10px;
        color: #166534;
        box-shadow: 0 2px 6px rgba(34, 197, 94, 0.1);
        transition: all 0.2s ease;
        position: relative;
    }
    
    .bullet-item:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
    }
    
    .bullet-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
        color: #15803d;
    }
    
    .bullet-icon {
        background: #22c55e;
        color: #ffffff;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 0.75rem;
    }
    
    /* Score colors - clear and distinct */
    .score-excellent { 
        color: #059669 !important;
    }
    .score-good { 
        color: #16a34a !important;
    }
    .score-fair { 
        color: #d97706 !important;
    }
    .score-poor { 
        color: #dc2626 !important;
    }
    
    /* Info box - blue theme with proper contrast */
    .info-box {
        background: #eff6ff;
        padding: 1.25rem;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1e40af;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .info-box strong {
        color: #1e3a8a;
    }
    
    .info-box-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
    }
    
    /* Tip box - amber theme */
    .tip-box {
        background: #fffbeb;
        padding: 1.25rem;
        border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        margin: 1rem 0;
        color: #92400e;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .tip-box strong {
        color: #78350f;
    }
    
    .tip-box ul, .tip-box ol {
        color: #92400e;
        margin: 0.5rem 0 0 0;
        padding-left: 1.25rem;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .section-header h2, .section-header h3 {
        margin: 0;
        color: #111827;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f3f4f6;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #4b5563;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #111827;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* History item */
    .history-item {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        border-color: #3b82f6;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.12);
    }
    
    /* Circular progress for score */
    .circular-progress {
        position: relative;
        width: 150px;
        height: 150px;
        margin: 0 auto;
    }
    
    .circular-progress svg {
        transform: rotate(-90deg);
    }
    
    .circular-progress .bg {
        fill: none;
        stroke: #e5e7eb;
        stroke-width: 10;
    }
    
    .circular-progress .progress {
        fill: none;
        stroke-width: 10;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s ease;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* File upload info */
    .upload-info {
        background: #f0fdf4;
        padding: 1rem;
        border: 1px solid #86efac;
        border-radius: 10px;
        margin-top: 0.5rem;
        color: #166534;
    }
    
    .upload-info strong {
        color: #15803d;
    }
    
    /* Quality indicator */
    .quality-indicator {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
        padding: 0.5rem 0.75rem;
        background: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    .quality-indicator .stats {
        color: #6b7280;
        font-size: 0.85rem;
    }
    
    .quality-indicator .label {
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6b7280;
    }
    
    .footer strong {
        color: #374151;
    }
    
    .footer .muted {
        color: #9ca3af;
        font-size: 0.85rem;
    }
    
    .footer .copyright {
        color: #d1d5db;
        font-size: 0.75rem;
        margin-top: 1rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-container h1 {
            font-size: 1.75rem;
        }
        .score-number {
            font-size: 3rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def get_score_color_class(score: int) -> str:
    if score >= 80: return "score-excellent"
    elif score >= 60: return "score-good"
    elif score >= 40: return "score-fair"
    else: return "score-poor"

def get_score_color(score: int) -> str:
    if score >= 80: return "#059669"
    elif score >= 60: return "#16a34a"
    elif score >= 40: return "#d97706"
    else: return "#dc2626"

def get_score_emoji(score: int) -> str:
    if score >= 80: return "🌟"
    elif score >= 60: return "✅"
    elif score >= 40: return "⚠️"
    else: return "❌"

def get_score_label(score: int) -> str:
    if score >= 80: return "Excellent Match"
    elif score >= 60: return "Good Match"
    elif score >= 40: return "Fair Match"
    else: return "Needs Work"

def get_score_feedback(score: int) -> str:
    if score >= 80:
        return "Outstanding! Your resume strongly aligns with this role. Minor tweaks could make it perfect."
    elif score >= 60:
        return "Good foundation! Focus on the suggestions below to boost your chances."
    elif score >= 40:
        return "Decent start. Consider the improvements to strengthen your application significantly."
    else:
        return "Significant gaps found. Review missing skills and implement the suggested rewrites."

def create_circular_progress(score: int) -> str:
    """Generate SVG for circular progress indicator"""
    color = get_score_color(score)
    circumference = 2 * 3.14159 * 60
    offset = circumference - (score / 100) * circumference
    
    return f"""
    <div class="circular-progress">
        <svg width="150" height="150" viewBox="0 0 150 150">
            <circle class="bg" cx="75" cy="75" r="60"/>
            <circle class="progress" cx="75" cy="75" r="60" 
                stroke="{color}" 
                stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}"/>
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
            <div class="score-number" style="color: {color};">{score}</div>
            <div style="font-size: 0.875rem; color: #6b7280;">out of 100</div>
        </div>
    </div>
    """

def export_to_text(result: Dict[Any, Any], resume_name: str, job_desc: str) -> str:
    """Export results to formatted text"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    score = result.get('score', 0)
    
    text = f"""
╔══════════════════════════════════════════════════════════════════╗
║              AI RESUME ANALYSIS REPORT                           ║
╚══════════════════════════════════════════════════════════════════╝

📅 Generated: {timestamp}
📄 Resume: {resume_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    MATCH SCORE: {score}/100 {get_score_emoji(score)}
                    Status: {get_score_label(score)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{get_score_feedback(score)}

┌──────────────────────────────────────────────────────────────────┐
│ 🎯 MISSING SKILLS ({len(result.get('missing_skills', []))})                                         │
└──────────────────────────────────────────────────────────────────┘
"""
    
    for i, skill in enumerate(result.get('missing_skills', []), 1):
        text += f"  {i}. {skill}\n"
    
    text += f"""
┌──────────────────────────────────────────────────────────────────┐
│ 💡 IMPROVEMENT SUGGESTIONS ({len(result.get('suggestions', []))})                               │
└──────────────────────────────────────────────────────────────────┘
"""
    
    for i, suggestion in enumerate(result.get('suggestions', []), 1):
        text += f"\n  [{i}] {suggestion}\n"
    
    text += f"""
┌──────────────────────────────────────────────────────────────────┐
│ ✨ OPTIMIZED RESUME BULLETS ({len(result.get('rewritten_bullets', []))})                          │
└──────────────────────────────────────────────────────────────────┘
"""
    
    for i, bullet in enumerate(result.get('rewritten_bullets', []), 1):
        text += f"\n  ▸ Bullet {i}:\n    {bullet}\n"
    
    text += f"""
┌──────────────────────────────────────────────────────────────────┐
│ 📋 JOB DESCRIPTION EXCERPT                                       │
└──────────────────────────────────────────────────────────────────┘
{job_desc[:800]}{'...' if len(job_desc) > 800 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by AI Resume Analyzer | Powered by RAG Technology
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return text

def export_to_json(result: Dict[Any, Any], resume_name: str) -> str:
    """Export results to JSON format"""
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "resume_name": resume_name,
        "analysis": result
    }
    return json.dumps(export_data, indent=2)

def display_results(result: Dict[Any, Any], resume_name: str = "", job_desc: str = ""):
    """Display analysis results with enhanced UI"""
    score = result.get('score', 0)
    
    st.markdown("---")
    
    # Results header
    st.markdown("""
        <div class="section-header">
            <h2 style="margin: 0; color: #111827;">📊 Analysis Results</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Score display with circular progress
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
            <div class="score-card animate-in">
                {create_circular_progress(score)}
                <div style="margin-top: 1rem;">
                    <span style="font-size: 1.25rem; font-weight: 700; color: {get_score_color(score)};">
                        {get_score_emoji(score)} {get_score_label(score)}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card animate-in" style="height: 100%;">
                <h3 style="margin: 0 0 1rem 0; color: #111827;">Analysis Summary</h3>
                <p style="color: #4b5563; font-size: 1rem; line-height: 1.6; margin-bottom: 1.5rem;">
                    {get_score_feedback(score)}
                </p>
                <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
                    <div>
                        <div class="metric-value" style="color: #ea580c;">{len(result.get('missing_skills', []))}</div>
                        <div class="metric-label">Missing Skills</div>
                    </div>
                    <div>
                        <div class="metric-value" style="color: #d97706;">{len(result.get('suggestions', []))}</div>
                        <div class="metric-label">Suggestions</div>
                    </div>
                    <div>
                        <div class="metric-value" style="color: #059669;">{len(result.get('rewritten_bullets', []))}</div>
                        <div class="metric-label">Optimized Bullets</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Export options
    if resume_name and job_desc:
        st.markdown("### 📥 Export Report")
        col1, col2 = st.columns(2)
        with col1:
            export_text = export_to_text(result, resume_name, job_desc)
            st.download_button(
                label="📄 Download as Text",
                data=export_text,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            export_json = export_to_json(result, resume_name)
            st.download_button(
                label="📋 Download as JSON",
                data=export_json,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Tabbed interface for results
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Missing Skills", "💡 Suggestions", "✨ Optimized Bullets", "🔍 Raw Data"])
    
    with tab1:
        missing_skills = result.get('missing_skills', [])
        if missing_skills:
            st.markdown(f"""
                <div class="info-box">
                    <span class="info-box-icon">ℹ️</span>
                    <div>
                        <strong>Skills Gap Analysis</strong><br/>
                        <span style="color: #1e40af;">These {len(missing_skills)} skills from the job description are not clearly demonstrated in your resume.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in missing_skills])
            st.markdown(f'<div style="margin: 1.5rem 0; line-height: 2.5;">{skills_html}</div>', unsafe_allow_html=True)
            
            st.markdown("""
                <div class="tip-box">
                    <span class="info-box-icon">💡</span>
                    <div>
                        <strong>Action Steps:</strong>
                        <ul>
                            <li>Add these skills to your resume if you have relevant experience</li>
                            <li>Include specific projects or achievements demonstrating each skill</li>
                            <li>Use keywords that match the job description exactly</li>
                            <li>Consider adding a "Technical Skills" or "Core Competencies" section</li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("🎉 Great news! Your resume covers all the key skills mentioned in the job description.")
    
    with tab2:
        suggestions = result.get('suggestions', [])
        if suggestions:
            st.markdown(f"""
                <div class="info-box">
                    <span class="info-box-icon">💡</span>
                    <div>
                        <strong>Personalized Recommendations</strong><br/>
                        <span style="color: #1e40af;">Implement these {len(suggestions)} suggestions to improve your resume's impact and ATS compatibility.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"""
                    <div class="suggestion-item animate-in" style="animation-delay: {i * 0.1}s;">
                        <span class="suggestion-number">{i}</span>
                        <span style="color: #92400e;">{suggestion}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 No specific suggestions - your resume is well-optimized!")
    
    with tab3:
        bullets = result.get('rewritten_bullets', [])
        if bullets:
            st.markdown(f"""
                <div class="info-box">
                    <span class="info-box-icon">✨</span>
                    <div>
                        <strong>ATS-Optimized Bullet Points</strong><br/>
                        <span style="color: #1e40af;">These {len(bullets)} rewritten bullets incorporate keywords from the job description and use impact-driven language.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for i, bullet in enumerate(bullets, 1):
                st.markdown(f"""
                    <div class="bullet-item animate-in" style="animation-delay: {i * 0.1}s;">
                        <div class="bullet-header">
                            <span class="bullet-icon">✓ {i}</span>
                            <span>Optimized Achievement Statement</span>
                        </div>
                        <div style="padding-left: 0.5rem; line-height: 1.6; color: #166534;">
                            {bullet}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Copy button using native streamlit
                if st.button(f"📋 Copy Bullet {i}", key=f"copy_{i}", use_container_width=False):
                    st.code(bullet, language=None)
            
            st.markdown("""
                <div class="tip-box">
                    <span class="info-box-icon">🎯</span>
                    <div>
                        <strong>Pro Tips for Maximum Impact:</strong>
                        <ul>
                            <li>Customize with your specific metrics and achievements</li>
                            <li>Use the STAR method (Situation, Task, Action, Result)</li>
                            <li>Start each bullet with a strong action verb</li>
                            <li>Quantify results wherever possible (%, $, #)</li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No rewritten bullets generated for this analysis.")
    
    with tab4:
        st.json(result)

def save_to_history(resume_name: str, score: int, job_title: str = ""):
    """Save analysis to history"""
    st.session_state.analysis_history.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'resume': resume_name,
        'score': score,
        'job_title': job_title
    })
    # Keep only last 10 entries
    if len(st.session_state.analysis_history) > 10:
        st.session_state.analysis_history = st.session_state.analysis_history[-10:]

def check_backend_health(url: str) -> bool:
    """Check if backend is reachable"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="margin: 0; font-size: 1.5rem; color: #111827;">📄 Resume Analyzer</h1>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0.5rem 0 0 0;">AI-Powered Career Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Backend status
    backend_url = st.text_input("🔗 Backend URL", value=BACKEND_URL, help="URL of the backend API server")
    
    is_healthy = check_backend_health(backend_url)
    if is_healthy:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Unavailable")
        st.caption("Start the server with:")
        st.code("uvicorn backend.app:app --reload", language="bash")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear", use_container_width=True, help="Clear analysis history"):
            st.session_state.analysis_history = []
            st.session_state.analysis_result = None
            st.rerun()
    with col2:
        if st.button("🔃 Refresh", use_container_width=True, help="Refresh connection"):
            st.rerun()
    
    # Analysis history
    if st.session_state.analysis_history:
        st.markdown("---")
        st.markdown("### 📊 Recent Analyses")
        
        for entry in reversed(st.session_state.analysis_history[-5:]):
            score_emoji = get_score_emoji(entry['score'])
            score_color = get_score_color(entry['score'])
            st.markdown(f"""
                <div class="history-item">
                    <div style="font-weight: 600; color: #111827; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        📄 {entry['resume'][:30]}{'...' if len(entry['resume']) > 30 else ''}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                        <span style="color: {score_color}; font-weight: 700;">{score_emoji} {entry['score']}/100</span>
                        <span style="color: #9ca3af; font-size: 0.75rem;">{entry['timestamp'].split()[0]}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About section
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
            **Powered by AI & RAG Technology**
            
            This tool analyzes your resume against job descriptions using cutting-edge AI:
            
            - 🎯 **Match Scoring** - Objective evaluation
            - 🔍 **Gap Analysis** - Missing skills identification
            - 💡 **Smart Suggestions** - Actionable improvements
            - ✨ **ATS Optimization** - Keyword-rich rewrites
            
            ---
            
            Built with:
            - 🚀 Streamlit
            - ⚡ FastAPI
            - 🤖 Groq AI
            - 🔗 FAISS Vector Store
        """)
    
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #9ca3af; font-size: 0.75rem;">
            <p>v2.0 • Made with ❤️</p>
        </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
    <div class="header-container">
        <h1>🤖 AI-Powered Resume Analyzer</h1>
        <p>Get instant, actionable feedback to land your dream job</p>
    </div>
""", unsafe_allow_html=True)

# Quick stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 1.75rem;">📄</div>
            <div style="font-weight: 600; color: #111827;">PDF Analysis</div>
            <div style="color: #6b7280; font-size: 0.8rem;">Upload your resume</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 1.75rem;">🎯</div>
            <div style="font-weight: 600; color: #111827;">Skills Gap</div>
            <div style="color: #6b7280; font-size: 0.8rem;">Find missing keywords</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 1.75rem;">💡</div>
            <div style="font-weight: 600; color: #111827;">AI Suggestions</div>
            <div style="color: #6b7280; font-size: 0.8rem;">Personalized tips</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 1.75rem;">✨</div>
            <div style="font-weight: 600; color: #111827;">ATS Ready</div>
            <div style="color: #6b7280; font-size: 0.8rem;">Optimized bullets</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tips section (collapsible)
with st.expander("💡 Tips for Best Results", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            **📄 Resume Tips:**
            - Use clean, ATS-friendly formatting
            - Include relevant keywords from the job
            - Quantify achievements with metrics
            - Keep it concise (1-2 pages)
            - Use strong action verbs
        """)
    
    with col2:
        st.markdown("""
            **💼 Job Description Tips:**
            - Paste the complete job posting
            - Include all requirements & qualifications
            - Don't edit or summarize the content
            - More detail = better analysis
            - Copy directly from the source
        """)
    
    with col3:
        st.markdown("""
            **🎯 Optimization Tips:**
            - Target 70%+ match score
            - Address all missing skills
            - Use suggested bullet rewrites
            - Tailor for each application
            - Update skills section regularly
        """)

# Input section with improved layout
st.markdown("### 📥 Upload Your Documents")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #111827;">📄 Resume (PDF)</span>
        </div>
    """, unsafe_allow_html=True)
    
    resume = st.file_uploader(
        "Upload resume",
        type=["pdf"],
        help="Upload your resume in PDF format (Max 10MB)",
        label_visibility="collapsed"
    )
    
    if resume:
        st.markdown(f"""
            <div class="upload-info">
                <span>✅</span>
                <strong>{resume.name}</strong><br/>
                <span style="font-size: 0.85rem; color: #166534;">
                    Size: {resume.size / 1024:.1f} KB
                </span>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #111827;">💼 Job Description</span>
        </div>
    """, unsafe_allow_html=True)
    
    jd = st.text_area(
        "Job description",
        height=200,
        placeholder="Paste the complete job description here...\n\n• Job title and company\n• Responsibilities\n• Required skills & qualifications\n• Preferred qualifications\n• Any other relevant details",
        help="More detail provides better analysis",
        label_visibility="collapsed"
    )
    
    if jd:
        word_count = len(jd.split())
        char_count = len(jd)
        
        if word_count >= 100:
            quality_color = "#059669"
            quality_label = "Excellent"
        elif word_count >= 50:
            quality_color = "#d97706"
            quality_label = "Good"
        else:
            quality_color = "#dc2626"
            quality_label = "Too Short"
        
        st.markdown(f"""
            <div class="quality-indicator">
                <span class="stats">📝 {word_count} words • {char_count} chars</span>
                <span class="label" style="color: {quality_color};">{quality_label}</span>
            </div>
        """, unsafe_allow_html=True)

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    analyze_button = st.button(
        "🚀 Analyze My Resume",
        use_container_width=True,
        disabled=not (resume and jd)
    )
    
    if not resume or not jd:
        st.caption("Upload a resume and paste a job description to enable analysis")

# Handle analysis
if analyze_button:
    if not resume:
        st.error("❌ Please upload a resume first!")
    elif not jd:
        st.error("❌ Please paste a job description!")
    else:
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                (10, "📤 Uploading resume..."),
                (30, "📝 Extracting text..."),
                (50, "🔍 Analyzing content..."),
                (70, "🤖 Generating insights..."),
                (90, "📊 Finalizing results..."),
            ]
            
            try:
                for progress, message in steps[:2]:
                    status_text.markdown(f"**{message}**")
                    progress_bar.progress(progress)
                    time.sleep(0.3)
                
                files = {"resume": resume}
                data = {"job_description": jd}
                
                for progress, message in steps[2:4]:
                    status_text.markdown(f"**{message}**")
                    progress_bar.progress(progress)
                
                response = requests.post(
                    f"{backend_url}/analyze",
                    files=files,
                    data=data,
                    timeout=180
                )
                
                status_text.markdown(f"**{steps[4][1]}**")
                progress_bar.progress(steps[4][0])
                
                if response.status_code == 200:
                    progress_bar.progress(100)
                    status_text.markdown("**✅ Analysis complete!**")
                    time.sleep(0.5)
                    
                    result = response.json()
                    st.session_state.analysis_result = result
                    
                    # Try to extract job title from JD
                    job_title = jd.split('\n')[0][:50] if jd else ""
                    save_to_history(resume.name, result.get('score', 0), job_title)
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.balloons()
                    display_results(result, resume.name, jd)
                    
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: HTTP {response.status_code}")
                    with st.expander("📋 Error Details"):
                        st.code(response.text)
                        
            except requests.exceptions.Timeout:
                progress_bar.empty()
                status_text.empty()
                st.error("⏱️ Request timed out. The analysis is taking longer than expected.")
                st.info("💡 Try again or check if the backend server is responding.")
                
            except requests.exceptions.ConnectionError:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Cannot connect to backend at {backend_url}")
                st.markdown("""
                    <div class="tip-box">
                        <span class="info-box-icon">💡</span>
                        <div>
                            <strong>How to fix:</strong>
                            <ol>
                                <li>Open a terminal in the project directory</li>
                                <li>Run the command below to start the backend</li>
                                <li>Wait for the server to start, then try again</li>
                            </ol>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.code("uvicorn backend.app:app --reload", language="bash")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Unexpected error: {str(e)}")
                with st.expander("📋 Technical Details"):
                    st.exception(e)

elif st.session_state.analysis_result:
    st.info("ℹ️ Showing previous analysis result. Upload new documents and click 'Analyze' for a fresh report.")
    display_results(st.session_state.analysis_result)

# Footer
st.markdown("---")
st.markdown(f"""
    <div class="footer">
        <p style="font-size: 1rem; margin-bottom: 0.5rem;">
            Built with ❤️ using <strong>Streamlit</strong> • <strong>FastAPI</strong> • <strong>Groq AI</strong>
        </p>
        <p class="muted">
            Powered by RAG (Retrieval Augmented Generation) • FAISS Vector Search
        </p>
        <p class="copyright">
            © {datetime.now().year} AI Resume Analyzer
        </p>
    </div>
""", unsafe_allow_html=True)