from rede.jogadores_conectados import conectados
from modelos.sessao import SessaoJogador
import json


async def jogador_movimentou_reponse(informacao, websocket):
    informacao_moveu = json.loads(informacao)
    for i, jogador in enumerate(conectados):
        if jogador.websocket == websocket:
            jogador_moveu = {"t": "moved","d": {"id": jogador.jogador.id, "x": f"{informacao_moveu["d"]["x"]}", "y": f"{ informacao_moveu["d"]["y"]}"}}
            for i in conectados:
                await i.websocket.send(json.dumps(jogador_moveu))


    

