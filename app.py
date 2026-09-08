import os
import requests
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

def whatsapp_credentials():
    """Reads Meta WhatsApp Cloud API credentials from env vars or Streamlit Secrets.
    Set these in .streamlit/secrets.toml (locally) or in your Streamlit Cloud app's
    Settings -> Secrets (in production). Never hardcode them in this file.
    """
    token = os.getenv("WHATSAPP_TOKEN", "")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    try:
        token = token or st.secrets.get("WHATSAPP_TOKEN", "")
        phone_id = phone_id or st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "")
        wa_cfg = st.secrets.get("whatsapp", {})
        token = token or wa_cfg.get("token", "")
        phone_id = phone_id or wa_cfg.get("phone_number_id", "")
    except Exception:
        pass
    return str(token), str(phone_id)

WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID = whatsapp_credentials()
GRAPH_API_VERSION = "v20.0"

def _graph_url():
    return f"https://graph.facebook.com/{GRAPH_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

def send_whatsapp_text(to, body):
    """Send a free-form text message. Only works within the 24h customer
    service window (i.e. the recipient messaged your number in the last 24h).
    `to` must be in international format with no + or leading zeros, e.g. 919845011223.
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        return False, "WhatsApp Cloud API is not configured. Add WHATSAPP_TOKEN and WHATSAPP_PHONE_NUMBER_ID to Streamlit Secrets."
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    try:
        r = requests.post(_graph_url(), headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json()
    except Exception as e:
        return False, str(e)

def send_whatsapp_template(to, template_name, lang_code="en_US", body_params=None):
    """Send a pre-approved template message. Required for the first message to a
    user, or any time outside the 24h session window. `template_name` must match
    a template already approved in Meta Business Manager.
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        return False, "WhatsApp Cloud API is not configured. Add WHATSAPP_TOKEN and WHATSAPP_PHONE_NUMBER_ID to Streamlit Secrets."
    components_payload = []
    if body_params:
        components_payload.append({
            "type": "body",
            "parameters": [{"type": "text", "text": p} for p in body_params],
        })
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": lang_code},
            "components": components_payload,
        },
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    try:
        r = requests.post(_graph_url(), headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json()
    except Exception as e:
        return False, str(e)

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
 color:#fff;
 position:relative; overflow-x:hidden;
}
.stApp:before, .stApp:after{
 content:''; position:fixed; border-radius:50%; filter:blur(60px); z-index:0; pointer-events:none;
 animation:blobfloat 14s ease-in-out infinite;
}
.stApp:before{ width:340px; height:340px; background:rgba(30,180,255,.20); top:-80px; left:-100px; }
.stApp:after{ width:280px; height:280px; background:rgba(70,90,255,.16); bottom:-60px; right:-80px; animation-delay:-7s; }
@keyframes blobfloat{
 0%,100%{ transform:translate(0,0) scale(1); }
 50%{ transform:translate(30px,-25px) scale(1.08); }
}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent!important; box-shadow:none!important;}
div[data-testid="stDecoration"]{display:none!important;}
.brand{text-align:center;margin:18px 0 27px; position:relative; z-index:1;}
.logo{
 width:78px;height:78px;margin:auto;border-radius:50% 50% 50% 60%/55% 55% 45% 45%;
 background:radial-gradient(circle at 32% 28%,#a6f8ff 0 9%,transparent 10%),
 radial-gradient(circle at 68% 65%,#168cff 0 26%,transparent 27%),
 radial-gradient(circle at 45% 47%,#00c9ff 0 34%,transparent 35%),
 linear-gradient(145deg,#6df3ff,#0aa2ff 55%,#2946e0);
 box-shadow:0 0 32px rgba(40,225,255,.55),0 0 80px rgba(0,120,255,.28);
 animation:blobmorph 6s ease-in-out infinite;
}
@keyframes blobmorph{
 0%,100%{ border-radius:50% 50% 50% 60%/55% 55% 45% 45%; transform:rotate(-6deg); }
 50%{ border-radius:60% 45% 55% 50%/50% 60% 45% 55%; transform:rotate(4deg); }
}
.brand h2{font-size:31px;margin:16px 0 5px;font-weight:800;letter-spacing:-1px}
.brand h2 span{color:#43eaff}
.brand p{color:#8fa8b8;font-size:13px;margin:0}
.card{
 padding:34px 38px 30px;border-radius:28px;
 border:1px solid rgba(125,220,255,.28);
 background:linear-gradient(145deg,rgba(40,75,94,.42),rgba(5,25,40,.72));
 box-shadow:0 35px 90px rgba(0,0,0,.45),0 0 45px rgba(0,190,255,.08);
 backdrop-filter:blur(28px);
 position:relative; z-index:1;
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
 border-radius:10px!important;min-height:38px!important;
 font-weight:600!important;font-size:13.5px!important;
 background:#141B2E!important; color:#E7ECF5!important;
 border:1px solid rgba(255,255,255,.14)!important;
}
div.stButton>button:hover{background:#1B2338!important; border-color:rgba(255,255,255,.22)!important;}
div.stButton>button[kind="primary"]{
 background:linear-gradient(100deg,#19dfff,#098dff 55%,#2760ff)!important;
 color:#fff!important; border:none!important;
}
div.stButton>button[kind="primary"]:hover{filter:brightness(1.08);}
div[data-testid="stExpander"]{
 background:#141B2E!important; border:1px solid rgba(255,255,255,.10)!important;
 border-radius:14px!important; margin-bottom:16px!important; overflow:hidden;
}
div[data-testid="stExpander"] summary{
 color:#E7ECF5!important; font-weight:600!important; padding:14px 18px!important;
}
div[data-testid="stExpander"] summary:hover{background:rgba(255,255,255,.04)!important;}
div[data-testid="stExpander"] svg{color:#8A96AC!important;}
.login-wrap div.stButton>button{
 width:100%;min-height:52px;border-radius:16px!important;
 border:1px solid rgba(130,235,255,.35)!important;
 background:linear-gradient(100deg,#19dfff,#098dff 55%,#2760ff)!important;
 color:white!important;font-weight:750!important;font-size:15px!important;
 box-shadow:0 10px 28px rgba(0,153,255,.24)!important;transition:.2s!important
}
.login-wrap div.stButton>button:hover{transform:translateY(-2px)}
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
.forgot-link{font-size:12px;color:#43ddff;text-align:right;margin-top:-2px}
.remember-row{display:flex;align-items:center;justify-content:space-between;margin-top:-8px}
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
    st.markdown("""
    <style>
    .block-container{max-width:650px!important; margin:0 auto!important; padding:35px 18px 60px!important;}
    </style>
    <div class="login-wrap">
    """, unsafe_allow_html=True)
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
    rc1, rc2 = st.columns([1, 1])
    with rc1:
        st.checkbox("Remember me")
    with rc2:
        st.markdown('<div class="forgot-link">Forgot password?</div>', unsafe_allow_html=True)

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
    st.markdown("""
    <style>
    .block-container{max-width:100%!important; padding:2.5rem 18px 0!important;}
    </style>
    """, unsafe_allow_html=True)
    top = st.columns([10, 1])
    with top[1]:
        if st.button("Sign out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    with st.expander("📲  Send a real WhatsApp message (Meta Cloud API)", expanded=False):
        if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
            st.warning(
                "WhatsApp Cloud API isn't connected yet. Add **WHATSAPP_TOKEN** and "
                "**WHATSAPP_PHONE_NUMBER_ID** to your Streamlit Secrets to enable real sending. "
                "The dashboard below stays fully usable as a demo in the meantime."
            )
        else:
            st.success("WhatsApp Cloud API is connected.")

        msg_type = st.radio("Message type", ["Text (24h session only)", "Template (first contact / anytime)"], horizontal=True)
        to_number = st.text_input("Recipient (international format, no + or leading 0)", placeholder="919845011223")

        if msg_type.startswith("Text"):
            body = st.text_area("Message", placeholder="Hello! This is a message from DV Analytics.")
            if st.button("Send text message", type="primary"):
                if not to_number or not body:
                    st.error("Enter both a recipient number and a message.")
                else:
                    ok, result = send_whatsapp_text(to_number, body)
                    if ok:
                        st.success(f"Sent! Message ID: {result.get('messages', [{}])[0].get('id', 'unknown')}")
                    else:
                        st.error(f"Failed to send: {result}")
        else:
            template_name = st.text_input("Template name (must be approved in Meta Business Manager)", placeholder="hello_world")
            lang_code = st.text_input("Language code", value="en_US")
            params_raw = st.text_input("Body variables, comma-separated (optional)", placeholder="Ananya, ₹18500, 30 Aug 2026")
            if st.button("Send template message", type="primary"):
                if not to_number or not template_name:
                    st.error("Enter both a recipient number and a template name.")
                else:
                    params = [p.strip() for p in params_raw.split(",") if p.strip()] if params_raw else None
                    ok, result = send_whatsapp_template(to_number, template_name, lang_code, params)
                    if ok:
                        st.success(f"Sent! Message ID: {result.get('messages', [{}])[0].get('id', 'unknown')}")
                    else:
                        st.error(f"Failed to send: {result}")

    dashboard_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        dashboard_html = f.read()
    components.html(dashboard_html, height=1400, scrolling=True)

if st.session_state.authenticated:
    app()
else:
    login()
