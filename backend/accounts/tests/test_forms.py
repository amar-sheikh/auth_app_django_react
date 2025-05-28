import pytest
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

@pytest.mark.django_db
class TestCustomUserCreationForm:

    @pytest.fixture
    def form_attributes(self):
        return {
            'username': 'user1',
            'email': 'user1@xyz.com',
            'password1': 'Password#123',
            'password2': 'Password#123',
            'first_name': 'abc',
            'last_name': '123'
        }

    def test_user_creation_form(self, form_attributes):
        assert User.objects.count() == 0

        form = CustomUserCreationForm(form_attributes)

        assert form.is_valid()
        form.save()
        assert User.objects.count() == 1
        user = User.objects.last()
        assert user.username == 'user1'
        assert user.email == 'user1@xyz.com'
        assert user.first_name == 'abc'
        assert user.last_name == '123'

    def test_user_creation_form_without_attributes(self):
        form = CustomUserCreationForm({})

        assert not form.is_valid()
        assert 'This field is required.' in form.errors['username']
        assert 'This field is required.' in form.errors['email']
        assert 'This field is required.' in form.errors['password1']
        assert 'This field is required.' in form.errors['password2']
        assert 'This field is required.' in form.errors['first_name']
        assert 'This field is required.' in form.errors['last_name']

    def test_user_creation_form_with_username_already_exists(self, form_attributes):
        User.objects.create(username= 'user1', email='user2@xyz.com')

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'A user with that username already exists.' in form.errors['username']

    def test_user_creation_form_with_email_already_exists(self, form_attributes):
        User.objects.create(username= 'user2', email='user1@xyz.com')

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'User with this Email address already exists.' in form.errors['email']

    def test_user_creation_form_with_username_having_invalid_character(self, form_attributes):
        form_attributes['username'] = 'User 1'

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in form.errors['username']

    def test_user_creation_form_with_shorter_password(self, form_attributes):
        form_attributes['password1'] = "123"
        form_attributes['password2'] = "123"

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'This password is too short. It must contain at least 8 characters.' in form.errors['password2']

    def test_user_creation_form_with_common_password(self, form_attributes):
        form_attributes['password1'] = "password123"
        form_attributes['password2'] = "password123"

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'This password is too common.' in form.errors['password2']

    def test_user_creation_form_with_only_numeric_password(self, form_attributes):
        form_attributes['password1'] = "12345678"
        form_attributes['password2'] = "12345678"

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'This password is entirely numeric.' in form.errors['password2']

    def test_user_creation_form_with_different_passwords(self, form_attributes):
        form_attributes['password1'] = "password123"
        form_attributes['password2'] = "password456"

        form = CustomUserCreationForm(form_attributes)

        assert not form.is_valid()
        assert 'The two password fields didn’t match.' in form.errors['password2']

@pytest.mark.django_db
class TestCustomUserChangeForm:

    @pytest.fixture
    def user(self):
        return User.objects.create(
            username= 'user1',
            email= 'user1@xyz.com',
            first_name= 'abc',
            last_name= '123'
        )

    @pytest.fixture
    def form_attributes(self, user):
        return {
            'id': user.id,
            'username': 'user2',
            'email': 'user2@xyz.com',
            'first_name': 'xyz',
            'last_name': '456'
        }

    def test_user_change_form(self, user, form_attributes):
        assert user.username == 'user1'
        assert user.email == 'user1@xyz.com'
        assert user.first_name == 'abc'
        assert user.last_name == '123'

        form = CustomUserChangeForm(instance=user, data=form_attributes)
        assert form.is_valid()
        form.save()
        assert user.username == 'user2'
        assert user.email == 'user2@xyz.com'
        assert user.first_name == 'xyz'
        assert user.last_name == '456'

    def test_user_change_form_without_attributes(self):
        form = CustomUserChangeForm({})

        assert not form.is_valid()
        assert 'This field is required.' in form.errors['username']
        assert 'This field is required.' in form.errors['email']
        assert 'This field is required.' in form.errors['first_name']
        assert 'This field is required.' in form.errors['last_name']

    def test_user_change_form_with_username_already_exists(self, form_attributes):
        form_attributes['username'] = 'user1'
        form = CustomUserChangeForm(form_attributes)

        assert not form.is_valid()
        assert 'A user with that username already exists.' in form.errors['username']

    def test_user_change_form_with_email_already_exists(self, form_attributes):
        form_attributes['email'] = 'user1@xyz.com'
        form = CustomUserChangeForm(form_attributes)

        assert not form.is_valid()
        assert 'User with this Email address already exists.' in form.errors['email']

    def test_user_change_username_having_invalid_character(self, form_attributes):
        form_attributes['username'] = 'User 1'

        form = CustomUserChangeForm(form_attributes)

        assert not form.is_valid()
        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in form.errors['username']
