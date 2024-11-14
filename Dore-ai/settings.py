import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QDateEdit, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import QDate


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Settings")
        self.setGeometry(100, 100, 400, 300)

        # Load settings
        self.load_settings()

        # Layout
        self.layout = QVBoxLayout()

        # Form layout for settings input
        form_layout = QFormLayout()

        # Username Field
        self.username_input = QLineEdit(self.username)
        form_layout.addRow("Username:", self.username_input)

        # Nickname Field
        self.nickname_input = QLineEdit(self.nickname)
        form_layout.addRow("Nickname:", self.nickname_input)

        # DOB Field (Date Edit)
        self.dob_input = QDateEdit(QDate.fromString(self.dob, "dd-MM-yyyy"))
        self.dob_input.setCalendarPopup(True)
        form_layout.addRow("Date of Birth:", self.dob_input)

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
        settings_file = "user_settings.json"

        # Default values if no settings file exists
        self.username = "Default User"
        self.nickname = "User"
        self.dob = "01-01-2000"

        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as file:
                    data = json.load(file)
                    self.username = data.get("name", self.username)
                    self.nickname = data.get("nickname", self.nickname)
                    self.dob = data.get("dob", self.dob)

                    # Validate the date format
                    if not QDate.fromString(self.dob, "dd-MM-yyyy").isValid():
                        self.dob = "01-01-2000"  # Reset to default if invalid
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to the JSON file."""
        settings_file = "user_settings.json"

        data = {
            "name": self.username_input.text(),
            "nickname": self.nickname_input.text(),
            "dob": self.dob_input.date().toString("dd-MM-yyyy")
        }

        try:
            with open(settings_file, 'w') as file:
                json.dump(data, file, indent=4)
            self.accept()  # Close the dialog
        except IOError as e:
            print(f"Error saving settings: {e}")

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
