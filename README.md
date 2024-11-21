# DOC-BOT
## Bot de Pediatría y Crianza

**Fecha**: 06/11/2024  
**Autor**: Emanuel A. Teper  
**Ubicación**: Buenos Aires, Argentina

---

## 1. Introducción

### Descripción general:
Este bot está diseñado para proporcionar consejos de salud pediátrica, responder preguntas frecuentes sobre enfermedades comunes, guiar a los padres, madres y cuidadores de niños sobre cuidados básicos y derivar casos graves a profesionales médicos.

### Objetivo:
Mejorar el acceso a información médica confiable para padres, madres y cuidadores de niños.

### Público objetivo:
- Madres, padres, cuidadores, tutores y personal de la salud.

---

## 2. Arquitectura

1. **Interfaz de usuario (UI)**:  
   Contiene una interfaz de usuario simple, un chat con preguntas y respuestas bien definidas. También tiene botones de acceso rápido a consultas y un botón para borrar el historial.

2. **Backend**:  
   En esta sección se encuentran tres archivos principales:
   - **main.py**: Se encarga de reunir todos los módulos del backend, aplicar la toma de decisiones y generar las respuestas.
   - **embeddings.py**: Gestiona el proceso de creación y uso de *embeddings* (representaciones vectoriales) de texto, fundamentales para el funcionamiento del bot.
   - **web scraping**: Se encarga de adquirir información de una web específica para mantener siempre actualizado al bot.

3. **Bot de IA**:  
   El motor de inteligencia artificial es **GPT-3.5-Turbo**.

---

## 3. Interacción del Usuario con el Bot

### Flujo de conversación:
El bot interactúa con el usuario de la siguiente manera:
1. Si un usuario pregunta **"¿cómo saber si mi hijo tiene fiebre?"**, el bot podría responder con una serie de preguntas relacionadas y luego proporcionar consejos.

### Sugerencias de preguntas frecuentes:
Los usuarios pueden hacer preguntas como:
- "¿Qué hacer si mi hijo tiene tos?"
- "¿Cómo saber si mi bebé tiene cólicos?"
- "¿Cuál es la dosis correcta de paracetamol para un niño?"

---


1. **Abrir terminal** y ejecutar el siguiente comando:
   ```bash
   python -m venv env

2. **Activar el env**:
   ```bash
   env/scripts/activate
3.  Si nos da un error por falta de autorización ejecutamos como administrador
el siguiente comando en el PowerShell de Windows:
   ```bash
      Set-ExecutionPolicy RemoteSigned -Scope LocalMachine
   ```
luego apretamos "s" para confirmar, luego repetimos el paso 2

4. **Instalar las dependencias con el comando**: 
   ```bash
      pip install -r requirements.txt
6. Ejecutar
   ```bash 
    streamlit run .\app_1.py

**RECUERDEN PONER SU API KEY**


<h2>MUCHAS GRACIAS POR USAR DOC-BOT!!!!</h2>
