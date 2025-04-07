import json
import numpy as np
import os
import openai
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

FAQS_PATH = "src/faqs.json"
EMBEDDINGS_PATH = "src/faq_embeddings.npy"

# Cargar las FAQs desde un archivo JSON
def cargar_faqs():
    with open(FAQS_PATH, "r", encoding="utf-8") as f:
        faqs = json.load(f)
    return faqs

# Crear o cargar los embeddings de las FAQs
def obtener_o_cargar_embeddings(faqs):
    if os.path.exists(EMBEDDINGS_PATH):
        print("Cargando embeddings existentes...")
        faq_embeddings = np.load(EMBEDDINGS_PATH)
    else:
        print("Generando embeddings desde OpenAI...")
        faq_embeddings = []
        for faq in faqs:
            # Generamos el embedding para cada respuesta
            respuesta = openai.embeddings.create(
                input=faq["answer"], model="text-embedding-ada-002"
            )
            # Accedemos a los embeddings correctamente usando e.embedding
            faq_embeddings.append(np.array([e.embedding for e in respuesta.data])[0])
        faq_embeddings = np.array(faq_embeddings)
        np.save(EMBEDDINGS_PATH, faq_embeddings)
    return faq_embeddings

# Buscar la respuesta más similar
def buscar_respuesta_similar(pregunta, faqs):
    faq_embeddings = obtener_o_cargar_embeddings(faqs)
    
    # Generamos el embedding de la pregunta
    respuesta_pregunta = openai.embeddings.create(
        input=pregunta, model="text-embedding-ada-002"
    )
    # Accedemos al embedding de la pregunta usando e.embedding
    pregunta_embedding = np.array([e.embedding for e in respuesta_pregunta.data])[0]
    
    # Calculamos la similitud entre la pregunta y las FAQ
    sim = cosine_similarity([pregunta_embedding], faq_embeddings)
    
    # Obtenemos la FAQ más similar
    indice_similar = sim.argmax()
    respuesta_similar = faqs[indice_similar]['answer']  # Usamos "answer" porque es el formato correcto
    return respuesta_similar
