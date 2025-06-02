import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from app.models import Address, Transaction

@pytest.mark.django_db
class TestAddressViewset:

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
    def data(self, user):
        return {
            'user': user.id,
            'line1': 'Address 1 - Line 1',
            'line2': 'Address 1 - Line 2',
            'city': 'City name',
            'country': 'Country name',
            'postcode': 'XYZ 123'
        }

    class TestList:
        def test_returns_addresses_for_logged_user_only(self, api_logged_in_client, user, django_user_model):
            user2 = django_user_model.objects.create(username='User2', email='user2@xyz.com', password='password456')
            Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )
            Address.objects.create(
                user=user2,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_logged_in_client.get(reverse('addresses-list'), format='json')

            assert response.status_code == 200
            assert response.data['count'] == 1
            assert response.data['results'][0]['user'] == user.id

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('addresses-list'), format='json')

            assert response.status_code == 403

    class TestCreate:
        def test_with_old_transactions_not_assigned_to_address(self, api_logged_in_client, data, user):
            transaction1 = Transaction.objects.create(user=user, amount=1)
            transaction2 = Transaction.objects.create(user=user, amount=2)

            assert Address.objects.count() == 0
            assert transaction1.address is None
            assert transaction2.address is None
            assert user.current_address is None

            response = api_logged_in_client.post(reverse('addresses-list'), data=data, format='json')

            assert response.status_code == 201
            assert Address.objects.count() == 1
            created_address = Address.objects.last()
            assert list(created_address.transactions.all()) == [transaction1, transaction2]
            assert user.current_address is None

        def test_without_current_user(self, api_logged_in_client, data, user):
            assert Address.objects.count() == 0
            assert user.current_address is None

            response = api_logged_in_client.post(reverse('addresses-list'), data=data, format='json')

            assert response.status_code == 201
            assert Address.objects.count() == 1
            created_address = Address.objects.last()
            assert user.current_address == created_address

        def test_with_current_user_that_doesnot_have_transactions(self, api_logged_in_client, data, user):
            old_address = Address.objects.create(
                user=user,
                line1='Address 0 - Line 1',
                line2='Address 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 123'
            )
            user.current_address = old_address
            user.save()
            assert Address.objects.count() == 1
            assert user.current_address == old_address

            response = api_logged_in_client.post(reverse('addresses-list'), data=data, format='json')

            assert response.status_code == 201
            assert Address.objects.count() == 2
            assert user.current_address == old_address

        def test_with_current_user_that_have_transactions(self, api_logged_in_client, data, user):
            old_address = Address.objects.create(
                user=user,
                line1='Address 0 - Line 1',
                line2='Address 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 123'
            )
            user.current_address = old_address
            user.save()
            Transaction.objects.create(user=user, address=old_address, amount=1)
            assert Address.objects.count() == 1
            assert user.current_address == old_address

            response = api_logged_in_client.post(reverse('addresses-list'), data=data, format='json')

            assert response.status_code == 201
            assert Address.objects.count() == 2
            created_address = Address.objects.last()
            assert user.current_address == created_address

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('addresses-list'), format='json')

            assert response.status_code == 403

    class TestRetrieve:
        def test_with_valid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_logged_in_client.get(reverse('addresses-detail', args=[address.id]), format='json')

            assert response.status_code == 200
            assert response.data['id'] == 1

        def test_with_invalid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_logged_in_client.get(reverse('addresses-detail', args=[address.id + 1]), format='json')

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_client.get(reverse('addresses-detail', args=[address.id]), format='json')

            assert response.status_code == 403

    class TestUpdate:
        def test_with_valid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 0 - Line 1',
                line2='Address 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 456'
            )

            assert (
                address.line1,
                address.line2,
                address.city,
                address.country,
                address.postcode
            ) == (
                'Address 0 - Line 1',
                'Address 0 - Line 2',
                'city',
                'country',
                'XYZ 456'
            )

            response = api_logged_in_client.put(
                reverse('addresses-detail', args=[address.id]),
                data={
                    'user': user.id,
                    'line1': 'Address 1 - Line 1',
                    'line2': 'Address 1 - Line 2',
                    'city': 'city 1',
                    'country': 'country 1',
                    'postcode': 'XYZ 123'
                },
                format='json'
            )

            assert response.status_code == 200
            address.refresh_from_db()
            assert (
                address.line1,
                address.line2,
                address.city,
                address.country,
                address.postcode
            ) == (
                'Address 1 - Line 1',
                'Address 1 - Line 2',
                'city 1',
                'country 1',
                'XYZ 123'
            )

        def test_with_invalid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 0 - Line 1',
                line2='Address 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 456'
            )

            response = api_logged_in_client.put(
                reverse('addresses-detail', args=[address.id + 2]),
                data={
                    'user': user.id,
                    'line1': 'Address 1 - Line 1',
                    'line2': 'Address 1 - Line 2',
                    'city': 'city 1',
                    'country': 'country 1',
                    'postcode': 'XYZ 123'
                },
                format='json'
            )

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 0 - Line 1',
                line2='Address 0 - Line 2',
                city='city',
                country='country',
                postcode='XYZ 456'
            )

            response = api_client.put(
                reverse('addresses-detail', args=[address.id]),
                data={
                    'user': user.id,
                    'line1': 'Address 1 - Line 1',
                    'line2': 'Address 1 - Line 2',
                    'city': 'city 1',
                    'country': 'country 1',
                    'postcode': 'XYZ 123'
                },
                format='json'
            )

            assert response.status_code == 403

    class TestPartialUpdate:
        def test_with_valid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            assert address.line1 == 'Address 1 - Line 1'

            response = api_logged_in_client.patch(
                reverse('addresses-detail', args=[address.id]),
                data={ 'line1': 'Address 2 - Line 2' },
                format='json'
            )

            assert response.status_code == 200
            address.refresh_from_db()
            assert address.line1 == 'Address 2 - Line 2'

        def test_with_invalid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_logged_in_client.patch(
                reverse('addresses-detail', args=[address.id + 2]),
                data={ 'line1': 'Address 2 - Line 2' },
                format='json'
            )

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_client.patch(
                reverse('addresses-detail', args=[address.id]),
                data={ 'line1': 'Address 2 - Line 2' },
                format='json'
            )

            assert response.status_code == 403

    class TestDestroy:
        def test_with_valid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            assert Address.objects.count() == 1

            response = api_logged_in_client.delete(reverse('addresses-detail', args=[address.id]), format='json')

            assert response.status_code == 204
            assert Address.objects.count() == 0

        def test_with_invalid_id(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_logged_in_client.delete(reverse('addresses-detail', args=[address.id + 1]), format='json')

            assert response.status_code == 404

        def test_without_logged_in_user_returns_403(self, api_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )

            response = api_client.delete(reverse('addresses-detail', args=[address.id]), format='json')

            assert response.status_code == 403

    class TestCurrentAddress:
        def test_with_current_address(self, api_logged_in_client, user):
            address = Address.objects.create(
                user=user,
                line1='Address 1 - Line 1',
                line2='Address 1 - Line 2',
                city='Address 1 - Line 2',
                country='Address 1 - Line 2',
                postcode='XYZ 123'
            )
            user.current_address = address
            user.save()

            response = api_logged_in_client.get(reverse('addresses-current-address',), format='json')

            assert response.status_code == 200
            assert (
                response.data['current_address']['user'],
                response.data['current_address']['line1'],
                response.data['current_address']['line2'],
                response.data['current_address']['city'],
                response.data['current_address']['country'],
                response.data['current_address']['postcode'],
            ) == (
                user.id,
                'Address 1 - Line 1',
                'Address 1 - Line 2',
                'Address 1 - Line 2',
                'Address 1 - Line 2',
                'XYZ 123'
            )

        def test_without_logged_in_user_returns_403(self, api_client):
            response = api_client.get(reverse('addresses-current-address'), format='json')

            assert response.status_code == 403
