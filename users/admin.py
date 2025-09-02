from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SentEmail, ContactForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # فیلدهایی که در لیست کاربران نمایش داده می‌شود
    list_display = ['username', 'email', 'role', 'is_staff']
    # اضافه کردن فیلد role به فرم ویرایش کاربر
    fieldsets = UserAdmin.fieldsets + (
        ('نقش‌ها', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'from_email', 'recipients', 'date_sent']
    list_filter = ['date_sent']
    search_fields = ['subject', 'from_email', 'body', 'recipients']
    readonly_fields = ['date_sent']
    ordering = ['-date_sent']  # مرتب‌سازی بر اساس تاریخ ارسال (جدیدترین اول)
    
    def get_recipients_display(self, obj):
        """نمایش گیرندگان به صورت خوانا"""
        recipients = obj.get_recipients_list()
        return ', '.join(recipients[:3]) + ('...' if len(recipients) > 3 else '')
    get_recipients_display.short_description = 'گیرندگان'


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "علامت‌گذاری به عنوان خوانده شده"
    
    actions = ['mark_as_read']