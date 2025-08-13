import os
from openai import OpenAI
import streamlit as st

def _client():
    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )

def chat_with_tools(messages, tools, model=None):
    client = _client()
    model = model or st.secrets.get("MODEL", "openai/gpt-4o-mini")
    # Extra headers help with OpenRouter usage attribution
    extra_headers = {
        "HTTP-Referer": st.secrets.get("HTTP_REFERER", "http://localhost:8501"),
        "X-Title": st.secrets.get("X_TITLE", "Smart Finances Caribbean"),
    }
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.3,
        extra_headers=extra_headers
    )
    return resp.choices[0].message
