from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib import messages

def send_welcome_email(user):
    """
    ارسال ایمیل خوشامدگویی به کاربر جدید
    
    Args:
        user: شیء کاربر که ایمیل خوشامدگویی برایش ارسال می‌شود
    """
    try:
        # ایجاد ایمیل خوشامدگویی (HTML)
        subject = "Welcome to our site"
        current_site = Site.objects.get_current()
        site_domain = getattr(current_site, 'domain', '')

        html_body = render_to_string(
            'users/welcome_email.html',
            {
                'user': user,
                'site_domain': f"https://{site_domain}" if site_domain else ''
            }
        )

        # ایجاد شیء EmailMessage با محتوای HTML
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        
        # ارسال ایمیل با استفاده از Email Backend پیش‌فرض
        email.send()
        
        print(f"✅ ایمیل خوشامدگویی برای {user.username} ({user.email}) ارسال شد.")
        return True
        
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل خوشامدگویی: {e}")
        return False

def activateEmail(request, user, to_email):
    messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on '
        'received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
