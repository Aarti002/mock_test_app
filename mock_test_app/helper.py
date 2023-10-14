from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(email , token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_contact_message_mail(email, message, user, subject):
    default_message = f'Hi , Myself {user} wanted to contact you to send some message. Hope you are doing great!\n'
    default_message+=message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, default_message, email_from, recipient_list)
    return True