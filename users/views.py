from .utils import activateEmail
from .forms import CustomUserCreationForm
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('homepage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(
        request=request,
        template_name="users/register.html",
        context={"form": form}
    )
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import CustomUserCreationForm
from django.contrib.auth import login

# این کلاس برای ثبت‌نام است و از قبل وجود داشت
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        # ایجاد کاربر جدید با وضعیت غیرفعال
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # ارسال پیام فعال‌سازی
        activateEmail(self.request, user, form.cleaned_data.get('email'))
        # پیام موفقیت ثبت‌نام
        messages.success(self.request, f"New account created: {user.username}")
        return redirect('/')

# این کلاس جدید برای نمایش صفحه پروفایل است
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

@login_required
def test_email_view(request):
    """
    View برای تست ارسال ایمیل
    """
    if request.method == 'POST':
        try:
            user = request.user
            subject = 'تست ایمیل خوشامدگویی'
            
            # محتوای HTML ایمیل
            html_message = render_to_string('users/welcome_email.html', {
                'user': user,
                'site_name': 'وب‌سایت تست'
            })
            
            # محتوای متنی ساده
            plain_message = strip_tags(html_message)
            
            # ارسال ایمیل
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'✅ ایمیل تست با موفقیت به {user.email} ارسال شد.')
            
        except Exception as e:
            messages.error(request, f'❌ خطا در ارسال ایمیل: {e}')
        
        return redirect('profile')
    
    return redirect('profile')