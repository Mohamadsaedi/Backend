from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام تگ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    body = models.TextField(verbose_name="متن اصلی")
    image = models.ImageField(upload_to='post_images/', verbose_name="تصویر", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="تگ‌ها", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"

    def __str__(self):
        return self.title