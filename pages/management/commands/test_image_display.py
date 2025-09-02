from django.core.management.base import BaseCommand
from pages.models import Post
from django.conf import settings
import os
import requests

class Command(BaseCommand):
    help = 'تست نمایش عکس‌ها در سایت'

    def handle(self, *args, **options):
        self.stdout.write("🧪 تست نمایش عکس‌ها...")
        self.stdout.write("=" * 50)
        
        posts = Post.objects.all()
        
        if not posts.exists():
            self.stdout.write("❌ هیچ پستی در دیتابیس وجود ندارد!")
            return
        
        for post in posts:
            self.stdout.write(f"\n📝 پست: {post.title}")
            self.stdout.write(f"   ID: {post.id}")
            
            if post.image:
                self.stdout.write(f"   📸 عکس: {post.image.name}")
                self.stdout.write(f"   🌐 URL: {post.image.url}")
                
                # بررسی وجود فایل
                if os.path.exists(post.image.path):
                    file_size = os.path.getsize(post.image.path)
                    self.stdout.write(f"   ✅ فایل موجود - اندازه: {file_size / 1024:.1f} KB")
                    
                    # تست URL
                    base_url = "http://127.0.0.1:8000"
                    image_url = base_url + post.image.url
                    self.stdout.write(f"   🌐 URL کامل: {image_url}")
                    
                    try:
                        response = requests.get(image_url, timeout=5)
                        if response.status_code == 200:
                            self.stdout.write(f"   ✅ عکس قابل دسترسی است (کد: {response.status_code})")
                        else:
                            self.stdout.write(f"   ❌ عکس قابل دسترسی نیست (کد: {response.status_code})")
                    except requests.exceptions.RequestException as e:
                        self.stdout.write(f"   ⚠️ خطا در تست URL: {e}")
                        self.stdout.write(f"   💡 سرور را اجرا کنید: python manage.py runserver")
                        
                else:
                    self.stdout.write("   ❌ فایل وجود ندارد!")
                    
                # بررسی تنظیمات
                self.stdout.write(f"   📂 MEDIA_ROOT: {settings.MEDIA_ROOT}")
                self.stdout.write(f"   🌐 MEDIA_URL: {settings.MEDIA_URL}")
                self.stdout.write(f"   🔧 DEBUG: {settings.DEBUG}")
                
            else:
                self.stdout.write("   ❌ بدون عکس")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🎯 نکات مهم:")
        self.stdout.write("1. اگر عکس‌ها نمایش داده نمی‌شوند:")
        self.stdout.write("   - DEBUG باید True باشد")
        self.stdout.write("   - سرور باید اجرا شده باشد")
        self.stdout.write("   - فایل‌ها باید در مسیر درست باشند")
        self.stdout.write("2. برای تست:")
        self.stdout.write("   - به http://127.0.0.1:8000/ بروید")
        self.stdout.write("   - عکس‌ها باید نمایش داده شوند")
        self.stdout.write("3. اگر مشکل ادامه دارد:")
        self.stdout.write("   - فایل‌های media را چک کنید")
        self.stdout.write("   - تنظیمات urls.py را بررسی کنید")
