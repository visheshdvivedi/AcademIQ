from tests.setup import session, client
from fastapi.testclient import TestClient
from starlette import status

test_credentials = [
    { "first_name": "Test", "last_name": "User", "email": "testuser@test.com", "password": "Test@123" }
]

def test_create_new_user_functionality(client: TestClient):
    """
    Test case to check if create new user functionality is working as expected

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    response = client.post("/user", json=test_credentials[0])
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "User created successfully"
    }

def test_create_user_with_duplicate_email(client: TestClient):
    """
    Test case to check creating user with existing email

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    response = client.post("/user", json=test_credentials[0])
    response = client.post("/user", json=test_credentials[0])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Email ID already exists, please login to continue"
    }

def test_missing_first_name_field(client: TestClient):
    """
    Test case to check missing first name field

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
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

def test_missing_last_name_field(client:TestClient):
    """
    Test case to check missing last name field

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
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

def test_missing_email_field(client: TestClient):
    """
    Test case to check missing email field

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
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

def test_missing_password_field(client: TestClient):
    """
    Test case to check missing password field

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
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

def test_long_first_name_value(client: TestClient):
    """
    Test case to check first name value longer than 255 characters

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    body = test_credentials[0].copy()
    body['first_name'] = test_credentials[0]['first_name'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': [{'message': 'String should have at most 255 characters', 'param': 'first_name', 'type': 'string_too_long'}]}

def test_long_last_name_value(client: TestClient):
    """
    Test case to check last name value longer than 255 characters

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    body = test_credentials[0].copy()
    body['last_name'] = test_credentials[0]['last_name'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': [{'message': 'String should have at most 255 characters', 'param': 'last_name', 'type': 'string_too_long'}]}

def test_long_email_value(client: TestClient):
    """
    Test case to check email value longer than 255 characters

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    body = test_credentials[0].copy()
    email_left, email_right = body['email'].split("@")
    body['email'] = (email_left * 100) + "@" + email_right

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "email",
                "message": "value is not a valid email address: The email address is too long before the @-sign (736 characters too many)."
            }
        ]
    }

def test_long_password_value(client: TestClient):
    """
    Test case to check password value longer than 255 characters

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """
    body = test_credentials[0].copy()
    body['password'] = test_credentials[0]['password'] * 100

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, 'password' length cannot be more than 255 characters."
            }
        ]
    }

def test_invalid_email_address(client: TestClient):
    """
    Test case to check for invalid email address

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """

    # check email without '@' symbol
    body = test_credentials[0].copy()
    body['email'] = body['email'].replace("@", "")

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "email",
                "message": "value is not a valid email address: An email address must have an @-sign."
            }
        ]
    }

    # check email without '.'
    body = test_credentials[0].copy()
    body['email'] = body['email'].replace(".", "")

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "email",
                "message": "value is not a valid email address: The part after the @-sign is not valid. It should have a period."
            }
        ]
    }

def test_password_strength(client: TestClient):
    """
    Test case to check for invalid email address

    Args:
        client (TestClient): fastapi.testclient.TestClient object
    """

    # check password length
    body = test_credentials[0].copy()
    body['password'] = "test"

    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, 'password' must be at least 8 characters long"
            }
        ]
    }

    # check password contains lowercase
    body['password'] = "SUPERSECRETPASSWORD"
    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, Password must have at least on lowercase character."
            }
        ]
    }

    # check password contains uppercase
    body['password'] = "supersecretpassword"
    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, Password must have at least one uppercase character."
            }
        ]
    }

    # check password contains number
    body['password'] = "SupersecretPass"
    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, Password must have at least on number."
            }
        ]
    }

    # check password contains special character
    body['password'] = "SupersecretPass1"
    response = client.post("/user", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "param": "password",
                "message": "Value error, Password must have at least one special character."
            }
        ]
    }