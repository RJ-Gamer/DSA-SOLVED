# 128. Longest Consecutive Sequence

**LeetCode:** https://leetcode.com/problems/longest-consecutive-sequence/
**Difficulty:** Medium
**Topics:** `Array` `Hash Map`

---

## Problem Statement

Given an unsorted array of integers `nums`, return the length of the longest
sequence of consecutive integers.

You must write an algorithm that runs in **O(n)** time.

### Example
```
Input:  nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4]. Length = 4.
```

```
Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
Explanation: [0, 1, 2, 3, 4, 5, 6, 7, 8]. Length = 9.
```

**Constraints:**
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

Find the longest run of consecutive integers (e.g. 1, 2, 3, 4) anywhere in the
array. The array is unsorted, duplicates may exist, and numbers can be far apart.

### Step 2 — Identify the constraint that matters

The O(n) time constraint rules out sorting (O(n log n)). We need a way to check
"does the next number exist?" in O(1) time.

### Step 3 — Think about data structures

A **hash set** gives O(1) lookup. If we dump all numbers into a set, we can
answer "is `x + 1` in the array?" instantly.

### Step 4 — Build the intuition

The key insight: **only start counting from sequence heads**.

A number `n` is the **head** of a sequence if `n - 1` is NOT in the set. If
`n - 1` exists, then `n` belongs to a sequence that already started earlier —
we'd be counting the same sequence twice.

By starting only at sequence heads and then walking forward (n+1, n+2, …), each
number is visited at most twice across the entire loop — once when we check it
as a candidate head, once when we step through it during a walk. Total work: O(n).

```
nums = [100, 4, 200, 1, 3, 2]
set  = {100, 4, 200, 1, 3, 2}

100 → 99 not in set → head! walk: 100, 101? No. streak = 1
  4 → 3 in set → skip (not a head)
200 → 199 not in set → head! walk: 200, 201? No. streak = 1
  1 → 0 not in set → head! walk: 1→2→3→4→5? No. streak = 4  ✓
  3 → 2 in set → skip
  2 → 1 in set → skip

Answer: 4
```

---

## Approaches

### Approach 1 — Brute Force (Sorting)

**Intuition:** Sort the array, then scan for consecutive runs.

**Steps:**
1. Sort `nums`.
2. Walk through, tracking current streak. Reset when a gap > 1 appears. Skip duplicates.
3. Return the max streak seen.

**Complexity:** Time O(n log n) / Space O(1) (or O(n) for sort depending on language)

**Code:**
```python
def longestConsecutive(nums):
    if not nums:
        return 0
    nums.sort()
    longest = 1
    current = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            continue          # skip duplicate
        if nums[i] == nums[i - 1] + 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest
```

---

### Approach 2 — Optimal (Hash Set)

**Intuition:** Use a set for O(1) lookup; only begin counting at sequence heads.

**Steps:**
1. Load all numbers into a set.
2. For each number, skip it if `num - 1` is in the set (not a head).
3. If it is a head, walk forward (`num + 1`, `num + 2`, …) until the chain breaks.
4. Track the max streak length.

**Illustration:**
```
nums = [100, 4, 200, 1, 3, 2]

Set = {1, 2, 3, 4, 100, 200}

num=1  → 0 not in set → HEAD
  walk: 1 → 2 → 3 → 4 → (5 missing) → streak = 4

num=2  → 1 in set → skip
num=3  → 2 in set → skip
num=4  → 3 in set → skip
num=100 → 99 not in set → HEAD → streak = 1
num=200 → 199 not in set → HEAD → streak = 1

longest = 4
```

**Complexity:** Time O(n) / Space O(n)

**Code:**
```python
def longestConsecutive(nums):
    num_set = set(nums)
    long_streak = 0

    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            long_streak = max(long_streak, current_streak)

    return long_streak
```

---

## Solution Breakdown — Step by Step

```python
def longestConsecutive(nums: List[int]) -> int:
    num_set = set(nums)         # O(n) build; O(1) lookup; duplicates removed
    long_streak = 0             # tracks the global best

    for num in num_set:         # iterate unique values only
        if num - 1 not in num_set:   # only start at sequence heads
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:  # extend the chain
                current_num += 1
                current_streak += 1

            long_streak = max(long_streak, current_streak)

    return long_streak
```

- `set(nums)` — deduplication is free here; we never need to count occurrences.
- `num - 1 not in num_set` — the head check. Without this, we'd re-walk every
  suffix of every sequence, making the inner while loop O(n) worst case per
  outer iteration — ruining the O(n) guarantee.
- The while loop is amortized O(1) per number: each number is touched as a
  starting point at most once, and stepped through at most once during walks.

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (Sort) | O(n log n) | O(1) |
| Optimal (Hash Set) | O(n) | O(n) |

---

## Common Mistakes

**Mistake 1 — Forgetting the head check (iterating `nums` instead of filtering)**

```python
# WRONG — walks from every number, not just heads
for num in num_set:
    current_num = num
    current_streak = 1
    while current_num + 1 in num_set:
        ...
```

This still gives the right answer but is O(n²) in the worst case (e.g. `[1, 2, 3, …, n]`):
each number walks the entire remaining sequence.

**Mistake 2 — Iterating over `nums` instead of `num_set`**

```python
# WRONG — duplicates cause redundant work and can inflate streak counts
for num in nums:   # should be num_set
    ...
```

With many duplicates the loop runs more than n times, and without careful
handling the streak counter may re-enter sequences already fully counted.

**Mistake 3 — Off-by-one in the walk condition**

```python
# WRONG
while current_num + 1 in num_set:
    current_streak += 1          # forgot to advance current_num → infinite loop
```

Always advance `current_num` inside the while loop.

---

## Pattern Recognition

> Use this pattern when you see: "find the longest/shortest run, subarray, or
> sequence" combined with an O(n) constraint that rules out sorting.

The core template is:
1. Dump values into a set.
2. Find "start" elements (those without a predecessor in the set).
3. Walk forward from each start, counting.

**Similar problems:**
- [LC 300 — Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) (DP / patience sort variant)
- [LC 594 — Longest Harmonious Subsequence](https://leetcode.com/problems/longest-harmonious-subsequence/)
- [LC 1048 — Longest String Chain](https://leetcode.com/problems/longest-string-chain/)

---

## Real World Use Cases

### 1. Version gap detection
Given a list of deployed build numbers, find the longest unbroken run of
sequential builds to identify a stable release streak.

### 2. Sensor continuity checking
In IoT or time-series data, find the longest uninterrupted sequence of
consecutive timestamps (no missing readings), to measure sensor uptime.

### 3. User activity streaks
Given a set of login days (stored as integers), compute the user's longest
daily login streak — the same algorithm, applied directly.

---

## Key Takeaways

- Convert to a set first: O(1) lookup is what makes O(n) possible.
- The "only start at sequence heads" trick is the entire key to the algorithm.
- Amortized analysis: even though there's a while loop inside a for loop, each element is processed at most twice total.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #128](https://leetcode.com/problems/longest-consecutive-sequence/) | Longest Consecutive Sequence | Medium |

> Part of **Blind 75** and **NeetCode 150**. Frequently asked at Google, Amazon, Facebook.
