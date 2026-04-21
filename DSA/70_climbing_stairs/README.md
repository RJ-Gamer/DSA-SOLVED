# 70. Climbing Stairs

**LeetCode:** [Problem #70](https://leetcode.com/problems/climbing-stairs/)
**Difficulty:** Easy
**Topics:** `Dynamic Programming`

---

## Problem Statement

You are climbing a staircase with `n` steps. Each time you can climb either
**1 step** or **2 steps**. In how many distinct ways can you reach the top?

**Constraints:**
- `1 <= n <= 45`

### Example
```
Input:  n = 2
Output: 2
Explanation: Two ways — [1+1] or [2]
```

```
Input:  n = 3
Output: 3
Explanation: Three ways — [1+1+1], [1+2], [2+1]
```

```
Input:  n = 5
Output: 8
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to count the number of distinct sequences of 1-step and 2-step moves
that sum to exactly `n`. Order matters — `[1, 2]` and `[2, 1]` are different paths.

### Step 2 — Identify the constraint that matters

To reach step `n`, you must have come from either step `n-1` (took 1 step) or
step `n-2` (took 2 steps). There is no other way. So:

```
ways(n) = ways(n-1) + ways(n-2)
```

This is exactly the **Fibonacci recurrence**. The number of ways to climb `n`
stairs equals the (n+1)th Fibonacci number.

### Step 3 — Think about data structures

The naive recursive solution recomputes the same subproblems exponentially.
Three progressively better approaches exist:

1. **Memoization** — cache results top-down, O(n) time and space
2. **Tabulation** — build bottom-up with an array, O(n) time and space
3. **Two variables** — only keep the last two values, O(n) time and O(1) space

### Step 4 — Build the intuition

Think of filling in an answer sheet from question 1 to question `n`. You know
the answers to questions 1 and 2 by heart. For every subsequent question, you
look at the previous two answers and add them up. You never need to go further
back than two steps — so you only need to remember two numbers at a time.

---

## Approaches

### Approach 1 — Brute Force (Pure Recursion)

**Intuition:** At each step, branch into two recursive calls — one for taking
1 step and one for taking 2 steps — until the base cases are reached.

**Steps:**
1. If `n == 1`, return 1
2. If `n == 2`, return 2
3. Otherwise return `climb(n-1) + climb(n-2)`

**Illustration:**
```
f(5)
├── f(4)
│   ├── f(3)
│   │   ├── f(2) = 2
│   │   └── f(1) = 1
│   └── f(2) = 2
└── f(3)          ← computed again!
    ├── f(2) = 2
    └── f(1) = 1
```
`f(3)` is computed twice, `f(2)` three times. Exponential blowup.

**Complexity:**
- Time: O(2^n) — call tree doubles at every level
- Space: O(n) — recursion stack depth

**Code:**
```python
def climbStairsRecursive(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climbStairsRecursive(n - 1) + climbStairsRecursive(n - 2)
```

---

### Approach 2 — Memoization (Top-Down DP)

**Intuition:** Same recursion, but cache each result the first time it is
computed so it is never recomputed.

**Steps:**
1. Maintain a `memo` dictionary outside the recursive calls
2. Before computing, check if the result is already cached
3. After computing, store the result before returning

**Complexity:**
- Time: O(n) — each value computed exactly once
- Space: O(n) — memo dictionary plus recursion stack

**Code:**
```python
def climbStairsMemoized(n: int, memo: dict = {}) -> int:
    if n in memo:
        return memo[n]
    if n <= 2:
        return n
    memo[n] = climbStairsMemoized(n - 1, memo) + climbStairsMemoized(n - 2, memo)
    return memo[n]
```

---

### Approach 3 — Tabulation (Bottom-Up DP)

**Intuition:** Build the answer from the ground up, filling a `ways` array
from index 1 to `n`.

**Steps:**
1. Create `ways` array of size `n + 1`
2. Set `ways[1] = 1`, `ways[2] = 2`
3. For each `i` from 3 to `n`: `ways[i] = ways[i-1] + ways[i-2]`
4. Return `ways[n]`

**Illustration:**
```
n = 5

ways[1] = 1
ways[2] = 2
ways[3] = 2 + 1 = 3
ways[4] = 3 + 2 = 5
ways[5] = 5 + 3 = 8  ✓
```

**Complexity:**
- Time: O(n)
- Space: O(n) — stores the full `ways` array

**Code:**
```python
def climbStairsTabulated(n: int) -> int:
    if n <= 2:
        return n
    ways = [0] * (n + 1)
    ways[1], ways[2] = 1, 2
    for i in range(3, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    return ways[n]
```

---

### Approach 4 — Optimal (Two Variables)

**Intuition:** We only ever look at the last two values, so we can replace the
entire array with two variables and slide them forward.

**Steps:**
1. Initialize `t1 = 1` (ways to reach step 1), `t2 = 2` (ways to reach step 2)
2. For each step from 3 to `n`: `t1, t2 = t2, t1 + t2`
3. Return `t2`

**Illustration:**
```
n = 5

Start:  t1=1, t2=2
i=3:    t1=2, t2=3
i=4:    t1=3, t2=5
i=5:    t1=5, t2=8  → return 8 ✓
```

**Complexity:**
- Time: O(n)
- Space: O(1) — only two variables

**Code:**
```python
def climbStairsOptimized(n: int) -> int:
    if n <= 2:
        return n
    t1, t2 = 1, 2
    for _ in range(3, n + 1):
        t1, t2 = t2, t1 + t2
    return t2
```

---

## Solution Breakdown — Step by Step

```python
def climbStairsOptimized(n: int) -> int:
    if n <= 2:
        return n
    t1, t2 = 1, 2
    for _ in range(3, n + 1):
        t1, t2 = t2, t1 + t2
    return t2
```

**Line by line:**

`if n <= 2: return n`
- Base cases: 1 step has 1 way, 2 steps have 2 ways
- Handles edge inputs before the loop starts

`t1, t2 = 1, 2`
- `t1` represents `ways(n-2)`, `t2` represents `ways(n-1)`
- These are the two most recent values we need to compute the next one

`for _ in range(3, n + 1):`
- We already know steps 1 and 2, so we start computing from step 3
- The loop variable is unused — we only care about the count of iterations

`t1, t2 = t2, t1 + t2`
- Python evaluates the right side first, so `t1 + t2` uses the old values
- Slides the window forward: old `t2` becomes new `t1`, new sum becomes new `t2`
- No temporary variable needed — simultaneous assignment handles it cleanly

`return t2`
- After the loop, `t2` holds `ways(n)`

---

## Quick Summary

| Solution | Approach | Time | Space |
|---|---|---|---|
| Pure Recursion | Top-down, no cache | O(2^n) | O(n) |
| Memoization | Top-down, with cache | O(n) | O(n) |
| Tabulation | Bottom-up, full array | O(n) | O(n) |
| Two Variables | Bottom-up, two vars | O(n) | **O(1)** |

---

## Common Mistakes

**1. Initializing base cases incorrectly**
```python
# WRONG — ways[0] = 0 causes wrong answers for n >= 3
ways[0] = 0
ways[1] = 1
# ways[2] = ways[1] + ways[0] = 1, but correct answer is 2
```
Always set `ways[1] = 1` and `ways[2] = 2` explicitly.

**2. Creating a memo dict inside the recursive function**
```python
def climb(n):
    memo = {}  # WRONG — reset on every call, never actually caches
    ...
```
The memo must persist across calls — define it outside or pass it as a parameter.

**3. Returning `t1` instead of `t2` at the end**
```python
t1, t2 = t2, t1 + t2
return t1  # WRONG — t1 is now the old t2, not the answer
```
After the swap, `t2` holds the current step's answer. Always return `t2`.

---

## Pattern Recognition

> Use the **Fibonacci / two-variable DP** pattern when you see:
> - "How many ways to reach position n with steps of size 1 or 2?"
> - A recurrence where `f(n)` depends only on `f(n-1)` and `f(n-2)`
> - Any problem reducible to counting paths with fixed step sizes

**Similar problems:**
- **Min Cost Climbing Stairs** — same recurrence, but minimize cost instead of counting paths
- **House Robber** — same two-variable sliding window, different recurrence
- **Fibonacci Number** — this problem is literally Fibonacci shifted by one
- **Decode Ways** — counting paths with variable step sizes, same DP structure

---

## Real World Use Cases

### 1. Step sequencing in robotics motion planning
A robot navigating a terrain with fixed step sizes uses the same counting
logic to enumerate all valid movement sequences between two positions. The
number of valid paths grows as a Fibonacci-like sequence, and the two-variable
approach lets the planner compute path counts in O(1) space even for large
distances.

### 2. Combinatorial pricing in e-commerce bundles
A pricing engine that allows customers to apply discount coupons in increments
of 1 or 2 units needs to count the number of distinct ways a customer can
reach a target discount level. This is structurally identical to climbing
stairs — the same recurrence applies.

### 3. Network packet routing with hop constraints
In network routing, counting the number of distinct paths between two nodes
where each hop covers exactly 1 or 2 links uses the Fibonacci recurrence.
Routers use this to estimate path diversity for redundancy planning.

---

## Key Takeaways

- The recurrence `ways(n) = ways(n-1) + ways(n-2)` is the Fibonacci sequence
- Pure recursion is O(2^n) — always cache or go bottom-up
- The two-variable approach reduces O(n) space to O(1) by keeping only the last two values
- Python's simultaneous assignment (`t1, t2 = t2, t1 + t2`) eliminates the need for a temp variable
- This problem is the gateway to understanding all 1D DP problems

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #70](https://leetcode.com/problems/climbing-stairs/) | Climbing Stairs | Easy |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
