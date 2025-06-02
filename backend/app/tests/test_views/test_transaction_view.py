import pytest
from app.models import Address, Transaction
from decimal import Decimal
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestTransactionViewset:

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123'
        )

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def api_logged_in_client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @pytest.fixture
    def address(self, user):
        return Address.objects.create(
            user = user,
            line1 = 'Transaction 1 - Line 1',
            line2 = 'Transaction 1 - Line 2',
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

    class TestList:
        def test_returns_transactions_for_logged_user_only(self, api_logged_in_client, user, django_user_model, address):
            user2 = django_user_model.objects.create(username='User2', email='user2@xyz.com', password='password456')
            Transaction.objects.create(
                user=user,
                address=address,
                amount= 20.05,
                additional_info='',
            )
            Transaction.objects.create(
                user=user2,
                address=address,
                amount= 20.05,
                additional_info=''
            )

            response = api_logged_in_client.get(reverse('transactions-list'), format='json')

            assert response.status_code == 200
            assert response.data['count'] == 1
            assert response.data['results'][0]['user'] == user.id

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('transactions-list'), format='json')

            assert response.status_code == 403

    class TestCreate:
        def test_with_current_user(self, api_logged_in_client, data, user):
            address = Address.objects.create(
                user=user,
                line1='Transaction 0 - Line 1',
                line2='Transaction 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 123'
            )
            user.current_address = address
            user.save()
            assert Transaction.objects.count() == 0
            assert user.current_address == address

            response = api_logged_in_client.post(reverse('transactions-list'), data=data, format='json')

            assert response.status_code == 201
            assert Transaction.objects.count() == 1
            assert Transaction.objects.last().address == address

        def test_without_current_user(self, api_logged_in_client, data, user):
            assert Transaction.objects.count() == 0
            assert user.current_address is None

            response = api_logged_in_client.post(reverse('transactions-list'), data=data, format='json')

            assert response.status_code == 201
            assert Transaction.objects.count() == 1
            assert Transaction.objects.last().address.id == data['address']

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('transactions-list'), format='json')

            assert response.status_code == 403

        def test_without_current_user_and_address(self, api_logged_in_client, data, user):
            del data['address']
            assert Transaction.objects.count() == 0
            assert user.current_address is None

            response = api_logged_in_client.post(reverse('transactions-list'), data=data, format='json')

            assert response.status_code == 201
            assert Transaction.objects.count() == 1
            assert Transaction.objects.last().address is None

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('transactions-list'), format='json')

            assert response.status_code == 403

    class TestRetrieve:
        def test_with_valid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 20.05,
                additional_info=''
            )

            response = api_logged_in_client.get(reverse('transactions-detail', args=[transaction.id]), format='json')

            assert response.status_code == 200
            assert response.data['id'] == 1

        def test_with_invalid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 20.05,
                additional_info=''
            )

            response = api_logged_in_client.get(reverse('transactions-detail', args=[transaction.id + 1]), format='json')

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 20.05,
                additional_info=''
            )

            response = api_client.get(reverse('transactions-detail', args=[transaction.id]), format='json')

            assert response.status_code == 403
    
    class TestUpdate:
        def test_with_valid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            assert (
                transaction.amount,
                transaction.additional_info,
            ) == (
                Decimal('5.5'),
                'Info',
            )

            response = api_logged_in_client.put(
                reverse('transactions-detail', args=[transaction.id]),
                data={
                    'user': user.id,
                    'address': address.id,
                    'amount': 20.05,
                    'additional_info': 'Updated info'
                },
                format='json'
            )

            assert response.status_code == 200
            transaction.refresh_from_db()
            assert (
                transaction.amount,
                transaction.additional_info,
            ) == (
                Decimal('20.05'),
                'Updated info',
            )

        def test_with_invalid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_logged_in_client.put(
                reverse('transactions-detail', args=[transaction.id + 2]),
                data={
                    'user': user.id,
                    'address': address.id,
                    'amount': 20.05,
                    'additional_info': 'Updated info'
                },
                format='json'
            )

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_client.put(
                reverse('transactions-detail', args=[transaction.id]),
                data={
                    'user': user.id,
                    'address': address.id,
                    'amount': 20.05,
                    'additional_info': 'Updated info'
                },
                format='json'
            )

            assert response.status_code == 403

    class TestPartialUpdate:
        def test_with_valid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            assert transaction.amount == Decimal('5.5')

            response = api_logged_in_client.patch(
                reverse('transactions-detail', args=[transaction.id]),
                data={ 'amount': 20.05 },
                format='json'
            )

            assert response.status_code == 200
            transaction.refresh_from_db()
            assert transaction.amount == Decimal('20.05')

        def test_with_invalid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_logged_in_client.patch(
                reverse('transactions-detail', args=[transaction.id + 2]),
                data={ 'line1': 'Transaction 2 - Line 2' },
                format='json'
            )

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_client.patch(
                reverse('transactions-detail', args=[transaction.id]),
                data={ 'line1': 'Transaction 2 - Line 2' },
                format='json'
            )

            assert response.status_code == 403

    class TestDestroy:
        def test_with_valid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            assert Transaction.objects.count() == 1

            response = api_logged_in_client.delete(reverse('transactions-detail', args=[transaction.id]), format='json')

            assert response.status_code == 204
            assert Transaction.objects.count() == 0

        def test_with_invalid_id(self, api_logged_in_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_logged_in_client.delete(reverse('transactions-detail', args=[transaction.id + 1]), format='json')

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user, address):
            transaction = Transaction.objects.create(
                user=user,
                address=address,
                amount= 5.5,
                additional_info='Info'
            )

            response = api_client.delete(reverse('transactions-detail', args=[transaction.id]), format='json')

            assert response.status_code == 403
