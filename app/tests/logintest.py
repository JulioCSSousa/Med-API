import httpx
import pytest


@pytest.mark.asyncio
async def test_login():
    # URL da rota de login na sua API FastAPI
    login_url = "https://med-api-production.up.railway.app/token"

    # Dados de login para o teste
    data = {'Content-Type': 'Application/json', 'username': 'neivcs@gmail.com', 'password': '159753'}

    # Realizar uma requisição POST usando httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(login_url, data=data)

        print(response.text)
    # Verificar se o código de status é 200 (bem-sucedido)
    assert response.status_code == 200
    assert "access_token" in response.json()
    # Verificar se a resposta contém um token ou outra indicação de login bem-sucedido
    print(response.text)

