import json
from players.logados import player_logado

player_lucas = {
    "id": "p_2",
    "name": "Lucas",
    "x": 7, "y": 5, "dir": 4,
    "hp": 100, "max_hp": 100,
    "inventory": [
      { "id": "sword", "name": "Espada", "qty": 1 },
      { "id": "potion", "name": "Poção", "qty": 3 }
    ]
}

player_admin = {
    "id": "p_1",
    "name": "Admin",
    "x": 6, "y": 4, "dir": 3,
    "hp": 50, "max_hp": 50,
    "inventory": [
      { "id": "sword", "name": "Espada", "qty": 1 },
      { "id": "potion", "name": "Poção", "qty": 3 }
    ]
}


async def logar_usuario(dados, websocket):
    usuario = dados.get("name")
    if usuario == "lucas":
        login_ok = {
          "t": "login_ok",
          "d": player_lucas
        }
        await websocket.send(json.dumps(login_ok))
        await player_logado(player_lucas, websocket)

    elif usuario == "admin":
        login_ok = {
          "t": "login_ok",
          "d": player_admin
        } 
        await websocket.send(json.dumps(login_ok))
        await player_logado(player_admin, websocket)

    else:
        reposta_login_errado = {
        "t": "login_err", "d": "Usuário ou senha incorretos"}
        await websocket.send(json.dumps(reposta_login_errado))