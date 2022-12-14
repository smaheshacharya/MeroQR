from django.core.mail import EmailMessage
import os


class Unit:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email = "iammaheshacharya@gmail.com",
            to = [data['to_email']],
        )
        email.send()
