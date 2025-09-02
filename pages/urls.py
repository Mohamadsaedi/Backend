from django.urls import path
from .views import PostListView, PostDetailView, SearchResultsView, ContactView

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', PostListView.as_view(), name='home'),
]