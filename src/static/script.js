document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const messages = document.getElementById("chat-messages");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const userMessage = input.value.trim();
        if (!userMessage) return;

        // Mostrar mensaje del usuario
        addMessage(userMessage, "user");
        input.value = "";

        try {
            const response = await fetch("/preguntar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ pregunta: userMessage })
            });

            if (!response.ok) {
                throw new Error("Error al obtener respuesta del servidor");
            }

            const data = await response.json();
            addMessage(data.respuesta, "bot");
        } catch (error) {
            addMessage("Lo siento, hubo un error procesando tu pregunta.", "bot");
            console.error("Error:", error);
        }
    });

    function addMessage(text, sender) {
        const messageEl = document.createElement("div");
        messageEl.classList.add("message", sender);

        const bubble = document.createElement("div");
        bubble.classList.add("bubble", sender);
        bubble.textContent = text;

        messageEl.appendChild(bubble);
        messages.appendChild(messageEl);
        messages.scrollTop = messages.scrollHeight;
    }
});
