import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLabel, QPushButton, 
    QHBoxLayout, QLineEdit, QMessageBox, QTextEdit, QDialog
)

from PyQt5.QtCore import Qt

# DEFAULT_COMMAND_LIST = {'increase volume':'Increasaes Volume','decrease volume':'Decreasaes Volume','mute':'Mute Audio',
#                         'increase brightness':'Increases Brightness','decrease brightness':'Decreases Brightness',
#                         'create file <file name>':'Create a File','read file <file name>':'Read the File','delete file':'Delete the File',
#                         'open browser':'Opens Web Browser','open text editor':'Open Default Text Editor',
#                         'open terminal':'Opens Termial','system info':'Shows System Information','system status':'Shows System Information',
#                         'search <query>':'Search on Browser','remind me <time in minutes>':'Set Remainer','shutdown':'Use carefully it shutdown the entire system',
#                         'restart':'Use carefully it restarts the entire system','battery':'Shows Battery current status','open file <file name>':'Opens the specified File'}

# def load_commands():
#     # Load user commands from a json file
#     try:
#         with open('user_commands.json', 'r') as f:
#             user_commands = json.load(f)
#             # convert to list
#             return user_commands
#     except FileNotFoundError:
#         return {}

# def save_commands(commands):
#     with open('user_commands.json', 'w') as file:
#         json.dump(commands, file, indent=4)

# class CommandUI(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.default_commands = DEFAULT_COMMAND_LIST
#         self.user_commands = load_commands()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Available Commands")
#         self.resize(600, 600)

#         self.layout = QVBoxLayout(self)

#         # Section for Default Commands
#         default_label = QLabel("Default Commands")
#         self.layout.addWidget(default_label)
#         self.default_table = QTableWidget(self)
#         self.layout.addWidget(self.default_table)
#         self.load_commands(self.default_table, self.default_commands)

#         # Section for User Commands
#         user_label = QLabel("User Commands")
#         self.layout.addWidget(user_label)
#         self.user_table = QTableWidget(self)
#         self.layout.addWidget(self.user_table)
#         self.load_commands(self.user_table, self.user_commands)

#         # CRUD Operations UI
#         self.command_input_layout = QHBoxLayout()

#         self.command_input = QLineEdit(self)
#         self.command_input.setPlaceholderText("Command name")
#         self.command_input_layout.addWidget(self.command_input)

#         self.description_input = QLineEdit(self)
#         self.description_input.setPlaceholderText("Command")
#         self.command_input_layout.addWidget(self.description_input)

#         self.add_button = QPushButton("Add", self)
#         self.add_button.clicked.connect(self.add_command)
#         self.command_input_layout.addWidget(self.add_button)

#         self.update_button = QPushButton("Update", self)
#         self.update_button.clicked.connect(self.update_command)
#         self.command_input_layout.addWidget(self.update_button)

#         self.delete_button = QPushButton("Delete", self)
#         self.delete_button.clicked.connect(self.delete_command)
#         self.command_input_layout.addWidget(self.delete_button)

#         self.layout.addLayout(self.command_input_layout)

#     def load_commands(self, table_widget, commands):
#         # Set up table widget
#         table_widget.setColumnCount(2)
#         table_widget.setRowCount(len(commands))
#         table_widget.setHorizontalHeaderLabels(["Command name", "Command"])
#         table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

#         # Populate table with commands
#         for row, (command, description) in enumerate(commands.items()):
#             table_widget.setItem(row, 0, QTableWidgetItem(command))
#             table_widget.setItem(row, 1, QTableWidgetItem(description))

#     def add_command(self):
#         command = self.command_input.text().strip()
#         description = self.description_input.text().strip()

#         if command and description:
#             if command in self.user_commands:
#                 QMessageBox.warning(self, "Warning", "Command already exists.")
#             else:
#                 self.user_commands[command] = description
#                 save_commands(self.user_commands)
#                 self.load_commands(self.user_table, self.user_commands)
#                 self.command_input.clear()
#                 self.description_input.clear()
#         else:
#             QMessageBox.warning(self, "Warning", "Please enter both command name and command.")

#     def update_command(self):
#         command = self.command_input.text().strip()
#         description = self.description_input.text().strip()

#         if command in self.user_commands:
#             self.user_commands[command] = description
#             save_commands(self.user_commands)
#             self.load_commands(self.user_table, self.user_commands)
#             self.command_input.clear()
#             self.description_input.clear()
#         else:
#             QMessageBox.warning(self, "Warning", "Command does not exist.")

#     def delete_command(self):
#         command = self.command_input.text().strip()

#         if command in self.user_commands:
#             del self.user_commands[command]
#             save_commands(self.user_commands)
#             self.load_commands(self.user_table, self.user_commands)
#             self.command_input.clear()
#             self.description_input.clear()
#         else:
#             QMessageBox.warning(self, "Warning", "Command does not exist.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     command_ui = CommandUI()
#     command_ui.show()
#     sys.exit(app.exec_())


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 700, 500)
        
        # Create main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create QTextEdit for displaying content
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        # Set the content with proper HTML formatting (Markdown-like)
        help_content = """
        <h2 style="color:#2980B9;">About:</h2>
        <ul>
            <li><strong>This is DORE-AI</strong> an offline personal assistant!</li>
            <li>It uses gemma2:2b (a local LLM for general conversation) by default, you can also use your prefred ollama models</li>
            <li>It was developed by <em>Spidey</em> and <em>Drackko</em></li>
        </ul>
        
        <h2 style="color:#2980B9;">Commands:</h2>
        <ul>
            <li><code>/settings</code> - open settings</li>
            <li><code>/commands</code> - list available voice commands</li>
            <li><code>/enable voice</code> - To enable voice chat</li>
            <li><code>/disable voice</code> - To disable voice chat</li>
        </ul>

        <h2 style="color:#2980B9;">If you are facing any issues,please contact the developers:</h2>
        <ul>
            <li><a href="mailto:theprosidd@gmail.com" style="color:#3498DB;">theprosidd@gmail.com</a></li>
            <li><a href="mailto:saidhin27@gmail.com" style="color:#3498DB;">saidhin27@gmail.com</a></li>
        </ul>
        """
        
        # Set the content as HTML
        self.text.setHtml(help_content)
        self.layout.addWidget(self.text)
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    help_window = HelpWindow()
    help_window.show()
    sys.exit(app.exec_())  # <--- sys.exit() is called here