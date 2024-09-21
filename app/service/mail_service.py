from flask_mail import Mail, Message


class MailService:
    def __init__(self, app) -> None:
        self.mail = None
        if app is not None:
            self.mail = self.init_config_mail(app)
            print("Mail service is established")

    def init_config_mail(self, app) -> Mail:
        app.config["MAIL_SERVER"] = "smtp.gmail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USE_SSL"] = False
        app.config["MAIL_USERNAME"] = "huynhdaihuybank3@gmail.com"
        app.config["MAIL_PASSWORD"] = "ufov qdsr ciyh hgga"
        app.config["MAIL_DEFAULT_SENDER"] = "huynhdaihuybank3@gmail.com"
        app.extensions['mail_service'] = self
        return Mail(app)

    def send_mail(self, subject, recipient, body):
        msg = Message(subject=subject, recipients=[recipient], body=body)
        try:
            self.mail.send(msg)
        except Exception as e:
            print(f"Fail to send mail {str(e)}")

    def send_verify_mail(self, email, token):
        subject = "[Elearning] - Email Verification"
        verification_link = f"http://127.0.0.1:5000/auth/verify-email/{token}"
        body = f"Please verify your email by clicking the link: {
            verification_link}"
        msg_config = Message(subject=subject, recipients=["huynhdaihuybank6@gmail.com"],
                             body=body)
        try:
            self.mail.send(msg_config)
        except Exception as e:
            print(f"Fail to send mail {str(e)}")

    def send_otp_mail(self, email, otp_code):
        subject = "[Elearning] - OTP Code Login "
        body = f"This is your OTP-code to login, it exist in 5 minutes, don't share this under any situation {
            otp_code}"
        msg_config = Message(subject=subject, recipients=["huynhdaihuybank6@gmail.com"],
                             body=body)
        try:
            self.mail.send(msg_config)
        except Exception as e:
            print(f"Fail to send mail {str(e)}")
