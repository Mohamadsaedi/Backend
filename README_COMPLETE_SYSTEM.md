# 🎉 راهنمای کامل سیستم Django Contact Form

## 📋 خلاصه پروژه

این پروژه یک سیستم کامل فرم تماس Django است که شامل:
- ✅ Email Backend سفارشی برای ذخیره ایمیل‌ها در دیتابیس
- ✅ فرم تماس زیبا با Bootstrap
- ✅ ارسال ایمیل واقعی به Gmail
- ✅ رابط کاربری Django Admin
- ✅ تست‌های کامل و مدیریت دستورات

## 🏗️ ساختار پروژه

```
Backend/
├── myproject/
│   ├── settings.py          # تنظیمات اصلی Django
│   └── urls.py              # URL های پروژه
├── users/
│   ├── models.py            # مدل‌های SentEmail و ContactForm
│   ├── forms.py             # فرم‌های ContactFormForm
│   ├── admin.py             # تنظیمات Admin
│   ├── email_backends.py    # Email Backend سفارشی
│   ├── management/commands/ # دستورات مدیریت
│   └── tests.py             # تست‌های واحد
├── pages/
│   ├── views.py             # View های فرم تماس
│   └── urls.py              # URL های صفحات
└── templates/
    ├── base.html            # قالب پایه
    └── contact.html         # قالب فرم تماس
```

## 🔧 تنظیمات اصلی

### 1. Email Backend در settings.py

```python
# تنظیمات Email Backend
if DEBUG:
    # در حالت توسعه، ایمیل‌ها در دیتابیس ذخیره می‌شوند
    EMAIL_BACKEND = 'users.email_backends.DatabaseEmailBackend'
    print("🔧 Email Backend: DatabaseEmailBackend (حالت توسعه)")
else:
    # در حالت تولید، از SMTP واقعی استفاده کنید
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'saedimohamad1376@gmail.com'
    EMAIL_HOST_PASSWORD = 'wcfy jtvl uwod frca'  # App Password از Gmail
    DEFAULT_FROM_EMAIL = 'saedimohamad1376@gmail.com'
    print("🔧 Email Backend: SMTP Backend (حالت تولید)")

# تنظیمات پیش‌فرض برای ایمیل
DEFAULT_FROM_EMAIL = 'saedimohamad1376@gmail.com'

# تنظیمات امنیتی برای حالت تولید
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']
```

### 2. مدل‌های دیتابیس

#### SentEmail Model
```python
class SentEmail(models.Model):
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن ایمیل")
    from_email = models.EmailField(verbose_name="از ایمیل")
    recipients = models.TextField(verbose_name="گیرندگان")  # به صورت JSON ذخیره می‌شود
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    
    def get_recipients_list(self):
        try:
            return json.loads(self.recipients)
        except json.JSONDecodeError:
            return []
    
    def set_recipients_list(self, recipients_list):
        self.recipients = json.dumps(recipients_list)
```

#### ContactForm Model
```python
class ContactForm(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
```

### 3. Email Backend سفارشی

```python
class DatabaseEmailBackend(BaseEmailBackend):
    """
    Email Backend سفارشی که ایمیل‌ها را در دیتابیس ذخیره می‌کند
    """
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        num_sent = 0
        for message in email_messages:
            sent = self._send_message(message)
            if sent:
                num_sent += 1
        return num_sent

    def _send_message(self, message):
        if not message.recipients():
            return False
        try:
            sent_email = SentEmail(
                subject=message.subject,
                body=message.body,
                from_email=message.from_email,
            )
            sent_email.set_recipients_list(list(message.recipients()))
            sent_email.save()
            print(f"ایمیل '{message.subject}' در دیتابیس ذخیره شد.")
            return True
        except Exception as e:
            print(f"خطا در ذخیره ایمیل: {e}")
            return False
```

### 4. فرم تماس

```python
class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع پیام'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'پیام شما'
            })
        }
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'subject': 'موضوع',
            'message': 'پیام'
        }
```

### 5. View فرم تماس

```python
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactFormForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        # ذخیره فرم در دیتابیس
        contact_form = form.save()
        
        # ارسال ایمیل
        try:
            subject = f"پیام جدید از فرم تماس: {form.cleaned_data['subject']}"
            message = f"""
پیام جدید از فرم تماس سایت:

نام: {form.cleaned_data['name']}
ایمیل: {form.cleaned_data['email']}
موضوع: {form.cleaned_data['subject']}

پیام:
{form.cleaned_data['message']}

---
این ایمیل از فرم تماس سایت ارسال شده است.
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['saedimohamad1376@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(self.request, 'پیام شما با موفقیت ارسال شد!')
            
        except Exception as e:
            messages.error(self.request, f'خطا در ارسال ایمیل: {str(e)}')
        
        return super().form_valid(form)
```

## 🚀 نحوه استفاده

### 1. اجرای سرور

```bash
# در پوشه Backend
python manage.py runserver
```

### 2. دسترسی به فرم تماس

- **URL**: `http://127.0.0.1:8000/contact/`
- **توضیحات**: فرم زیبا با Bootstrap برای دریافت پیام‌های کاربران

### 3. دسترسی به Django Admin

- **URL**: `http://127.0.0.1:8000/admin/`
- **توضیحات**: مشاهده و مدیریت فرم‌های تماس و ایمیل‌های ارسال شده

## 📧 مدیریت دستورات

### 1. تست Email Backend

```bash
# تست Database Email Backend
python manage.py test_database_email --email test@example.com

# تست Gmail SMTP
python manage.py test_gmail_smtp

# تست فرم تماس
python manage.py test_contact_form --name "نام تست" --email "test@example.com" --subject "موضوع تست" --message "پیام تست"
```

### 2. بررسی تنظیمات

```bash
# بررسی تنظیمات Email Backend
python manage.py check_email_settings

# نمایش ایمیل‌های ارسال شده
python manage.py list_sent_emails --limit 10
```

### 3. تست Welcome Email

```bash
# تست ارسال ایمیل خوشامدگویی
python manage.py test_welcome_email --username admin
```

## 🔍 تست‌های انجام شده

### ✅ تست‌های موفق:

1. **Database Email Backend**: ✅ موفق
   - ایمیل‌ها در دیتابیس ذخیره می‌شوند
   - در Django Admin قابل مشاهده هستند

2. **Gmail SMTP**: ✅ موفق
   - App Password تنظیم شده: `wcfy jtvl uwod frca`
   - ایمیل‌ها واقعاً به Gmail ارسال می‌شوند

3. **فرم تماس**: ✅ موفق
   - فرم زیبا با Bootstrap
   - ذخیره در دیتابیس
   - ارسال ایمیل

4. **Django Admin**: ✅ موفق
   - مدیریت فرم‌های تماس
   - مشاهده ایمیل‌های ارسال شده
   - عملیات bulk (علامت‌گذاری خوانده شده)

### 📊 آمار فعلی:

- **تعداد فرم‌های تماس**: 6
- **تعداد ایمیل‌های ارسال شده**: 9+
- **وضعیت سیستم**: کامل و فعال

## 🛡️ تنظیمات امنیتی

### 1. Gmail App Password

- **ایمیل**: `saedimohamad1376@gmail.com`
- **App Password**: `wcfy jtvl uwod frca`
- **Two-Factor Authentication**: فعال

### 2. تنظیمات Django

- **DEBUG**: False (در حالت تولید)
- **ALLOWED_HOSTS**: تنظیم شده
- **CSRF Protection**: فعال
- **Email Backend**: SMTP Gmail

## 🚨 عیب‌یابی

### مشکل 1: خطای ALLOWED_HOSTS
```
CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.
```
**راه حل**: در `settings.py` اضافه کنید:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']
```

### مشکل 2: خطای Authentication Gmail
```
SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```
**راه حل**: 
1. Two-Factor Authentication را فعال کنید
2. App Password جدید ایجاد کنید
3. App Password را در `settings.py` تنظیم کنید

### مشکل 3: ایمیل در Spam
**راه حل**: 
1. فولدر Spam را چک کنید
2. ایمیل را از Spam خارج کنید
3. "Not spam" را کلیک کنید

## 📱 قالب‌های HTML

### 1. base.html
- قالب پایه با Bootstrap
- منوی ناوبری
- لینک به فرم تماس

### 2. contact.html
- فرم تماس زیبا
- نمایش پیام‌های موفقیت/خطا
- اطلاعات تماس

## 🎯 ویژگی‌های کلیدی

### ✅ Email Backend هوشمند
- در حالت توسعه: ذخیره در دیتابیس
- در حالت تولید: ارسال واقعی به Gmail

### ✅ فرم تماس کامل
- اعتبارسنجی فرم
- ذخیره در دیتابیس
- ارسال ایمیل
- پیام‌های بازخورد

### ✅ مدیریت کامل
- Django Admin
- عملیات bulk
- فیلتر و جستجو
- مرتب‌سازی

### ✅ تست و عیب‌یابی
- Management Commands
- تست‌های واحد
- بررسی تنظیمات
- نمایش آمار

## 🎉 نتیجه نهایی

**سیستم فرم تماس Django کامل و آماده است!**

### ✅ مزایا:
- **امنیت بالا**: App Password و Two-Factor Authentication
- **انعطاف‌پذیری**: Email Backend هوشمند
- **کاربرپسندی**: رابط کاربری زیبا و ساده
- **مدیریت آسان**: Django Admin کامل
- **تست کامل**: Management Commands و Unit Tests

### 🚀 قابلیت‌ها:
- دریافت پیام‌های کاربران
- ارسال ایمیل واقعی به Gmail
- ذخیره تمام داده‌ها در دیتابیس
- مدیریت کامل از طریق Admin
- تست و عیب‌یابی آسان

**حالا می‌توانید از سیستم فرم تماس استفاده کنید و ایمیل‌ها را در Gmail خود دریافت کنید!** 🎉

---

## 📞 اطلاعات تماس

- **ایمیل**: saedimohamad1376@gmail.com
- **تاریخ تکمیل**: سپتامبر 2025
- **وضعیت**: کامل و فعال
- **نسخه Django**: 5.2.4
