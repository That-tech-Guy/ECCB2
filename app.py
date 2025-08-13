import streamlit as st
from llm import chat_with_tools
from router import respond
from storage import ECCU_COUNTRIES, valid_email, save_user_profile, save_chat_log



st.set_page_config(page_title="Smart Finances Caribbean", page_icon="💬")
st.title("Smart Finances Caribbean – Unified Chatbot")

# --- Session bootstrap ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = None
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# --- Onboarding form (collect once) ---
def onboarding_form():
    with st.form("user_onboarding", clear_on_submit=False):
        st.subheader("👋 Quick Setup")
        name = st.text_input("Your name")
        country = st.selectbox("Your country (ECCU)", ECCU_COUNTRIES, index=ECCU_COUNTRIES.index("Montserrat") if "Montserrat" in ECCU_COUNTRIES else 0)
        email = st.text_input("Email (for progress + reports)")
        submitted = st.form_submit_button("Save & Continue")
        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
                return
            if not valid_email(email):
                st.error("Please enter a valid email address.")
                return
            st.session_state.profile = save_user_profile(name, country, email)
            st.success(f"Saved. Welcome, {name} from {country}!")
            st.rerun()

if not st.session_state.profile:
    onboarding_form()
    st.stop()

# --- Capability launcher (buttons) ---
st.markdown("### 🚀 What I can do")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💱 Currency Converter"):
        st.session_state.preset_prompt = "Convert XCD to USD (ask me for amount)."
        st.rerun()
    if st.button("🧠 ECCU Quiz"):
        # Show difficulty buttons inline
        st.session_state.preset_prompt = None  # will be set by radios below
with c2:
    if st.button("📊 Budget Planner"):
        st.session_state.preset_prompt = "Create a budget. Ask me for income and expenses."
        st.rerun()
    if st.button("🌍 Investing Guide"):
        st.session_state.preset_prompt = "I want investment education. Ask my risk and horizon."
        st.rerun()
with c3:
    if st.button("🧵 Side Hustles"):
        st.session_state.preset_prompt = "Suggest side hustles; start by asking if I prefer remote and low-cost."
        st.rerun()
    if st.button("🚨 Scam Checker"):
        st.session_state.preset_prompt = "Teach me about common scams in my ECCU country."
        st.rerun()

# Difficulty selector for quiz (renders whenever chosen)
with st.expander("🧠 ECCU Quiz difficulty", expanded=False):
    lvl = st.radio("Pick a level", ["easy","hard","big_leagues"], horizontal=True, index=0)
    if st.button("Start Quiz"):
        # Craft a clear user message so the router picks start_quiz with our level & country
        country = st.session_state.profile["country"]
        st.session_state.preset_prompt = f"Start ECCU financial literacy quiz at level='{lvl}' for country='{country}'."
        st.rerun()

# --- Show chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle preset prompt triggers (from buttons) ---
if st.session_state.preset_prompt:
    # Inject as a user message and process immediately
    preset = st.session_state.preset_prompt
    st.session_state.preset_prompt = None
    st.session_state.messages.append({"role":"user","content":preset})
    with st.chat_message("user"): st.markdown(preset)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            text, trace = respond(st.session_state.messages, chat_with_tools)
            st.markdown(text)
            st.session_state.messages.append({"role":"assistant","content":text})
    # Save chat after each turn
    save_chat_log(st.session_state.profile["email"], st.session_state.messages)

# --- Regular chat input ---
user_input = st.chat_input("Ask anything (or use the buttons above)…")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            text, trace = respond(st.session_state.messages, chat_with_tools)
            st.markdown(text)
            st.session_state.messages.append({"role":"assistant","content":text})

    # Save chat log tied to the user
    save_chat_log(st.session_state.profile["email"], st.session_state.messages)
