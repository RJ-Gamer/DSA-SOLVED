# 104. Maximum Depth of Binary Tree

**LeetCode:** [https://leetcode.com/problems/maximum-depth-of-binary-tree/](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
**Difficulty:** Easy
**Topics:** [Binary Tree] [DFS] [BFS] [Recursion]

---

## Problem Statement

Given the `root` of a binary tree, return its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`
- `-100 <= Node.val <= 100`

### Example
```
Input:  root = [3,9,20,null,null,15,7]
        
        3
       / \
      9  20
        /  \
       15   7

Output: 3

Input:  root = [1,null,2]
        
        1
         \
          2

Output: 2
```

---

## How to Think About This Problem

### Step 1 — Understand depth vs height
Depth = number of nodes from root to current node. Height = number of nodes from current node to farthest leaf. We want maximum depth (longest path from root).

### Step 2 — Recognize the recursive structure
The max depth of a tree = 1 + max(depth of left subtree, depth of right subtree). This naturally suggests recursion.

### Step 3 — Identify base case
A tree with no nodes has depth 0. A tree with just root has depth 1.

### Step 4 — Choose approach
Two ways: DFS (recursion or stack) to explore nodes, or BFS (queue) to explore level by level.

---

## Approaches

### Approach 1 — DFS Recursive (Most Intuitive)
**Intuition:** Recursively find max depth of left and right subtrees, then add 1 for current node.

**Steps:**
1. Base case: if node is None, return 0
2. Recursively get max depth of left subtree
3. Recursively get max depth of right subtree
4. Return 1 + max(left_depth, right_depth)

**Illustration:** For the tree `3 -> [9, 20] -> [15, 7]`
```
maxDepth(3)
├─ maxDepth(9) -> return 1 (9 has no children)
├─ maxDepth(20)
   ├─ maxDepth(15) -> return 1 (leaf)
   ├─ maxDepth(7) -> return 1 (leaf)
   └─ return 1 + max(1, 1) = 2
└─ return 1 + max(1, 2) = 3
```

**Complexity:** Time O(n) visits each node / Space O(h) recursion stack

---

### Approach 2 — BFS Iterative (Level Order)
**Intuition:** Use a queue to traverse level by level. Track depth and return when done.

**Steps:**
1. If root is None, return 0
2. Initialize queue with (root, depth=1)
3. While queue has nodes:
   - Dequeue (node, depth)
   - Update max_depth
   - Enqueue children if they exist
4. Return max_depth

**Illustration:** Same tree, level-by-level
```
Level 1: Process node 3 (depth=1)
Level 2: Process nodes 9 (depth=2), 20 (depth=2)
Level 3: Process nodes 15 (depth=3), 7 (depth=3)
Max depth = 3
```

**Complexity:** Time O(n) / Space O(w) where w is max width

---

## Solution Breakdown — Step by Step

### DFS Recursive Solution
```python
def maxDepth(root: Optional[TreeNode]) -> int:
    if not root:              # Base case: empty tree
        return 0
    
    # Recursive case: 1 + max depth of subtrees
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

**Line-by-line:**
- `if not root: return 0`: Empty subtree has depth 0
- `maxDepth(root.left)`: Get depth of left subtree
- `maxDepth(root.right)`: Get depth of right subtree
- `max(...)`: Take the larger of the two
- `1 + ...`: Add current node (1) to the max of subtrees

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| DFS Recursive | O(n) | O(h) |
| BFS Iterative | O(n) | O(w) |

Where h = height, w = max width

---

## Common Mistakes

### Mistake 1 — Forgetting base case
❌ **Wrong:**
```python
def maxDepth(root):
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
    # This will crash on None (no base case)
```

✅ **Correct:**
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Mistake 2 — Counting edges instead of nodes
❌ **Wrong:**
```python
# Counting edges makes a single node have depth 0
return max(maxDepth(root.left), maxDepth(root.right))  # Missing the +1
```

✅ **Correct:**
```python
# Count nodes, not edges
return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

## Pattern Recognition

> Use this pattern when you see: Find maximum or minimum values in trees, or traverse all nodes calculating aggregate values (sum, product, height, etc.).

**Similar problems:**
- LeetCode 111: Minimum Depth of Binary Tree
- LeetCode 110: Balanced Binary Tree
- LeetCode 112: Path Sum
- LeetCode 129: Sum Root to Leaf Numbers

---

## Real World Use Cases

### 1. Tree Balancing Algorithms
AVL trees and Red-Black trees check depth to maintain balance constraints.

### 2. Database Index Structures
B-trees store data indexes; depth determines query performance and is critical to optimize.

### 3. DOM Structure Analysis
Web browsers analyze DOM trees' depth to optimize rendering and styling calculations.

---

## Key Takeaways

- Maximum depth is the count of nodes on the longest path from root to leaf
- Recursion naturally expresses the recursive structure of trees
- Base case (None returns 0) is crucial
- Both DFS and BFS work; DFS is typically simpler to implement

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Maximum Depth of Binary Tree | Easy |
| [LeetCode #111](https://leetcode.com/problems/minimum-depth-of-binary-tree/) | Minimum Depth of Binary Tree | Easy |
| [LeetCode #110](https://leetcode.com/problems/balanced-binary-tree/) | Balanced Binary Tree | Easy |

> Essential binary tree problem — foundation for tree traversal patterns.
