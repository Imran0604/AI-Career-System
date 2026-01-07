import streamlit as st
import os
from utils import fetch_jobs_from_db, predict_career_with_ai, refine_resume_with_ai, create_pdf

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Career Agent", page_icon="🚀", layout="wide")

if 'page' not in st.session_state: st.session_state['page'] = 'Home'
if 'theme' not in st.session_state: st.session_state['theme'] = 'light'

def navigate_to(page): st.session_state['page'] = page; st.rerun()

# --- 2. HIGH CONTRAST THEME ENGINE ---
if st.session_state['theme'] == 'dark':
    # Dark Mode Colors
    primary = "#4F8BF9"
    bg_color = "#0E1117"
    sidebar_bg = "#262730"
    text_color = "#FFFFFF" 
    input_bg = "#1E1E1E"
    border_color = "#41444C"
    hero_text = "#FFFFFF"
    hero_bg = "linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%)"
else:
    # Light Mode Colors (High Contrast)
    primary = "#2563EB"
    bg_color = "#FFFFFF"
    sidebar_bg = "#F8F9FA"
    text_color = "#000000"  # Pure Black for clarity
    input_bg = "#FFFFFF"
    border_color = "#AAAAAA" # Darker border for visibility
    hero_text = "#000000"
    hero_bg = "linear-gradient(135deg, #E0EAFC 0%, #CFDEF3 100%)"

# Inject Custom CSS
st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* Inputs (Text, Area, Select) */
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stFileUploader {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px;
    }}
    
    /* Text Clarity */
    h1, h2, h3, h4, h5, h6, p, label, li {{
        color: {text_color} !important;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* Hero Section */
    .hero-box {{
        background: {hero_bg};
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .hero-box h1, .hero-box p {{
        color: {hero_text} !important;
    }}

    /* Buttons */
    .stButton>button {{
        background-color: {input_bg};
        color: {text_color} !important;
        border: 1px solid {border_color};
        border-radius: 8px;
        font-weight: 600;
    }}
    button[kind="primary"] {{
        background-color: {primary} !important;
        color: white !important;
        border: none !important;
    }}

    /* Job Cards */
    .job-card {{
        background-color: {input_bg};
        border: 1px solid {border_color};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .match-tag {{
        background-color: {primary};
        color: white;
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)

    st.markdown(f"<h2 style='text-align: center; color: {text_color};'>Career Agent</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True): navigate_to("Home")
    if st.button("📝 Build CV", use_container_width=True): navigate_to("Build CV")
    if st.button("🔮 Predict", use_container_width=True): navigate_to("Predict")
    if st.button("🎯 Jobs", use_container_width=True): navigate_to("Jobs")
    if st.button("✨ AI Fix", use_container_width=True): navigate_to("AI Fix")
    
    st.markdown("---")
    # Theme Toggle
    btn_text = "☀️ Light Mode" if st.session_state['theme'] == 'dark' else "🌙 Dark Mode"
    if st.button(btn_text):
        st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
        st.rerun()

# --- 4. PAGES ---
page = st.session_state['page']

if page == "Home":
    st.markdown(f"""<div class="hero-box"><h1>Intelligent Career Guidance</h1><p>Optimize your resume, predict your career path, and find your dream job with AI.</p></div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Building Your Resume Now", type="primary", use_container_width=True): navigate_to("Build CV")

    st.markdown("---")
    st.markdown("### Features")
    c1, c2, c3 = st.columns(3)
    # Using markdown containers for cards to ensure CSS applies
    with c1: st.markdown(f"""<div class="job-card"><h3>🔮 Smart Prediction</h3><p>AI analyzes your skills to suggest the perfect career path.</p></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="job-card"><h3>🎯 Precision Matching</h3><p>Get jobs ranked by how well they match your actual resume.</p></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class="job-card"><h3>✨ AI Enhancement</h3><p>Turn weak bullet points into powerful success stories.</p></div>""", unsafe_allow_html=True)

elif page == "Build CV":
    st.title("📝 Resume Builder")
    with st.form("cv"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name"); role = c2.text_input("Target Role")
        email = c1.text_input("Email"); phone = c2.text_input("Phone")
        linkedin = st.text_input("LinkedIn")
        up = st.file_uploader("Photo", type=["jpg","png"])
        skills = st.text_input("Skills (e.g. Python, SQL)")
        summ = st.text_area("Summary"); exp = st.text_area("Experience"); edu = st.text_area("Education")
        sub = st.form_submit_button("Generate PDF", type="primary")
    
    if sub:
        img = "temp.png" if up else None
        if up: 
            with open("temp.png", "wb") as f: f.write(up.getbuffer())
        pdf = create_pdf(name, email, phone, linkedin, role, summ, skills.split(","), exp, edu, img)
        st.download_button("Download PDF", pdf, "resume.pdf", "application/pdf")
        st.session_state['skills'] = skills
        if img: os.remove(img)

elif page == "Jobs":
    st.title("🎯 Job Matcher")
    skills = st.session_state.get('skills', "")
    if not skills: skills = st.text_input("Enter Skills")
    
    if st.button("Find Matches", type="primary"):
        jobs = fetch_jobs_from_db(skills)
        st.success(f"Found {len(jobs)} matches!")
        for job in jobs:
            st.markdown(f"""
            <div class="job-card">
                <h3>{job['title']} <span class="match-tag">{job['score']}% Match</span></h3>
                <p><strong>{job['company']}</strong> | 📍 {job['location']} | 💰 {job['salary']}</p>
                <p>{job['description']}</p>
                <small>Type: {job['type']}</small>
            </div>
            """, unsafe_allow_html=True)

elif page == "Predict":
    st.title("🔮 Career Predictor")
    skills = st.session_state.get('skills', "")
    if not skills: skills = st.text_input("Enter Skills")
    if st.button("Predict Role", type="primary"):
        with st.spinner("Analyzing..."):
            res = predict_career_with_ai(skills.split(","))
            st.success(f"Recommended Role: **{res}**")

elif page == "AI Fix":
    st.title("✨ AI Enhancer")
    txt = st.text_area("Weak Text (e.g. 'I did sales')")
    if st.button("Enhance", type="primary"):
        with st.spinner("Refining..."):
            res = refine_resume_with_ai(txt)
            st.text_area("Improved Version", res)