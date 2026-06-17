import json
from main import conectados
resposta_login_certo_Lucas = {
  "t": "login_ok",
  "d": {
    "id": "p_3",
    "name": "Lucas",
    "x": 7, "y": 5, "dir": 4,
    "hp": 100, "max_hp": 100,
    "inventory": [
      { "id": "sword", "name": "Espada", "qty": 1 },
      { "id": "potion", "name": "Poção", "qty": 3 }
    ]
  }
}

resposta_login_certo_admin = {
  "t": "login_ok",
  "d": {
    "id": "p_1",
    "name": "Admin",
    "x": 6, "y": 4, "dir": 3,
    "hp": 50, "max_hp": 50,
    "inventory": [
      { "id": "sword", "name": "Espada", "qty": 1 },
      { "id": "potion", "name": "Poção", "qty": 3 }
    ]
  }
}

reposta_login_errado = {
  "t": "login_err", "d": "Usuário ou senha incorretos"}


async def player_conectado(dados):
    player = json.dumps({ "t": "player_joined", "d": { "id": dados.get("id"), "name": dados.get("name"), 
        "x": dados.get("x"), "y": dados.get("y")
        , "dir": dados.get("dir"), "hp": dados.get("hp"), "max_hp": dados.get("max_hp") } })
    for i in conectados:
        await i.send(player)


async def logar_usuario(dados, websocket):
    usuario = dados.get("name")
    if usuario == "lucas":
        conectados.add(websocket)
        await player_conectado(resposta_login_certo_Lucas)
        return json.dumps(resposta_login_certo_Lucas)
    elif usuario == "admin":
        conectados.add(websocket)
        await player_conectado(resposta_login_certo_admin)
        return json.dumps(resposta_login_certo_admin)
    else:
        return json.dumps(reposta_login_errado)