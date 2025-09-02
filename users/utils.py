from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_welcome_email(user):
    """
    Sends a welcome email to the new user.
    """
    try:
        subject = "Welcome to Our Website!"
        html_body = render_to_string('users/welcome_email.html', {'user': user})
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send()
        print(f"✅ Welcome email for {user.username} ({user.email}) sent.")
        return True
    except Exception as e:
        print(f"❌ Error sending welcome email: {e}")
        return False

def activateEmail(request, user):
    """
    Sends an activation email to the user.
    """
    try:
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        body = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()
        print(f"✅ Activation email for {user.username} ({user.email}) sent.")
    except Exception as e:
        print(f"❌ Error sending activation email: {e}")
