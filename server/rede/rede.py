import json
from autenticador.auth import logar_usuario
from autenticador.bemvindo import bem_vindo

async def tratar_mensagem(informacao, websocket):
    dados = json.loads(informacao)
    if dados["t"] == "login":
        from autenticador.auth import logar_usuario
        return await logar_usuario(dados["d"], websocket)
    if dados["t"] == "welcome":
        return await bem_vindo(websocket)
    return json.dumps(dados)
