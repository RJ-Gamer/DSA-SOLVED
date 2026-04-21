# 53. Maximum Subarray

**LeetCode:** [Problem #53](https://leetcode.com/problems/maximum-subarray/)  
**Difficulty:** Medium  
**Topics:** `Array` `Dynamic Programming`

---

## Problem Statement

Given an integer array `nums`, find the **contiguous subarray** (containing at
least one number) which has the **largest sum** and return its sum.

A subarray is a contiguous portion of an array.

**Constraints:**
- `1 <= nums.length <= 10⁵`
- `-10⁴ <= nums[i] <= 10⁴`

### Example
```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: [4, -1, 2, 1] has the largest sum = 6
```

```
Input:  nums = [1]
Output: 1
Explanation: only one element, subarray is [1]
```

```
Input:  nums = [5, 4, -1, 7, 8]
Output: 23
Explanation: [5, 4, -1, 7, 8] — the entire array is the best subarray
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to find a contiguous slice of the array whose elements sum to the largest
possible value. The slice must include at least one element (we can't return 0 for
an empty slice). The array can contain negative numbers, which is what makes this
non-trivial.

### Step 2 — Identify the constraint that matters

If all numbers were positive, the answer would always be the entire array. If all
were negative, the answer would be the single least-negative element.

The hard case is mixed arrays. A negative number mid-subarray "drags down" the
sum — but it might be worth keeping if the numbers ahead are large enough to
compensate. We need a rule to decide: **when is it worth extending the current
subarray, and when should we start fresh?**

### Step 3 — Think about data structures

We don't need a complex data structure here. We need two running values:

1. **`current_sum`** — the best subarray sum *ending at the current position*
2. **`max_sum`** — the best subarray sum seen *anywhere so far*

At each position, we make a local decision: extend the existing subarray, or
start a new one here?

### Step 4 — Build the intuition

The key insight is **Kadane's observation**:

> At each position, the best subarray ending here is either:
> - Just the current element alone (start fresh), OR
> - The current element plus the best subarray ending at the previous position
>
> Take whichever is larger.

Formally: `current_sum = max(num, current_sum + num)`

Why does this work? If `current_sum` is already negative, adding it to `num`
makes `num` smaller than it would be alone. So it's always better to cut the
dead weight and start over with just `num`.

Think of it like this: you're collecting money along a road. At each stop, you
decide — keep what you've collected so far and add what's here, or throw it all
away and only keep what's at this stop. You always choose the option that gives
you more money.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Try every possible subarray by exhausting all start and end index
combinations, tracking the maximum sum found.

**Steps:**
1. For each starting index `i`, reset a running `current_sum` to 0
2. For each ending index `j >= i`, extend the subarray by adding `nums[j]`
3. Update `max_sum` if `current_sum` exceeds it
4. Return `max_sum`

**Illustration:**
```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Starting at i=0 (num=-2):
  j=0: sum=-2      max=-2
  j=1: sum=-1      max=-1
  j=2: sum=-4      max=-1
  j=3: sum=0       max=0
  j=4: sum=-1      max=0
  j=5: sum=1       max=1
  j=6: sum=2       max=2
  ...

Starting at i=3 (num=4):
  j=3: sum=4       max=4
  j=4: sum=3       max=4
  j=5: sum=5       max=5
  j=6: sum=6       max=6  ← [4, -1, 2, 1]
  j=7: sum=1       max=6
  j=8: sum=5       max=6

Final max_sum = 6 ✓
```

**Complexity:**
- Time: O(n²) — two nested loops over n elements
- Space: O(1) — only two variables maintained

**Code:**
```python
def max_sub_array_brute_force(nums: list[int]) -> int:
    max_sum = float("-inf")
    for i in range(len(nums)):
        current_sum = 0
        for j in range(i, len(nums)):
            current_sum += nums[j]
            max_sum = max(max_sum, current_sum)
    return max_sum
```

---

### Approach 2 — Optimal (Kadane's Algorithm)

**Intuition:** At each element, decide whether to extend the current subarray or
start a new one — whichever yields the larger value — while tracking the global maximum.

**Steps:**
1. Initialize `max_sum = -∞` (handles all-negative arrays) and `current_sum = 0`
2. For each number `num`:
   - `current_sum = max(num, current_sum + num)` — extend or restart
   - `max_sum = max(max_sum, current_sum)` — update global best
3. Return `max_sum`

**Illustration:**
```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

num=-2: current = max(-2, 0 + -2) = max(-2, -2) = -2   max=-2
num= 1: current = max( 1, -2 + 1) = max( 1, -1) =  1   max= 1
num=-3: current = max(-3,  1 + -3) = max(-3, -2) = -2   max= 1
num= 4: current = max( 4, -2 + 4) = max( 4,  2) =  4   max= 4
num=-1: current = max(-1,  4 + -1) = max(-1,  3) =  3   max= 4
num= 2: current = max( 2,  3 +  2) = max( 2,  5) =  5   max= 5
num= 1: current = max( 1,  5 +  1) = max( 1,  6) =  6   max= 6  ← [4,-1,2,1]
num=-5: current = max(-5,  6 + -5) = max(-5,  1) =  1   max= 6
num= 4: current = max( 4,  1 +  4) = max( 4,  5) =  5   max= 6

Return 6 ✓
```

**Complexity:**
- Time: O(n) — single pass through the array
- Space: O(1) — only two variables, no extra storage

**Code:**
```python
def max_sub_array_optimal(nums: list[int]) -> int:
    max_sum = float("-inf")
    current_sum = 0

    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum
```

---

## Solution Breakdown — Step by Step

```python
def max_sub_array_optimal(nums: list[int]) -> int:
    max_sum = float("-inf")
    current_sum = 0

    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum
```

**Line by line:**

`max_sum = float("-inf")`
- Initialized to negative infinity so any real number will be larger
- This correctly handles all-negative arrays like `[-5, -3, -8]` — the answer
  is `-3`, not `0`; starting at `0` would incorrectly return `0`

`current_sum = 0`
- The running sum of the best subarray ending at the *current* position
- Starts at 0 because before the loop, no subarray has been started

`for num in nums:`
- Single pass — no index needed, just values
- Every element is visited exactly once

`current_sum = max(num, current_sum + num)`
- The heart of Kadane's algorithm — a local optimality decision
- `num` alone: "throw away everything before and start a new subarray here"
- `current_sum + num`: "extend the existing subarray with this element"
- If `current_sum` is negative, adding it to `num` hurts us — we restart
- If `current_sum` is positive, keeping it helps — we extend

`max_sum = max(max_sum, current_sum)`
- After updating `current_sum` for position `i`, we check: is this the best
  subarray ending anywhere so far?
- `max_sum` is our global answer — it never decreases

`return max_sum`
- After visiting all elements, `max_sum` holds the sum of the best subarray found

---

## Common Mistakes

**1. Initializing `max_sum` to 0 instead of `-∞`**
```python
# WRONG — fails for all-negative arrays
max_sum = 0
# nums = [-3, -1, -2] → should return -1, but returns 0
```
Use `float("-inf")` so the first real element always wins the first comparison.

**2. Initializing `current_sum` to `nums[0]` and skipping the first element**
```python
# Fragile — requires careful index handling
current_sum = nums[0]
max_sum = nums[0]
for num in nums[1:]:  # off-by-one risk
```
Starting `current_sum` at 0 and iterating all elements is cleaner and handles
single-element arrays without special-casing.

**3. Swapping the order of the two `max` calls**
```python
# WRONG order — updates max_sum before updating current_sum
max_sum = max(max_sum, current_sum)     # ← uses stale current_sum
current_sum = max(num, current_sum + num)
```
Always update `current_sum` first, then compare it to `max_sum`.

**4. Thinking you need to track subarray boundaries**
The problem only asks for the sum, not the actual subarray. Tracking start/end
indices adds complexity without benefit for this problem — only do it if asked.

---

## Pattern Recognition

> Use **Kadane's algorithm** when you see:
> - "Find the maximum/minimum sum subarray"
> - "Find the contiguous subarray with property X"
> - Local decisions (extend vs restart) that build a global optimum

**Similar problems:**
- **Maximum Product Subarray** — same idea, but tracking both max and min (negatives flip sign)
- **Best Time to Buy and Sell Stock** — equivalent to max subarray on price differences
- **Minimum Subarray Sum** — flip `max` to `min`, flip initialization
- **Maximum Sum Circular Subarray** — Kadane's + total sum trick for wrap-around case

---

## Real World Use Cases

### 1. Network packet loss analysis in monitoring systems
Site reliability engineers monitor rolling windows of packet loss metrics over
time. Finding the contiguous time window with the highest cumulative anomaly
score (to identify peak degradation periods) is structurally identical to maximum
subarray — the Kadane's approach scans the metric stream in one pass without
storing the full history.

### 2. Genomics sequence analysis
In bioinformatics, researchers look for contiguous segments of a DNA sequence
with the highest cumulative biological signal score (e.g., conservation scores,
expression weights). Kadane's algorithm is used to identify the most biologically
significant contiguous region in genome-scale arrays with hundreds of millions
of positions.

### 3. Profit/loss maximization in algorithmic trading
A trading system processing a stream of per-minute PnL (profit and loss) deltas
uses the maximum subarray pattern to identify the most profitable contiguous
trading window in historical data. One O(n) pass over years of tick data is far
more practical than O(n²) when n is in the tens of millions.

---

## Key Takeaways

- Kadane's algorithm makes one greedy local decision per element: extend or restart
- Initialize `max_sum` to `-∞`, not `0` — negative-only arrays would otherwise return the wrong answer
- The recurrence `current_sum = max(num, current_sum + num)` captures the entire algorithm
- This is a Dynamic Programming problem where the subproblem is "best subarray ending here"
- O(n) time and O(1) space — no auxiliary storage needed beyond two variables
