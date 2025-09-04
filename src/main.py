from dotenv import load_dotenv

import streamlit as st
import json
import os
import requests


load_dotenv()
N8N_URL = os.getenv("N8N_URL")



if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.correct_answer = None
    st.session_state.explanation = None
    st.session_state.options = []

def get_new_question():
    response = requests.post(N8N_URL,data={"query" : ""})
    raw_text = response.text 


    # Intentar parsear el JSON
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        st.error("❌ Gemini devolvió algo que no es JSON")
        st.write("Respuesta cruda:", raw_text)
        return

    st.session_state.question = data["question"]
    st.session_state.options = data["options"]
    st.session_state.correct_answer = data["correct_answer"]
    st.session_state.explanation = data["explanation"]

if st.button("Nueva Pregunta") or st.session_state.question is None:
    get_new_question()

st.title("🐍 Programación con Python")


st.subheader(st.session_state.question)


selected = st.radio("Elige una opción:", st.session_state.options)

if st.button("Responder"):
    if selected == st.session_state.correct_answer:
        st.success("🎉 ¡Bien hecho! Ganaste un caramelo 🍬")
        st.balloons()
        st.session_state.question = None  
    else:
        st.error("❌ Ops, casi...")
        st.info(f"👉 Explicación: {st.session_state.explanation}")
