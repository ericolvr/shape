"""background tasks for email"""
import time


def send_welcome_email(email: str, name: str):
    time.sleep(2)
    print(
        f"[Background Task] Email de boas-vindas enviado para {name} {email}")
