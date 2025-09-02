from django.core.management.base import BaseCommand
from pages.models import Post, Tag
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'ایجاد پست تست با عکس'

    def handle(self, *args, **options):
        self.stdout.write("🧪 ایجاد پست تست با عکس...")
        self.stdout.write("=" * 50)
        
        try:
            # ایجاد تگ تست
            tag, created = Tag.objects.get_or_create(name='تست')
            if created:
                self.stdout.write("✅ تگ 'تست' ایجاد شد")
            else:
                self.stdout.write("✅ تگ 'تست' از قبل وجود دارد")
            
            # ایجاد پست تست
            post = Post.objects.create(
                title='پست تست با عکس',
                body='این یک پست تست است که برای بررسی نمایش عکس‌ها ایجاد شده است. اگر این عکس را می‌بینید، یعنی سیستم درست کار می‌کند!'
            )
            post.tags.add(tag)
            
            self.stdout.write(f"✅ پست تست ایجاد شد (ID: {post.id})")
            self.stdout.write(f"   عنوان: {post.title}")
            self.stdout.write(f"   تگ‌ها: {', '.join([tag.name for tag in post.tags.all()])}")
            
            # بررسی عکس‌های موجود
            media_dir = 'media/post_images'
            if os.path.exists(media_dir):
                images = [f for f in os.listdir(media_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                if images:
                    # انتخاب اولین عکس موجود
                    image_path = os.path.join(media_dir, images[0])
                    self.stdout.write(f"   📸 عکس انتخاب شده: {images[0]}")
                    
                    # اضافه کردن عکس به پست
                    with open(image_path, 'rb') as img_file:
                        post.image.save(images[0], File(img_file), save=True)
                    
                    self.stdout.write(f"   ✅ عکس به پست اضافه شد: {post.image.url}")
                else:
                    self.stdout.write("   ⚠️ هیچ عکسی در پوشه media/post_images یافت نشد")
            else:
                self.stdout.write("   ❌ پوشه media/post_images وجود ندارد")
            
            self.stdout.write("\n🎯 برای مشاهده پست:")
            self.stdout.write(f"   - صفحه اصلی: http://127.0.0.1:8000/")
            self.stdout.write(f"   - جزئیات پست: http://127.0.0.1:8000/post/{post.id}/")
            self.stdout.write(f"   - Admin: http://127.0.0.1:8000/admin/pages/post/{post.id}/change/")
            
        except Exception as e:
            self.stdout.write(f"❌ خطا در ایجاد پست تست: {e}")
