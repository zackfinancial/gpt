import os
import time
import yaml
import streamlit as st
from typing import List, Dict

# Optional: 'openai' package supports the modern Responses API.
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

st.set_page_config(page_title="Finance Services Chatbot", layout="wide")
st.title("💬 Finance Services Chatbot")
st.caption("Educational use only — not legal or tax advice.")

# --- Load services catalog ---
@st.cache_data
def load_services() -> List[Dict]:
    with open("services.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("services", [])

services = load_services()

# --- Sidebar config ---
st.sidebar.header("Firm Settings")
firm_name = st.sidebar.text_input("Firm name", os.environ.get("FIRM_NAME", "Zack Financial"))
contact_email = st.sidebar.text_input("Contact email", os.environ.get("CONTACT_EMAIL", "info@zackfinancial.com"))
model_name = st.sidebar.text_input("Model", os.environ.get("MODEL_NAME", "gpt-4o-mini"))

st.sidebar.markdown("---")
st.sidebar.write("**Deploy notes**: Set your `OPENAI_API_KEY` in Streamlit Secrets or as an environment variable on your host.")

# --- Initialize OpenAI client ---
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
if not OPENAI_API_KEY:
    st.warning("No OPENAI_API_KEY found. Add it in Streamlit secrets or as an environment variable to enable responses.")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and OpenAI else None

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a concise, friendly finance assistant for a CPA/Advisory firm. "
            "Answer questions clearly (aim for 5-8 sentences max), ask 1-2 clarifying questions when needed, "
            "and never provide legal/tax advice—stick to educational guidance only."
        )}
    ]

def simple_match_services(user_text: str, catalog: List[Dict], top_k: int = 3) -> List[Dict]:
    """Very simple keyword matcher (no embeddings to keep it free & generic)."""
    text = (user_text or "").lower()
    scored = []
    for svc in catalog:
        score = 0
        for kw in (svc.get("keywords") or []):
            if kw.lower() in text:
                score += 1
        score += sum(1 for w in (svc.get("name","") + " " + svc.get("summary","")).lower().split() if w in text)
        scored.append((score, svc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for sc, s in scored if sc > 0][:top_k] or catalog[:top_k]

# --- Chat UI ---
chat_container = st.container()
with chat_container:
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.chat_message("user").write(m["content"])
        elif m["role"] in ("assistant", "system"):
            if m["role"] == "assistant":
                st.chat_message("assistant").write(m["content"])

user_input = st.chat_input("Ask a finance question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    matched = simple_match_services(user_input, services, top_k=3)

    assistant_guidelines = f"""
    You are representing {firm_name}. The user's email contact is {contact_email}.

    Rules:
    - Be concise (5-8 sentences). Educational, not legal/tax advice.
    - If needed, ask up to 2 clarifying questions.
    """

    assistant_content = "I'm currently offline; please configure OPENAI_API_KEY to enable responses."
    if client:
        try:
            resp = client.responses.create(
                model=model_name,
                input=[
                    {"role": "system", "content": assistant_guidelines},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"]
                ],
            )
            if hasattr(resp, "output_text"):
                assistant_content = resp.output_text
            else:
                assistant_content = str(resp)
        except Exception as e:
            assistant_content = f"Error reaching the model: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    st.chat_message("assistant").write(assistant_content)

st.markdown("---")
st.caption(f"© {time.strftime('%Y')} {firm_name} — Educational information only.")
