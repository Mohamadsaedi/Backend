from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from users.models import CustomUser
from users.utils import send_welcome_email


@receiver(post_save, sender=CustomUser)
def send_welcome_email_post_save(sender, instance: CustomUser, created: bool, **kwargs):
    """
    ارسال خودکار ایمیل خوش‌آمدگویی پس از ایجاد کاربر جدید
    """
    if created and instance and instance.email:
        try:
            send_welcome_email(instance)
        except Exception:
            # در حالت توسعه می‌خواهیم خطاها باعث کرش نشوند
            if getattr(settings, "DEBUG", True):
                return
            raise


