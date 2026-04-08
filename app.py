import streamlit as st
import openai
import pandas as pd
from fpdf import FPDF
import os

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Tube Fellow",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DARK MODE CSS
# ============================================
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .stSidebar { background-color: #1a1a1a; }
    .stButton>button {
        background-color: #ff0000;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #cc0000; }
    .stTextInput>div>div>input {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444;
    }
    .stTab { background-color: #1a1a1a; }
    h1, h2, h3 { color: #ff0000; }
    .metric-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/youtube-play.png", width=80)
    st.title("Tube Fellow")
    st.markdown("---")

    api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")
    target_country = st.selectbox("🌍 Target Country", ["USA", "UK", "Canada", "Australia"])
    niche = st.selectbox("🎯 Niche", ["Finance", "Technology", "SaaS", "Health", "Education", "Gaming"])
    
    st.markdown("---")
    st.markdown("**CPM Rates:**")
    st.markdown("🇺🇸 USA: $20–$30")
    st.markdown("🇬🇧 UK: $15–$25")
    st.markdown("🇨🇦 Canada: $15–$20")

# ============================================
# MAIN HEADER
# ============================================
st.markdown("<h1 style='text-align:center'>🎯 Tube Fellow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888'>Your AI-Powered YouTube Growth Engine</p>", unsafe_allow_html=True)
st.markdown("---")

# ============================================
# TABS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Strategy", "✍️ Scriptwriting", "🎨 Visuals", "💰 Revenue"])

# ============================================
# HELPER FUNCTION
# ============================================
def ask_gpt(prompt, api_key):
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": """You are an expert YouTube Growth Hacker with 10+ years of experience.
                You specialize in:
                - High-retention video patterns (Hooks, Loops, Pacing)
                - High-CPM niches (Finance, SaaS, Tech)
                - Viral Psychology (CTR optimization and Audience Retention)
                - Script writing that keeps viewers watching till the end
                Always respond in professional English."""
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ============================================
# TAB 1 - STRATEGY (TREND RADAR)
# ============================================
with tab1:
    st.markdown("## 📡 Global Trend Radar")
    st.markdown("Discover what's going viral in the next 24 hours")
    
    trend_topic = st.text_input("🔍 Enter your niche or topic", placeholder="e.g. AI tools for business")
    
    if st.button("🚀 Analyze Trends", key="trend_btn"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API Key in the sidebar")
        elif not trend_topic:
            st.error("⚠️ Please enter a topic")
        else:
            with st.spinner("🔍 Analyzing global trends..."):
                prompt = f"""
                Analyze the YouTube trend potential for: "{trend_topic}" in {target_country} for the {niche} niche.
                
                Provide:
                1. TOP 5 viral video ideas for the next 24 hours
                2. Best keywords to target (with estimated search volume)
                3. Competition level (Low/Medium/High)
                4. Viral potential score (1-10)
                5. Best time to upload
                6. Recommended video length
                
                Format your response clearly with sections and bullet points.
                """
                result = ask_gpt(prompt, api_key)
                st.markdown("### 🎯 Trend Analysis Results")
                st.markdown(result)

# ============================================
# TAB 2 - SCRIPTWRITING
# ============================================
with tab2:
    st.markdown("## ✍️ Script Surgeon")
    st.markdown("Generate retention-optimized scripts with engagement spikes")
    
    video_topic = st.text_input("🎬 Video Topic", placeholder="e.g. How to invest $1000 in 2025")
    video_length = st.selectbox("⏱️ Video Length", ["5 minutes", "10 minutes", "15 minutes", "20 minutes"])
    
    if st.button("✍️ Generate Script", key="script_btn"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API Key in the sidebar")
        elif not video_topic:
            st.error("⚠️ Please enter a video topic")
        else:
            with st.spinner("✍️ Writing your retention-optimized script..."):
                prompt = f"""
                Create a complete YouTube script for: "{video_topic}"
                Target: {target_country} audience | Niche: {niche} | Length: {video_length}
                
                Structure the script as a detailed table with these exact columns:
                | Timestamp | Audio (Script) | Visual (B-Roll/Scenes) | Retention Strategy |
                
                Rules:
                - Start with a POWERFUL hook (first 30 seconds)
                - Add pattern interrupts every 60-90 seconds
                - Flag any [BORING ZONE] and replace with [ENGAGEMENT SPIKE]
                - End with a strong CTA
                - Make it conversational and engaging
                
                After the table, add:
                - 3 KEY HOOKS to use in the first 30 seconds
                - 5 PATTERN INTERRUPTS to keep viewers watching
                """
                result = ask_gpt(prompt, api_key)
                
                st.markdown("### 📝 Your Script")
                st.markdown(result)
                
                # PDF Export
                st.markdown("---")
                if st.button("📥 Download Script as PDF", key="pdf_btn"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=f"Script: {video_topic}", ln=True, align='C')
                    pdf.ln(10)
                    
                    for line in result.split('\n'):
                        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 10, txt=clean_line)
                    
                    pdf_path = "script.pdf"
                    pdf.output(pdf_path)
                    
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Click to Download PDF",
                            data=f,
                            file_name=f"{video_topic}_script.pdf",
                            mime="application/pdf"
                        )

# ============================================
# TAB 3 - VISUALS
# ============================================
with tab3:
    st.markdown("## 🎨 Visual Studio")
    st.markdown("Generate high-CTR thumbnail concepts")
    
    thumb_topic = st.text_input("🖼️ Video Topic for Thumbnail", placeholder="e.g. How I made $10k with AI")
    
    if st.button("🎨 Generate Thumbnail Concepts", key="visual_btn"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API Key in the sidebar")
        elif not thumb_topic:
            st.error("⚠️ Please enter a topic")
        else:
            with st.spinner("🎨 Designing thumbnail concepts..."):
                prompt = f"""
                Create 3 DALL-E 3 prompts for YouTube thumbnails for: "{thumb_topic}"
                Target: {target_country} | Niche: {niche}
                
                For each thumbnail provide:
                1. DALL-E 3 Prompt (detailed, specific)
                2. Color Scheme
                3. Emotion to convey
                4. Text Overlay (max 5 words)
                5. Lighting description
                6. Why this will achieve 10%+ CTR
                
                Make each concept completely different in style.
                """
                result = ask_gpt(prompt, api_key)
                st.markdown("### 🖼️ Thumbnail Concepts")
                st.markdown(result)

# ============================================
# TAB 4 - REVENUE
# ============================================
with tab4:
    st.markdown("## 💰 Revenue Engine")
    st.markdown("Calculate your earning potential")
    
    col1, col2 = st.columns(2)
    
    with col1:
        views = st.number_input("👁️ Expected Views", min_value=1000, max_value=10000000, value=10000, step=1000)
    with col2:
        revenue_topic = st.text_input("📝 Video Topic", placeholder="e.g. Investment strategies 2025")
    
    if st.button("💰 Calculate Revenue", key="revenue_btn"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API Key in the sidebar")
        else:
            # CPM Rates
            cpm_rates = {"USA": (20, 30), "UK": (15, 25), "Canada": (15, 20), "Australia": (15, 22)}
            niche_multipliers = {"Finance": 1.5, "Technology": 1.3, "SaaS": 1.4, "Health": 1.2, "Education": 1.1, "Gaming": 0.9}
            
            cpm_min, cpm_max = cpm_rates[target_country]
            multiplier = niche_multipliers[niche]
            
            revenue_min = (views / 1000) * cpm_min * multiplier
            revenue_max = (views / 1000) * cpm_max * multiplier
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💵 Min Revenue", f"${revenue_min:,.0f}")
            with col2:
                st.metric("💰 Max Revenue", f"${revenue_max:,.0f}")
            with col3:
                st.metric("📊 CPM Range", f"${cpm_min}–${cpm_max}")
            
            st.markdown("---")
            
            # Affiliate Products
            if revenue_topic:
                with st.spinner("🔍 Finding affiliate products..."):
                    prompt = f"""
                    For a YouTube video about: "{revenue_topic}" targeting {target_country} in the {niche} niche,
                    
                    Recommend 3 specific affiliate products from Amazon or ClickBank.
                    
                    For each product provide:
                    1. Product Name
                    2. Platform (Amazon/ClickBank)
                    3. Estimated Commission per sale
                    4. Why it matches this video's audience
                    5. How to naturally mention it in the video
                    
                    Focus on high-converting products with good commission rates.
                    """
                    result = ask_gpt(prompt, api_key)
                    st.markdown("### 🛍️ Recommended Affiliate Products")
                    st.markdown(result)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#555'>Tube Fellow © 2025 | Powered by GPT-4o</p>", unsafe_allow_html=True)