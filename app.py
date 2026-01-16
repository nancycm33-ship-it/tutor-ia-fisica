import streamlit as st
import google.generative_ai as genai

st.set_page_config(page_title="Tutor Física ITVM", page_icon="🎓")

st.title("🎓 Tutor Virtual de Física")
st.write("Dra. Nancy: Hazme preguntas sobre los apuntes o el programa.")

# Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los secretos de Streamlit.")

# Instrucciones del sistema
sys_prompt = """
Eres un tutor experto en Física y Agronomía del ITVM. 
Responde dudas basándote en principios físicos claros. 
Sé amable y guía al alumno paso a paso.
"""

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=sys_prompt)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "parts": ["¡Hola! ¿En qué tema de física te ayudo hoy?"]}]

for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(role).write(msg["parts"][0])

# Chat
if prompt := st.chat_input("Escribe tu duda..."):
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    st.chat_message("user").write(prompt)
    
    try:
        chat = model.start_chat(history=st.session_state.messages)
        response = chat.send_message(prompt)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
