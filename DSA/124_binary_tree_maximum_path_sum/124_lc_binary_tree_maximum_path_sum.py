# LeetCode Problem #124: Binary Tree Maximum Path Sum


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root: TreeNode) -> int:
    max_sum = [float('-inf')]

    def dfs(node):
        if not node:
            return 0

        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)

        # Path through this node using both branches
        path_sum = node.val + left_gain + right_gain
        max_sum[0] = max(max_sum[0], path_sum)

        # Return max gain through this node in a single direction
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum[0]


def build_tree(values):
    if not values:
        return None
    nodes = [TreeNode(v) if v is not None else None for v in values]
    for i in range(len(nodes)):
        if nodes[i]:
            left_i, right_i = 2 * i + 1, 2 * i + 2
            if left_i < len(nodes):
                nodes[i].left = nodes[left_i]
            if right_i < len(nodes):
                nodes[i].right = nodes[right_i]
    return nodes[0]


root1 = build_tree([1, 2, 3])
print(maxPathSum(root1))  # 6

root2 = build_tree([-10, 9, 20, None, None, 15, 7])
print(maxPathSum(root2))  # 42

root3 = build_tree([-3])
print(maxPathSum(root3))  # -3
