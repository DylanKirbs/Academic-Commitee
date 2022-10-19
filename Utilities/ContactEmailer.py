import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

class ContactEmailer:
    
    def __init__(self, path:str):
        """
        :param path: The path to the config file
        :return: A ContactEmailer object
        """
        with open(path, "r") as f:
            config = json.load(f)

        self._email = config["email"]
        self._password = config["password"]
        self._server = smtplib.SMTP(config["server"])
        self._subject = config["subject"]

        self._server.starttls()
        self._server.login(self._email, self._password)

    def sendMail(self, to_mail:str, message:str):
        msg = MIMEMultipart()
        msg["From"] = self._email
        msg["To"] = to_mail
        msg["Subject"] = self._subject

        msg.attach(MIMEText(message, "plain"))
        text = msg.as_string()
        self._server.sendmail(self._email, to_mail, text)

    def close(self):
        self._server.quit()

    def __del__(self):
        self.close()