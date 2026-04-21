# 746. Min Cost Climbing Stairs

**LeetCode:** [Problem #746](https://leetcode.com/problems/min-cost-climbing-stairs/)
**Difficulty:** Easy
**Topics:** `Dynamic Programming`

---

## Problem Statement

You are given an integer array `cost` where `cost[i]` is the cost of the `i`th
step on a staircase. Once you pay the cost, you can climb either **one or two
steps**. You can start from step index `0` or step index `1`.

Return the minimum cost to reach the top of the staircase (past the last step).

**Constraints:**
- `2 <= cost.length <= 1000`
- `0 <= cost[i] <= 999`

### Example
```
Input:  cost = [10, 15, 20]
Output: 15
Explanation: Start at index 1, pay 15, jump 2 steps to the top.
```

```
Input:  cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
Output: 6
Explanation: Pay 1 at steps 0, 2, 3, 4, 6, 7 — total 6.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to find the cheapest sequence of steps to get past the last index.
We can start at index 0 or 1 (free choice), and from any step we can jump
1 or 2 steps forward after paying that step's cost.

### Step 2 — Identify the constraint that matters

The cost to reach step `i` depends on the cheapest way to reach either
`i-1` or `i-2`. This is a classic overlapping subproblem — the same
sub-costs are reused many times if computed naively.

The recurrence is:
```
dp[i] = cost[i] + min(dp[i-1], dp[i-2])
```

The final answer is `min(dp[-1], dp[-2])` because from either of the last
two steps you can jump directly to the top.

### Step 3 — Think about data structures

Two approaches:
1. **Tabulation** — fill a `dp` array of the same length as `cost`, O(n) space
2. **Two variables** — only keep the last two `dp` values, O(1) space

The two-variable approach is optimal and mirrors the space optimization in
Climbing Stairs.

### Step 4 — Build the intuition

Imagine each step has a toll booth. You want to reach the exit (past the last
step) paying as little as possible. At each booth, you look back at the two
previous booths and choose the cheaper path to arrive from. The receipt for
each step = its own toll + the cheaper of the two paths leading to it.

---

## Approaches

### Approach 1 — Tabulation (Full Array)

**Intuition:** Build a `dp` array where `dp[i]` = the minimum total cost to
stand on step `i`. Fill it left to right using the recurrence.

**Steps:**
1. Set `dp[0] = cost[0]`, `dp[1] = cost[1]`
2. For each `i` from 2 to `len(cost) - 1`: `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`
3. Return `min(dp[-1], dp[-2])`

**Illustration:**
```
cost = [10, 15, 20]

dp[0] = 10
dp[1] = 15
dp[2] = 20 + min(15, 10) = 30

Answer: min(dp[-1], dp[-2]) = min(30, 15) = 15 ✓
```

```
cost = [10, 15, 20, 4, 6, 8]

dp[0] = 10
dp[1] = 15
dp[2] = 20 + min(15, 10) = 30
dp[3] =  4 + min(30, 15) = 19
dp[4] =  6 + min(19, 30) = 25
dp[5] =  8 + min(25, 19) = 27

Answer: min(27, 25) = 25 ✓
```

**Complexity:**
- Time: O(n)
- Space: O(n) — stores the full `dp` array

**Code:**
```python
def min_cost_tabulated(cost: list[int]) -> int:
    n = len(cost)
    dp = [0] * n
    dp[0], dp[1] = cost[0], cost[1]
    for i in range(2, n):
        dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])
    return min(dp[-1], dp[-2])
```

---

### Approach 2 — Optimal (Two Variables)

**Intuition:** We only ever look at the last two `dp` values, so we can
replace the array with two variables and slide them forward.

**Steps:**
1. Initialize `t0 = cost[0]`, `t1 = cost[1]`
2. For each `i` from 2 to `len(cost) - 1`: `t0, t1 = t1, cost[i] + min(t0, t1)`
3. Return `min(t0, t1)`

**Illustration:**
```
cost = [10, 15, 20, 4, 6, 8]

Start:  t0=10, t1=15
i=2:    t0=15, t1=20+min(10,15)=30
i=3:    t0=30, t1= 4+min(15,30)=19
i=4:    t0=19, t1= 6+min(30,19)=25
i=5:    t0=25, t1= 8+min(19,25)=27

Answer: min(25, 27) = 25 ✓
```

**Complexity:**
- Time: O(n)
- Space: O(1) — only two variables

**Code:**
```python
def min_cost_optimized(cost: list[int]) -> int:
    t0, t1 = cost[0], cost[1]
    for i in range(2, len(cost)):
        t0, t1 = t1, cost[i] + min(t0, t1)
    return min(t0, t1)
```

---

## Solution Breakdown — Step by Step

```python
def min_cost_optimized(cost: list[int]) -> int:
    t0, t1 = cost[0], cost[1]
    for i in range(2, len(cost)):
        t0, t1 = t1, cost[i] + min(t0, t1)
    return min(t0, t1)
```

**Line by line:**

`t0, t1 = cost[0], cost[1]`
- Base cases: the minimum cost to stand on step 0 is `cost[0]`, on step 1 is `cost[1]`
- No cheaper path exists to either of these — they are the starting options

`for i in range(2, len(cost)):`
- We already know the cost for steps 0 and 1, so we start computing from step 2

`t0, t1 = t1, cost[i] + min(t0, t1)`
- Python evaluates the right side first — `min(t0, t1)` uses the old values
- `cost[i] + min(t0, t1)` = this step's toll + the cheaper of the two paths leading here
- After the assignment: `t0` holds the old `t1`, `t1` holds the new minimum cost for step `i`
- The window slides forward by one step

`return min(t0, t1)`
- After the loop, `t0 = dp[-2]` and `t1 = dp[-1]`
- From either of the last two steps you can jump directly to the top
- We return whichever is cheaper

---

## Quick Summary

| Solution | Time | Space |
|---|---|---|
| Tabulation (full array) | O(n) | O(n) |
| Two Variables (optimal) | O(n) | **O(1)** |

---

## Common Mistakes

**1. Returning only `dp[-1]` instead of `min(dp[-1], dp[-2])`**
```python
return dp[-1]  # WRONG — misses the case where jumping from second-to-last is cheaper
```
The top is reachable from either of the last two steps. Always return the minimum of both.

**2. Confusing this with Climbing Stairs**
Climbing Stairs counts paths. This problem minimizes cost. The recurrence looks
similar but the semantics are different — here we add `cost[i]`, there we add 1.

**3. Off-by-one in the loop range**
```python
for i in range(2, len(cost) + 1):  # WRONG — index out of bounds
```
The loop should run from 2 to `len(cost) - 1` inclusive, i.e. `range(2, len(cost))`.

**4. Using `if/else` instead of simultaneous assignment**
```python
temp = t1
t1 = cost[i] + min(t0, t1)
t0 = temp  # correct but verbose
```
Python's simultaneous assignment `t0, t1 = t1, cost[i] + min(t0, t1)` is cleaner
and eliminates the need for a temporary variable.

---

## Pattern Recognition

> Use the **two-variable sliding DP** pattern when you see:
> - "Minimum/maximum cost to reach the end with 1 or 2 step jumps"
> - A recurrence where `dp[i]` depends only on `dp[i-1]` and `dp[i-2]`
> - Any 1D DP where only the last two states are needed

**Similar problems:**
- **Climbing Stairs** — same recurrence, count paths instead of minimizing cost
- **House Robber** — same two-variable pattern, different recurrence (`max` instead of `min`)
- **Jump Game** — greedy variant of path-finding on an array
- **Decode Ways** — 1D DP with variable step sizes

---

## Real World Use Cases

### 1. Minimum-cost routing in toll road networks
A navigation system computing the cheapest route through a sequence of toll
booths uses the same recurrence: the cost to reach each checkpoint equals its
toll plus the minimum cost of the two cheapest ways to arrive. This scales to
thousands of checkpoints in O(n) time and O(1) space.

### 2. Energy-optimal step scheduling in robotics
A robot climbing a ramp with variable energy costs per step uses this exact
DP to plan the minimum-energy sequence of 1-step and 2-step moves. The
two-variable approach is critical for embedded systems with limited memory.

### 3. Minimum-penalty task scheduling
A job scheduler where each task has a penalty cost and tasks can be skipped
in groups of 1 or 2 uses the same structure to find the minimum total penalty
path through a task queue.

---

## Key Takeaways

- The recurrence `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` captures the entire problem
- The answer is `min(dp[-1], dp[-2])` — not just `dp[-1]` — because the top is reachable from either of the last two steps
- Two variables replace the full array because only the last two states are ever needed
- Python's simultaneous assignment evaluates the right side before any assignment, making the sliding window update safe without a temp variable
- This is the cost-minimization counterpart to Climbing Stairs

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #746](https://leetcode.com/problems/min-cost-climbing-stairs/) | Min Cost Climbing Stairs | Easy |

> This problem is part of the **NeetCode 150** interview prep list.
