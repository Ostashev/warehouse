import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.schemas.product import ProductDB
from app.main import app

@pytest.mark.asyncio
async def test_get_product_by_id():
    product_data = {
        "id": 2,
        "model": "Model B",
        "current_status": "OUT_OF_STOCK"
    }

    with patch("app.crud.product.product_crud.get", new_callable=AsyncMock,
               return_value=ProductDB(**product_data)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/product/2")

    assert response.status_code == 200
    data = response.json()
    assert data == product_data
