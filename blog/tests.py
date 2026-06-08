from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from blog.models import Post
from django.urls import reverse


class AuthTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='amar', password='12345')
        self.login_url = '/blog/api/auth/jwt/login/'
        self.refresh_url = '/blog/api/auth/jwt/refresh/'

    def test_login(self):
        response = self.client.post(self.login_url, {
            "username": "amar",
            "password": "12345"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_refresh_token(self):
        response = self.client.post(self.login_url, {
            "username": "amar",
            "password": "12345"
        })

        refresh = response.data['refresh']

        response = self.client.post(self.refresh_url, {
            "refresh": refresh
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)


class PostTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='amar', password='12345')

        login_response = self.client.post('/blog/api/auth/jwt/login/', {
            "username": "amar",
            "password": "12345"
        })

        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.post_url = '/blog/api/v1/posts/'

    def test_create_post(self):
        data = {
            "title": "Test Post",
            "content": "Test content",
            "is_published": True
        }

        response = self.client.post(self.post_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Test Post")


class PermissionTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='amar', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')

        self.post = Post.objects.create(
            title="Test",
            content="Test",
            author=self.user1
        )

        login_response = self.client.post('/blog/api/auth/jwt/login/', {
            "username": "user2",
            "password": "12345"
        })

        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_permission(self):
        response = self.client.put(f'/blog/api/v1/posts/{self.post.id}/', {
            "title": "Hack"
        })

        self.assertEqual(response.status_code, 403)