from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtGui
import os
from groq import Groq

class ChatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat")
        self.resize(700, 450)
        self.layout = QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Type your message here...")
        self.layout.addWidget(self.user_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

        self.setStyleSheet("QTextEdit { font-size: 16px; } QLineEdit { font-size: 16px; } QPushButton { font-size: 16px; }")

        groq_api_key = os.environ.get('GROQ_API_KEY')
        if groq_api_key is None:
            raise KeyError("Environment variable 'GROQ_API_KEY' is not set.")
        
        self.client = Groq(api_key=groq_api_key)

    def send_message(self):
        user_message = self.user_input.text()
        if not user_message:
            QMessageBox.warning(self, "Warning", "Please enter a message.")
            return

        self.chat_history.insertHtml(f"<span style='color: green;'>You: {user_message}</span><br>")
        self.user_input.clear()

        try:
            response = self.get_gpt_response(user_message)
            self.type_response(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get response: {e}")

    def get_gpt_response(self, prompt):
        relevant_summary = self.get_relevant_summary(prompt)
        
        combined_prompt = f"{relevant_summary}\n\nUser Question: {prompt}"
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": combined_prompt},
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def get_relevant_summary(self, user_prompt):
        try:
            with open("description.txt", "r") as file:
                summary = file.read()
        except Exception as e:
            summary = "Summary information could not be loaded."
        return summary

    def type_response(self, response):
        self.response_text = response
        self.current_index = 0
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.update_chat_history)
        self.typing_timer.start(5)  

    def update_chat_history(self):
        if self.current_index < len(self.response_text):
            
            self.chat_history.moveCursor(QTextCursor.End)  
            self.chat_history.insertPlainText(self.response_text[self.current_index])
            self.current_index += 1
        else:
            self.typing_timer.stop()
            self.chat_history.append('')  
