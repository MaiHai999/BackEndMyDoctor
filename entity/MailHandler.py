from flask_mail import Message
import os

class EmailSender:
    def __init__(self, mail):
        self.mail = mail

    def send_email(self, recipients, token):
        body = "Cảm ơn bạn đã đăng kí vào hệ thống của chúng tôi.Đây là code xác thực : " + token
        subject = "Thư xác thực từ MyDoctor"
        sender = os.environ.get("MAIL_USERNAME")
        msg = Message(subject, sender=sender, recipients=[recipients])
        msg.body = body
        self.mail.send(msg)
