import smtplib
import AccountManagement.settings as settings


class SMTPMail:
    def __init__(self, host, port, username, password):
        self.conn = smtplib.SMTP(host, port)
        self.conn.ehlo()
        self.conn.starttls()
        try:
            self.conn.login(username, password)
        except smtplib.SMTPAuthenticationError as e:
            print(e)

    def sendmail(self, subject, message, receivers=[], sender=settings.email):
        message = f"""From: {sender}
To: {receivers[0]}
Subject: {subject}

{message}
"""
        try:
            self.conn.sendmail(sender, receivers, message)
        except smtplib.SMTPException as e:
            print(e)

    def exit(self):
        self.conn.quit()


def send_mail(receiver, message, subject):
    if isinstance(receiver, str):
        recipients = []
        recipients.append(receiver)
    else:
        if not isinstance(receiver, list):
            return
        recipients = [] + receiver
    smtp = SMTPMail(settings.mail_host, settings.smtp_port, settings.email, settings.email_password)
    smtp.sendmail(subject, message, recipients)
    smtp.exit()


def send_registration_mail(receiver, email_token):
    message = """Thank you for registering at The Battle Of AI.
To complete your registration, please go to https://battleofai.net/verifyEmail.html?email_token=""" + str(email_token) + """
If you did not issue this email, please ignore it.
For more information on privacy policy and terms of use, please fo to https://battleofai.net/
"""
    send_mail(receiver, message, 'Your registration at the Battle Of AI')


def send_pwforgot_email(receiver, email_token):
    message = """
Did you forget your password? Because you told us so.
If you did not, ignore this email.
If you did, here's your link to reset it:
https://battleofai.net/resetPassword.html?email_token=""" + str(email_token) + """
For more information on privacy policy and terms of use, please fo to https://battleofai.net/
"""
    send_mail(receiver, message, 'Password Reset at the Battle of AI')
