from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_user_creation(self):
        """Test that a user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_user_str(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), f"{self.user.first_name} {self.user.last_name} <{self.user.email}> ({self.user.role})")

    def test_user_has_required_fields(self):
        """Test that the user model includes required fields"""
        self.assertTrue(self.User.REQUIRED_FIELDS)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.login_url = '/api/login/'  # Update with your login endpoint
        self.user_detail_url = f'/api/users/{self.user.uuid}/'  # Update with your endpoint
        self.change_password_url = f'/api/users/{self.user.uuid}/change/'
        self.restricted_url = '/api/restricted/'

    def test_user_login(self):
        """Test user can log in with valid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_authenticated(self):
        """Test retrieving user details when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_user_detail_unauthenticated(self):
        """Test retrieving user details when not authenticated"""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_permission(self):
        """Test user permission for accessing restricted resources"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(restricted_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_permission(self):
        """Test user permission for accessing restricted resources"""
        # Create a restricted resource
        restricted_url = '/api/restricted/'  # Update with actual restricted endpoint
        self.client.force_authenticate(user=self.user)

        response = self.client.get(restricted_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_registration(self):
        """Test user registration endpoint"""
        registration_url = '/api/auth/register/'  # Update with your endpoint
        response = self.client.post(registration_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')

    def test_change_password(self):
        """Test changing password for authenticated user"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.change_password_url, {
            'old_password': 'password123',
            'new_password': 'newpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if new password works
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))


