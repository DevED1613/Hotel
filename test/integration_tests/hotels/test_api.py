async def test_get_hotels(async_client):
    response = await async_client.get(
        "/hotels", params={"date_from": "2025-01-01", "date_to": "2025-01-15"}
    )
    assert response.status_code == 200
