import pytest
import httpx
@pytest.mark.asyncio
async def test_users():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Teste depuração')
    login_url = "https://med-api-production.up.railway.app/users"
    auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZWl2Y3NAZ21haWwuY29tIiwiZXhwIjoxNzAzOTQzMjUwfQ._n89i505dgRPcqZoi6t37xWVvKjXZx-1deSMnvkfUEc"
    headers = {'Authorization': auth_token}

    # Realizar uma requisição POST usando httpx
    async with httpx.AsyncClient(base_url=login_url, follow_redirects=False ) as client:
        response = await client.get(login_url, headers=headers)

        print(response.text)
    # Verificar se o código de status é 200 (bem-sucedido)
    assert response.status_code == 200
    assert "access_token" in response.json()
    # Verificar se a resposta contém um token ou outra indicação de login bem-sucedido
    print(response.text)
