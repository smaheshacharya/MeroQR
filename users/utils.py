from django.conf import settings
from twilio.rest import Client
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
 

class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number = f'+977{phone_number}'
        self.otp_number = otp

    def send_otp_on_phone(self):
        client = Client(settings.ACCOUNT_SSID, settings.AUTH_TOKEN)
        try:
            message = client.messages.create(
                                body=f'Your OTP is  {self.otp_number}',
                                from_=settings.VERIFY_NUMBER,
                                to=self.phone_number
                            )
        except TwilioRestException as err:
            # Implement your fallback code here
            print(err)
    