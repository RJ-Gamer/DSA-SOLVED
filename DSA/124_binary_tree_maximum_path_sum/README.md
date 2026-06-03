# 124. Binary Tree Maximum Path Sum

**LeetCode:** [Problem #124](https://leetcode.com/problems/binary-tree-maximum-path-sum/)  
**Difficulty:** Hard  
**Topics:** `Binary Tree` `DFS` `Recursion` `Dynamic Programming`

---

## Problem Statement

Given the `root` of a binary tree, return the **maximum path sum** of any
non-empty path. A path is a sequence of nodes where each pair of adjacent
nodes has an edge, and no node appears more than once. The path does not
need to pass through the root.

**Constraints:**
- The number of nodes in the tree is in the range `[1, 3 * 10⁴]`
- `-1000 <= Node.val <= 1000`

### Example
```
Input:  root = [1, 2, 3]
Output: 6
Explanation: Path 2 → 1 → 3 has sum 6.

Input:  root = [-10, 9, 20, null, null, 15, 7]
Output: 42
Explanation: Path 15 → 20 → 7 has sum 42.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

A "path" in a binary tree connects any node to any other node going through
edges — it does not have to pass through the root or even be top-down. The
tricky part: a path can go through a node and use both its left and right
subtrees, but when that same node contributes to a parent's path, it can
only continue in one direction (you can't fork a path upward).

### Step 2 — Identify the constraint that matters

When a DFS function visits a node, it faces two separate questions:
1. **What is the best path that passes through this node as its "peak"?**
   (can use both children)
2. **What is the best gain this node can contribute upward to its parent?**
   (can only go one direction)

These are different. The answer to question 1 updates a global maximum.
The return value of the function answers question 2.

### Step 3 — Think about data structures

We need a single DFS traversal. Each call returns the maximum one-sided gain
from that node. A single mutable container (a list of one value) lets us track
the global maximum across all recursive calls without relying on a nonlocal variable.

### Step 4 — Build the intuition

Think of the DFS function as: "I am a node. I'll ask my children for their
best contributions. I'll compute the best path that bends through me (both
children + myself). I'll report that to the global max. Then I'll return my
best single-direction gain to my parent."

Negative contributions are discarded with `max(gain, 0)` — you'd never
include a subtree that drags the sum down.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Enumerate every possible path in the tree by trying all
pairs of nodes and computing path sums via LCA traversal.

**Steps:**
1. For every pair of nodes, find the path between them
2. Sum the path and track the maximum

**Complexity:**
- Time: O(n²) to O(n³) — enumerating paths and computing sums
- Space: O(n) — recursion stack

**Code:**
```python
# Not practical — enumeration of all paths is O(n²) at minimum.
# The DFS approach is superior in every way.
```

---

### Approach 2 — Optimal (DFS with Global Max)

**Intuition:** Post-order DFS. At each node, compute the best "bent" path
through it and report the best straight-line gain upward to the parent.

**Steps:**
1. DFS post-order (visit children before parent)
2. At each node, clamp children gains to zero with `max(gain, 0)`
3. Compute `path_sum = node.val + left_gain + right_gain` — this is the
   candidate for the global max (path bends here)
4. Update the global max
5. Return `node.val + max(left_gain, right_gain)` — best single-sided gain

**Illustration:**
```
Tree: [-10, 9, 20, null, null, 15, 7]

         -10
        /    \
       9      20
             /  \
            15    7

DFS on 9:  left=0, right=0 → path=-10+9=... wait, each node is independent
  → gains: left=0, right=0 → path_sum=9, global_max=9, return=9

DFS on 15: left=0, right=0 → path_sum=15, global_max=15, return=15
DFS on 7:  left=0, right=0 → path_sum=7,  global_max=15, return=7

DFS on 20:
  left_gain=15, right_gain=7
  path_sum = 20 + 15 + 7 = 42  → global_max = 42
  return 20 + max(15, 7) = 35

DFS on -10:
  left_gain = max(9, 0)  = 9
  right_gain = max(35, 0) = 35
  path_sum = -10 + 9 + 35 = 34  → global_max stays 42
  return -10 + max(9, 35) = 25

Answer: 42 ✓
```

**Complexity:**
- Time: O(n) — each node visited once
- Space: O(h) — recursion stack depth, where h is tree height

**Code:**
```python
def maxPathSum(root):
    max_sum = [float('-inf')]

    def dfs(node):
        if not node:
            return 0
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum[0]
```

---

## Solution Breakdown — Step by Step

```python
def maxPathSum(root: TreeNode) -> int:
    max_sum = [float('-inf')]

    def dfs(node):
        if not node:
            return 0
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        path_sum = node.val + left_gain + right_gain
        max_sum[0] = max(max_sum[0], path_sum)
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum[0]
```

**Line by line:**

`max_sum = [float('-inf')]`
- A list is used so the inner function `dfs` can mutate it (Python closure
  limitation — assigning to a plain variable would create a local copy)
- Initialized to `-inf` because node values can be negative — a single
  negative node is still a valid path

`if not node: return 0`
- Base case: a null node contributes zero gain
- This is intentional — combined with `max(..., 0)` below, negative subtrees
  are dropped cleanly

`left_gain = max(dfs(node.left), 0)`
- Clamp to zero: if the left subtree only makes things worse (all negatives),
  don't include it — the path simply starts at this node
- Same logic applies to `right_gain`

`path_sum = node.val + left_gain + right_gain`
- This is the best path that bends through this node as its highest point
- It uses both children (or neither, or one — clamping handles all cases)
- This path cannot extend further up to the parent — it's the "peak" candidate

`max_sum[0] = max(max_sum[0], path_sum)`
- Every node is a candidate peak — we track the global best

`return node.val + max(left_gain, right_gain)`
- This is what the parent needs: the best single-direction extension from here
- A path continuing upward cannot fork — it must choose left or right

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (enumerate all paths) | O(n²)–O(n³) | O(n) |
| Optimal (DFS with global max) | O(n) | O(h) |

---

## Common Mistakes

**1. Returning the bent path sum to the parent**
```python
# WRONG — the parent can't use a forked path
return node.val + left_gain + right_gain

# CORRECT — return only the best single-sided gain
return node.val + max(left_gain, right_gain)
```
If you return the full path sum, the parent thinks it can extend it further —
but a path that forks cannot be extended.

**2. Not clamping negative gains to zero**
```python
# WRONG — a negative subtree drags the sum down
left_gain = dfs(node.left)

# CORRECT
left_gain = max(dfs(node.left), 0)
```
If the left subtree is all negatives, it's better to not include it.

**3. Using a plain int instead of a list for the global max**
```python
max_sum = float('-inf')

def dfs(node):
    max_sum = max(max_sum, ...)  # UnboundLocalError — creates a new local
```
Use a list (`max_sum = [float('-inf')]`) or a `nonlocal` declaration.

---

## Pattern Recognition

### How to Recognize
- Binary tree problem asking for a "path" that can go through any node
- The path can change direction once (at the peak node)
- Needs a global result updated during DFS traversal

### How to Identify
- Does the optimal path potentially bend through an interior node?
- Does the return value need to be different from the value used to update the answer?

### How to Remember
> **Mental model:** Each node asks "what's the best path that bends through me?"
> and separately reports "what's the best contribution I can give my parent?"

**Similar problems:**
- **Diameter of Binary Tree (LeetCode #543)** — same structure, track max diameter globally
- **Longest Univalue Path (LeetCode #687)** — same DFS pattern, different path condition
- **Binary Tree Maximum Path Sum II** — path must go root to leaf

---

## Real World Use Cases

### 1. Network routing optimization
Finding the highest-bandwidth path between any two nodes in a tree-structured
network topology. Each edge has a weight; the problem reduces to finding the
maximum sum path in a weighted tree.

### 2. Organizational reporting chains
In corporate hierarchies modeled as trees, finding the pair of employees
(and the chain between them) that maximizes total performance scores — used
in workforce analytics to identify high-impact reporting chains.

### 3. Phylogenetic tree analysis
In bioinformatics, evolutionary trees are analyzed to find the pair of species
with the highest cumulative similarity score along their connecting path —
directly equivalent to this problem.

---

## Key Takeaways

- The return value and the value used to update the global max are two different things
- Clamp gains to zero with `max(gain, 0)` to handle all-negative subtrees cleanly
- Use a list or `nonlocal` to share mutable state across recursive calls in Python
- Every node is a candidate "peak" — the DFS checks all of them in O(n)
- This pattern (return one thing, update global with another) appears in Diameter of Binary Tree too

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Binary Tree Maximum Path Sum | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
