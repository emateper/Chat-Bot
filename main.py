import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferWindowMemory
from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from embeddings import initialize_embeddings  
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")
load_dotenv()


pdf_paths = [
    './resources/pdfcoffee.com_hoy-no-es-siempre-sabrina-critzmann-2-pdf-free.pdf',
    './resources/Protocolo Clínico ABM #37- Cuidado del bebé basado en la fisiología.pdf'
]

# Inicializar datos (esto debe hacerse una sola vez al inicio)
loaded_vectors = initialize_embeddings(pdf_paths=pdf_paths)

# Crear memoria para agente
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=4,
    return_messages=True,
    chat_memory=ChatMessageHistory()
)

# Crear herramienta de búsqueda
busqueda_libro_pediatria = create_retriever_tool(
    retriever=loaded_vectors.as_retriever(),
    name='busqueda_libro_pediatria',
    description="Busca informacion dentro del libro Hoy no es siempre y del PDF sobre Fisiología"
)

# Función para realizar scraping de la página de SAP utilizando BeautifulSoup
def scrape_sap_articles(query=""):
    
    response = requests.get("https://www.sap.org.ar/novedades/novedades.html")

    
    if response.status_code != 200:
        return ["Error al acceder a la página"]

    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    news_items = soup.find_all('div', class_='news_item')

    for news_item in news_items:
        title = news_item.find('h3')
        title_text = title.get_text(strip=True) if title else "Título no disponible"

        content = news_item.find('p')
        content_text = content.get_text(strip=True) if content else "Contenido no disponible"

        articles.append({"title": title_text, "content": content_text})

    if query:
        result = []
        for article in articles:
            if query.lower() in article["title"].lower():
                result.append(f"Título: {article['title']}\nContenido: {article['content']}")
        return result if result else ["No se encontraron artículos relevantes."]

    return articles  

# Crear una clase para la herramienta de scraping que sea compatible con Langchain
class ScrapSAPTool(Tool):
    def __init__(self, name: str, description: str, func):
        super().__init__(name=name, description=description, func=func)
        self.func = func

    def _run(self, query: str):
        return self.func(query)

    async def _arun(self, query: str):
        return self.func(query)

# Crear la herramienta de scraping y agregarla a las herramientas del agente
scrap_sap_tool = ScrapSAPTool(name="scraping_sap", description="Realiza scraping de los artículos en la página SAP", func=scrape_sap_articles)
tools = [busqueda_libro_pediatria, scrap_sap_tool]

# Definir el prompt para el agente
prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages[0].prompt.template = """
Eres un asistente virtual llamado Doc-Bot especializado en pediatría y crianza. Tu objetivo es ayudar a los padres, cuidadores y profesionales de la salud a comprender mejor el desarrollo infantil, las necesidades de los niños y proporcionar consejos prácticos basados en conocimientos médicos y psicológicos sobre el cuidado infantil. 
Responde de manera amigable, empática y profesional, siempre considerando el bienestar y la seguridad del niño. 

Por favor, ten en cuenta que tu audiencia puede ser diversa, desde padres primerizos hasta profesionales con experiencia. Si la pregunta es compleja, intenta dar explicaciones claras y accesibles sin perder la precisión.

Ejemplos de cómo responder:
1. Si un usuario pregunta sobre la alimentación de un bebé de 6 meses, puedes responder con una recomendación general, indicando cuándo es adecuado introducir alimentos sólidos, y también mencionar señales de alerta.
2. Si se trata de una consulta sobre el desarrollo motor de un niño, ofrece información sobre los hitos típicos y cuándo podría ser necesario buscar la opinión de un especialista.
3. Si la consulta trata sobre algo urgente, trata de ser expeditivo y resumir tu respuesta

Responde siempre con confianza y empatía, y evita dar consejos médicos sin una base científica. Si la pregunta está fuera de tu alcance, indica amablemente que se consulte con un profesional.
"""

# Crear agente
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)  # Asegúrate de que el modelo está correctamente definido
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# Función para el chatbot
def chatbot(query: str, chat_history):
    response = agent_executor.invoke({'input': f'{query}', "chat_history": chat_history})['output']
    return response

