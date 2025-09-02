from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'تست Email Backend که ایمیل‌ها را در دیتابیس ذخیره می‌کند'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='ایمیل برای تست',
        )

    def handle(self, *args, **options):
        email = options['email']
        
        self.stdout.write("🧪 شروع تست Email Backend...")
        
        try:
            # ارسال ایمیل تست
            send_mail(
                subject='تست Email Backend',
                message='این یک ایمیل تست است که در دیتابیس ذخیره می‌شود.',
                from_email='noreply@example.com',
                recipient_list=[email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ ایمیل تست با موفقیت ارسال و در دیتابیس ذخیره شد.')
            )
            self.stdout.write(f'📧 گیرنده: {email}')
            self.stdout.write(f'🔧 Email Backend: {settings.EMAIL_BACKEND}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ خطا در ارسال ایمیل: {e}')
            )
