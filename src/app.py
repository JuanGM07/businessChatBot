from flask import Flask, render_template, request, jsonify
from embedding import buscar_respuesta_similar, cargar_faqs  # Asegúrate de tener esta función cargar_faqs

app = Flask(__name__)

# Cargar las FAQs desde el archivo antes de que lleguen las solicitudes
faqs = cargar_faqs()  # Esta función debería devolver tus FAQs cargadas

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta = data.get("pregunta")

    if not pregunta:
        return jsonify({"respuesta": "Por favor, escribe una pregunta válida."})

    try:
        # Pasar las FAQs a la función de búsqueda
        respuesta = buscar_respuesta_similar(pregunta, faqs)
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        print("❌ Error al procesar pregunta:", e)
        return jsonify({"respuesta": "Lo siento, hubo un error procesando tu pregunta."})

if __name__ == "__main__":
    app.run(debug=True)
