import json
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FAQS_PATH = "src/faqs.json"
EMBEDDINGS_PATH = "src/faq_embeddings.npy"

# Cargar las FAQs desde un archivo JSON
def cargar_faqs():
    with open(FAQS_PATH, "r", encoding="utf-8") as f:
        faqs = json.load(f)
    return faqs

# Función para agregar una nueva pregunta manualmente
def agregar_pregunta_y_respuesta_nueva(pregunta, respuesta):
    # Primero agregamos la nueva pregunta al archivo JSON
    faqs = cargar_faqs()
    faqs.append({"question": "¿Cual es el rango de precios?", "answer": "Hay precios desde los 500€ hasta los 2000€. Apto para todos los bolsillos."})
    
    # Guardamos el JSON actualizado
    with open(FAQS_PATH, "w", encoding="utf-8") as f:
        json.dump(faqs, f, ensure_ascii=False, indent=4)
    
    # Luego generamos el embedding para la nueva pregunta y lo agregamos a los embeddings
    agregar_embedding_nueva_pregunta(pregunta)

def agregar_embedding_nueva_pregunta(pregunta):
    # Generar el embedding para la nueva pregunta
    respuesta_pregunta = client.embeddings.create(
        input=pregunta, model="text-embedding-ada-002"
    )
    pregunta_embedding = np.array(respuesta_pregunta['data'][0]['embedding'])
    
    # Cargar los embeddings existentes
    faq_embeddings = np.load("faq_embeddings.npy")
    
    # Agregar el nuevo embedding al archivo de embeddings
    faq_embeddings = np.append(faq_embeddings, [pregunta_embedding], axis=0)
    
    # Guardar el archivo de embeddings actualizado
    np.save("faq_embeddings.npy", faq_embeddings)
    print("Nuevo embedding añadido correctamente.")

# Crear o cargar los embeddings de las FAQs
def obtener_o_cargar_embeddings(faqs):
    if os.path.exists(EMBEDDINGS_PATH):
        print("✅ Cargando embeddings existentes...")
        return np.load(EMBEDDINGS_PATH)
    
    print("🧠 Generando embeddings desde OpenAI...")
    embeddings = []

    for faq in faqs:
        try:
            response = client.embeddings.create(
                input=faq["answer"],
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)
        except Exception as e:
            print(f"❌ Error al generar embedding: {e}")
            embeddings.append(np.zeros(1536))  # Relleno con ceros en caso de fallo

    embeddings = np.array(embeddings)
    np.save(EMBEDDINGS_PATH, embeddings)
    return embeddings

# Buscar la respuesta más similar o usar el modelo directamente
def buscar_respuesta_similar(pregunta, faqs):
    faq_embeddings = obtener_o_cargar_embeddings(faqs)

    if faq_embeddings is None or len(faq_embeddings) == 0:
        return "No se pudieron cargar los embeddings de las preguntas frecuentes."

    try:
        response = client.embeddings.create(
            input=pregunta,
            model="text-embedding-ada-002"
        )
        pregunta_embedding = np.array(response.data[0].embedding).reshape(1, -1)
    except Exception as e:
        print("❌ Error al generar embedding de la pregunta:", e)
        return "No se pudo procesar tu pregunta en este momento."

    if pregunta_embedding is None or faq_embeddings is None:
        return "No se pudieron obtener los datos necesarios para responder."

    try:
        sim = cosine_similarity(pregunta_embedding, faq_embeddings)
        mejor_indice = np.argmax(sim)
        mejor_similitud = sim[0, mejor_indice]

        if mejor_similitud < 0.5:
            # Si no hay coincidencia clara, responde con el modelo
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente para una tienda de ordenadores llamada JGMComponents."},
                    {"role": "user", "content": pregunta}
                ]
            )
            return completion.choices[0].message.content

        return faqs[mejor_indice]["answer"]

    except Exception as e:
        print("❌ Error al calcular similitud:", e)
        return "Hubo un error al procesar tu pregunta."
