import json

conectados = []

async def logados_lista(websocket):
    print(conectados)
    listagem = conectados
    listagem_tradada = []
    for i in listagem:
        i.pop("websocket")
        listagem_tradada.append(i["d"])
    players = {
            "t": "players",
            "d": {
                "players": listagem_tradada
            }
            }
    await websocket.send((players))




async def player_logado(dados, websocket):
    player = {
            "d": {
                "id": dados["id"],
                "name": dados["name"],
                "x": dados["x"],
                "y": dados["y"],
                "dir": dados["dir"],
                "hp": dados["hp"],
                "max_hp": dados["max_hp"]
            },
            "websocket": websocket
        }
    
    conectados.append(player)
    await logados_lista(websocket)

    await anuncio_player_logado()


async def anuncio_player_logado():
    for i in conectados:
        player = json.dumps({
            "t": "player_joined",
            "d":{                
                "id": i["d"]["id"],
                "name": i["d"]["name"],
                "x": i["d"]["x"],
                "y": i["d"]["y"],
                "dir": i["d"]["dir"],
                "hp": i["d"]["hp"],
                "max_hp": i["d"]["max_hp"]}

            })
        await i["websocket"].send((player))

