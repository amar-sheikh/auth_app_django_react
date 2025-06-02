import pytest
from app.models import Address, Transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@pytest.mark.django_db
class TestAddress:

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123'
        )

    @pytest.fixture
    def transaction(self, user):
        return Transaction.objects.create(user=user, amount=20)

    def test_valid_data(self, user, transaction):
        assert Address.objects.count() == 0

        address = Address.objects.create(
            user = user,
            line1 = 'Address 1 - Line 1',
            line2 = 'Address 1 - Line 2',
            city = 'City name',
            country = 'Country name',
            postcode = 'XYZ 123'
        )
        address.transactions.add(transaction)
        address.save()
        address.full_clean()

        assert Address.objects.count() == 1

    def test_without_user(self, transaction):
        with pytest.raises(IntegrityError) as exception_info:
            address = Address.objects.create(
                line1 = 'Address 1 - Line 1',
                line2 = 'Address 1 - Line 2',
                city = 'City name',
                country = 'Country name',
                postcode = 'XYZ 123'
            )
            address.transactions.add(transaction)
            address.save()

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_address.user_id'

    def test_without_any_transaction(self, user):
        address = Address.objects.create(
            user=user,
            line1 = 'Address 1 - Line 1',
            line2 = 'Address 1 - Line 2',
            city = 'City name',
            country = 'Country name',
            postcode = 'XYZ 123'
        )
        address.full_clean()

    def test_with_invalid_data(self, user):
        with pytest.raises(ValidationError) as exception_info:
            address = Address.objects.create(
                user=user,
                line1 = 'A' * 256,
                line2 = 'B' * 256,
                city = 'C' * 128,
                country = 'D' * 64,
                postcode = 'E' * 16
            )
            address.full_clean()

        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['line1']
        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['line2']
        assert 'Ensure this value has at most 127 characters (it has 128).' in exception_info.value.message_dict['city']
        assert 'Ensure this value has at most 63 characters (it has 64).' in exception_info.value.message_dict['country']
        assert 'Ensure this value has at most 15 characters (it has 16).' in exception_info.value.message_dict['postcode']
