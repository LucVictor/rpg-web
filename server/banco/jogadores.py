from modelos.jogador import Jogador, Item

item: Item = Item(id="sword", name="Espada", qty=1)
item_2: Item = Item(id="sword", name="Espada", qty=2)


jogador_1: Jogador = Jogador(id=1, name="lucas", x=7, y=5, dir=4, hp=100, max_hp=100, inventory=[item])

jogador_2: Jogador = Jogador(id=2, name="admin", x=5, y=3, dir=2, hp=100, max_hp=100, inventory=[item_2])

jogadores    = [jogador_1, jogador_2]

