from models import ConversionRate


def test_convert_success(client, db_session):
    # Arrange: Seed rate
    db_session.add(ConversionRate(from_currency="USD", to_currency="EUR", rate=0.9))
    db_session.commit()

    # Act
    response = client.get("/convert?from_currency=USD&to_currency=EUR&amount=100")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 0.9
    assert data["result"] == 90.0


def test_convert_missing_rate(client):
    # Act
    response = client.get("/convert?from_currency=GBP&to_currency=JPY&amount=50")

    # Assert
    assert response.status_code == 500  # Internal server error from missing rate
    assert "Exchange rate not found" in response.json()["detail"]
