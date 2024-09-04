from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Definir los precios y promociones
precios = {
    1: 38,
    2: 42,
    3: 46
}

# Enlace a la página web
pagina_web = "https://sites.google.com/view/top1material/cursos?authuser=0"

# Configuración de Twilio
account_sid = 'TU_ACCOUNT_SID'  # Reemplaza con tu Account SID
auth_token = 'TU_AUTH_TOKEN'    # Reemplaza con tu Auth Token
twilio_number = 'whatsapp:+14155238886'  # Reemplaza con tu número de WhatsApp de Twilio
client = Client(account_sid, auth_token)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data['message'].lower()
    to_number = data.get('to')  # Número de destino

    # Responder a solicitudes comunes
    if "material de" in message:
        curso = message.split("material de")[-1].strip()
        response = f"{curso} es nuestra especialidad 💯. ¿Estás interesado en otros cursos?\n\n¡Estamos en oferta!\n\n1 curso -> {precios[1]} soles\n2 cursos -> {precios[2]} soles\n3 cursos -> {precios[3]} soles\n\nPara más información, visita nuestra página web: {pagina_web}"
    
    elif "precio" in message or "costo" in message:
        response = f"¡Estamos en oferta!\n\n1 curso -> {precios[1]} soles\n2 cursos -> {precios[2]} soles\n3 cursos -> {precios[3]} soles\n\n¿Te gustaría adquirir alguno? Visita nuestra página web para más detalles: {pagina_web}"
    
    elif "yape" in message:
        response = f"El numero de yape es +51 991 308 394✅\n\n .Envía la captura del yapeo y tu correo PUCP. La entrega es inmediata 💯. Visita nuestra página web para ver más cursos: {pagina_web}"
    
    elif "información" in message:
        response = f"Para más información sobre nuestros cursos, visita nuestra página web: {pagina_web} o dime el curso específico sobre el que te gustaría saber más."
    
    else:
        response = f"No entendí tu solicitud, ¿podrías especificar un poco más? Estoy aquí para ayudarte con cualquier duda sobre los cursos. Visita nuestra página web: {pagina_web}"

    # Enviar mensaje a través de WhatsApp usando Twilio
    message = client.messages.create(
        from_=twilio_number,
        body=response,
        to=to_number
    )

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5000)
