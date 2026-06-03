# 200. Number of Islands

**LeetCode:** [https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)
**Difficulty:** Medium
**Topics:** [Graph] [DFS] [BFS] [Matrix]

---

## Problem Statement

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An island is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

### Constraints
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`

### Example
```
Input:  grid = [
          ["1","1","1","1","0"],
          ["1","1","0","1","0"],
          ["1","1","0","0","0"],
          ["0","0","0","0","0"]
        ]
Output: 1

Input:  grid = [
          ["1","1","0","0","0"],
          ["1","1","0","0","0"],
          ["0","0","1","0","0"],
          ["0","0","0","1","1"]
        ]
Output: 3
```

---

## How to Think About This Problem

### Step 1 — Understand what constitutes an island
Connected land cells ('1') form one island. Connection is only horizontal/vertical, not diagonal. Each island must be counted exactly once.

### Step 2 — Recognize this as a graph connectivity problem
Cells are nodes. Adjacent land cells have edges. Counting islands = counting connected components.

### Step 3 — Choose exploration strategy
When we find a '1', we must mark all connected '1's as visited to count them as one island. DFS or BFS both work.

### Step 4 — Mark visited cells to avoid double-counting
Either modify the grid or use a separate visited set. Modifying the grid is simpler and saves space.

---

## Approaches

### Approach 1 — DFS (Recursive)
**Intuition:** When we find a '1', recursively mark all connected '1's as '0', then increment island count.

**Steps:**
1. Iterate through each cell in the grid
2. When we find a '1':
   - Start DFS from that cell
   - DFS marks all connected '1's as '0'
   - Increment island counter
3. Return island counter

**DFS Helper:** For current cell, check all 4 directions (up, down, left, right) and recursively mark them as visited.

**Illustration:** First example
```
Initial grid (1=land, 0=water):
1 1 1 1 0
1 1 0 1 0
1 1 0 0 0
0 0 0 0 0

Find first '1' at (0,0), start DFS:
Marks all connected lands as 0:
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0

Island count = 1
```

**Complexity:** Time O(m*n) each cell visited once / Space O(m*n) recursion stack

---

### Approach 2 — BFS (Iterative)
**Intuition:** Use a queue instead of recursion to explore connected '1's.

**Steps:**
1. Iterate through each cell
2. When we find a '1':
   - Start BFS from that cell using a queue
   - Dequeue a cell, mark it as '0', enqueue its unvisited neighbors
   - Continue until queue is empty
   - Increment island counter
3. Return island counter

**Illustration:** Same example with BFS
```
Queue-based exploration of connected lands:
Start with first unvisited '1', add to queue
Process neighbors, add to queue
Continue until all connected lands are marked 0
Move to next unvisited '1'
```

**Complexity:** Time O(m*n) / Space O(min(m,n)) queue space

---

## Solution Breakdown — Step by Step

### DFS Solution
```python
def numIslands(grid):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Boundary check and water/visited check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        grid[r][c] = '0'  # Mark as visited
        
        # Explore 4 directions
        dfs(r + 1, c)     # Down
        dfs(r - 1, c)     # Up
        dfs(r, c + 1)     # Right
        dfs(r, c - 1)     # Left
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                dfs(i, j)  # Explore this island
                count += 1 # Island found
    
    return count
```

**Line-by-line:**
- `if not grid or not grid[0]: return 0`: Handle empty grid
- `if r < 0 or r >= rows or c < 0 or c >= cols`: Out of bounds check
- `if grid[r][c] == '0': return`: Already visited or water
- `grid[r][c] = '0'`: Mark current cell as visited
- `dfs(r±1, c) and dfs(r, c±1)`: Recursively explore 4 neighbors
- `if grid[i][j] == '1': dfs(i, j); count += 1`: Count and explore each new island

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| DFS Recursive | O(m*n) | O(m*n) |
| BFS Iterative | O(m*n) | O(min(m,n)) |

---

## Common Mistakes

### Mistake 1 — Exploring diagonals
❌ **Wrong:**
```python
# Problem states only horizontal/vertical connections
dfs(r+1, c+1)  # Diagonal - NOT allowed
```

✅ **Correct:**
```python
# Only 4 directions
dfs(r+1, c), dfs(r-1, c), dfs(r, c+1), dfs(r, c-1)
```

### Mistake 2 — Not marking visited
❌ **Wrong:**
```python
def dfs(r, c):
    # Count the same land cell multiple times!
    dfs(r + 1, c)
    dfs(r - 1, c)
    # ... missing grid[r][c] = '0'
```

✅ **Correct:**
```python
def dfs(r, c):
    grid[r][c] = '0'  # Mark visited FIRST
    dfs(r + 1, c)
    # ... now won't revisit
```

---

## Pattern Recognition

> Use this pattern when you see: Connected components in a grid, islands, number of clusters, or any 2D grid connectivity problem.

**Similar problems:**
- LeetCode 463: Island Perimeter
- LeetCode 694: Number of Distinct Islands
- LeetCode 1905: Count Sub-Islands
- LeetCode 130: Surrounded Regions

---

## Real World Use Cases

### 1. Map Analysis
Geographic systems need to identify island regions, lake regions, or any clustered geographic features.

### 2. Social Networks
Finding groups of connected users (friends of friends) for community detection.

### 3. Image Processing
Identifying connected components in binary images for object detection and analysis.

---

## Key Takeaways

- Islands are connected components in a grid graph
- Mark cells as visited to avoid counting them multiple times
- Both DFS and BFS solve this; DFS is usually simpler
- Always check boundaries before accessing grid cells
- The key insight is recognizing this as a graph connectivity problem

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | Number of Islands | Medium |
| [LeetCode #463](https://leetcode.com/problems/island-perimeter/) | Island Perimeter | Easy |
| [LeetCode #1905](https://leetcode.com/problems/count-sub-islands/) | Count Sub-Islands | Medium |

> Classic graph problem on a grid — frequently asked in interviews.
