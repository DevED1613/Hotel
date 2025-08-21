import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("huyambaaa@123.com", "1613", 200),
        ("huyambaaa@123.com", "16134", 409),
        ("cotopes@123.com", "2kl12rjd", 200),
        ("huyamba@123.com", "", 409),
    ],
)
async def test_auth(
    email: str,
    password: str,
    status_code: int,
    async_client: AsyncClient,
):
    # register
    response = await async_client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code
    if status_code != 200:
        return

    # login
    response = await async_client.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == status_code
    assert async_client.cookies["access_token"]
    assert response.json().get("access_token")

    # me
    responce = await async_client.get("/auth/only_auth")
    assert response.status_code == status_code
    user = responce.json()
    assert responce.json().get("email") == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # logout
    responce = await async_client.post("/auth/logout")
    assert responce.status_code == 200
    assert "access_token" not in async_client.cookies
