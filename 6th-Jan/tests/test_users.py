import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/users/",
            json={"name": "Atharva", "email": "atharva@test.com"}
        )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_users():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.get("/users/")

    assert response.status_code == 200
