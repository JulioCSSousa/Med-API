import base64
import httpx
import logging
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.main import app  # Substitua pelo caminho real do seu módulo FastAPI




def test_http_base_with_json_content_type():
    import logging
    # Configuração do logger
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)  # Nível de log DEBUG
    logger.addHandler(logging.StreamHandler())  # Adiciona um manipulador para exibir logs na saída padrão
    logging.basicConfig(level=logging.DEBUG)
    url = "https://med-api-production.up.railway.app/token"  # Substitua pela URL correta da sua aplicação
    username = "neivcs@gmail.com"
    password = "159753"

    credentials = f"{username} {password}"
    credentials_base64 = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }

    data = {"username": "neivcs@gmail.com", "password": "159753"}

    with httpx.Client() as client:
        response = client.post(url, json=data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"mensagem": "Resposta esperada"}
    assert logger