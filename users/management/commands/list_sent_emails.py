from django.core.management.base import BaseCommand
from users.models import SentEmail

class Command(BaseCommand):
    help = 'نمایش ایمیل‌های ارسال شده در دیتابیس'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='تعداد ایمیل‌ها برای نمایش (پیش‌فرض: 10)',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        
        self.stdout.write("📧 ایمیل‌های ارسال شده در دیتابیس:")
        self.stdout.write("=" * 80)
        
        # دریافت ایمیل‌ها
        emails = SentEmail.objects.all().order_by('-date_sent')[:limit]
        
        if not emails:
            self.stdout.write(self.style.WARNING("هیچ ایمیلی در دیتابیس یافت نشد."))
            return
        
        total_count = SentEmail.objects.count()
        self.stdout.write(f"تعداد کل ایمیل‌ها: {total_count}")
        self.stdout.write(f"نمایش {len(emails)} ایمیل آخر:")
        self.stdout.write("")
        
        for i, email in enumerate(emails, 1):
            self.stdout.write(f"{i}. {email.subject}")
            self.stdout.write(f"   از: {email.from_email}")
            self.stdout.write(f"   به: {email.get_recipients_list()}")
            self.stdout.write(f"   تاریخ: {email.date_sent.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdout.write(f"   متن: {email.body[:50]}{'...' if len(email.body) > 50 else ''}")
            self.stdout.write("-" * 80)
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ {len(emails)} ایمیل نمایش داده شد.")
        )
