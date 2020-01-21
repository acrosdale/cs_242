import pytest

# todo pytest.mark.django_db is a transactional maker,
# todo --any test made changes will be rolled back  after the test completes


@pytest.mark.django_db
def test_with_client(client,django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    response = client.get('/twit/v1/account/hello/')
    assert response.data['message'] == 1


@pytest.mark.django_db
def test_with_authenticated_client(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get('/twit/v1/account/hello/')
    assert response.data['message'] == 1


@pytest.mark.django_db
def test_with_authenticated_client2(client, django_user_model):

    user = django_user_model.objects.first()

    if user is None:
        assert True
