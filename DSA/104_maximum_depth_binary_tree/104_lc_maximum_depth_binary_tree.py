"""
LeetCode 104: Maximum Depth of Binary Tree
Difficulty: Easy
Topics: Binary Tree, DFS, BFS, Recursion

Time Complexity: O(n)
Space Complexity: O(h) where h is height / O(n) worst case
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxDepth(root: Optional[TreeNode]) -> int:
    """
    Find the maximum depth of a binary tree using DFS.
    
    Args:
        root: The root node of the binary tree
        
    Returns:
        The maximum depth (number of nodes along the longest path)
    """
    if not root:
        return 0
    
    return 1 + max(maxDepth(root.left), maxDepth(root.right))


def maxDepthIterative(root: Optional[TreeNode]) -> int:
    """
    Find the maximum depth of a binary tree using BFS.
    
    Args:
        root: The root node of the binary tree
        
    Returns:
        The maximum depth
    """
    if not root:
        return 0
    
    queue = deque([(root, 1)])
    max_depth = 0
    
    while queue:
        node, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return max_depth


# Test cases
if __name__ == "__main__":
    # Test 1: Balanced tree
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert maxDepth(root) == 3
    
    # Test 2: Single node
    root = TreeNode(1)
    assert maxDepth(root) == 1
    
    # Test 3: Empty tree
    assert maxDepth(None) == 0
    
    # Test 4: Linear tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert maxDepthIterative(root) == 3
    
    print("All tests passed!")
