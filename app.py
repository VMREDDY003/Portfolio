import os
from dotenv import load_dotenv
import streamlit as st
import requests
import smtplib
from email.message import EmailMessage
import markdown2

# ------------------------------
# CONFIGURATION
# ------------------------------
load_dotenv()  # Loads variables from .env into environment

GITHUB_USERNAME = st.secrets["GITHUB_USERNAME"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
PROFILE_IMAGE = "123444116.jpg"  # Update path if needed

# ------------------------------
# FUNCTIONS
# ------------------------------

def send_email(name, sender_email, message):
    try:
        msg = EmailMessage()
        msg['Subject'] = f'Portfolio Contact from {name}'
        msg['From'] = sender_email
        msg['To'] = EMAIL
        msg.set_content(f"Sender: {name} <{sender_email}>\n\nMessage:\n{message}")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        st.error("GitHub API rate limit exceeded. Please try again later.")
        return []
    else:
        st.error(f"GitHub API error: {response.status_code} - {response.reason}")
        return []

def fetch_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def generate_ai_summary(repo_name):
    return f"\U0001F6A7 *No README available*. This project, **{repo_name}**, appears to be a data-focused repository by Malleswara. Check the code for more info."

# ------------------------------
# THEME SELECTION (WITHOUT Default theme)
# ------------------------------

st.sidebar.markdown("## 🎨 Theme")
theme = st.sidebar.selectbox("Choose a theme", ["Dark", "Ocean", "Forest", "Light"])

THEMES = {
    "Dark": {"bg": "#1e1e1e", "text": "#ffffff", "input_bg": "#2c2c2c", "input_text": "#ffffff"},
    "Ocean": {"bg": "#005f73", "text": "#ffffff", "input_bg": "#0a9396", "input_text": "#ffffff"},
    "Forest": {"bg": "#2e8b57", "text": "#ffffff", "input_bg": "#3cb371", "input_text": "#ffffff"},
    "Light": {"bg": "#ffffff", "text": "#000000", "input_bg": "#f0f0f0", "input_text": "#000000"},
}

bg_color = THEMES.get(theme, THEMES["Light"])["bg"]
text_color = THEMES.get(theme, THEMES["Light"])["text"]
input_bg = THEMES.get(theme, THEMES["Light"])["input_bg"]
input_text = THEMES.get(theme, THEMES["Light"])["input_text"]

# ------------------------------
# SIDEBAR
# ------------------------------

st.sidebar.image(PROFILE_IMAGE, use_container_width=True)
st.sidebar.markdown(f"""
<h2 style='text-align: center;'>Malleswara Reddy</h2>
<h4 style='text-align: center; color: gray;'>Data Analyst</h4>
<p style='text-align: center;'>Transforming raw data into impactful insights to support decision-making and business growth.</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<h4>🛠 Skills</h4>
<ul>
<li><strong>SQL</strong> – Data querying and manipulation</li>
<li><strong>Power BI</strong> – Interactive dashboards & visualizations</li>
<li><strong>Tableau</strong> – Business storytelling with data</li>
<li><strong>Python</strong> – Data analysis, Pandas, NumPy, matplotlib</li>
<li><strong>Machine Learning</strong> – Basic models and use-cases</li>
<li><strong>Excel</strong> – Formulas, pivot tables, and automation</li>
</ul>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<h4>📬 Contact Me</h4>", unsafe_allow_html=True)

with st.sidebar.form("contact_form", clear_on_submit=True):
    name = st.text_input("Your Name")
    sender_email = st.text_input("Your Email")
    message = st.text_area("Message")
    if st.form_submit_button("Send"):
        if not name or not sender_email or not message:
            st.error("Please fill in all fields.")
        else:
            if send_email(name, sender_email, message):
                st.success("Message sent successfully! I will get back to you soon.")

# ------------------------------
# MAIN PAGE
# ------------------------------

st.title("👋 Welcome to My Portfolio")
st.markdown(f"""
<p style='font-size:18px; font-weight:500;'>
I’m <strong>Malleswara Reddy</strong>, a passionate <span style='color:#4CAF50'>Data Enthusiast</span> who transforms numbers into <em>compelling narratives</em>. Equipped with expertise in analytics tools and business intelligence, I help companies make <strong>data-driven decisions</strong>.
</p>
""", unsafe_allow_html=True)

st.markdown("## 🚀 Projects from GitHub")

# Add a Refresh button
if st.button("🔄 Refresh Projects"):
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("Streamlit version does not support rerun.")

repos = fetch_repos(GITHUB_USERNAME)
if repos:
    for repo in repos:
        st.markdown(f"### [{repo['name']}]({repo['html_url']})")
        description = repo.get("description", "")
        st.markdown(description if description else "_No description provided._")

        readme = fetch_readme(GITHUB_USERNAME, repo['name'])
        if readme:
            with st.expander("📘 View README"):
                html = markdown2.markdown(readme, extras=["fenced-code-blocks"])
                st.markdown(html, unsafe_allow_html=True)
        else:
            st.info(generate_ai_summary(repo['name']))

        st.markdown("---")
else:
    st.warning("No repositories found or failed to fetch.")

# ------------------------------
# STYLING
# ------------------------------

st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    h1, h2, h3, h4, h5, h6, p, li, span, div, label,
    .stTextInput>div>div>input,
    .stTextArea>div>textarea {{
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {bg_color};
        color: {text_color};
    }}
    input, textarea {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border-radius: 6px;
        padding: 0.5rem;
        width: 100%;
        border: 1px solid #ccc;
    }}
    header[data-testid="stHeader"] {{
        background-color: #ffffff00;
    }}
</style>
""", unsafe_allow_html=True)
