import httpx
import pytest


async def test_login():
    # URL da rota de login na sua API FastAPI
    login_url = "https://med-api-production.up.railway.app/token"

    # Dados de login para o teste
    login_data = {"email": "larissa@gemail.com", "password": "159753"}

    # Realizar uma requisição POST usando httpx
    with httpx.Client() as client:
        response = client.post(login_url, json=login_data)

    # Verificar se o código de status é 200 (bem-sucedido)
    assert response.status_code == 200

    # Verificar se a resposta contém um token ou outra indicação de login bem-sucedido
    assert "token" in response.json()

