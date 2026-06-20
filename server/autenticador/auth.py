import json
from banco.jogadores import jogadores
from modelos.jogador import Jogador
from rede.jogadores_conectados import adicionar_jogador_listagem, resposta_lista_jogadores_conectados


def login_ok_reposta(player_dados: Jogador):
  jogador = player_dados.model_dump()
  response = {
  "t": "login_ok",
  "d": jogador
}
  return response
  


async def logar_usuario(dados, websocket):
    usuario = dados.get("name")
    player = next(
        (x for x in jogadores if x.name == usuario),
        None
    )
    if player:
      await websocket.send(json.dumps(login_ok_reposta(player)))
      await resposta_lista_jogadores_conectados(websocket)
      await adicionar_jogador_listagem(player, websocket)

    else:
        reposta_login_errado = {
        "t": "login_err", "d": "Usuário ou senha incorretos"}
        await websocket.send(json.dumps(reposta_login_errado))