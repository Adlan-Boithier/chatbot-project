# Importation des bibliothèques nécessaires
from dotenv import load_dotenv
import os
import sys
from PyQt5 import QtWidgets, QtCore
from mistralai.client import MistralClient

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API depuis la variable d'environnement
API_KEY = os.getenv("MISTRAL_API_KEY")

# Vérifier si la clé API a bien été chargée
if not API_KEY:
    print("Erreur : la clé API n'a pas été trouvée dans le fichier .env")
else:
    print("Clé API chargée avec succès")
# Initialisation du client Mistral AI
client = MistralClient(api_key=API_KEY)

# Fonction pour envoyer le message et obtenir la réponse
def chatbot_conversation(user_input):
    try:
        # Structure du message pour l'API Mistral
        messages = [{"role": "user", "content": user_input}]
        response = client.chat(model="mistral-tiny", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur API : {e}"

# Classe pour l'interface graphique du chatbot
class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle("Chatbot Mistral AI")
        self.setGeometry(100, 100, 600, 400)

        # Zone de texte pour afficher la conversation
        self.chat_window = QtWidgets.QTextEdit(self)
        self.chat_window.setReadOnly(True)
        self.chat_window.setStyleSheet("background-color: #f0f0f0; color: #333; font-size: 14px;")

        # Zone de saisie pour l'utilisateur
        self.input_box = QtWidgets.QLineEdit(self)
        self.input_box.setStyleSheet("background-color: white; color: #333; font-size: 14px;")
        self.input_box.returnPressed.connect(self.send_message)

        # Bouton pour envoyer le message
        self.send_button = QtWidgets.QPushButton("Envoyer", self)
        self.send_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
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
            self.chat_window.append(f"Vous: {user_input}")
            self.input_box.clear()

            # Obtenir la réponse du chatbot
            bot_response = chatbot_conversation(user_input)
            self.chat_window.append(f"Chatbot: {bot_response}")
            QtWidgets.QApplication.processEvents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Maintenant 'sys' est défini
    chatbot_app = ChatbotApp()
    chatbot_app.show()
    sys.exit(app.exec_())