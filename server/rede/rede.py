import json

async def tratar_mensagem(informacao, websocket):
    dados = json.loads(informacao)
    if dados["t"] == "login":
        from autenticador.auth import logar_usuario
        return await logar_usuario(dados["d"], websocket)
    return json.dumps(dados)
