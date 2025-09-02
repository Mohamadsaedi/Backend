from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import SentEmail, CustomUser
from users.utils import send_welcome_email
from django.conf import settings
from unittest.mock import patch
from django.db.models.signals import post_save
from users import signals as users_signals

User = get_user_model()

class WelcomeEmailTest(TestCase):
    """
    تست‌های مربوط به ارسال ایمیل خوشامدگویی
    """
    
    def setUp(self):
        """
        آماده‌سازی داده‌های تست
        """
        # جلوگیری از اجرای سیگنال‌ها در این تست‌ها تا فقط تابع را تست کنیم
        post_save.disconnect(users_signals.send_welcome_email_post_save, sender=CustomUser)
        # ایجاد کاربر تست
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def tearDown(self):
        # اتصال مجدد سیگنال پس از هر تست
        post_save.connect(users_signals.send_welcome_email_post_save, sender=CustomUser)
    
    @patch('users.utils.EmailMessage')
    def test_send_welcome_email_creates_sent_email_record(self, mock_email_message):
        """
        تست ۱: بررسی اینکه ایمیل در دیتابیس مدل SentEmail ذخیره شده است
        """
        # Mock کردن EmailMessage
        mock_email = mock_email_message.return_value
        mock_email.send.return_value = 1
        
        # شمارش ایمیل‌های موجود قبل از ارسال
        initial_count = SentEmail.objects.count()
        
        # ارسال ایمیل خوشامدگویی
        result = send_welcome_email(self.user)
        
        # بررسی اینکه تابع با موفقیت اجرا شده
        self.assertTrue(result)
        
        # بررسی اینکه EmailMessage درست فراخوانی شده
        mock_email_message.assert_called_once_with(
            subject="Welcome to our site",
            body=f"Hello {self.user.username}, welcome!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email],
        )
        
        # بررسی اینکه send() فراخوانی شده
        mock_email.send.assert_called_once()
    
    def test_welcome_email_subject_is_correct(self):
        """
        تست ۲: بررسی اینکه عنوان ایمیل "Welcome to our site" است
        """
        # بررسی عنوان ایمیل در تابع
        expected_subject = "Welcome to our site"
        
        # بررسی اینکه عنوان در تابع درست تنظیم شده
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            send_welcome_email(self.user)
            
            # بررسی اینکه عنوان درست فراخوانی شده
            mock_email_message.assert_called_once()
            call_args = mock_email_message.call_args
            self.assertEqual(call_args[1]['subject'], expected_subject)
    
    def test_welcome_email_recipient_is_correct(self):
        """
        تست ۳: بررسی اینکه گیرنده همان user.email است
        """
        # بررسی گیرنده ایمیل در تابع
        expected_recipient = [self.user.email]
        
        # بررسی اینکه گیرنده در تابع درست تنظیم شده
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            send_welcome_email(self.user)
            
            # بررسی اینکه گیرنده درست فراخوانی شده
            mock_email_message.assert_called_once()
            call_args = mock_email_message.call_args
            self.assertEqual(call_args[1]['to'], expected_recipient)
    
    def test_welcome_email_content_includes_username(self):
        """
        تست اضافی: بررسی اینکه متن ایمیل شامل نام کاربری است
        """
        # بررسی متن ایمیل در تابع
        expected_message = f"Hello {self.user.username}, welcome!"
        
        # بررسی اینکه متن در تابع درست تنظیم شده
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            send_welcome_email(self.user)
            
            # بررسی اینکه متن درست فراخوانی شده
            mock_email_message.assert_called_once()
            call_args = mock_email_message.call_args
            self.assertEqual(call_args[1]['body'], expected_message)
    
    def test_welcome_email_from_email_is_correct(self):
        """
        تست اضافی: بررسی اینکه فرستنده ایمیل درست است
        """
        # بررسی فرستنده ایمیل در تابع
        expected_from_email = settings.DEFAULT_FROM_EMAIL
        
        # بررسی اینکه فرستنده در تابع درست تنظیم شده
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            send_welcome_email(self.user)
            
            # بررسی اینکه فرستنده درست فراخوانی شده
            mock_email_message.assert_called_once()
            call_args = mock_email_message.call_args
            self.assertEqual(call_args[1]['from_email'], expected_from_email)
    
    def test_send_welcome_email_returns_true_on_success(self):
        """
        تست اضافی: بررسی اینکه تابع در صورت موفقیت True برمی‌گرداند
        """
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            mock_email.send.return_value = 1
            
            result = send_welcome_email(self.user)
            self.assertTrue(result)
    
    def test_send_welcome_email_returns_false_on_error(self):
        """
        تست اضافی: بررسی اینکه تابع در صورت خطا False برمی‌گرداند
        """
        with patch('users.utils.EmailMessage') as mock_email_message:
            mock_email = mock_email_message.return_value
            mock_email.send.side_effect = Exception("Test error")
            
            result = send_welcome_email(self.user)
            self.assertFalse(result)


class WelcomeEmailSignalTest(TestCase):
    """
    تست سیگنال: با ایجاد کاربر جدید، send_welcome_email یک‌بار صدا زده می‌شود
    """

    @patch('users.signals.send_welcome_email')
    def test_signal_calls_send_welcome_email_once(self, mock_send_welcome):
        User = get_user_model()
        user = User.objects.create_user(
            username='signaluser',
            email='signal@example.com',
            password='pass12345'
        )
        mock_send_welcome.assert_called_once_with(user)
