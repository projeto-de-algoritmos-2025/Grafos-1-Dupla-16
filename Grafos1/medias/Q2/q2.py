# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        curr = root
        while curr:
            if curr.left:
                # Encontra o último nó da subárvore esquerda (predecessor)
                prev = curr.left
                while prev.right:
                    prev = prev.right
                # Conecta o lado direito antigo no final do lado esquerdo
                prev.right = curr.right
                # Move a subárvore esquerda para a direita
                curr.right = curr.left
                curr.left = None
            # Anda para o próximo nó
            curr = curr.right
