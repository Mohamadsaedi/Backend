from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from users.models import ContactForm

class Command(BaseCommand):
    help = 'تست فرم تماس و ارسال ایمیل'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='تست کاربر',
            help='نام کاربر',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='ایمیل کاربر',
        )
        parser.add_argument(
            '--subject',
            type=str,
            default='تست فرم تماس',
            help='موضوع پیام',
        )
        parser.add_argument(
            '--message',
            type=str,
            default='این یک پیام تست است.',
            help='متن پیام',
        )

    def handle(self, *args, **options):
        name = options['name']
        email = options['email']
        subject = options['subject']
        message = options['message']

        self.stdout.write("🧪 شروع تست فرم تماس...")
        self.stdout.write("=" * 50)

        # 1. ذخیره در دیتابیس
        try:
            contact_form = ContactForm.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ فرم تماس در دیتابیس ذخیره شد (ID: {contact_form.id})")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ خطا در ذخیره فرم: {e}")
            )
            return

        # 2. ارسال ایمیل
        try:
            email_subject = f"پیام جدید از فرم تماس: {subject}"
            email_message = f"""
پیام جدید از فرم تماس سایت:

نام: {name}
ایمیل: {email}
موضوع: {subject}

پیام:
{message}

---
این ایمیل از فرم تماس سایت ارسال شده است.
            """

            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['saedimohamad1376@gmail.com'],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS("✅ ایمیل با موفقیت ارسال شد!")
            )
            self.stdout.write(f"📧 گیرنده: saedimohamad1376@gmail.com")
            self.stdout.write(f"🔧 Email Backend: {settings.EMAIL_BACKEND}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ خطا در ارسال ایمیل: {e}")
            )

        # 3. نمایش اطلاعات
        self.stdout.write("")
        self.stdout.write("📋 اطلاعات فرم:")
        self.stdout.write(f"   نام: {name}")
        self.stdout.write(f"   ایمیل: {email}")
        self.stdout.write(f"   موضوع: {subject}")
        self.stdout.write(f"   پیام: {message[:50]}{'...' if len(message) > 50 else ''}")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("🎉 تست فرم تماس کامل شد!")
        )
