# Importation des bibliothèques nécessaires
from dotenv import load_dotenv
import os
import sys
from PyQt5 import QtWidgets, QtCore
from mistralai import Mistral, UserMessage

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API depuis la variable d'environnement
API_KEY = os.getenv("MISTRAL_API_KEY")

# Vérifier si la clé API a bien été chargée
if not API_KEY:
    print("Erreur : la clé API n'a pas été trouvée dans le fichier .env")
    sys.exit(1)
else:
    print("Clé API chargée avec succès")

# Initialisation du client Mistral AI
client = Mistral(api_key=API_KEY)

# Fonction pour envoyer le message et obtenir la réponse
def chatbot_conversation(user_input):
    try:
        # Structure du message pour l'API Mistral
        messages = [UserMessage(content=user_input)]
        print("Envoi de la requête à l'API Mistral...")  # Log
        response = client.chat.complete(model="mistral-tiny", messages=messages)
        print("Réponse reçue de l'API Mistral :", response)  # Log
        return response.choices[0].message.content
    except Exception as e:
        print("Erreur lors de l'appel à l'API :", e)  # Log
        return f"Erreur API : {e}"

# Nouvelle classe ChatbotApp avec l'interface sombre
class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle("Chatbot Mistral AI")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e;")  # Fond sombre

        # Zone de texte pour afficher la conversation
        self.chat_window = QtWidgets.QListWidget(self)
        self.chat_window.setStyleSheet("""
            background-color: #2d2d2d;  # Fond sombre
            color: #ffffff;  # Texte blanc
            font-size: 14px;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #444;
        """)

        # Zone de saisie pour l'utilisateur
        self.input_box = QtWidgets.QLineEdit(self)
        self.input_box.setPlaceholderText("Tapez votre message ici...")
        self.input_box.setStyleSheet("""
            background-color: #2d2d2d;  # Fond sombre
            color: #ffffff;  # Texte blanc
            font-size: 14px;
            border-radius: 15px;
            padding: 10px;
            border: 1px solid #444;
        """)
        self.input_box.returnPressed.connect(self.send_message)

        # Bouton pour envoyer le message
        self.send_button = QtWidgets.QPushButton("Envoyer", self)
        self.send_button.setStyleSheet("""
            background-color: #4CAF50;  # Bouton vert
            color: white;
            font-size: 14px;
            border-radius: 15px;
            padding: 10px 20px;
            border: none;
        """)
        self.send_button.clicked.connect(self.send_message)

        # Disposition des éléments
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.chat_window)

        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def send_message(self):
        user_input = self.input_box.text()
        if user_input.strip():
            # Afficher le message de l'utilisateur
            self.display_message("Vous", user_input, "user")
            self.input_box.clear()

            # Simuler un indicateur de saisie
            self.display_message("Chatbot", "Chatbot est en train d'écrire...", "bot", is_typing=True)
            QtWidgets.QApplication.processEvents()

            # Obtenir la réponse du chatbot
            bot_response = chatbot_conversation(user_input)
            self.chat_window.takeItem(self.chat_window.count() - 1)  # Supprimer l'indicateur de saisie
            self.display_message("Chatbot", bot_response, "bot")

    def display_message(self, sender, message, role, is_typing=False):
        # Créer un élément de liste stylisé
        item = QtWidgets.QListWidgetItem()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        label_sender = QtWidgets.QLabel(f"<b>{sender}:</b>")
        label_message = QtWidgets.QLabel(message)
        label_message.setWordWrap(True)

        # Appliquer des styles en fonction du rôle
        if role == "bot":
            label_sender.setStyleSheet("color: #1e88e5;")  # Bleu pour le chatbot
            label_message.setStyleSheet("""
                background-color: #333333;  # Fond sombre pour les messages du bot
                color: #ffffff;  # Texte blanc
                font-size: 14px;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #444;
                margin: 5px 0;
            """)
        else:
            label_sender.setStyleSheet("color: #4CAF50;")  # Vert pour l'utilisateur
            label_message.setStyleSheet("""
                background-color: #333333;  # Fond sombre pour les messages de l'utilisateur
                color: #ffffff;  # Texte blanc
                font-size: 14px;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #444;
                margin: 5px 0;
            """)

        layout.addWidget(label_sender)
        layout.addWidget(label_message)
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.chat_window.addItem(item)
        self.chat_window.setItemWidget(item, widget)

        # Faire défiler automatiquement vers le bas
        self.chat_window.scrollToBottom()

# Point d'entrée du programme
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chatbot_app = ChatbotApp()
    chatbot_app.show()
    sys.exit(app.exec_())