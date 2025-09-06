# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')  # guarda o resultado global

        def dfs(node):
            if not node:
                return 0
            
            # calcula o melhor caminho pela esquerda e direita, ignorando negativos
            left = max(dfs(node.left), 0)
            right = max(dfs(node.right), 0)

            # melhor caminho passando pelo nó atual
            self.max_sum = max(self.max_sum, node.val + left + right)

            # retorna o maior caminho descendente (só pode escolher um lado)
            return node.val + max(left, right)

        dfs(root)
        return self.max_sum
