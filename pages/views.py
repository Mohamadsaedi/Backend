from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from .models import Post, Tag
from users.forms import ContactFormForm
from django.db.models import Q

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        tag_name = self.request.GET.get('tag')
        if tag_name:
            return Post.objects.filter(tags__name=tag_name)
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
        return Post.objects.none()


class ContactView(FormView):
    """
    View برای فرم تماس
    """
    template_name = 'contact.html'
    form_class = ContactFormForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        # ذخیره فرم در دیتابیس
        contact_form = form.save()
        
        # ارسال ایمیل
        try:
            # تنظیم محتوای ایمیل
            subject = f"پیام جدید از فرم تماس: {form.cleaned_data['subject']}"
            message = f"""
پیام جدید از فرم تماس سایت:

نام: {form.cleaned_data['name']}
ایمیل: {form.cleaned_data['email']}
موضوع: {form.cleaned_data['subject']}

پیام:
{form.cleaned_data['message']}

---
این ایمیل از فرم تماس سایت ارسال شده است.
            """
            
            # ارسال ایمیل
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['saedimohamad1376@gmail.com'],  # ایمیل شما
                fail_silently=False,
            )
            
            messages.success(self.request, 'پیام شما با موفقیت ارسال شد!')
            
        except Exception as e:
            messages.error(self.request, f'خطا در ارسال ایمیل: {str(e)}')
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return super().form_invalid(form)