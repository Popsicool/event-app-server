from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse
import os
from decouple import config
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class SendMail:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

    @staticmethod
    def send_mail_with_attachment(data):
        subject = "Contract mail"
        body = "Please find attached your contract"
        pdf_path = os.path.join(os.path.dirname(__file__), 'contract.pdf')
        email = EmailMessage(
            subject=subject, body=body, to=[data['to_email']])
        email.attach_file(pdf_path)
        EmailThread(email).start()


    @staticmethod
    def send_email_verification_mail(data):
        frontend_url = config("FRONTEND_URL", "")
        email_verification_url = f'{frontend_url}?verification=true&email={data["to_email"]}&otp={data["token"]}'
        message = f'Hello {data["username"]},\nYour securely generated token is available below.' \
                  f'\n\n{data["token"]}' \
                  f'\n{email_verification_url}'
        data['email_body'] = message
        data['email_subject'] = 'Verify Your Email'
        SendMail.send_email(data)

    @staticmethod
    def send_password_reset_mail(data, request):

        current_site = get_current_site(request=request).domain

        # construct url
        relativeLink = reverse(
            'password-reset-confirm', kwargs={'uid64': data["uid64"], 'token': data["token"]})
        # redirect_url = request.data.get('redirect_url', '')
        # base_url = "https://roofbucks-admin.onrender.com/reset-password"
        base_url = config("FRONTEND_URL")
        # frontend_url = config("FRONTEND_URL", "")
        absurl = f'{base_url}/reset-password?uid64={data["uid64"]}&token={data["token"]}'

        email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
        data = {'email_body': email_body, 'to_email': data["email"],
                'email_subject': 'Reset your passsword'}
        SendMail.send_email(data)
    
