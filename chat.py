from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtGui
import os
from groq import Groq

class ChatDialog(QDialog):
    """Dialog for chatting with a Groq-based GPT model, displaying conversation and typing effect.

    Attributes:
        client (Groq): Initialized Groq client for API calls.
        chat_history (QTextEdit): Read-only widget displaying chat messages.
        user_input (QLineEdit): Field where the user types their message.
        send_button (QPushButton): Button to send the user’s message.
    """

    def __init__(self, parent=None) -> None:
        """Initialize the chat UI, set up Groq client, and verify API key."""
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
        self.setStyleSheet(
            "QTextEdit { font-size: 16px; } "
            "QLineEdit { font-size: 16px; } "
            "QPushButton { font-size: 16px; }"
        )

        api_key = os.environ.get('GROQ_API_KEY')
        if api_key is None:
            raise KeyError("Environment variable 'GROQ_API_KEY' is not set.")
        self.client = Groq(api_key=api_key)

    def send_message(self) -> None:
        """Handle user input, display it, request a response, and display via typewriter effect."""
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

    def get_gpt_response(self, prompt: str) -> str:
        """Send prompt to Groq API and return the model’s text response."""
        summary = self.get_relevant_summary(prompt)
        combined = f"{summary}\n\nUser Question: {prompt}"
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": combined}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def get_relevant_summary(self, user_prompt: str) -> str:
        """Load and return summary context from 'description.txt', or an error message."""
        try:
            with open("description.txt", "r") as file:
                return file.read()
        except Exception:
            return "Summary information could not be loaded."

    def type_response(self, response: str) -> None:
        """Initialize typewriter effect for displaying the response character by character."""
        self.response_text = response
        self.current_index = 0
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.update_chat_history)
        self.typing_timer.start(5)

    def update_chat_history(self) -> None:
        """Append the next character of the response to chat_history until complete."""
        if self.current_index < len(self.response_text):
            self.chat_history.moveCursor(QTextCursor.End)
            self.chat_history.insertPlainText(self.response_text[self.current_index])
            self.current_index += 1
        else:
            self.typing_timer.stop()
            self.chat_history.append('')
