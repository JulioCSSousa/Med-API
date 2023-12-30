import pytest
import httpx
@pytest.mark.asyncio
async def test_users_post():
    login_url = "https://med-api-production.up.railway.app/register"
    auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZWl2Y3NAZ21haWwuY29tIiwiZXhwIjoxNzAzOTQ0ODEyfQ.IPohgVtFuZuu_gryXKEpX79zn4aMdQQ84lPjM3r8MOk"

    data = {"name": "XinXunXon", "username": "xin.xun.xon", "password": "159753"}
    headers = {"Authorization": auth_token}
    # Realizar uma requisição POST usando httpx

    async with httpx.AsyncClient(base_url="https://med-api-production.up.railway.app") as client:
        response = await client.post(login_url, headers=headers, json=data)

        print(response.text)
    # Verificar se o código de status é 200 (bem-sucedido)
    assert response.status_code == 200
    assert response.json() == {"XinJinPin", "xin.jin.pin159753", "159753"}