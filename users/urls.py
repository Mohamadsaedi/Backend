from django.urls import path
from .views import SignUpView, ProfileView, test_email_view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('test-email/', test_email_view, name='test_email'),
]