from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail



def send_email_confirm(user,request):
    current_site = get_current_site(request)
    subject = 'Activate Your MySite Account'
    message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
    resp = send_mail(subject=subject,message='',recipient_list=[user.email], html_message=message,from_email=None)