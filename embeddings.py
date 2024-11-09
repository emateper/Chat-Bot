from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def initialize_embeddings(pdf_paths=None):
    # Si no se proporcionan PDFs, se usa uno por defecto
    if pdf_paths is None:
        pdf_paths = [
            './resources/pdfcoffee.com_hoy-no-es-siempre-sabrina-critzmann-2-pdf-free.pdf',
            './resources/Protocolo Clínico ABM #37- Cuidado del bebé basado en la fisiología.pdf'
        ]
    
    all_documents = [] 
    
    # Procesar cada archivo PDF
    for pdf_path in pdf_paths:
        try:
            print(f"Cargando el archivo PDF: {pdf_path}")  
            loader = PyPDFLoader(file_path=pdf_path)
            doc = loader.load()
            print(f"Se cargaron {len(doc)} documentos del archivo '{pdf_path}'")  # Imprimir la cantidad de documentos cargados
            
            if doc:
                print(f"Primeros 500 caracteres del documento: {doc[0].page_content[:500]}")
            all_documents.extend(doc) 
        except Exception as e:
            print(f"Error al cargar el PDF '{pdf_path}': {e}")
            continue  # Si falla uno, seguimos con el siguiente
    
    if not all_documents:
        print("No se cargaron documentos de ningún PDF.")
        return None
    
    # Dividir los documentos en fragmentos de texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=200, 
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Dividir los documentos cargados en fragmentos
    text = text_splitter.split_documents(documents=all_documents)
    print(f"Se dividieron en {len(text)} fragmentos de texto.")
    
    # Generar los embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(text, embeddings)
    
    # Guardar el vectorstore localmente
    vectorstore.save_local("vectors")
    
    # Cargar los vectores
    try:
        loaded_vectors = FAISS.load_local("vectors", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error al cargar los vectores: {e}")
        return None
    
    return loaded_vectors




