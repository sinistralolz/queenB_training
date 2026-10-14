

import os
import smtplib
from email.message import EmailMessage

from queenbee.domain.model import Alert


class EmailNotifier:
    """Envoie une alerte par e-mail via SMTP sécurisé."""

    def __init__(
        self,
        host: str = "mail.local",
        port: int = 587,
        username: str = "queenbee",
    ):
        self.host = host
        self.port = port
        self.username = username

    def send(self, alert: Alert) -> None:
        password = os.environ.get("SMTP_PASSWORD")

        if not password:
            raise ValueError("SMTP_PASSWORD n'est pas configuré")

        message = EmailMessage()
        message["From"] = "qb@local"
        message["To"] = "soc@local"
        message["Subject"] = "Queen Bee - Alerte de sécurité"
        message.set_content(
            f"Règle : {alert.rule}\n"
            f"Adresse IP : {alert.source_ip}\n"
            f"Gravité : {alert.severity.value}\n"
            f"Message : {alert.message}"
        )

        with smtplib.SMTP(self.host, self.port, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(self.username, password)
            smtp.send_message(message)
