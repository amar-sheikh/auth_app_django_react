import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

@pytest.mark.django_db
class TestUser:

    @pytest.fixture
    def user(self):
        return User.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123',
            first_name='abc',
            last_name='123'
        )

    def test_user_creation(self, user):
        user.full_clean()
        assert user.username == 'User1'
    
    def test_user_creation_duplicate_username(self, user):
        with pytest.raises(IntegrityError) as exception_info:
            User.objects.create(
                username='User1',
                email='user2@xyz.com',
                password='password123',
            )
        
        assert str(exception_info.value) == 'UNIQUE constraint failed: auth_user.username'

    def test_user_creation_duplicate_email(self, user):
        with pytest.raises(IntegrityError) as exception_info:
            User.objects.create(
                username='User2',
                email='user1@xyz.com',
                password='password123',
            )
        
        assert str(exception_info.value) == 'UNIQUE constraint failed: auth_user.email'

    def test_user_creation_username_having_invalid_character(self, user):
        with pytest.raises(ValidationError) as exception_info:
            user2 = User.objects.create(
                username='User 1',
                email='user2@xyz.com',
                password='password123',
            )
            user2.full_clean()
        
        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in exception_info.value.message_dict['username']

    def test_user_creation_without_attributes(self):
        with pytest.raises(ValidationError) as exception_info:
            user2 = User.objects.create()
            user2.full_clean()

        assert 'This field cannot be blank.' in exception_info.value.message_dict['username']
        assert 'This field cannot be blank.' in exception_info.value.message_dict['password']