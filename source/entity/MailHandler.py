from flask_mail import Message
import os

class EmailSender:
    def __init__(self, mail):
        self.mail = mail
        self.sender = os.environ.get("MAIL_USERNAME")

    def send_email(self,subject, recipients, body):
        msg = Message(subject, sender=self.sender, recipients=[recipients])
        msg.html = body
        self.mail.send(msg)


    def send_email_login(self , token , recipient):
        subject = "Thư xác thực từ MyDoctor"
        body = """
                Xin chào,<br><br>
                Cảm ơn vì đã đăng kí hệ thống của chúng tôi. Đây là mã xác thực: <b>{}</b> <br>
                Thân ái.
                """.format(token)
        self.send_email(subject , recipient , body)


    def send_email_reset(self,token , recipient):
        subject = "Thư xác thực từ MyDoctor"
        body = """
                Xin chào,<br><br>
                Để thiết lập lại mật khẩu vui lòng nhập mã xác thực. Đây là mã xác thực: <b>{}</b> <br>
                Thân ái.
                """.format(token)
        self.send_email(subject, recipient, body)


