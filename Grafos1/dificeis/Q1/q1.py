from typing import List
from collections import deque

class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        n = len(graph)
        MOUSE, CAT = 1, 2

        color = [[[0]*2 for _ in range(n)] for __ in range(n)]
        degree = [[[0]*2 for _ in range(n)] for __ in range(n)]

        for m in range(n):
            for c in range(n):
                degree[m][c][0] = len(graph[m])
                degree[m][c][1] = len([v for v in graph[c] if v != 0])

        q = deque()

        for i in range(n):
            for t in range(2):
                if i != 0:
                    color[0][i][t] = MOUSE
                    q.append((0, i, t, MOUSE))
                color[i][i][t] = CAT
                q.append((i, i, t, CAT))

        def parents(m, c, t):
            if t == 0:
                for pc in graph[c]:
                    if pc != 0:
                        yield (m, pc, 1)
            else:
                for pm in graph[m]:
                    yield (pm, c, 0)

        while q:
            m, c, t, res = q.popleft()
            for pm, pc, pt in parents(m, c, t):
                if color[pm][pc][pt] != 0:
                    continue
                if (pt == 0 and res == MOUSE) or (pt == 1 and res == CAT):
                    color[pm][pc][pt] = res
                    q.append((pm, pc, pt, res))
                else:
                    degree[pm][pc][pt] -= 1
                    if degree[pm][pc][pt] == 0:
                        color[pm][pc][pt] = CAT if pt == 0 else MOUSE
                        q.append((pm, pc, pt, color[pm][pc][pt]))

        return color[1][2][0] if color[1][2][0] != 0 else 0
