import pytest
from app.models import Address, Transaction
from app.serializers import TransactionSerializer

@pytest.mark.django_db
class TestTransactionSerializer:

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

    @pytest.fixture
    def data(self, user, address):
        return {
            'user': user.id,
            'address': address.id,
            'amount': 20.05,
            'additional_info': '',
        }

    def test_valid_data(self, data):
        assert Transaction.objects.count() == 0

        serializer = TransactionSerializer(data=data)

        assert serializer.is_valid()
        serializer.save()
        assert Transaction.objects.count() == 1

    def test_without_data(self, data):
        serializer = TransactionSerializer(data={})
        assert not serializer.is_valid()

        # 'address' and 'additional_info' are not included as can be null
        for field in [ 'user', 'amount']:
            assert str(serializer.errors[field][0]) == 'This field is required.'

    def test_with_invalid_data(self, user, address):
        data = {
            'user': user.id,
            'address': address.id,
            'amount': -20.05,
            'additional_info': 'A' * 256,
        }

        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()

        assert str(serializer.errors['amount'][0]) == 'Ensure this value is greater than or equal to 0.'
        assert str(serializer.errors['additional_info'][0]) == 'Ensure this field has no more than 255 characters.'
