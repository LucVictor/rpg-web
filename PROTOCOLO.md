# Protocolo de Comunicação — RPG Web

Documento de referência do protocolo entre **cliente** (navegador) e **servidor**.
Use isto como contrato: se o seu servidor responder exatamente como descrito aqui, o cliente funciona sem nenhuma alteração.

---

## 1. Transporte

- **Tecnologia:** WebSocket (texto, não binário).
- **Formato:** toda mensagem é um **JSON em UMA linha** (sem quebras de linha internas).
- **Encoding:** UTF-8.
- **URL padrão:** `ws://localhost:8765`
- **Direção:** full-duplex. Cliente e servidor podem enviar a qualquer momento.

### Envelope comum

Toda mensagem — em qualquer direção — tem esta forma:

```json
{ "t": "<tipo>", "d": { ...dados... } }
```

| Campo | Tipo   | Descrição                                  |
|-------|--------|--------------------------------------------|
| `t`   | string | Tipo da mensagem (o "comando"). Ver tabelas abaixo. |
| `d`   | object | Payload. Pode ser `{}` se não houver dados. |

> **Dica:** manter `t` curto e `d` como objeto facilita versionar depois (é só adicionar campos em `d`).

---

## 2. Tipos de coordenada

- O mapa é um **grid** de células. `x` e `y` são **inteiros** (coluna, linha), começando em `0`.
- O canto superior-esquerdo é `(0,0)`. `x` cresce para a direita, `y` para baixo.
- `dir` (direção do avatar) é um inteiro 0–7 (estilo isométrico/8 direções):

```
   7  0  1
    \ | /
  6 - P - 2
    / | \
   5  4  3
```

Para um MVP você pode usar só 0=cima, 2=direita, 4=baixo, 6=esquerda.

---

## 3. Fluxo geral (handshake → jogo)

```
Cliente                              Servidor
  |  --- connect (WebSocket) ------->  |
  |  <----------- welcome -----------  |   (envia mapa + seu id)
  |  --- login {name} -------------->  |
  |  <----------- login_ok ----------  |   (seus dados de jogador)
  |  <----------- players -----------  |   (lista de quem já está online)
  |  <----------- chat (system) -----  |   ("Fulano entrou")
  |                                    |
  |  --- move {x,y} ---------------->  |
  |  <----------- moved -------------  |   (broadcast p/ todos)
  |  --- say {text} ---------------->  |
  |  <----------- chat --------------  |   (broadcast p/ todos)
  |  --- attack {id} --------------->  |
  |  <----------- combat ------------  |   (dano, hp atualizado)
  |                                    |
  |  (ao desconectar)                  |
  |  <----------- player_left -------  |   (broadcast p/ os outros)
```

---

## 4. Mensagens SERVIDOR → CLIENTE

### 4.1 `welcome`
Enviada logo após a conexão abrir. Dá ao cliente o mapa e o id que ele terá.

```json
{
  "t": "welcome",
  "d": {
    "your_id": "p_3",
    "map": {
      "w": 15,
      "h": 11,
      "tiles": [[0,0,1,0, ...], ...]
    }
  }
}
```

| Campo            | Tipo            | Descrição |
|------------------|-----------------|-----------|
| `your_id`        | string          | Id único do jogador nesta sessão. |
| `map.w`,`map.h`  | int             | Largura/altura do grid em células. |
| `map.tiles`      | int[h][w]       | Matriz. `0` = chão andável, `1` = bloqueado (parede). |

### 4.2 `login_ok`
Confirma o login e devolve o estado inicial do jogador.

```json
{
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
```

### 4.3 `login_err`
Login recusado (nome inválido, já em uso, etc).

```json
{ "t": "login_err", "d": { "reason": "Nome já em uso" } }
```

### 4.4 `players`
Lista completa de jogadores atualmente na sala (inclui você). Útil ao entrar.

```json
{
  "t": "players",
  "d": {
    "players": [
      { "id": "p_1", "name": "Ana",   "x": 3, "y": 2, "dir": 4, "hp": 100, "max_hp": 100 },
      { "id": "p_3", "name": "Lucas", "x": 7, "y": 5, "dir": 4, "hp": 100, "max_hp": 100 }
    ]
  }
}

```

### 4.5 `player_joined`
Um novo jogador entrou (broadcast para os demais).

```json
{ "t": "player_joined", "d": { "id": "p_5", "name": "Bia", "x": 1, "y": 1, "dir": 4, "hp": 100, "max_hp": 100 } }
```

### 4.6 `player_left`
Um jogador saiu/desconectou.

```json
{ "t": "player_left", "d": { "id": "p_5" } }
```

### 4.7 `moved`
Confirma/propaga um movimento. Enviada a TODOS (inclusive quem moveu).

```json
{ "t": "moved", "d": { "id": "p_3", "x": 8, "y": 5, "dir": 2 } }
```

> **Dica de servidor autoritativo:** valide o movimento (célula adjacente? é andável?) ANTES de aceitar. Se inválido, não envie `moved` (ou envie a posição antiga só para o autor corrigir).

### 4.8 `chat`
Mensagem de chat. `from` ausente ou `"system"` indica mensagem do sistema.

```json
{ "t": "chat", "d": { "id": "p_1", "name": "Ana", "text": "olá!" } }
{ "t": "chat", "d": { "name": "system", "text": "Bia entrou na sala" } }
```

### 4.9 `monsters`
Lista/estado dos monstros na sala.

```json
{
  "t": "monsters",
  "d": {
    "monsters": [
      { "id": "m_1", "name": "Slime", "x": 10, "y": 3, "hp": 30, "max_hp": 30 }
    ]
  }
}
```

### 4.10 `combat`
Resultado de um ataque (de jogador em monstro, ou monstro em jogador).

```json
{
  "t": "combat",
  "d": {
    "attacker": "p_3",
    "target": "m_1",
    "damage": 12,
    "target_hp": 18,
    "target_kind": "monster"
  }
}
```

| Campo         | Tipo   | Descrição |
|---------------|--------|-----------|
| `attacker`    | string | Id de quem atacou. |
| `target`      | string | Id de quem recebeu. |
| `damage`      | int    | Dano aplicado. |
| `target_hp`   | int    | HP restante do alvo (após o dano). |
| `target_kind` | string | `"monster"` ou `"player"`. |

### 4.11 `monster_died`
Monstro morreu (hp <= 0).

```json
{ "t": "monster_died", "d": { "id": "m_1", "by": "p_3" } }
```

### 4.12 `inventory`
Atualização do inventário do jogador (após pegar item, usar poção, etc).

```json
{
  "t": "inventory",
  "d": { "inventory": [ { "id": "potion", "name": "Poção", "qty": 2 } ] }
}
```

### 4.13 `hp`
Atualização de HP de um jogador (após curar, levar dano, respawn).

```json
{ "t": "hp", "d": { "id": "p_3", "hp": 80, "max_hp": 100 } }
```

### 4.14 `error`
Erro genérico para qualquer comando inválido.

```json
{ "t": "error", "d": { "reason": "Comando desconhecido: foo" } }
```

---

## 5. Mensagens CLIENTE → SERVIDOR

### 5.1 `login`
```json
{ "t": "login", "d": { "name": "Lucas" } }
```
Servidor responde `login_ok` ou `login_err`, depois `players` e `monsters`.

### 5.2 `move`
Pedido de mover para uma célula. O cliente envia o destino desejado (célula adjacente).
```json
{ "t": "move", "d": { "x": 8, "y": 5 } }
```
> Servidor calcula `dir` a partir do delta, valida e responde com `moved`.

### 5.3 `say`
```json
{ "t": "say", "d": { "text": "olá pessoal" } }
```
Servidor faz broadcast com `chat`.

### 5.4 `attack`
```json
{ "t": "attack", "d": { "id": "m_1" } }
```
Servidor valida distância (alvo adjacente?) e responde com `combat` (e `monster_died` se aplicável).

### 5.5 `use_item`
```json
{ "t": "use_item", "d": { "id": "potion" } }
```
Ex.: poção cura HP. Servidor responde `hp` + `inventory`.

### 5.6 `ping` (opcional)
```json
{ "t": "ping", "d": {} }
```
Servidor responde `{ "t": "pong", "d": {} }`. Útil para medir latência / keep-alive.

---

## 6. Regras de validação recomendadas (servidor autoritativo)

O **servidor manda** — o cliente só pede e desenha. Sempre valide:

1. **Movimento:** destino deve ser célula adjacente (8-dir), dentro do grid e `tiles[y][x] == 0`. Caso contrário, ignore.
2. **Ataque:** alvo precisa existir e estar a 1 célula de distância (Chebyshev `max(|dx|,|dy|) <= 1`).
3. **Chat:** limite de tamanho (ex.: 200 chars), descarte vazio.
4. **Login:** nome não-vazio, único, sanitizado (sem caracteres de controle).
5. **HP:** nunca abaixo de 0; ao morrer, respawn na posição inicial com HP cheio (ou regra sua).
6. **Rate limit:** ignore movimentos rápidos demais (ex.: 1 a cada 150 ms) para evitar speedhack.

---

## 7. Tabela-resumo de tipos

| `t`              | Direção | Quando |
|------------------|---------|--------|
| `welcome`        | S→C     | logo após conectar |
| `login`          | C→S     | usuário entra com nome |
| `login_ok`       | S→C     | login aceito |
| `login_err`      | S→C     | login recusado |
| `players`        | S→C     | estado inicial de jogadores |
| `player_joined`  | S→C     | alguém entrou |
| `player_left`    | S→C     | alguém saiu |
| `move`           | C→S     | pedir movimento |
| `moved`          | S→C     | movimento aceito (broadcast) |
| `say`            | C→S     | enviar chat |
| `chat`           | S→C     | mensagem de chat (broadcast) |
| `monsters`       | S→C     | estado dos monstros |
| `attack`         | C→S     | atacar um alvo |
| `combat`         | S→C     | resultado do ataque |
| `monster_died`   | S→C     | monstro morreu |
| `use_item`       | C→S     | usar item do inventário |
| `inventory`      | S→C     | inventário atualizado |
| `hp`             | S→C     | HP atualizado |
| `error`          | S→C     | comando inválido |
| `ping`/`pong`    | C↔S     | keep-alive (opcional) |

---

## 8. Exemplo de sessão completa (logs)

```
S→C  {"t":"welcome","d":{"your_id":"p_2","map":{"w":15,"h":11,"tiles":[[...]]}}}
C→S  {"t":"login","d":{"name":"Lucas"}}
S→C  {"t":"login_ok","d":{"id":"p_2","name":"Lucas","x":7,"y":5,"dir":4,"hp":100,"max_hp":100,"inventory":[...]}}
S→C  {"t":"players","d":{"players":[...]}}
S→C  {"t":"monsters","d":{"monsters":[...]}}
S→C  {"t":"chat","d":{"name":"system","text":"Lucas entrou na sala"}}
C→S  {"t":"move","d":{"x":8,"y":5}}
S→C  {"t":"moved","d":{"id":"p_2","x":8,"y":5,"dir":2}}
C→S  {"t":"attack","d":{"id":"m_1"}}
S→C  {"t":"combat","d":{"attacker":"p_2","target":"m_1","damage":12,"target_hp":18,"target_kind":"monster"}}
C→S  {"t":"say","d":{"text":"morre slime!"}}
S→C  {"t":"chat","d":{"id":"p_2","name":"Lucas","text":"morre slime!"}}
```
