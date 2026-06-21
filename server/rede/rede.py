import json
from autenticador.auth import logar_usuario
from autenticador.bemvindo import bem_vindo
from chat.chat import digitou_no_chat
from movimentacao.movimentacao import jogador_movimentou_reponse


async def tratar_mensagem(informacao, websocket):
    dados = json.loads(informacao)
    if dados["t"] == "login":
        await logar_usuario(dados["d"], websocket)
    if dados["t"] == "welcome":
        await bem_vindo(websocket)
    if dados["t"] == "move":
        await jogador_movimentou_reponse(dados, websocket)
    if dados["t"] == "say":
        await digitou_no_chat(dados, websocket)