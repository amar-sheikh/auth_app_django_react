import pytest
from app.models import Address, Transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@pytest.mark.django_db
class TestTransaction:

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123'
        )

    @pytest.fixture
    def address(self, user):
        return Address.objects.create(
            user = user,
            line1 = 'Address 1 - Line 1',
            line2 = 'Address 1 - Line 2',
            city = 'City name',
            country = 'Country name',
            postcode = 'XYZ 123'
        )

    def test_valid_data(self, user, address):
        assert Transaction.objects.count() == 0

        transaction = Transaction.objects.create(
            user = user,
            address = address,
            amount = 20.50,
            additional_info = 'Addition information'
        )
        transaction.full_clean()

        assert Transaction.objects.count() == 1

    def test_without_user(self, address):
        with pytest.raises(IntegrityError) as exception_info:
            Transaction.objects.create(
                address = address,
                amount = 20.50,
                additional_info = 'Addition information'
            )

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_transaction.user_id'

    def test_without_address(self, user):
        transaction = Transaction.objects.create(
            user = user,
            amount = 20.50,
            additional_info = 'Addition information'
        )
        transaction.full_clean()

    def test_with_invalid_data(self, user, address):
        with pytest.raises(ValidationError) as exception_info:
            transaction = Transaction.objects.create(
                user=user,
                address = address,
                amount = -0.50,
                additional_info = 'A' * 256
            )
            transaction.full_clean()

        assert 'Ensure this value is greater than or equal to 0.' in exception_info.value.message_dict['amount']
        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['additional_info']
