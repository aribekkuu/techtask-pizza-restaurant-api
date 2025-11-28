import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/restaurants")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 2
        print(data)