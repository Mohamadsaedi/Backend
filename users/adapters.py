from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        # اگر نام کاربری خالی است، از ایمیل استفاده کن
        if not user.username:
            user.username = user.email.split('@')[0]
            # اگر نام کاربری تکراری است، عدد اضافه کن
            counter = 1
            original_username = user.username
            while User.objects.filter(username=user.username).exists():
                user.username = f"{original_username}{counter}"
                counter += 1
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # تولید نام کاربری منحصر به فرد از ایمیل
        if user.email:
            base_username = user.email.split('@')[0]
            # حذف کاراکترهای غیرمجاز
            base_username = ''.join(c for c in base_username if c.isalnum() or c in '._-')
            username = base_username
            
            # اگر نام کاربری تکراری است، عدد اضافه کن
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user.username = username
            
            # تنظیم نام و نام خانوادگی از Google
            if sociallogin.account.extra_data:
                extra_data = sociallogin.account.extra_data
                if 'given_name' in extra_data:
                    user.first_name = extra_data['given_name']
                if 'family_name' in extra_data:
                    user.last_name = extra_data['family_name']
            
            print(f"کاربر جدید: {username} ({user.email}) - {user.first_name} {user.last_name}")
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # اطمینان از ذخیره شدن اطلاعات
        user.save()
        return user
    
    def is_auto_signup_allowed(self, request, sociallogin):
        # اجازه auto signup برای همه
        return True
    
    def pre_social_login(self, request, sociallogin):
        # اگر کاربر قبلاً وجود دارد، آن را وارد کن
        if sociallogin.is_existing:
            return
        
        # بررسی وجود کاربر با همین ایمیل
        if sociallogin.account.extra_data.get('email'):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            email = sociallogin.account.extra_data['email']
            try:
                existing_user = User.objects.get(email=email)
                # اتصال حساب اجتماعی به کاربر موجود
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
    
    def get_connect_redirect_url(self, request, socialaccount):
        # بعد از اتصال، به صفحه اصلی برو
        return '/'
    
    def get_signup_redirect_url(self, request, socialaccount):
        # بعد از ثبت نام، به صفحه اصلی برو
        return '/'
