from django.core.management.base import BaseCommand
from pages.models import Post
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'بررسی عکس‌های پست‌ها و مسیرهای فایل'

    def handle(self, *args, **options):
        self.stdout.write("🔍 بررسی عکس‌های پست‌ها...")
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
                self.stdout.write(f"   📁 مسیر کامل: {post.image.path}")
                self.stdout.write(f"   🌐 URL: {post.image.url}")
                
                # بررسی وجود فایل
                if os.path.exists(post.image.path):
                    file_size = os.path.getsize(post.image.path)
                    self.stdout.write(f"   ✅ فایل موجود - اندازه: {file_size / 1024:.1f} KB")
                else:
                    self.stdout.write("   ❌ فایل وجود ندارد!")
                    
                # بررسی MEDIA_ROOT
                self.stdout.write(f"   📂 MEDIA_ROOT: {settings.MEDIA_ROOT}")
                self.stdout.write(f"   🌐 MEDIA_URL: {settings.MEDIA_URL}")
                
            else:
                self.stdout.write("   ❌ بدون عکس")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🎯 نکات مهم:")
        self.stdout.write("1. اگر عکس‌ها نمایش داده نمی‌شوند، مطمئن شوید که:")
        self.stdout.write("   - MEDIA_URL در urls.py تنظیم شده باشد")
        self.stdout.write("   - پوشه media وجود داشته باشد")
        self.stdout.write("   - فایل‌های عکس در مسیر درست ذخیره شده باشند")
        self.stdout.write("2. در template، شرط user.role == 'viewer' حذف شده باشد")
        self.stdout.write("3. عکس‌ها با {{ post.image.url }} نمایش داده شوند")
