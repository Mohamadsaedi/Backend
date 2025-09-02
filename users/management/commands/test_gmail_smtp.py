from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'تست سریع Gmail SMTP'

    def handle(self, *args, **options):
        self.stdout.write("🧪 تست سریع Gmail SMTP...")
        self.stdout.write("=" * 50)
        
        try:
            # ارسال ایمیل تست
            send_mail(
                subject='تست Gmail SMTP - Django Contact Form',
                message='''
سلام!

این یک ایمیل تست است که از Django Contact Form ارسال شده است.

تنظیمات:
- Email Backend: SMTP Gmail
- From: saedimohamad1376@gmail.com
- To: saedimohamad1376@gmail.com

اگر این ایمیل را دریافت کردید، یعنی تنظیمات Gmail SMTP درست کار می‌کند!

---
با تشکر
سیستم Django Contact Form
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['saedimohamad1376@gmail.com'],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS("✅ ایمیل تست با موفقیت ارسال شد!")
            )
            self.stdout.write("📧 گیرنده: saedimohamad1376@gmail.com")
            self.stdout.write("🔧 Email Backend: SMTP Gmail")
            self.stdout.write("")
            self.stdout.write("💡 حالا Gmail خود را چک کنید!")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ خطا در ارسال ایمیل: {e}")
            )
            self.stdout.write("")
            self.stdout.write("🔧 نکات عیب‌یابی:")
            self.stdout.write("1. App Password را چک کنید")
            self.stdout.write("2. Two-Factor Authentication فعال باشد")
            self.stdout.write("3. اینترنت را چک کنید")
            self.stdout.write("4. فولدر Spam را چک کنید")
