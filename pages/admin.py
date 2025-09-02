from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image', 'created_at')
    filter_horizontal = ('tags',)

    def get_image(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width="100px" />'
            )
        return "عکسی آپلود نشده"
    
    get_image.short_description = "پیش‌نمایش تصویر"

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)