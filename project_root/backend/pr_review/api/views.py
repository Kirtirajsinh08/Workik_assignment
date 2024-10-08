from django.shortcuts import render

# Create your views here.
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import GithubUser, Repository
from .serializers import RepositorySerializer

class GitHubAuthView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
        return JsonResponse({
            'authorization_url': f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=repo'
        })

class GitHubCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        access_token = self.get_access_token(code)
        user_data = self.get_user_data(access_token)
        
        user, created = GithubUser.objects.update_or_create(
            github_id=user_data['id'],
            defaults={
                'username': user_data['login'],
                'access_token': access_token
            }
        )
        
        self.create_webhooks(user)
        
        return JsonResponse({'message': 'Authentication successful'})
    
    def get_access_token(self, code):
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': settings.GITHUB_CLIENT_ID,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code
            },
            headers={'Accept': 'application/json'}
        )
        return response.json()['access_token']
    
    def get_user_data(self, access_token):
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        return response.json()
    
    def create_webhooks(self, user):
        repos = self.get_user_repositories(user.access_token)
        for repo in repos:
            repository, created = Repository.objects.get_or_create(
                github_id=repo['id'],
                name=repo['name'],
                owner=user
            )
            if created:
                self.create_webhook(user.access_token, repo['full_name'], repository)

    def get_user_repositories(self, access_token):
        response = requests.get(
            'https://api.github.com/user/repos',
            headers={'Authorization': f'token {access_token}'}
        )
        return response.json()

    def create_webhook(self, access_token, repo_full_name, repository):
        response = requests.post(
            f'https://api.github.com/repos/{repo_full_name}/hooks',
            headers={'Authorization': f'token {access_token}'},
            json={
                'name': 'web',
                'active': True,
                'events': ['pull_request'],
                'config': {
                    'url': settings.WEBHOOK_URL,
                    'content_type': 'json'
                }
            }
        )
        if response.status_code == 201:
            repository.webhook_id = response.json()['id']
            repository.save()

class RepositoryListView(APIView):
    def get(self, request):
        user = GithubUser.objects.get(github_id=request.user.id)
        repositories = Repository.objects.filter(owner=user)
        serializer = RepositorySerializer(repositories, many=True)
        return Response(serializer.data)

class WebhookView(APIView):
    def post(self, request):
        event = request.headers.get('X-GitHub-Event')
        if event == 'pull_request':
            pr_data = request.data['pull_request']
            if pr_data['state'] == 'open':
                self.review_pr(pr_data)
        return Response(status=200)

    def review_pr(self, pr_data):
        diff_url = pr_data['diff_url']
        diff_content = requests.get(diff_url).text
        
        # Use OpenAI's GPT-3 to review the PR
        review = self.get_ai_review(diff_content)
        
        # Post the review as a comment
        self.post_review_comment(pr_data['comments_url'], review)

    def get_ai_review(self, diff_content):
        # Implement your AI model here to review the PR
        # For this example, we'll use a placeholder
        return "This is an AI-generated review of your PR."

    def post_review_comment(self, comments_url, review):
        user = GithubUser.objects.first()  # You might want to implement a better way to get the user
        response = requests.post(
            comments_url,
            headers={'Authorization': f'token {user.access_token}'},
            json={'body': review}
        )
        return response.status_code == 201