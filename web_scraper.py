import requests
from bs4 import BeautifulSoup

# URL de la página de SAP
url = "https://www.sap.org.ar/novedades/novedades.html"

# Hacer una solicitud HTTP GET para obtener el contenido de la página
response = requests.get(url)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('a')  

    # Inicializamos una lista para almacenar los artículos
    articles = []

    for title in titles:
        title_text = title.get_text(strip=True)  
        content = title.find_next('p')  

        if content:
            content_text = content.get_text(strip=True)  # Extraer el texto del contenido
        else:
            content_text = "Contenido no disponible o no encontrado"

        # Almacenamos el título y el contenido en un diccionario
        articles.append({"title": title_text, "content": content_text})

    # Imprimir los resultados
    for idx, article in enumerate(articles, start=1):
        print(f"Artículo {idx}:")
        print(f"Título: {article['title']}")
        print(f"Contenido: {article['content']}")
        print("-" * 40)

else:
    print(f"Error al acceder a la página: {response.status_code}")
