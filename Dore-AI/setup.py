import sys
import platform
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox


class SetupUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ollama & Gemma Model Setup")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Status Label
        self.status_label = QLabel("Press 'Install Ollama' to begin.")
        layout.addWidget(self.status_label)

        # Install Ollama Button
        self.install_ollama_btn = QPushButton("Install Ollama", self)
        self.install_ollama_btn.clicked.connect(self.install_ollama)
        layout.addWidget(self.install_ollama_btn)

        # Install Gemma Model Button
        self.install_gemma_btn = QPushButton("Install Gemma:2B Model", self)
        self.install_gemma_btn.clicked.connect(self.install_gemma_model)
        self.install_gemma_btn.setEnabled(False)  # Disable until Ollama is installed
        layout.addWidget(self.install_gemma_btn)

        # Set main layout
        self.setLayout(layout)

    def install_ollama(self):
        """Install Ollama based on the OS."""
        system = platform.system()
        try:
            self.status_label.setText("Installing Ollama...")
            if system == "Darwin":  # macOS
                subprocess.run(["brew", "install", "ollama"], check=True)
            elif system == "Linux":
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "ollama"], check=True)
            elif system == "Windows":
                subprocess.run(["winget", "install", "Ollama"], check=True)
            else:
                QMessageBox.critical(self, "Error", f"Unsupported OS: {system}")
                return

            self.status_label.setText("Ollama installed successfully.")
            self.install_gemma_btn.setEnabled(True)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Installation Failed", f"Failed to install Ollama: {e}")
            self.status_label.setText("Failed to install Ollama.")

    def install_gemma_model(self):
        """Install the Gemma:2B model using Ollama."""
        try:
            self.status_label.setText("Installing Gemma:2B model...")
            subprocess.run(["ollama", "pull", "gemma:2b"], check=True)
            self.status_label.setText("Gemma:2B model installed successfully.")
            QMessageBox.information(self, "Success", "Gemma:2B model installed successfully.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Installation Failed", f"Failed to install Gemma:2B model: {e}")
            self.status_label.setText("Failed to install Gemma:2B model.")


def main():
    app = QApplication(sys.argv)
    setup_ui = SetupUI()
    setup_ui.show()

    # Use QApplication.exec() instead of exec_() to avoid conflicts with other main loops
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
