# ⚔️ RPG Web — Cliente + Servidor de Referência

Um RPG **tile-based top-down** (grid, estilo Habbo/Dofus) que roda no navegador e
fala com um **servidor externo** via **WebSocket + JSON**.

A ideia do projeto: o **cliente está pronto** e o **servidor é seu treino**. Você
constrói o seu servidor do zero, na linguagem que quiser, seguindo o
[`PROTOCOLO.md`](./PROTOCOLO.md). Para comparar, incluímos um servidor de
referência em Python (`server.py`).

---

## 📁 Arquivos

| Arquivo         | O que é |
|-----------------|---------|
| `index.html`    | **Cliente** completo (HTML/CSS/JS num arquivo só). Não precisa build. |
| `server.py`     | **Servidor de referência** em Python (asyncio + websockets). Gabarito. |
| `PROTOCOLO.md`  | **Contrato** do protocolo — toda mensagem cliente↔servidor descrita. |
| `test_flow.py`  | Teste automatizado que simula 2 clientes contra o servidor. |
| `README.md`     | Este arquivo. |

---

## 🚀 Como rodar (com o servidor de referência)

1. **Instale a dependência do servidor:**
   ```bash
   pip install websockets
   ```

2. **Suba o servidor:**
   ```bash
   python server.py
   # -> Servidor de referência em ws://0.0.0.0:8765
   ```

3. **Abra o cliente:** abra `index.html` no navegador (duplo clique já serve).
   - Ele tenta conectar em `ws://localhost:8765` automaticamente.
   - Digite um nome e clique **Entrar**.
   - Abra em **duas abas** para ver o multiplayer.

> Dica: para abrir o cliente via servidor local (evita travas de alguns navegadores):
> `python -m http.server 8080` e acesse `http://localhost:8080/index.html`.

### Controles
- **Andar:** clique numa célula vizinha.
- **Atacar:** clique num monstro que esteja a 1 célula de você.
- **Chat:** digite embaixo e Enter.
- **Itens:** botão **Usar** no inventário (a Poção cura 30 HP).

---

## 🧠 Conceito central: servidor autoritativo

O **cliente é "burro" de propósito**. Ele só:
1. desenha o que o servidor manda, e
2. pede ações (`move`, `attack`, `say`...).

**Quem decide é o servidor.** Ele valida tudo (a célula é andável? o alvo está
perto?) e só então faz *broadcast* do resultado. Isso evita trapaça e mantém
todos os clientes sincronizados.

```
Cliente: "quero ir pra (8,5)"   --->  Servidor valida  --->  "moved: p_2 foi pra (8,5)"  (pra todos)
```

Se o servidor não responde `moved`, o cliente simplesmente não anda. Sem confiar
no cliente.

---

## 🛠️ Construindo o SEU servidor — passo a passo sugerido

Faça em ordem; cada passo já dá pra testar no cliente real.

1. **Aceitar conexão WebSocket** na porta `8765` e, ao conectar, enviar
   `welcome` com o mapa. → O cliente já desenha o grid.
2. **`login`** → responder `login_ok` + `players` + `monsters`. → Seu avatar aparece.
3. **Multiplayer:** guardar lista de jogadores, fazer `broadcast` de
   `player_joined` / `player_left`. → Abra 2 abas e veja os dois.
4. **`move`** → validar adjacência + colisão, fazer `broadcast` de `moved`.
5. **`say`** → `broadcast` de `chat`.
6. **`attack`** → validar distância, mandar `combat`, e `monster_died` quando HP≤0.
7. **`use_item`** → mexer no inventário, mandar `inventory` + `hp`.

Cada mensagem está detalhada com exemplo JSON no [`PROTOCOLO.md`](./PROTOCOLO.md).

---

## 💡 Dicas práticas

- **Comece pelo `welcome`.** Se o cliente desenha o mapa, sua base de WebSocket
  e JSON já está certa. É o "hello world" do projeto.
- **JSON em uma linha.** Cada mensagem é um objeto `{"t":"...","d":{...}}`.
  Nada de múltiplas linhas por mensagem.
- **Use o `server.py` como oráculo.** Não sabe o formato exato de um campo? Suba
  o servidor de referência, abra o **console do navegador** (F12) e veja as
  mensagens chegando, ou olhe os `print` do servidor.
- **Debug do cliente:** no console do navegador, mensagens não tratadas aparecem
  com `console.log("Mensagem não tratada:", ...)`. JSON inválido também é logado.
- **Teste sem navegador:** rode `python test_flow.py` (com o servidor no ar) pra
  validar login, movimento, chat, ataque e inventário de forma automática.
- **IDs:** mantenha um id único e estável por sessão (`p_1`, `p_2`...). O cliente
  usa o id pra saber qual avatar é o "você" (campo `your_id` do `welcome`).
- **Coordenadas:** grid inteiro, `(0,0)` no canto superior-esquerdo, `x`→direita,
  `y`→baixo. `dir` 0–7 (veja diagrama no protocolo); pode usar só 0/2/4/6.
- **Validação primeiro, broadcast depois.** Nunca propague uma ação sem checar.
- **Rate limit no `move`** (ex.: 1 a cada 150 ms) evita "speedhack". Opcional no MVP.
- **Respawn:** o servidor de referência ressuscita o monstro 8s após morrer — boa
  ideia de mecânica simples pra copiar.

---

## 🧪 Checklist de paridade (seu servidor vs. referência)

- [ ] Conecta e recebe `welcome` (mapa desenha).
- [ ] `login` → avatar aparece com nome e HP.
- [ ] Segunda aba aparece pra primeira (e vice-versa).
- [ ] Andar funciona; parede e célula ocupada bloqueiam.
- [ ] Chat aparece em todas as abas.
- [ ] Atacar monstro adjacente tira HP; longe dá `error`.
- [ ] Monstro morre e some; respawn (se implementar).
- [ ] Poção cura e diminui a quantidade no inventário.

---

## 🔌 Trocar a URL do servidor

No topo do cliente há um campo de URL (`ws://localhost:8765`). Mude para o
endereço do seu servidor e clique **Conectar**. Funciona com qualquer servidor
que siga o protocolo — Python, Node, Go, C#, etc.

---

## 📈 Próximos passos (quando o básico estiver redondo)

- Pathfinding no servidor (clicar longe e andar passo a passo).
- Mais mapas / troca de sala.
- Persistência (salvar jogador em arquivo/DB).
- Loot ao matar monstro (manda `inventory`).
- Stats/level/XP.
- IA dos monstros (perseguir, atacar de volta com `combat` + `hp`).

Bom treino! 🎮
