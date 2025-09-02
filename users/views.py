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
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .utils import activateEmail, send_welcome_email

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activateEmail(self.request, user)
        messages.success(self.request, f"New account created: {user.username}. Please check your email to activate your account.")
        return redirect('/')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        send_welcome_email(user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

@login_required
def test_email_view(request):
    """
    View for testing email sending
    """
    if request.method == 'POST':
        try:
            user = request.user
            subject = 'Test welcome email'
            
            html_message = render_to_string('users/welcome_email.html', {
                'user': user,
                'site_name': 'Test Website'
            })
            
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'✅ Test email sent successfully to {user.email}.')
            
        except Exception as e:
            messages.error(request, f'❌ Error sending email: {e}')
        
        return redirect('profile')
    
    return redirect('profile')