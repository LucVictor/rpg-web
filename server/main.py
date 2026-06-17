import asyncio
import websockets
from rede.rede import tratar_mensagem

conectados = set()
async def servidor(websocket):
    print("Cliente conectado")
    print(websocket)

    try:
        while True:
            recebida = await websocket.recv()
            print(f"Mensagem recebida: {recebida}")


            resposta = await tratar_mensagem(recebida, websocket)
            print(f"Mensagem apos tratar: {resposta}")

            await websocket.send(resposta)
            print(20*"=")

    except websockets.ConnectionClosed:
        print("Cliente desconectado")


async def main():
    server = await websockets.serve(
        servidor,
        "0.0.0.0",
        8765
    )

    print("Servidor iniciado")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())