from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class CustomUser(AbstractUser):
    # تعریف نقش‌ها
    ROLE_CHOICES = (
        ('viewer', 'بیننده عکس'),
        ('regular', 'کاربر عادی'),
    )
    # فیلد جدید برای نقش
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular', verbose_name="نقش")

class SentEmail(models.Model):
    """
    مدل برای ذخیره ایمیل‌های ارسال شده
    """
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن ایمیل")
    from_email = models.EmailField(verbose_name="از ایمیل")
    recipients = models.TextField(verbose_name="گیرندگان")  # به صورت JSON ذخیره می‌شود
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    
    class Meta:
        verbose_name = "ایمیل ارسال شده"
        verbose_name_plural = "ایمیل‌های ارسال شده"
        ordering = ['-date_sent']
    
    def __str__(self):
        return f"{self.subject} - {self.from_email}"
    
    def get_recipients_list(self):
        """
        تبدیل JSON به لیست گیرندگان
        """
        try:
            return json.loads(self.recipients)
        except json.JSONDecodeError:
            return []
    
    def set_recipients_list(self, recipients_list):
        """
        تبدیل لیست گیرندگان به JSON
        """
        self.recipients = json.dumps(recipients_list)


class ContactForm(models.Model):
    """
    مدل برای ذخیره فرم‌های تماس
    """
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    
    class Meta:
        verbose_name = "فرم تماس"
        verbose_name_plural = "فرم‌های تماس"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"