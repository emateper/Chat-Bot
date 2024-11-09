import streamlit as st
from main import *
from PIL import Image
import time

# Cargar imagen y configurar la página
img = Image.open("./resources/doctor.jpg")
st.set_page_config(page_title="Doc-Bot", page_icon=img)

# Crear columnas para el título y la imagen
col1, col2, col3 = st.columns([5, 1, 2])
with col1:
    st.title("Bot sobre pediatría y crianza")
with col2:
    pass  # Espacio vacío
with col3:
    st.image(img, width=200)
    

# Definir avatares
usuario = "🙂"
bot = "👨🏽‍⚕️"

# Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial en la aplicación
for message in st.session_state.messages:
    avatar = usuario if message["role"] == "user" else bot
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Definir un diccionario con los temas y sus respuestas
temas = {
    "Vacunación": """La vacunación es una medida fundamental para proteger a los niños contra enfermedades graves y prevenibles. 
                Sigue el calendario de vacunación recomendado por los profesionales de la salud 
                para garantizar la inmunización adecuada y la protección de tu hijo. 
                Siempre consulta con un pediatra para obtener información específica sobre las vacunas necesarias para tu hijo. """,
    
    "Crecimiento y desarrollo": """El crecimiento y desarrollo son procesos continuos y únicos en cada niño. 
                                Es importante monitorear los hitos del desarrollo, como gatear, caminar y hablar, 
                                para asegurarse de que tu hijo esté progresando adecuadamente. 
                                Si tienes preocupaciones sobre el crecimiento o desarrollo de tu hijo, 
                                consulta con un pediatra para obtener orientación y apoyo.""",
    "Emergencias": """En Argentina, el número de emergencias es 911. Si te encuentras en una situación de emergencia con un niño, 
                    llama a este número para recibir asistencia inmediata. Mantén la calma y 
                    sigue las instrucciones del operador para garantizar la mejor atención para el niño.""",
    "Consejos para padres": """1. Escucha activamente a tu hijo para comprender sus necesidades y emociones. 
                            2. Establece rutinas saludables para promover el bienestar físico y emocional de tu hijo. 
                            3. Fomenta un ambiente seguro y amoroso para que tu hijo se sienta apoyado y confiado. ▌"""
}

# Sección de Asistencia Rápida con botones dinámicos en el sidebar
st.sidebar.title("Asistencia rápida")
for tema, respuesta in temas.items():
    if st.sidebar.button(tema):  # Crear un botón para cada tema en el sidebar
        # Añadir consulta al historial
        st.session_state.messages.append({"role": "user", "content": f'Consulta: {tema}'})
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
    
if st.sidebar.button("Borrar historial"):
    st.session_state.messages = []
    chat_history = []
    memory.clear()
# Mostrar mensajes del historial actualizado en la parte principal
for message in st.session_state.messages:
    avatar = usuario if message["role"] == "user" else bot
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Aceptar entrada del usuario para una consulta personalizada
if prompt := st.chat_input("Ingrese su consulta:"):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=usuario):
        st.markdown(prompt)

    # Construir historial de chat
    chat_history = "\n".join([message["content"] for message in st.session_state.messages if message["role"] == "user"])

    # Mostrar respuesta del asistente
    with st.chat_message("assistant", avatar=bot):
        contenedor_respuesta = st.empty()
        full_response = ""

        respuesta = chatbot(prompt, chat_history)
        for chunk in respuesta.split():
            full_response += chunk + ' '
            time.sleep(0.10)  # Simulación de tiempo de respuesta
            contenedor_respuesta.markdown(full_response + "▌")

    # Añadir la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
