# Business Chat Bot

[![Screenshot-from-2025-04-08-12-00-28.png](https://i.postimg.cc/BZpTf0JN/Screenshot-from-2025-04-08-12-00-28.png)](https://postimg.cc/grwX31X6)

Este chatbot de negocio es fácil de integrar en tu web: solo necesitas agregar tus preguntas y respuestas en el archivo /src/faqs.json, luego generar los embeddings ejecutando el script /src/app.py. Con esta simple configuración, el chatbot podrá responder automáticamente a las consultas de los usuarios, usando la tecnología de OpenAI para respuestas más complejas cuando no se encuentra una coincidencia directa. Ideal para ofrecer soporte 24/7 sin complicaciones adicionales. Todo el código está en mi GitHub. Para cualquier problema o propuesta: juanglezm3@gmail.com

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Vas a necesitar una api-key:

* [OpenAI Api Key](https://platform.openai.com/api-keys) -> Enlace para obtenerla.

En primer lugar crea un archivo .env, ahí guardaras tus claves con el siguiente par clave valor:

* OPENAI_API_KEY = "tu_api_key" (esta será tu api_key de OPenAI, no cambies el nombre)

### Pre-requisitos 📋

Todos los requerimientos estan en requirements.txt:
```bash
  pip install -r requirements.txt
```
He utilizado python 3.12.3, para perfecta compatibilidad utilizar misma versión.

### Instalación 🔧

_Creamos un virtual environment_

_Linux/MacOS:_

```
python3 -m venv nombre_venv
source nombre_venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

_Windows_

```
python3 -m venv nombre_venv
nombre venv\Scripts\activate.bat
pip install -r requirements.txt
python3 app.py
```

_Ya tendrias la herramienta corriendo en tu maquina local_

## Construido con 🛠️

* [Flask](https://flask.palletsprojects.com/en/stable/) - El framework web usado
* [OpenAI](https://platform.openai.com/docs/overview) - Análisis del modelo GPT
* [sklearn](https://scikit-learn.org/stable/) - Calcular la similitud entre las preguntas del usuario y las respuestas almacenadas en el archivo faqs.json, utilizando la función cosine_similarity


## Licencia 📄

Mira el archivo [LICENSE.md](LICENSE.md) para detalles. Si quieres usar esta herramienta para tu uso personal, agrega un enlace a este repositorio en tu readme por favor. Espero que sea de utilidad.

## Mis redes sociales 🌐

* Comenta a otros sobre este proyecto 📢
* Mis redes sociales son: 
* [Tiktok](https://www.tiktok.com/@jgmdev) 
* [Linkedin](https://www.linkedin.com/in/jgmdatascience/) 

