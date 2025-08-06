async def test_facilities(async_client):
    response = await async_client.get("/facilities")
    assert response.status_code == 200

    response_update = await async_client.post("/facilities", json={"title": "test"})

    data_response = response_update.json().get("data")
    assert data_response.get("title") == "test"

    response_delete = await async_client.delete("/facilities/1", params={"id": 1})
    data_response = response_delete.json().get("data")

    assert response_delete.status_code == 200
    assert data_response is None
