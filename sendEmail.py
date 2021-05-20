import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class Gmail:
    smtp_server = "smtp.gmail.com"
    port = 587


    mail_mal = {'message': None,
                'From': Config.gmail,
                'To': Config.gmail_receiver,
                'Subject': "Room Booking"}

    def __init__(self, email, passwd,):
        self.email = email
        self.password = passwd


    def send_email(self, *args, **kwargs):
        input_message = locals()
        message = MIMEMultipart("alternative")
        text = None

        if args:
            text, = args

        for key, value in self.mail_mal.items():
            if key in kwargs.keys():
                message[key] = kwargs[key]
                continue
            message[key] = value

        if 'message' in kwargs.keys():
            text = kwargs['message']

        if not text:
            raise Exception("Error, need to specify message")

        text += "\n\nSendt from python"

        compress = MIMEText(text, "plain")

        message.attach(compress)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.email, self.password)
            server.sendmail(
                self.email, message['To'], message.as_string()
            )







