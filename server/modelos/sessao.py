from .jogador import Jogador
from pydantic import BaseModel, ConfigDict
from websockets.asyncio.server import ServerConnection

class SessaoJogador(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    jogador: Jogador
    websocket: ServerConnection

