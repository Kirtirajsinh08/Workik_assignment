from django.urls import path
from .views import GitHubAuthView, GitHubCallbackView, RepositoryListView, WebhookView

urlpatterns = [
    path('github-auth/', GitHubAuthView.as_view(), name='github-auth'),
    path('github-callback/', GitHubCallbackView.as_view(), name='github-callback'),
    path('repositories/', RepositoryListView.as_view(), name='repository-list'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]