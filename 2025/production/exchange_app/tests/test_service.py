from exchange_app.models import ConversionRate
from exchange_app.services import ExchangeRateService

def test_service_convert_valid(db_session):
    db_session.add(ConversionRate(from_currency="USD", to_currency="JPY", rate=150))
    db_session.commit()

    service = ExchangeRateService(db_session)
    result = service.convert("usd", "jpy", 10)

    assert result["rate"] == 150
    assert result["result"] == 1500


def test_service_convert_invalid_currency(db_session):
    service = ExchangeRateService(db_session)
    try:
        service.convert("AAA", "BBB", 10)
        assert False, "Expected HTTPException"
    except Exception as e:
        assert "Exchange rate not found" in str(e)