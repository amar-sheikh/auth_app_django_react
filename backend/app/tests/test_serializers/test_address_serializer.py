import pytest
from app.models import Address, Transaction
from app.serializers import AddressSerializer

@pytest.mark.django_db
class TestAddressSerializer:

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123'
        )

    @pytest.fixture
    def data(self, user):
        return {
            'user': user.id,
            'line1': 'Transaction 1 - Line 1',
            'line2': 'Transaction 1 - Line 2',
            'city': 'City name',
            'country': 'Country name',
            'postcode': 'XYZ 123'
        }

    def test_valid_data(self, data, user):
        assert Address.objects.count() == 0

        serializer = AddressSerializer(data=data)

        assert serializer.is_valid()
        serializer.save()
        assert (
            serializer.data['user'],
            serializer.data['line1'],
            serializer.data['line2'],
            serializer.data['city'],
            serializer.data['country'],
            serializer.data['have_transactions'],
            serializer.data['postcode'],
        ) == (
            user.id,
            data['line1'],
            data['line2'],
            data['city'],
            data['country'],
            False,
            data['postcode']
        )
        assert Address.objects.count() == 1

    def test_without_data(self, data):
        serializer = AddressSerializer(data={})
        assert not serializer.is_valid()

        # 'line2' not included as can be null
        for field in [ 'user', 'line1', 'country', 'city', 'postcode']:
            assert str(serializer.errors[field][0]) == 'This field is required.'

    def test_with_invalid_data(self, user):
        data = {
            'user': user.id,
            'line1': 'A' * 256,
            'line2': 'B' * 256,
            'city': 'C' * 128,
            'country': 'D' * 64,
            'postcode': 'E' * 16
        }

        serializer = AddressSerializer(data=data)
        assert not serializer.is_valid()

        assert str(serializer.errors['line1'][0]) == 'Ensure this field has no more than 255 characters.'
        assert str(serializer.errors['line2'][0]) == 'Ensure this field has no more than 255 characters.'
        assert str(serializer.errors['city'][0]) == 'Ensure this field has no more than 127 characters.'
        assert str(serializer.errors['country'][0]) == 'Ensure this field has no more than 63 characters.'
        assert str(serializer.errors['postcode'][0]) == 'Ensure this field has no more than 15 characters.'

    def test_with_instance(self, user):
        transaction = Transaction.objects.create(user=user, amount=20.00)
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

        serializer = AddressSerializer(address)

        assert (
            serializer.data['user'],
            serializer.data['line1'],
            serializer.data['line2'],
            serializer.data['city'],
            serializer.data['country'],
            serializer.data['have_transactions'],
            serializer.data['postcode'],
        ) == (
            user.id,
            address.line1,
            address.line2,
            address.city,
            address.country,
            True,
            address.postcode
        )
