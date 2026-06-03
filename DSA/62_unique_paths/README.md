# 62. Unique Paths

**LeetCode:** [Problem #62](https://leetcode.com/problems/unique-paths/)
**Difficulty:** Medium
**Topics:** `Dynamic Programming` `Math`

---

## Problem Statement

A robot is located at the top-left corner of an `m x n` grid. The robot can
only move either **right** or **down** at each step. The robot is trying to
reach the bottom-right corner.

How many possible unique paths are there?

**Constraints:**
- `1 <= m, n <= 100`

### Example
```
Input:  m = 3, n = 7
Output: 28
```

```
Input:  m = 3, n = 2
Output: 3
Explanation: Three paths:
  Right → Down → Down
  Down  → Right → Down
  Down  → Down  → Right
```

```
Input:  m = 1, n = 1
Output: 1
Explanation: Already at the destination — one trivial path.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to count all distinct sequences of right and down moves that take the
robot from the top-left to the bottom-right. The robot must make exactly
`(m-1)` down moves and `(n-1)` right moves in some order — the question is
how many orderings exist.

### Step 2 — Identify the constraint that matters

The robot can only move right or down. This means the number of ways to reach
any cell `(i, j)` is exactly the sum of the ways to reach the cell above it
`(i-1, j)` and the cell to its left `(i, j-1)`. There is no other way to
arrive at `(i, j)`.

This overlapping subproblem structure is the hallmark of dynamic programming.

### Step 3 — Think about data structures

Two approaches:
1. **Full grid** — fill an `m × n` table, O(m × n) space
2. **Single row** — reuse one row in place, O(n) space

The single-row approach is optimal because when filling row `i`, we only ever
look at the row above (already in the array) and the cell to the left (already
updated this row).

### Step 4 — Build the intuition

Think of the grid as a city map. Each intersection shows how many distinct
routes lead from the starting corner to that point. The first row and first
column each have exactly 1 route (no choices — only one direction is possible).
Every other intersection is the sum of the intersection above and the one to
the left. Fill the map top-to-bottom, left-to-right, and read the answer from
the bottom-right corner.

---

## Approaches

### Approach 1 — Full Grid (Tabulation)

**Intuition:** Fill an `m × n` grid where each cell holds the number of unique
paths to reach it. The answer is the bottom-right cell.

**Steps:**
1. Create an `m × n` grid initialized to 0
2. Set all cells in row 0 to 1 (only one way — keep going right)
3. Set all cells in column 0 to 1 (only one way — keep going down)
4. For every other cell: `grid[i][j] = grid[i-1][j] + grid[i][j-1]`
5. Return `grid[m-1][n-1]`

**Illustration:**
```
m=3, n=7

After initializing row 0 and column 0:
[  1   1   1   1   1   1   1 ]
[  1   0   0   0   0   0   0 ]
[  1   0   0   0   0   0   0 ]

After filling:
[  1   1   1   1   1   1   1 ]
[  1   2   3   4   5   6   7 ]
[  1   3   6  10  15  21  28 ]

Answer: grid[2][6] = 28 ✓
```

**Complexity:**
- Time: O(m × n) — every cell visited once
- Space: O(m × n) — stores the entire grid

**Code:**
```python
def unique_paths_grid(m: int, n: int) -> int:
    grid = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            grid[i][j] = grid[i - 1][j] + grid[i][j - 1]
    return grid[m - 1][n - 1]
```

---

### Approach 2 — Optimal (Single Row)

**Intuition:** When filling row `i`, `row[j]` already holds the value from
row `i-1` (the cell above). Adding `row[j-1]` (already updated this row)
gives the correct value for `(i, j)`. We never need older rows.

**Steps:**
1. Initialize `row = [1] * n` (represents row 0 — all ones)
2. For each row from 1 to `m-1`:
   - For each column from 1 to `n-1`: `row[j] += row[j-1]`
3. Return `row[-1]`

**Illustration:**
```
m=3, n=7

Start:       [1, 1, 1, 1, 1, 1, 1]   ← row 0
After row 1: [1, 2, 3, 4, 5, 6, 7]
After row 2: [1, 3, 6, 10, 15, 21, 28]

Answer: row[-1] = 28 ✓
```

**Complexity:**
- Time: O(m × n) — same number of operations
- Space: O(n) — only one row stored at a time

**Code:**
```python
def unique_paths_optimized(m: int, n: int) -> int:
    row = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]
```

---

## Solution Breakdown — Step by Step

```python
def unique_paths_optimized(m: int, n: int) -> int:
    row = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]
```

**Line by line:**

`row = [1] * n`
- Represents the first row of the grid — every cell in row 0 has exactly 1 path
- Also serves as the running state that gets updated in place for each subsequent row

`for i in range(1, m):`
- We skip row 0 (already initialized) and process rows 1 through `m-1`
- The outer loop variable `i` is not used inside — we only need the count of rows

`for j in range(1, n):`
- We skip column 0 (always 1, never changes) and process columns 1 through `n-1`

`row[j] += row[j - 1]`
- `row[j]` currently holds the value from the row above (inherited from the previous iteration of the outer loop)
- `row[j-1]` holds the already-updated value to the left in the current row
- Adding them gives the correct path count for cell `(i, j)`
- The in-place update means we never need a second array

`return row[-1]`
- After processing all rows, `row[-1]` holds the path count for the bottom-right cell

---

## Quick Summary

| Solution | Time | Space |
|---|---|---|
| Full Grid | O(m × n) | O(m × n) |
| Single Row (optimal) | O(m × n) | **O(n)** |

---

## Common Mistakes

**1. Initializing the grid to 0 and forgetting to set the first row and column**
```python
grid = [[0] * n for _ in range(m)]
# Forgetting: grid[0] = [1]*n and grid[i][0] = 1 for all i
# Results in all zeros except the start cell
```
Either initialize the entire grid to 1 and skip row/column 0 in the loop, or
explicitly fill the borders before the main loop.

**2. Starting the inner loop at `j = 0` in the single-row approach**
```python
for j in range(0, n):   # WRONG — row[j] += row[j-1] when j=0 reads row[-1]
    row[j] += row[j - 1]
```
Column 0 is always 1 and should never be updated. Start the inner loop at `j = 1`.

**3. Swapping `m` and `n`**
The grid has `m` rows and `n` columns. `row` has length `n`. The outer loop
runs `m-1` times. Swapping them gives the right answer only when `m == n`.

---

## Pattern Recognition

### How to Recognize
- Problem involves counting paths in a grid from top-left to bottom-right
- Movement is restricted to two directions only (right and down)
- Each cell's answer depends only on the cell above and the cell to the left

### How to Identify
- Does `paths(i, j) = paths(i-1, j) + paths(i, j-1)` capture the recurrence?
- Can you reduce space from O(m × n) to O(n) by reusing a single row?

### How to Remember
> **Mental model:** Each intersection = roads from above + roads from the left

**Similar problems:**
- **Unique Paths II** — same grid DP with obstacles blocking certain cells
- **Minimum Path Sum** — same traversal, minimize sum instead of counting paths
- **Triangle** — 2D DP on a triangular grid
- **Edit Distance** — 2D DP where each cell depends on three neighbors

---

## Real World Use Cases

### 1. Route enumeration in warehouse automation
Automated guided vehicles (AGVs) in warehouses move on grid-based floor plans
with right/down movement constraints. Counting unique paths between two
locations helps engineers assess routing flexibility and plan redundancy.
The single-row DP runs in O(n) space regardless of warehouse size.

### 2. Combinatorial test case generation
In software testing, generating all distinct sequences of two types of actions
(e.g., "add item" and "remove item") up to a fixed total count uses the same
path-counting logic. The grid represents the state space, and each cell's
value is the number of test sequences reaching that state.

### 3. Probability calculation in stochastic processes
In a Markov chain where a system can transition right or down at each step,
the number of paths to a given state is proportional to the probability of
reaching it. The grid DP computes these counts efficiently for large state spaces.

---

## Key Takeaways

- The number of paths to any cell is the sum of paths from above and from the left
- The first row and first column always have exactly 1 path — initialize them to 1
- The single-row optimization works because we only ever look at the current row and the row above
- In-place update (`row[j] += row[j-1]`) is safe because we process left to right
- This is the foundation for all 2D grid DP problems

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #62](https://leetcode.com/problems/unique-paths/) | Unique Paths | Medium |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
