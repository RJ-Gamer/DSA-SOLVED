# 63. Unique Paths II

**LeetCode:** [Problem #63](https://leetcode.com/problems/unique-paths-ii/)
**Difficulty:** Medium
**Topics:** `Dynamic Programming`

---

## Problem Statement

A robot is located at the top-left corner of an `m x n` grid. The robot can
only move **right** or **down**. Some cells contain obstacles (`1`); the robot
cannot step on them. Empty cells are marked `0`.

Return the number of unique paths from the top-left to the bottom-right corner.

**Constraints:**
- `1 <= m, n <= 100`
- `obstacleGrid[i][j]` is `0` or `1`

### Example
```
Input:  obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: The obstacle in the middle forces the robot to go around.
  Path 1: Right → Right → Down → Down
  Path 2: Down → Down → Right → Right
```

```
Input:  obstacleGrid = [[0,1],[0,0]]
Output: 1
```

```
Input:  obstacleGrid = [[1,0]]
Output: 0
Explanation: Start cell is blocked — no path exists.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

This is Unique Paths with one added rule: cells marked `1` are walls. Any path
that passes through a wall is invalid. We need to count only the paths that
stay entirely on `0` cells.

### Step 2 — Identify the constraint that matters

The key difference from Unique Paths is that obstacles break the "first row and
column are all 1s" assumption. If an obstacle appears anywhere in the first row,
every cell to its right becomes unreachable (0 paths). Same for the first column.

Any cell that is itself an obstacle must be set to 0 paths — the robot can never
land there regardless of how it arrived.

### Step 3 — Think about data structures

The single-row space-optimized approach from Unique Paths extends naturally:
- If a cell is an obstacle, set `array[j] = 0`
- Otherwise, add paths from the left: `array[j] += array[j-1]`
- The value already in `array[j]` represents paths from above (inherited from
  the previous row iteration)

No second array is needed.

### Step 4 — Build the intuition

Imagine the grid is a city with some streets blocked by fallen trees. You're
sweeping row by row, maintaining a running count of "how many ways can I reach
this intersection?" Whenever you hit a blocked cell, you erase its count to 0.
That zero then propagates — any cell that could only be reached through the
blocked cell also gets 0.

---

## Approaches

### Approach 1 — Full Grid (Tabulation)

**Intuition:** Fill an `m × n` grid where each cell holds the number of valid
paths to reach it. Obstacle cells are always 0.

**Steps:**
1. If `obstacleGrid[0][0] == 1`, return 0 immediately
2. Create a grid of zeros; set `grid[0][0] = 1`
3. Fill row 0: `grid[0][j] = grid[0][j-1]` if no obstacle, else 0
4. Fill column 0: `grid[i][0] = grid[i-1][0]` if no obstacle, else 0
5. Fill the rest: if obstacle → 0, else `grid[i][j] = grid[i-1][j] + grid[i][j-1]`
6. Return `grid[m-1][n-1]`

**Illustration:**
```
obstacleGrid:        dp grid:
0  0  0              1  1  1
0  1  0    →         1  0  1
0  0  0              1  1  2

Answer: dp[2][2] = 2 ✓
```

**Complexity:**
- Time: O(m × n)
- Space: O(m × n)

**Code:**
```python
def unique_paths_with_obstacles_grid(obstacleGrid: list[list[int]]) -> int:
    if obstacleGrid[0][0] == 1:
        return 0
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] if obstacleGrid[0][j] == 0 else 0
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] if obstacleGrid[i][0] == 0 else 0
    for i in range(1, m):
        for j in range(1, n):
            if obstacleGrid[i][j] == 1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

---

### Approach 2 — Optimal (Single Array)

**Intuition:** Reuse a single 1D array updated in place, row by row. An
obstacle zeroes out its cell; that zero naturally blocks any path that would
have passed through it.

**Steps:**
1. If `obstacleGrid[0][0] == 1`, return 0
2. Initialize `array = [0] * n`, set `array[0] = 1`
3. For each row `i` and column `j`:
   - If obstacle: `array[j] = 0`
   - Else if `j > 0`: `array[j] += array[j-1]`
4. Return `array[-1]`

**Illustration:**
```
obstacleGrid:
0  0  0
0  1  0
0  0  0

Start:   array = [1, 0, 0]

Row 0:   j=1: array[1] += array[0] → [1, 1, 0]
         j=2: array[2] += array[1] → [1, 1, 1]

Row 1:   j=0: skip (first column)
         j=1: obstacle → array[1] = 0  → [1, 0, 1]
         j=2: array[2] += array[1] → [1, 0, 1]

Row 2:   j=1: array[1] += array[0] → [1, 1, 1]
         j=2: array[2] += array[1] → [1, 1, 2]

Answer: array[-1] = 2 ✓
```

**Complexity:**
- Time: O(m × n)
- Space: O(n) — one row only

**Code:**
```python
def unique_paths_with_obstacles(obstacleGrid: list[list[int]]) -> int:
    if obstacleGrid[0][0] == 1:
        return 0
    rows, cols = len(obstacleGrid), len(obstacleGrid[0])
    array = [0] * cols
    array[0] = 1
    for i in range(rows):
        for j in range(cols):
            if obstacleGrid[i][j] == 1:
                array[j] = 0
            elif j > 0:
                array[j] += array[j - 1]
    return array[cols - 1]
```

---

## Solution Breakdown — Step by Step

```python
def unique_paths_with_obstacles(obstacleGrid: list[list[int]]) -> int:
    if obstacleGrid[0][0] == 1:
        return 0
    rows, cols = len(obstacleGrid), len(obstacleGrid[0])
    array = [0] * cols
    array[0] = 1
    for i in range(rows):
        for j in range(cols):
            if obstacleGrid[i][j] == 1:
                array[j] = 0
            elif j > 0:
                array[j] += array[j - 1]
    return array[cols - 1]
```

**Line by line:**

`if obstacleGrid[0][0] == 1: return 0`
- If the start cell is blocked, no path can ever begin — return 0 immediately

`array = [0] * cols; array[0] = 1`
- Initialize all cells to 0 (no paths yet)
- Set the start cell to 1 — there is exactly one way to be at the start

`for i in range(rows): for j in range(cols):`
- Process every cell in row-major order (left to right, top to bottom)
- This ensures `array[j]` always holds the correct count from the row above before we update it

`if obstacleGrid[i][j] == 1: array[j] = 0`
- Obstacle: zero out this cell — no path can land here
- This zero will propagate: any cell that could only be reached through this one will also get 0

`elif j > 0: array[j] += array[j - 1]`
- Not an obstacle and not the first column: add paths from the left
- `array[j]` already holds paths from above (inherited from the previous row)
- `array[j-1]` holds paths from the left (already updated this row)
- We skip `j == 0` because there is nothing to the left; the value from above is already correct

`return array[cols - 1]`
- After processing all rows, the last element holds the path count for the bottom-right cell

---

## Quick Summary

| Solution | Time | Space |
|---|---|---|
| Full Grid | O(m × n) | O(m × n) |
| Single Array (optimal) | O(m × n) | **O(n)** |

---

## Common Mistakes

**1. Not handling the obstacle at the start cell**
```python
array[0] = 1  # WRONG if obstacleGrid[0][0] == 1
```
Always check the start cell first. If it is blocked, return 0 before any setup.

**2. Not zeroing out obstacle cells in the first row or column**
```python
# WRONG — initializes first row to all 1s regardless of obstacles
for j in range(n):
    array[j] = 1
```
In Unique Paths (no obstacles) this is fine. Here, an obstacle in the first row
makes all cells to its right unreachable. The single-array approach handles this
automatically because `array[j]` starts at 0 and only gets incremented if there
is no obstacle.

**3. Using `array[j] = array[j] + array[j-1]` instead of `+=`**
Not wrong, but the `+=` form makes it clear we are accumulating on top of the
existing value (paths from above), not replacing it.

**4. Forgetting the `elif j > 0` guard**
```python
array[j] += array[j - 1]  # WRONG when j == 0 — reads array[-1] (last element)
```
Always guard with `j > 0` to avoid wrapping around to the last element.

---

## Pattern Recognition

> Use the **obstacle-aware grid DP** pattern when you see:
> - "Count paths in a grid where some cells are blocked"
> - "Grid traversal with right/down movement and walls"
> - Any Unique Paths variant with constraints on which cells are reachable

**Similar problems:**
- **Unique Paths** — same grid DP without obstacles
- **Minimum Path Sum** — same traversal, minimize sum instead of counting paths
- **Dungeon Game** — grid DP with health constraints
- **Cherry Pickup** — two-robot grid DP with shared obstacles

---

## Real World Use Cases

### 1. Robot path planning with static obstacles
Warehouse robots navigating around fixed shelving units use obstacle-aware
grid DP to count valid routes and select the one with the best properties
(shortest, most redundant, etc.). The single-array approach is memory-efficient
for large warehouse floor plans.

### 2. Network routing around failed links
In a grid-topology data center network, failed switches act as obstacles.
Counting valid paths between two servers helps network engineers assess
redundancy and reroute traffic. The DP runs in O(m × n) time over the
topology grid.

### 3. Game map pathfinding preprocessing
Strategy games precompute path counts for every cell pair on a grid map
(with walls) to support AI decision-making. The obstacle-aware DP is the
building block for these precomputation passes.

---

## Key Takeaways

- Obstacles are handled by zeroing out their cell — the zero propagates naturally to all cells that depended on it
- The single-array approach from Unique Paths extends directly: just add an obstacle check before the `+=`
- Always check the start cell first — a blocked start means zero paths regardless of the rest of the grid
- The `elif j > 0` guard prevents reading `array[-1]` when processing the first column
- This problem is Unique Paths with one extra line of logic per cell

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #63](https://leetcode.com/problems/unique-paths-ii/) | Unique Paths II | Medium |

> This problem is part of the **NeetCode 150** interview prep list.
