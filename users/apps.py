from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # اطمینان از بارگذاری سیگنال‌ها
        try:
            from . import signals  # noqa: F401
        except Exception:
            # در زمان مهاجرت‌ها ممکن است ماژول‌ها کامل نباشند
            pass