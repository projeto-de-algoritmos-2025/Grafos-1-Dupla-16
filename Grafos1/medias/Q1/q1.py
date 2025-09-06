# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        # Se a árvore estiver vazia, retorna None
        if not root:
            return root

        # Começa a partir do nó mais à esquerda da árvore (raiz inicialmente)
        leftmost = root

        # Percorre os níveis da árvore até que não haja mais filhos à esquerda
        while leftmost.left:
            # "head" percorre os nós do nível atual
            head = leftmost
            while head:
                # Conecta o filho esquerdo ao filho direito
                head.left.next = head.right

                # Se houver um próximo nó no mesmo nível, conecta o filho direito
                # ao filho esquerdo do próximo nó
                if head.next:
                    head.right.next = head.next.left

                # Move para o próximo nó no nível
                head = head.next

            # Desce para o próximo nível mais à esquerda
            leftmost = leftmost.left

        # Retorna a raiz com todos os ponteiros "next" conectados
        return root
