from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'بررسی تنظیمات Email Backend'

    def handle(self, *args, **options):
        self.stdout.write("🔧 بررسی تنظیمات Email Backend")
        self.stdout.write("=" * 50)
        
        # بررسی تنظیمات DEBUG
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        if settings.DEBUG:
            self.stdout.write(
                self.style.SUCCESS("✅ حالت توسعه فعال - ایمیل‌ها در دیتابیس ذخیره می‌شوند")
            )
        else:
            self.stdout.write(
                self.style.WARNING("⚠️ حالت تولید فعال - ایمیل‌ها واقعاً ارسال می‌شوند")
            )
        
        # بررسی اینکه آیا Email Backend درست تنظیم شده
        if 'users.email_backends.DatabaseEmailBackend' in settings.EMAIL_BACKEND:
            self.stdout.write(
                self.style.SUCCESS("✅ DatabaseEmailBackend فعال است")
            )
        else:
            self.stdout.write(
                self.style.WARNING("⚠️ DatabaseEmailBackend فعال نیست")
            )
