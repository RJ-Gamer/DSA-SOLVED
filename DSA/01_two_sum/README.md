# 01. Two Sum

**LeetCode:** [Problem #1](https://leetcode.com/problems/two-sum/)  
**Difficulty:** Easy  
**Topics:** `Array` `Hash Map`

---

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the
**indices** of the two numbers that add up to `target`.

You may assume exactly one solution exists, and you may not use the
same element twice. You can return the answer in any order.

**Constraints:**
- `2 <= nums.length <= 10⁴`
- `-10⁹ <= nums[i] <= 10⁹`
- `-10⁹ <= target <= 10⁹`
- Only one valid answer exists

### Example
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

```
Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
Explanation: nums[1] + nums[2] = 2 + 4 = 6
```

---

## How to Think About This Problem

Before writing a single line of code, let's think through this carefully.

### Step 1 — Understand what's being asked

We have a list of numbers. We need to find **two of them** that add up
to a target. We need to return their **positions** (indices), not their
values.

Key word: **indices**. Not the numbers themselves.

### Step 2 — Identify the constraint that matters

We can't use the same element twice. So `nums = [3, 3]` with `target = 6`
is valid (indices 0 and 1 are different), but we can't use index 0 twice.

### Step 3 — Think about data structures

The brute force is obvious: check every pair. Two nested loops. But
that's O(n²).

Now ask: **what information do we wish we had instantly?**

When we're at index `i` looking at number `num`, we want to know:
> "Has the number I *need* (`target - num`) appeared before?"

If only we had a fast way to check "have I seen X before, and if so,
where was it?" — that's exactly what a **hash map** does. O(1) lookup.

### Step 4 — Build the intuition

Think of it like this: you're walking through a list of numbers, and
you're holding a notebook. For each number you see:

1. Check your notebook — is the number you *need* already written there?
2. If yes — you found your pair. Return both positions.
3. If no — write this number and its position in your notebook, keep walking.

The notebook is the hash map. `seen = {value: index}`.

The key insight: **you don't need to look forward — you only need to
remember what you've already passed.**

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Check every possible pair of numbers.

**Steps:**
1. Loop through each element with index `i`
2. For each `i`, loop through every element after it with index `j`
3. If `nums[i] + nums[j] == target`, return `[i, j]`

**Illustration:**
```
nums = [2, 7, 11, 15], target = 9

i=0, j=1: 2 + 7  = 9  ✓ → return [0, 1]

(If not found at j=1, we'd continue:)
i=0, j=2: 2 + 11 = 13 ✗
i=0, j=3: 2 + 15 = 17 ✗
i=1, j=2: 7 + 11 = 18 ✗
... and so on
```

**Complexity:**
- Time: O(n²) — nested loops, every pair checked
- Space: O(1) — no extra data structure

**Code:**
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

---

### Approach 2 — Optimal (Hash Map)

**Intuition:** For each number, check if its complement already exists
in a hash map. One pass, O(1) lookups.

**Steps:**
1. Create an empty hash map `seen = {}`
2. Loop through `nums` with index and value
3. Calculate `complement = target - num`
4. If `complement` is in `seen` → return `[seen[complement], i]`
5. Otherwise → store `seen[num] = i` and continue

**Illustration:**
```
nums = [2, 7, 11, 15], target = 9

i=0, num=2
  complement = 9 - 2 = 7
  seen = {}
  7 not in seen
  → store seen[2] = 0
  seen = {2: 0}

i=1, num=7
  complement = 9 - 7 = 2
  seen = {2: 0}
  2 IS in seen → return [seen[2], 1] = [0, 1] ✓
```

```
nums = [3, 2, 4], target = 6

i=0, num=3
  complement = 6 - 3 = 3
  seen = {}
  3 not in seen
  → store seen[3] = 0
  seen = {3: 0}

i=1, num=2
  complement = 6 - 2 = 4
  seen = {3: 0}
  4 not in seen
  → store seen[2] = 1
  seen = {3: 0, 2: 1}

i=2, num=4
  complement = 6 - 4 = 2
  seen = {3: 0, 2: 1}
  2 IS in seen → return [seen[2], 2] = [1, 2] ✓
```

**Complexity:**
- Time: O(n) — single pass through the array
- Space: O(n) — hash map stores up to n elements

**Code:**
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i
```

---

## Solution Breakdown — Step by Step

```python
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i
```

**Line by line:**

`seen = {}`
- A hash map storing `{number: index}` for every element we've visited
- We need to remember both the value (to look up later) and the index
  (to return as part of the answer)
- Dictionary lookup in Python is O(1) average — this is why we use it

`for i, num in enumerate(nums):`
- `enumerate` gives us both the index (`i`) and the value (`num`)
  simultaneously
- We need `i` because the answer requires indices, not values
- Without enumerate, we'd need `range(len(nums))` and `nums[i]` separately

`complement = target - num`
- The mathematical core of the solution
- If `a + b = target`, then `b = target - a`
- We're asking: "what number, paired with the current number, reaches target?"
- We call it `complement` because it "completes" the pair

`if complement in seen:`
- O(1) hash map lookup — this is what makes the solution O(n) overall
- We're checking: "have we already seen the number we need?"
- `in` on a dict checks keys, not values — and our keys are the numbers

`return [seen[complement], i]`
- `seen[complement]` gives us the index where we previously saw the complement
- `i` is the current index
- We return them in order `[earlier_index, current_index]`

`seen[num] = i`
- We store the current number and its index for future lookups
- **Critical:** this line comes AFTER the check — see Common Mistakes below

---

## Common Mistakes

**1. Storing before checking**
```python
# WRONG — checks if num equals its own complement (uses same element twice)
seen[num] = i
if complement in seen:
    return [seen[complement], i]
```
If `target = 6` and `num = 3`, complement is also `3`. Storing first
means you find `num` itself and return `[i, i]` — using the same index
twice. Always check first, store after.

**2. Returning values instead of indices**
```python
# WRONG
return [complement, num]  # returns numbers, not positions
# CORRECT
return [seen[complement], i]  # returns indices
```

**3. Using a list instead of a dict for `seen`**
```python
# WRONG — O(n) lookup, defeats the purpose
seen = []
if complement in seen:  # this is O(n), making total O(n²)
```
Always use a dict for O(1) lookup. This is the entire reason the
optimal solution is faster.

---

## Pattern Recognition

> Use the **Hash Map complement** pattern when you see:
> - "Find two elements that sum to X"
> - "Find a pair that satisfies condition Y"
> - You need to check "have I seen X before?" in O(1)

**Similar problems:**
- **Two Sum II (sorted array)** — same idea but use Two Pointers since array is sorted
- **3Sum** — reduce to Two Sum by fixing one element in outer loop
- **4Sum** — reduce to Two Sum by fixing two elements
- **Subarray Sum Equals K** — prefix sum + hash map, same "complement" thinking
- **Contains Duplicate** — simpler version: just check if num is in seen

---

## Real World Use Cases

### 1. Transaction matching in fintech
In payment reconciliation systems, you have two lists of transactions
and need to find pairs that sum to a specific settlement amount. The
hash map approach lets you match millions of transactions in O(n)
instead of O(n²) — the difference between seconds and hours at scale.

### 2. Inventory pairing in e-commerce
When building bundle recommendations ("frequently bought together"),
you need to find product pairs whose combined price hits a target
discount threshold. The complement pattern lets you scan a product
catalogue once instead of comparing every product against every other.

### 3. Cache-hit detection in API systems
When rate-limiting API requests, you store seen request hashes in a
hash map and check if a complementary request (one that would exceed
the quota) has arrived. This is structurally identical to Two Sum —
"have I seen the thing that, combined with this, crosses the limit?"

### 4. Sensor data fusion in IoT
In systems processing sensor readings (temperature + pressure pairs,
for example), finding two sensor values that together indicate a fault
condition uses the exact same pattern. One pass through the readings,
hash map lookup for the complement value.

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (nested loops) | O(n²) | O(1) |
| Optimal (hash map) | O(n) | O(n) |

---

## Key Takeaways

- Trading **space for time** is often the right call: O(n) space to get O(n) time
- Hash maps give O(1) lookup — reach for them when you need "have I seen X?"
- The **complement pattern** (`target - current`) is reusable across many problems
- Always check the hash map **before** inserting the current element
- `enumerate()` is cleaner than `range(len())` when you need both index and value

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #1](https://leetcode.com/problems/two-sum/) | Two Sum | Easy |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.