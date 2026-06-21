
from modelos.jogador import Jogador
from rede.jogadores_conectados import conectados
import json


async def entrou_no_chat(jogador: Jogador):
    response = { "t": "chat", "d": { "name": "system", "text": f"{jogador.name} entrou na sala" } }
    for i in conectados:
        await i.websocket.send(json.dumps(response))

async def digitou_no_chat(dados, websocket):
    for i, jogador in enumerate(conectados):
        if jogador.websocket == websocket:
            for i in conectados:
                response = { "t": "chat", "d": { "id": jogador.jogador.id, "name": jogador.jogador.name, "text": dados["d"]["text"] } }
                await i.websocket.send(json.dumps(response))
