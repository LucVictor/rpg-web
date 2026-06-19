import asyncio
import websockets
from rede.rede import tratar_mensagem
from autenticador.bemvindo import bem_vindo

conectados = set()
async def servidor(websocket):
    await bem_vindo(websocket)

    try:
        while True:
            recebida = await websocket.recv()
            print(f"Mensagem recebida: {recebida}")


            await tratar_mensagem(recebida, websocket)

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