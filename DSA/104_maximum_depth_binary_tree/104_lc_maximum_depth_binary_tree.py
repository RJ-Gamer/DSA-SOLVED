"""
LeetCode 104: Maximum Depth of Binary Tree
Difficulty: Easy
Topics: Binary Tree, DFS, BFS, Recursion

Time Complexity: O(n)
Space Complexity: O(h) where h is height / O(n) worst case
"""

# LeetCode Problem #104: Maximum Depth of Binary Tree

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def max_depth_bfs(root: TreeNode) -> int:
    if not root:
        return 0
    from collections import deque
    q = deque([(root, 1)])
    depth = 0
    while q:
        node, d = q.popleft()
        depth = max(depth, d)
        if node.left:
            q.append((node.left, d + 1))
        if node.right:
            q.append((node.right, d + 1))
    return depth


root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
print(max_depth(root))

