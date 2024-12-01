import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, subject, body, sender_email, sender_password):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # SMTP Configuration
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)

        # Send the email
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)

        # Close the connection to the server
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"



class EmailSenderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Sender")
        self.setGeometry(100, 100, 400, 300)

        # UI Elements
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Email Fields
        self.recipient_input = QLineEdit(self)
        self.subject_input = QLineEdit(self)
        self.body_input = QTextEdit(self)
        self.time_input = QTextEdit(self)

        # Send Button
        self.send_button = QPushButton("Send Email", self)

        # Result Label
        self.result_label = QLabel(self)

        # Add widgets to the form
        self.form_layout.addRow("Recipient:", self.recipient_input)
        self.form_layout.addRow("Subject:", self.subject_input)
        self.form_layout.addRow("Body:", self.body_input)
        self.form_layout.addRow("Time:". self.time_input)

        # Add send button and result label
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.result_label)

        # Set layout for the window
        self.setLayout(self.layout)

        # Connect the send button to send_email function
        self.send_button.clicked.connect(self.send_email)

    def send_email(self):
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        body = self.body_input.toPlainText()

        # Get sender email and password (can be input fields or hardcoded)
        sender_email = "t7711256@gmail.com"  # Replace with your email address
        sender_password = "fjek zieq hskc eobu"  # Replace with your Gmail app password (NOT your Google password)

        if not recipient or not subject or not body:
            self.result_label.setText("All fields are required!")
            self.result_label.setStyleSheet("color: red;")
            return

        # Call the send_email function from the other file
        result = send_email(recipient, subject, body, sender_email, sender_password)
        
        # Display the result in the label
        self.result_label.setText(result)
        self.result_label.setStyleSheet("color: green;" if "success" in result else "color: red;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailSenderApp()
    window.show()
    sys.exit(app.exec_())
