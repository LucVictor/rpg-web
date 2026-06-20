from pydantic import BaseModel

class Item(BaseModel):
    id: str
    name: str
    qty: int

class Jogador(BaseModel):
    id: int
    name: str
    x: int
    y: int 
    dir: int
    hp: int
    max_hp: int
    inventory: list[Item] = []
