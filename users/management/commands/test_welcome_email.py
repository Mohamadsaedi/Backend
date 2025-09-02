from django.core.management.base import BaseCommand
from users.models import CustomUser
from users.utils import send_welcome_email

class Command(BaseCommand):
    help = 'تست تابع send_welcome_email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='شناسه کاربر برای تست',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='نام کاربری برای تست',
        )

    def handle(self, *args, **options):
        user_id = options['user_id']
        username = options['username']
        
        self.stdout.write("🧪 تست تابع send_welcome_email")
        self.stdout.write("=" * 50)
        
        # پیدا کردن کاربر
        user = None
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'کاربر با شناسه {user_id} یافت نشد.')
                )
                return
        elif username:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'کاربر با نام کاربری {username} یافت نشد.')
                )
                return
        else:
            # استفاده از اولین کاربر موجود
            try:
                user = CustomUser.objects.first()
                if not user:
                    self.stdout.write(
                        self.style.ERROR('هیچ کاربری در دیتابیس وجود ندارد.')
                    )
                    return
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'خطا در پیدا کردن کاربر: {e}')
                )
                return
        
        self.stdout.write(f"👤 کاربر انتخاب شده: {user.username} ({user.email})")
        
        # تست ارسال ایمیل خوشامدگویی
        try:
            result = send_welcome_email(user)
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS("✅ ایمیل خوشامدگویی با موفقیت ارسال شد!")
                )
            else:
                self.stdout.write(
                    self.style.ERROR("❌ خطا در ارسال ایمیل خوشامدگویی")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ خطا در تست: {e}")
            )
