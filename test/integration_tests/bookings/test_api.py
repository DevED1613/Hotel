async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[-1].id
    responce = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-01-01",
            "date_to": "2025-01-15",
        },
    )

    assert responce.status_code == 200

    res = responce.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
