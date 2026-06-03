# 42. Trapping Rain Water

**LeetCode:** [Problem #42](https://leetcode.com/problems/trapping-rain-water/)  
**Difficulty:** Hard  
**Topics:** `Array` `Two Pointers` `Stack` `Dynamic Programming`

---

## Problem Statement

Given `n` non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

**Constraints:**
- `n == height.length`
- `1 <= n <= 2 * 10⁴`
- `0 <= height[i] <= 10⁵`

### Example
```
Input:  height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6
Explanation: 6 units of water are trapped between the bars.

Input:  height = [4, 2, 0, 3, 2, 5]
Output: 9
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

Water sits on top of shorter bars, bounded by taller bars on both sides.
At any position `i`, the water level is determined by how tall the shortest
"wall" is on either side. Water above the bar itself is `min(left_max, right_max) - height[i]`.

### Step 2 — Identify the constraint that matters

For each index, we need to know the tallest bar to its left and the tallest
to its right. The water at that index is the "ceiling" (the shorter wall) minus
the bar's own height. If negative, no water sits there.

### Step 3 — Think about data structures

- Brute force: for each index, scan left and right. O(n²).
- Precompute: build `left_max[]` and `right_max[]` arrays. O(n) time, O(n) space.
- Optimal: use two pointers — the pointer on the shorter side always has a
  definitive answer because the other side is guaranteed to be at least as tall.

### Step 4 — Build the intuition

Two pointers start at both ends. We always process the pointer at the shorter
side. Why? If `height[left] < height[right]`, then `right_max >= height[right] > height[left]`,
so `min(left_max, right_max) = left_max`. The water at `left` is fully
determined — `left_max - height[left]`. Move `left` inward. Mirror logic for the right side.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** For each position, scan both sides to find the tallest bars.

**Steps:**
1. For each `i` from 1 to n-2, compute `max(height[:i+1])` and `max(height[i:])`
2. Water at `i` = `min(left_max, right_max) - height[i]`

**Complexity:**
- Time: O(n²) — two scans per element
- Space: O(1)

**Code:**
```python
def trap_brute(height):
    water = 0
    for i in range(1, len(height) - 1):
        left_max = max(height[:i + 1])
        right_max = max(height[i:])
        water += min(left_max, right_max) - height[i]
    return water
```

---

### Approach 2 — Precompute Arrays

**Intuition:** Precompute the maximum height to the left and right of each
index. Then a single pass calculates the water.

**Steps:**
1. Build `left_max[i]` = max height from index 0 to i
2. Build `right_max[i]` = max height from index i to n-1
3. For each `i`: `water += min(left_max[i], right_max[i]) - height[i]`

**Complexity:**
- Time: O(n) — three passes
- Space: O(n) — two extra arrays

**Code:**
```python
def trap_precompute(height):
    n = len(height)
    left_max, right_max = [0] * n, [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
```

---

### Approach 3 — Optimal (Two Pointers)

**Intuition:** The pointer at the shorter side always knows its answer —
the taller side is guaranteed to be at least as tall. Process the shorter side,
update its max, accumulate water, then move inward.

**Steps:**
1. `left = 0`, `right = n - 1`, `left_max = right_max = 0`, `water = 0`
2. While `left < right`:
   - If `height[left] < height[right]`: update `left_max`, add `left_max - height[left]`, move `left` right
   - Else: update `right_max`, add `right_max - height[right]`, move `right` left
3. Return `water`

**Illustration:**
```
height = [4, 2, 0, 3, 2, 5]
          L                R   left_max=0, right_max=0

height[L]=4 >= height[R]=5? No → process left side.
  height[L]=4 >= left_max=0 → left_max=4
  water += 4 - 4 = 0    → L moves to 1

height[L]=2 >= height[R]=5? No → process left.
  height[L]=2 < left_max=4 → water += 4 - 2 = 2   → L moves to 2

height[L]=0 >= height[R]=5? No → process left.
  height[L]=0 < left_max=4 → water += 4 - 0 = 4   → L moves to 3

height[L]=3 >= height[R]=5? No → process left.
  height[L]=3 < left_max=4 → water += 4 - 3 = 1   → L moves to 4

height[L]=2 >= height[R]=5? No → process left.
  height[L]=2 < left_max=4 → water += 4 - 2 = 2   → L moves to 5

L == R → stop
Total water = 0 + 2 + 4 + 1 + 2 = 9 ✓
```

**Complexity:**
- Time: O(n) — single pass
- Space: O(1) — only four variables

**Code:**
```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water
```

---

## Solution Breakdown — Step by Step

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water
```

**Line by line:**

`left, right = 0, len(height) - 1`
- Two pointers starting at the outermost bars — the widest possible boundary

`left_max = right_max = 0`
- Track the tallest bar seen from the left and right respectively

`if height[left] < height[right]:`
- Choose the shorter side — that side's water is fully determined
- The taller side guarantees `right_max >= height[right] > height[left]`
  so the bottleneck is definitely `left_max`

`if height[left] >= left_max: left_max = height[left]`
- Current bar is taller than anything we've seen — update max, no water here

`else: water += left_max - height[left]`
- Current bar is shorter than the max seen — water fills up to `left_max`

`left += 1`
- Advance the pointer inward after processing

`else:` (mirror for right side)
- Same logic applied to the right pointer when `height[right] <= height[left]`

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (double scan) | O(n²) | O(1) |
| Precompute Arrays | O(n) | O(n) |
| Optimal (two pointers) | O(n) | O(1) |

---

## Common Mistakes

**1. Not updating the max before accumulating water**
```python
# WRONG — uses old left_max before checking if current bar is taller
water += left_max - height[left]
left_max = max(left_max, height[left])  # should come first
```
The update must happen before (or instead of) accumulation when `height[i] >= max`.

**2. Confusing which pointer to move**
```python
# WRONG — always moving left regardless of which side is shorter
if height[left] < height[right]:
    left += 1  # missing the actual water calculation before moving
```
The calculation for the current position must happen before moving the pointer.

**3. Using strict `<` vs `<=` when choosing a side**
```python
# When height[left] == height[right], either side is fine
# Using either < or <= in the condition is correct — just be consistent
```
The key invariant is that the shorter side's answer is fully determined,
and equal heights satisfy both sides.

---

## Pattern Recognition

### How to Recognize
- Array of heights/walls and you need to find trapped area/water
- Water at any position depends on the min of left_max and right_max
- Need O(1) space solution beyond O(n) precompute

### How to Identify
- Is each element's contribution determined by the best values on both sides?
- Can you use two pointers where one side always has a definitive answer?

### How to Remember
> **Mental model:** Two walls closing in. The shorter wall already knows how
> much water is above it — the taller wall guarantees nothing leaks that way.

**Similar problems:**
- **Container With Most Water (LeetCode #11)** — two pointers on height array
- **Largest Rectangle in Histogram (LeetCode #84)** — stack-based, related idea
- **Maximal Rectangle (LeetCode #85)** — extends histogram idea to 2D

---

## Real World Use Cases

### 1. Civil engineering drainage modeling
Simulating water accumulation in terrain profiles (cross-sections of valleys
and ridges) to design drainage systems. The two-pointer algorithm processes
entire elevation profiles in linear time.

### 2. Urban flood risk analysis
City planners model street cross-sections as height arrays. Computing total
water volume trapped between buildings during heavy rain uses this exact
algorithm to identify flood-prone areas.

### 3. Signal processing baseline correction
In spectrum analysis, "trapped water" between peaks corresponds to baseline
noise that must be subtracted. The algorithm efficiently computes the noise
envelope from a 1D signal.

---

## Key Takeaways

- The water at any position equals `min(left_max, right_max) - height[i]` — clamped to zero
- Two pointers work because the shorter side's bottleneck is already known
- Always update the max first, then add water — never accumulate on a new max
- Three approaches with different time/space trade-offs: O(n²)/O(1), O(n)/O(n), O(n)/O(1)
- The two-pointer technique here is more subtle than in Two Sum — understanding why it's safe is the key insight

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #42](https://leetcode.com/problems/trapping-rain-water/) | Trapping Rain Water | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
