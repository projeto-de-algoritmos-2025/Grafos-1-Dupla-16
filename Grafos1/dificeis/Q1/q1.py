from typing import List
from collections import deque

class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        # n = número de nós no grafo
        n = len(graph)

        # Constantes de resultado: 1 = rato vence, 2 = gato vence
        MOUSE, CAT = 1, 2

        # color[m][c][t] guarda o resultado do estado:
        #   m = posição do rato, c = posição do gato, t = quem joga (0=rato, 1=gato)
        # Valores possíveis: 0=indefinido, 1=rato vence, 2=gato vence
        color = [[[0]*2 for _ in range(n)] for __ in range(n)]

        # degree[m][c][t] = número de jogadas possíveis a partir do estado (m,c,t)
        # (usado para detectar quando todas as opções levam à derrota)
        degree = [[[0]*2 for _ in range(n)] for __ in range(n)]

        # Pré-calcula os graus de cada estado:
        # - turno do rato (t=0): ele pode ir para qualquer vizinho de m
        # - turno do gato  (t=1): ele pode ir para qualquer vizinho de c, exceto o buraco (0)
        for m in range(n):
            for c in range(n):
                degree[m][c][0] = len(graph[m])
                degree[m][c][1] = len([v for v in graph[c] if v != 0])

        # Fila para BFS reverso (propaga resultados conhecidos para estados "pais")
        q = deque()

        # Estados terminais conhecidos:
        # - se o rato está no buraco (m=0), rato vence
        # - se gato e rato estão na mesma célula (m=c), gato vence
        # Inserimos ambos os turnos (t=0 e t=1) para cada base
        for i in range(n):
            for t in range(2):
                if i != 0:
                    color[0][i][t] = MOUSE
                    q.append((0, i, t, MOUSE))  # rato no buraco -> vitória do rato
                color[i][i][t] = CAT
                q.append((i, i, t, CAT))       # mesma posição -> gato vence

        # Função geradora que lista os estados "pais" de (m,c,t).
        # Pais são estados que, com um movimento, chegam ao estado atual.
        def parents(m, c, t):
            if t == 0:
                # Se o turno atual é do rato, então o estado anterior era o turno do gato (t=1),
                # que moveu de pc -> c. O gato não pode ir ao buraco (0).
                for pc in graph[c]:
                    if pc != 0:
                        yield (m, pc, 1)
            else:
                # Se o turno atual é do gato, o estado anterior era o turno do rato (t=0),
                # que moveu de pm -> m.
                for pm in graph[m]:
                    yield (pm, c, 0)

        # BFS reverso:
        # Começamos pelos estados resolvidos (terminais) e propagamos
        # para trás, colorindo os pais quando possível.
        while q:
            m, c, t, res = q.popleft()

            for pm, pc, pt in parents(m, c, t):
                # Se o pai já foi resolvido, ignore
                if color[pm][pc][pt] != 0:
                    continue

                # Regra 1 (melhor jogada): se do estado pai é a vez do jogador X (pt)
                # e existe um movimento que leva a uma vitória de X (res), então X
                # escolhe esse movimento e o estado pai fica ganho para X.
                if (pt == 0 and res == MOUSE) or (pt == 1 and res == CAT):
                    color[pm][pc][pt] = res
                    q.append((pm, pc, pt, res))
                else:
                    # Regra 2 (pior caso): senão, esse movimento leva a uma derrota para quem joga em 'pt'.
                    # Diminuímos o grau de opções ainda "não perdedoras".
                    degree[pm][pc][pt] -= 1

                    # Se TODAS as opções do estado pai levam à vitória do oponente,
                    # então o estado pai é derrota para quem joga nele.
                    if degree[pm][pc][pt] == 0:
                        color[pm][pc][pt] = CAT if pt == 0 else MOUSE
                        q.append((pm, pc, pt, color[pm][pc][pt]))

        # Resultado pedido: estado inicial (rato=1, gato=2, turno do rato)
        # Se continuar 0 (indefinido), por definição é empate.
        return color[1][2][0] if color[1][2][0] != 0 else 0
