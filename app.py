from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Liste des membres du groupe (à remplacer par une base de données)
group_members = {
    "user1": "+1234567890",
    "user2": "+0987654321",
}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body').lower()
    sender = request.form.get('From')
    response = MessagingResponse()

    # Vérifier si le bot est mentionné
    if "@bot" in incoming_msg:
        if ".tagall" in incoming_msg:
            # Taguer tous les membres
            tags = " ".join([f"@{member}" for member in group_members.keys()])
            response.message(f"Tagging everyone: {tags}")
        elif ".welcome" in incoming_msg:
            # Taguer un nouveau membre
            new_member = incoming_msg.split(".welcome ")[1].strip()
            response.message(f"Bienvenue dans le groupe, @{new_member} !")
        elif ".help" in incoming_msg:
            # Afficher les commandes disponibles
            help_text = (
                "Commandes disponibles :\n"
                ".tagall - Taguer tous les membres\n"
                ".welcome @membre - Souhaiter la bienvenue à un nouveau membre\n"
                ".help - Afficher cette aide"
            )
            response.message(help_text)
        else:
            response.message("Commande non reconnue. Tapez .help pour voir les commandes disponibles.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
