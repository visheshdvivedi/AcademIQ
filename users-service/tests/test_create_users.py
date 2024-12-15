from tests.setup import session, client
from starlette import status

test_credentials = [
    { "first_name": "Test", "last_name": "User", "email": "testuser@test.com", "password": "Test@123" }
]

def test_create_new_user_functionality(client):
    response = client.post("/user", json=test_credentials[0])
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "User created successfully"
    }

def test_create_user_with_duplicate_email(client):
    response = client.post("/user", json=test_credentials[0])
    response = client.post("/user", json=test_credentials[0])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Email ID already exists, please login to continue"
    }

def test_missing_first_name_field(client):
    body = test_credentials[0].copy()
    del body['first_name']

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "param": "first_name",
                "message": "Field required"
            }
        ]
    }
def test_missing_first_name_field(client):
    body = test_credentials[0].copy()
    del body['first_name']

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "param": "first_name",
                "message": "Field required"
            }
        ]
    }

def test_missing_last_name_field(client):
    body = test_credentials[0].copy()
    del body['last_name']

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "param": "last_name",
                "message": "Field required"
            }
        ]
    }

def test_missing_email_field(client):
    body = test_credentials[0].copy()
    del body['email']

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "param": "email",
                "message": "Field required"
            }
        ]
    }

def test_missing_password_field(client):
    body = test_credentials[0].copy()
    del body['password']

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "param": "password",
                "message": "Field required"
            }
        ]
    }

def test_long_first_name_value(client):
    body = test_credentials[0].copy()
    body['first_name'] = test_credentials[0]['first_name'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "value too long for type character varying(255)\n"
    }

def test_long_last_name_value(client):
    body = test_credentials[0].copy()
    body['last_name'] = test_credentials[0]['last_name'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "value too long for type character varying(255)\n"
    }

def test_long_email_value(client):
    body = test_credentials[0].copy()
    body['email'] = test_credentials[0]['email'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "value too long for type character varying(255)\n"
    }

def test_long_email_value(client):
    body = test_credentials[0].copy()
    body['email'] = test_credentials[0]['password'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "value too long for type character varying(255)\n"
    }