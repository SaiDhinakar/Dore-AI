import os
import json
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QDateEdit, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import QDate
import sys

# FILES_DIR = "Dore-AI_V_2.0/Files/"
FILES_DIR = "../Files/"
USER_SETTINGS_FILE = "settings.json"

class User:
    def __init__(self):
        # Check if the settings file exists
        files = os.listdir(FILES_DIR)
        if USER_SETTINGS_FILE not in files:
            if not self.load_data():
                self.create_user()  # Create default user settings if not found
        else:
            self.data = self.load_data()  # Load existing user data
        # print('User module initialized!')

    def create_user(self):
        """Method to create a new user."""
        print("Creating a new user...")
        username = "User"#input("Enter your username: ")
        self.data = {
            "username": username,
        }
        self.save_data()
        print(f"User '{username}' created successfully!")

    def add_details(self):
        """Method to add more details to the user profile."""
        if not self.data:
            print("No user data found! Please create a user first.")
            return
        
        print("Adding details...")
        details = list(map(str,input("Enter additional details (e.g., email:'jondoe@example.com', address): ").split(':')))
        self.data[details[0].lower()] = details[1]
        self.save_data()
        print("Details added successfully.")

    def update_details(self):
        """Method to update existing user details."""
        if not self.data:
            print("No user data found! Please create a user first.")
            return
        
        print("Updating user details...")
        new_username = input(f"Enter new username (current: {self.data['username']}): ")
        if new_username.strip():
            self.data["username"] = new_username.strip()
            print(f"Username updated to {self.data['username']}.")
        
        new_details = input("Enter new details (Leave blank to keep current details): ")
        if new_details.strip():
            self.data["details"] = new_details.strip()
            print("Details updated successfully.")
        
        self.save_data()

    def save_data(self):
        """Save user data to the settings.json file."""
        try:
            with open(FILES_DIR + USER_SETTINGS_FILE, 'w') as f:
                json.dump(self.data, f, indent=4)
            print("User data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """Load user data from the settings.json file."""
        try:
            with open(FILES_DIR + USER_SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print("Settings file not found.")
            return False
        except json.JSONDecodeError:
            print("Error decoding the settings file.")
            return False


# Settings UI
import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QFileDialog, QDialogButtonBox, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Settings")
        self.setGeometry(100, 100, 500, 350)

        # Load settings
        self.load_settings()

        # Main Layout
        self.layout = QVBoxLayout()

        # Form layout for settings input
        form_layout = QFormLayout()

        # Username Field
        self.username_input = QLineEdit(self.username)
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.username_input)

        # Email Field
        self.email_input = QLineEdit(self.email)
        self.email_input.setPlaceholderText("Enter your email address")
        form_layout.addRow("Email:", self.email_input)

        # Chat model Field
        self.chat_model_name_input = QLineEdit(self.chat_model_name)
        self.chat_model_name_input.setPlaceholderText("gemma2:2b")
        form_layout.addRow("Chat Model Name:", self.chat_model_name_input)

        # Music Directory Field with Browse Button
        self.music_dir_input = QLineEdit(self.music)
        self.music_dir_input.setPlaceholderText("Select your music directory")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_music_directory)

        music_layout = QVBoxLayout()
        music_layout.addWidget(self.music_dir_input)
        music_layout.addWidget(self.browse_button)
        form_layout.addRow("Music Directory:", music_layout)

        # Add the form layout to the main layout
        self.layout.addLayout(form_layout)

        # Save and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_settings)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
        self.setModal(True)  # Make the dialog modal

    def load_settings(self):
        """Load user settings from a JSON file."""
        settings_file = FILES_DIR+USER_SETTINGS_FILE

        # Default values if no settings file exists
        self.username = "Default User"
        self.email = "example@gmail.com"
        self.music = ""
        self.chat_model_name = "gemma2:2b"

        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as file:
                    data = json.load(file)
                    self.username = data.get("username", self.username)
                    self.email = data.get("email", self.email)
                    self.music = data.get("music_dir", self.music)
                    self.chat_model_name = data.get("chat_model", self.chat_model_name)
            except (json.JSONDecodeError, IOError) as e:
                QMessageBox.warning(self, "Error", f"Error loading settings: {e}")

    def browse_music_directory(self):
        """Open a file dialog to select a directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Music Directory")
        if directory:
            self.music_dir_input.setText(directory)

    def save_settings(self):
        """Save settings to the JSON file."""
        settings_file = FILES_DIR+USER_SETTINGS_FILE

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        music_dir = self.music_dir_input.text().strip()
        chat_model = self.chat_model_name_input.text().strip()

        # Basic validation
        if not username or not email:
            QMessageBox.warning(self, "Validation Error", "Username and Email cannot be empty.")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address.")
            return

        data = {
            "username": username,
            "email": email,
            "music_dir": music_dir,
            "chat_model":chat_model
        }

        try:
            with open(settings_file, 'w') as file:
                json.dump(data, file, indent=4)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()  # Close the dialog
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {e}")


# Main Application
def open_settings_dialog():
    # Ensure that a QApplication instance exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = SettingsWindow()

    # Execute the settings dialog and check if it was accepted
    if window.exec_() == QDialog.Accepted:
        print("Settings saved successfully!")


if __name__ == "__main__":
    open_settings_dialog()


    # user = User()
    # print(user.load_data())


# Example usage
# if __name__ == "__main__":
    # obj = User()

    # You can now interact with the user object
    # Uncomment the following lines to test the functionality
    # obj.add_details()
    # obj.update_details()
    # print(obj.load_data())
