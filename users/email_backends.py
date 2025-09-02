from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from .models import SentEmail
import json

class DatabaseEmailBackend(BaseEmailBackend):
    """
    Email Backend سفارشی که ایمیل‌ها را در دیتابیس ذخیره می‌کند
    """
    
    def send_messages(self, email_messages):
        """
        ارسال پیام‌های ایمیل و ذخیره آن‌ها در دیتابیس
        """
        if not email_messages:
            return 0
        
        num_sent = 0
        for message in email_messages:
            sent = self._send_message(message)
            if sent:
                num_sent += 1
        
        return num_sent
    
    def _send_message(self, message):
        """
        ارسال یک پیام ایمیل و ذخیره آن در دیتابیس
        """
        if not message.recipients():
            return False
        
        try:
            # ذخیره ایمیل در دیتابیس
            sent_email = SentEmail(
                subject=message.subject,
                body=message.body,
                from_email=message.from_email,
            )
            # ذخیره گیرندگان به صورت JSON
            sent_email.set_recipients_list(list(message.recipients()))
            sent_email.save()
            
            print(f"ایمیل '{message.subject}' در دیتابیس ذخیره شد.")
            return True
            
        except Exception as e:
            print(f"خطا در ذخیره ایمیل: {e}")
            return False
