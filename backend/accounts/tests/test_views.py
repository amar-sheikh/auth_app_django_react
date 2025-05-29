import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import json
import time

@pytest.fixture
def user():
    return User.objects.create_user(
        username='user1',
        email='user1@xyz.com',
        password='Password#123',
        first_name='abc',
        last_name='123'
    )

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def logged_in_client(user):
    client = Client()
    client.login(username='user1', password='Password#123')
    return client

def test_csrf_view(client):
    response = client.get(reverse('csrf'))

    assert response.status_code == 200
    assert 'csrftoken' in response.cookies, 'CSRF Token is missing in respons.'
    assert json.loads(response.content)['message'] == 'CSRF token set successfully.'

@pytest.mark.django_db
class TestWhoAmIView:
    def test_whoami_view_with_user_logged_in(self, logged_in_client, user):
        response = logged_in_client.get(reverse('whoami'))

        assert response.status_code == 200
        assert json.loads(response.content)['user']['id'] == user.id
        assert json.loads(response.content)['user']['username'] == 'user1'

    def test_whoami_view_with_user_logged_in(self, client):
        response = client.get(reverse('whoami'))

        assert response.status_code == 401
        assert json.loads(response.content)['error'] == 'User not authenticated.'

@pytest.mark.django_db
class TestRegisterView:

    @pytest.fixture
    def form_attributes(self):
        return {
            'username': 'user1',
            'email': 'user2@xyz.com',
            'password1': 'Password#123',
            'password2': 'Password#123',
            'first_name': 'abc',
            'last_name': '123'
        }

    def test_register_view(self, client, form_attributes):
        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 201
        assert json.loads(response.content)['message'] == 'User registered successfully.'

    def test_register_view_with_get_request(self, client):
        response = client.get(reverse('register'))

        assert response.status_code == 405

    def test_register_view_with_username_already_exists(self, client, user, form_attributes):
        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'A user with that username already exists.' in json.loads(response.content)['errors']['username']

    def test_register_view_with_email_already_exists(self, client, user, form_attributes):
        form_attributes['username'] = 'user2'
        form_attributes['email'] = 'user1@xyz.com'

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'User with this Email address already exists.' in json.loads(response.content)['errors']['email']

    def test_register_view_without_attributes(self, client):
        response = client.post(reverse('register'),
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        errors = json.loads(response.content)['errors']
        assert 'This field is required.' in errors['username']
        assert 'This field is required.' in errors['email']
        assert 'This field is required.' in errors['password1']
        assert 'This field is required.' in errors['password2']
        assert 'This field is required.' in errors['first_name']
        assert 'This field is required.' in errors['last_name']

    def test_register_view_with_username_having_invalid_character(self, client, form_attributes):
        form_attributes['username'] = 'User 1'

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in json.loads(response.content)['errors']['username']

    def test_register_view_with_shorter_password(self, client, form_attributes):
        form_attributes['password1'] = "123"
        form_attributes['password2'] = "123"

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too short. It must contain at least 8 characters.' in json.loads(response.content)['errors']['password2']

    def test_register_view_with_common_password(self, client, form_attributes):
        form_attributes['password1'] = "password123"
        form_attributes['password2'] = "password123"

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too common.' in json.loads(response.content)['errors']['password2']

    def test_register_view_with_only_numeric_password(self, client, form_attributes):
        form_attributes['password1'] = "12345678"
        form_attributes['password2'] = "12345678"

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is entirely numeric.' in json.loads(response.content)['errors']['password2']

    def test_register_view_with_different_passwords(self, client, form_attributes):
        form_attributes['password1'] = "password123"
        form_attributes['password2'] = "password456"

        response = client.post(reverse('register'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'The two password fields didn’t match.' in json.loads(response.content)['errors']['password2']

@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def form_attributes(self):
        return {
            'username': 'user1',
            'password': 'Password#123',
        }

    def test_login_view_with_valid_credentials(self, client, user, form_attributes):
        response = client.post(reverse('login'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'User logged in successfully.'
        assert 'sessionid' in response.cookies, 'Session id missing in response.'

    def test_login_view_with_valid_credentials(self, client, user, form_attributes):
        form_attributes['password'] = 'password123'
        response = client.post(reverse('login'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 401
        assert json.loads(response.content)['error'] == 'Invalid credential: Either User name or password is incorrect.'
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_login_view_with_get_request(self, client):
        response = client.get(reverse('login'))

        assert response.status_code == 405
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

@pytest.mark.django_db
class TestLogoutView:

    def test_logout_view_without_user_logged_in(self, client):
        response = client.post(reverse('logout'))

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'User logged out successfully.'

    def test_logout_view_with_user_logged_in(self, logged_in_client):
        response = logged_in_client.post(reverse('logout'))

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'User logged out successfully.'

    def test_logout_view_with_get_request(self, client):
        response = client.get(reverse('logout'))

        assert response.status_code == 405

@pytest.mark.django_db
class TestUpdateUserView:

    @pytest.fixture
    def form_attributes(self, user):
        return {
            'id': user.id,
            'username': 'user2',
            'email': 'user2@xyz.com',
            'first_name': 'xyz',
            'last_name': '456'
        }

    def test_update_user_view(self, logged_in_client, user, form_attributes):
        assert user.username == 'user1'
        assert user.email == 'user1@xyz.com'
        assert user.first_name == 'abc'
        assert user.last_name == '123'

        response = logged_in_client.post(reverse('update'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'User updated successfully.'
        user.refresh_from_db()
        assert user.username == 'user2'
        assert user.email == 'user2@xyz.com'
        assert user.first_name == 'xyz'
        assert user.last_name == '456'

    def test_update_user_view_with_get_request(self, logged_in_client):
        response = logged_in_client.get(reverse('update'))

        assert response.status_code == 405

    def test_update_user_view_without_logged_in_user(self, client, form_attributes):
        response = client.post(reverse('update'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 401
        assert json.loads(response.content)['error'] == 'User not authenticated.'

    def test_update_user_view_with_username_already_exists(self, logged_in_client, form_attributes):
        user1 = User.objects.create_user(username='user2')

        response = logged_in_client.post(reverse('update'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'A user with that username already exists.' in json.loads(response.content)['errors']['username']

    def test_update_user_view_with_email_already_exists(self, logged_in_client, form_attributes):
        user1 = User.objects.create_user(username='user3', email='user2@xyz.com')

        response = logged_in_client.post(reverse('update'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'User with this Email address already exists.' in json.loads(response.content)['errors']['email']

    def test_update_user_view_without_attributes(self, logged_in_client):
        response = logged_in_client.post(reverse('update'),
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        errors = json.loads(response.content)['errors']
        assert 'This field is required.' in errors['username']
        assert 'This field is required.' in errors['email']
        assert 'This field is required.' in errors['first_name']
        assert 'This field is required.' in errors['last_name']

    def test_update_user_view_with_username_having_invalid_character(self, logged_in_client, form_attributes):
        form_attributes['username'] = 'User 1'

        response = logged_in_client.post(reverse('update'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in json.loads(response.content)['errors']['username']

@pytest.mark.django_db
class TestUpdatePasswordView:

    @pytest.fixture
    def form_attributes(self, user):
        return {
            'old_password': 'Password#123',
            'new_password1': 'new_password123',
            'new_password2': 'new_password123'
        }

    def test_update_password_view(self, logged_in_client, user, form_attributes):
        old_password_hash = user.password
        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'Password changed successfully.'
        user.refresh_from_db()
        new_password_hash = user.password
        assert new_password_hash != old_password_hash
        assert 'sessionid' in response.cookies, 'Session id missing in response.'

    def test_update_password_view_with_get_request(self, logged_in_client):
        response = logged_in_client.get(reverse('update-password'))

        assert response.status_code == 405
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_update_password_view_without_attrbites(self, logged_in_client):
        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        errors = json.loads(response.content)['errors']
        assert 'This field is required.' in errors['old_password']
        assert 'This field is required.' in errors['new_password1']
        assert 'This field is required.' in errors['new_password2']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_update_password_view_without_logged_in_user(self, client, form_attributes):
        response = client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 401
        assert json.loads(response.content)['error'] == 'User not authenticated.'
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_update_password_view_with_invalid_old_password(self, logged_in_client, form_attributes):
        form_attributes['old_password'] = 'Invalid'

        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'Your old password was entered incorrectly. Please enter it again.' in json.loads(response.content)['errors']['old_password']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_register_view_with_shorter_password(self, logged_in_client, form_attributes):
        form_attributes['new_password1'] = "123"
        form_attributes['new_password2'] = "123"

        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too short. It must contain at least 8 characters.' in json.loads(response.content)['errors']['new_password2']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_register_view_with_common_password(self, logged_in_client, form_attributes):
        form_attributes['new_password1'] = "password123"
        form_attributes['new_password2'] = "password123"

        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too common.' in json.loads(response.content)['errors']['new_password2']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_register_view_with_only_numeric_password(self, logged_in_client, form_attributes):
        form_attributes['new_password1'] = "12345678"
        form_attributes['new_password2'] = "12345678"

        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is entirely numeric.' in json.loads(response.content)['errors']['new_password2']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

    def test_update_password_view_with_different_new_passwords(self, logged_in_client, form_attributes):
        form_attributes['new_password1'] = 'Notsame'

        response = logged_in_client.post(reverse('update-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'The two password fields didn’t match.' in json.loads(response.content)['errors']['new_password2']
        assert 'sessionid' not in response.cookies, 'Session id present in response.'

@pytest.mark.django_db
class TestSendResetPasswordEmailView:

    @pytest.fixture
    def form_attributes(self, user):
        return {
            'username': user.username,
            'redirect': '/reset-password'
        }

    def test_send_reset_password_email_view(self, client, user, form_attributes):
        assert len(mail.outbox) == 0

        response = client.post(reverse('send-password-reset-email'),
            data=json.dumps(form_attributes),
            content_type='application/json',
            headers={
                'Origin':'example.com'
            }
        )

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'Password reset mail send successfully.'
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Reset password'
        assert mail.outbox[0].body == ''
        assert user.email in mail.outbox[0].to

    def test_send_reset_password_email_view_with_get_request(self, client):
        assert len(mail.outbox) == 0

        response = client.get(reverse('send-password-reset-email'))

        assert response.status_code == 405
        assert len(mail.outbox) == 0

    def test_send_reset_password_email_view_without_username(self, client, form_attributes):
        del form_attributes['username']

        assert len(mail.outbox) == 0

        response = client.post(reverse('send-password-reset-email'),
            data=json.dumps(form_attributes),
            content_type='application/json',
            headers={
                'Origin':'example.com'
            }
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == repr('username')
        assert len(mail.outbox) == 0

    def test_send_reset_password_email_view_without_redirect(self, client, form_attributes):
        del form_attributes['redirect']

        assert len(mail.outbox) == 0
 
        response = client.post(reverse('send-password-reset-email'),
            data=json.dumps(form_attributes),
            content_type='application/json',
            headers={
                'Origin':'example.com'
            }
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == repr('redirect')
        assert len(mail.outbox) == 0

    def test_send_reset_password_email_view_with_nonexisting_username(self, client, form_attributes):
        form_attributes['username'] = 'non_existing_username'

        assert len(mail.outbox) == 0

        response = client.post(reverse('send-password-reset-email'),
            data=json.dumps(form_attributes),
            content_type='application/json',
            headers={
                'Origin':'example.com'
            }
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == 'User matching query does not exist.'
        assert len(mail.outbox) == 0

@pytest.mark.django_db
class TestResetPasswordView:

    @pytest.fixture
    def token_expiry_2_seconds(self, settings):
        settings.PASSWORD_RESET_TIMEOUT = 2
        return settings

    @pytest.fixture
    def form_attributes(self, user):
        return {
            'uid':  urlsafe_base64_encode(force_bytes(user.id)),
            'token': default_token_generator.make_token(user),
            'new_password1': 'Pswd#123',
            'new_password2': 'Pswd#123',
        }

    def test_reset_password_view(self, client, user, form_attributes):
        old_password_hash = user.password

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'Password reset successfully.'
        user.refresh_from_db()
        new_password_hash = user.password
        assert new_password_hash != old_password_hash

    def test_reset_password_view_with_get_request(self, client):
        response = client.get(reverse('reset-password'))

        assert response.status_code == 405

    def test_reset_password_view_invalid_uid(self, client, user, form_attributes):
        form_attributes['uid'] = urlsafe_base64_encode(force_bytes(user.id + 2))

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json',
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == 'User matching query does not exist.'

    def test_reset_password_view_invalid_token(self, client, user, form_attributes):
        form_attributes['token'] = 'Invalid token'

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json',
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == 'Invalid or expired token.'

    def test_reset_password_view_expired_token(self, client, user, token_expiry_2_seconds, form_attributes):
        time.sleep(3)

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json',
        )

        assert response.status_code == 400
        assert json.loads(response.content)['error'] == 'Invalid or expired token.'

    def test_register_view_with_shorter_password(self, client, form_attributes):
        form_attributes['new_password1'] = "123"
        form_attributes['new_password2'] = "123"

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too short. It must contain at least 8 characters.' in json.loads(response.content)['errors']['new_password2']

    def test_register_view_with_common_password(self, client, form_attributes):
        form_attributes['new_password1'] = "password123"
        form_attributes['new_password2'] = "password123"

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is too common.' in json.loads(response.content)['errors']['new_password2']

    def test_register_view_with_only_numeric_password(self, client, form_attributes):
        form_attributes['new_password1'] = "12345678"
        form_attributes['new_password2'] = "12345678"

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'This password is entirely numeric.' in json.loads(response.content)['errors']['new_password2']

    def test_reset_password_view_with_different_password_fields(self, client, user, form_attributes):
        form_attributes['new_password2'] = 'NotSame'

        response = client.post(reverse('reset-password'),
            data=json.dumps(form_attributes),
            content_type='application/json',
        )

        assert response.status_code == 400
        assert 'The two password fields didn’t match.' in json.loads(response.content)['errors']['new_password2']
