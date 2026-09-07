import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DV Analytics • Campaign Studio", page_icon="🔷", layout="wide")

def credentials():
    user = os.getenv("APP_USERNAME", "")
    pwd = os.getenv("APP_PASSWORD", "")
    try:
        user = user or st.secrets.get("APP_USERNAME", "")
        pwd = pwd or st.secrets.get("APP_PASSWORD", "")
        app_cfg = st.secrets.get("app", {})
        user = user or app_cfg.get("username", "")
        pwd = pwd or app_cfg.get("password", "")
    except Exception:
        pass
    return str(user), str(pwd)

APP_USERNAME, APP_PASSWORD = credentials()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{font-family:Inter,sans-serif!important}
.stApp{
 min-height:100vh;
 background:radial-gradient(circle at 50% 12%,rgba(0,210,255,.18),transparent 28%),
 radial-gradient(circle at 10% 85%,rgba(25,100,255,.14),transparent 30%),
 linear-gradient(145deg,#061421,#092a40 52%,#03111e);
 color:#fff
}
#MainMenu,footer{visibility:hidden}
.block-container{padding:14px 18px 0!important; max-width:100% !important}
.login-wrap{max-width:650px;margin:0 auto;padding:35px 18px 60px}
.brand{text-align:center;margin:18px 0 27px}
.logo{
 width:76px;height:76px;margin:auto;border-radius:25px;
 background:radial-gradient(circle at 30% 30%,#8df8ff 0 7%,transparent 8%),
 radial-gradient(circle at 65% 62%,#168cff 0 22%,transparent 23%),
 radial-gradient(circle at 45% 47%,#00c9ff 0 31%,transparent 32%),
 linear-gradient(145deg,#54f1ff,#087dff 55%,#2735c7);
 box-shadow:0 0 28px rgba(40,225,255,.5),0 0 70px rgba(0,120,255,.25);
 transform:rotate(-7deg)
}
.brand h2{font-size:31px;margin:16px 0 5px;font-weight:800;letter-spacing:-1px}
.brand h2 span{color:#43eaff}
.brand p{color:#8fa8b8;font-size:13px;margin:0}
.card{
 padding:34px 38px 30px;border-radius:28px;
 border:1px solid rgba(125,220,255,.28);
 background:linear-gradient(145deg,rgba(40,75,94,.48),rgba(5,25,40,.78));
 box-shadow:0 35px 90px rgba(0,0,0,.45),0 0 45px rgba(0,190,255,.08);
 backdrop-filter:blur(24px)
}
.welcome{text-align:center}
.welcome h1{font-size:27px;margin:0;font-weight:750}
.welcome p{color:#8ea6b5;font-size:14px;margin:9px 0 24px}
div[data-testid="stTextInput"]{margin-bottom:10px}
div[data-testid="stTextInput"] label{display:none!important}
div[data-testid="stTextInput"]>div>div{
 border:1px solid rgba(155,216,239,.18)!important;
 border-radius:15px!important;background:rgba(255,255,255,.055)!important
}
div[data-testid="stTextInput"]>div>div:focus-within{
 border-color:rgba(47,218,255,.7)!important;
 box-shadow:0 0 0 3px rgba(47,218,255,.08)!important
}
div[data-testid="stTextInput"] input{
 color:#f5fbff!important;background:transparent!important;
 font-size:14px!important;height:52px!important;padding:0 17px!important
}
div[data-testid="stTextInput"] input::placeholder{color:#7f98a8!important}
div[data-testid="stCheckbox"] label{color:#91a6b4!important;font-size:12px!important}
div.stButton>button{
 width:100%;min-height:52px;border-radius:16px!important;
 border:1px solid rgba(130,235,255,.35)!important;
 background:linear-gradient(100deg,#19dfff,#098dff 55%,#2760ff)!important;
 color:white!important;font-weight:750!important;font-size:15px!important;
 box-shadow:0 10px 28px rgba(0,153,255,.24)!important;transition:.2s!important
}
div.stButton>button:hover{transform:translateY(-2px)}
.oauth div.stButton>button{
 background:rgba(255,255,255,.06)!important;
 border:1px solid rgba(173,217,235,.16)!important;
 box-shadow:none!important;color:#dcecf4!important
}
.divider{display:flex;align-items:center;gap:12px;margin:19px 0 15px;color:#718997;font-size:11px}
.divider:before,.divider:after{content:"";height:1px;flex:1;background:rgba(154,210,231,.12)}
.bottom{text-align:center;color:#708b99;font-size:11px;margin-top:20px;line-height:1.6}
.bottom b{color:#43ddff}
.error{background:rgba(255,65,100,.08);border:1px solid rgba(255,90,120,.3);color:#ffb0be;border-radius:12px;padding:10px;font-size:12px;margin:12px 0}
@media(max-width:600px){.card{padding:28px 20px}.brand h2{font-size:27px}}
</style>
""", unsafe_allow_html=True)

def brand():
    st.markdown("""
    <div class="brand">
      <div class="logo"></div>
      <h2><span>DV</span> Analytics</h2>
      <p>AI • Data • Technology</p>
    </div>
    """, unsafe_allow_html=True)

def login():
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    brand()
    st.markdown("""
    <div class="card">
      <div class="welcome">
        <h1>Welcome back</h1>
        <p>Good to see you. Dive back in.</p>
      </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Email", placeholder="Email or username",
                             label_visibility="collapsed")
    password = st.text_input("Password", placeholder="Password", type="password",
                             label_visibility="collapsed")
    st.checkbox("Remember me")

    if st.button("Sign in", type="primary", use_container_width=True):
        if not APP_USERNAME or not APP_PASSWORD:
            st.error("Credentials are not configured. Add APP_USERNAME and APP_PASSWORD to Streamlit Secrets.")
        elif username.strip() == APP_USERNAME and password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown('<div class="error">Incorrect email/username or password. Please try again.</div>',
                        unsafe_allow_html=True)

    st.markdown('<div class="divider">or continue with</div><div class="oauth">',
                unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        if st.button("🌐  Google", use_container_width=True):
            st.info("Google OAuth can be connected here.")
    with b:
        if st.button("  Apple", use_container_width=True):
            st.info("Apple OAuth can be connected here.")
    st.markdown("""
      </div>
      <div class="bottom">New here? <b>Create account</b><br><br>
      🔒 Never store passwords directly in your GitHub source code.</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def app():
    top = st.columns([6, 1])
    with top[1]:
        if st.button("Sign out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    dashboard_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        dashboard_html = f.read()
    components.html(dashboard_html, height=1400, scrolling=True)

if st.session_state.authenticated:
    app()
else:
    login()
