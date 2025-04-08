from flask import Flask, request, jsonify, render_template
from embedding import cargar_faqs, obtener_o_cargar_embeddings, buscar_respuesta_similar

app = Flask(__name__)

# Cargar preguntas frecuentes y embeddings al iniciar
faqs = cargar_faqs()
faq_embeddings = obtener_o_cargar_embeddings(faqs)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    try:
        data = request.get_json()
        pregunta = data.get("pregunta", "").strip()

        if not pregunta:
            return jsonify({"respuesta": "Por favor, introduce una pregunta válida."})

        respuesta = buscar_respuesta_similar(pregunta, faqs)
        return jsonify({"respuesta": respuesta})

    except Exception as e:
        print(f"❌ Error general: {e}")
        return jsonify({"respuesta": "Ocurrió un error procesando tu pregunta."})

if __name__ == "__main__":
    app.run(debug=True)
