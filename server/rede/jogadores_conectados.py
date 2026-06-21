
from modelos.sessao import SessaoJogador
from modelos.jogador import Jogador
import json

conectados: list[SessaoJogador]= []

async def resposta_lista_jogadores_conectados(websocket):
    listagem_conectados = [
    ]
    for i in conectados:
        listagem_conectados.append(i.jogador.model_dump())

    listagem_conectados_tradada = {
        "t": "players",
        "d": { 
            "players": listagem_conectados
        }
        }
        
    await websocket.send(json.dumps(listagem_conectados_tradada))


async def resposta_jogador_conectou(jogador: Jogador):
    conectou = { "t": "player_joined", "d": jogador.model_dump()}
    for i in conectados:
        await i.websocket.send(json.dumps(conectou))


async def adicionar_jogador_listagem(jogador: Jogador, websocket):
    novo_jogador_conectado = SessaoJogador(jogador=jogador, websocket=websocket)
    conectados.append(novo_jogador_conectado)
    await resposta_jogador_conectou(jogador)

async def remover_jogador_listagem(websocket):
    for i, jogador in enumerate(conectados):
        if jogador.websocket == websocket:
            del conectados[i]
            await resposta_jogador_removido(jogador)
            break

    
async def resposta_jogador_removido(jogador: SessaoJogador):
    resposta = { "t": "player_left", "d": { "id": jogador.jogador.id } }
    for i in conectados:
        await i.websocket.send(json.dumps(resposta))