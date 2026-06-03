# 84. Largest Rectangle in Histogram

**LeetCode:** [Problem #84](https://leetcode.com/problems/largest-rectangle-in-histogram/)  
**Difficulty:** Hard  
**Topics:** `Array` `Stack` `Monotonic Stack`

---

## Problem Statement

Given an array of integers `heights` representing the histogram bar heights
(each bar has width 1), return the area of the **largest rectangle** that can
be formed within the histogram.

**Constraints:**
- `1 <= heights.length <= 10⁵`
- `0 <= heights[i] <= 10⁴`

### Example
```
Input:  heights = [2, 1, 5, 6, 2, 3]
Output: 10
Explanation: The largest rectangle spans bars at indices 2 and 3 (heights 5 and 6),
             giving area 5 * 2 = 10.

Input:  heights = [2, 4]
Output: 4
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

A rectangle in the histogram is defined by:
- A contiguous range of bars `[l, r]`
- Height = the minimum bar height in that range (the rectangle can only be as
  tall as the shortest bar)
- Area = height × width = `min(heights[l..r]) * (r - l + 1)`

We want the maximum such area over all possible ranges.

### Step 2 — Identify the constraint that matters

For every bar, ask: "What is the widest rectangle where this bar is the
shortest (i.e., the height)?" If we know the nearest shorter bar to the
left (`left_boundary`) and to the right (`right_boundary`) for each bar,
the rectangle's width is `right_boundary - left_boundary - 1`.

This is the key insight: **each bar is the height of exactly one maximal rectangle**.

### Step 3 — Think about data structures

Finding the nearest smaller element to the left and right for every bar is
a classic **monotonic stack** problem. Maintain a stack of bars in
increasing height order. When a shorter bar arrives, it defines the right
boundary for all taller bars still on the stack.

### Step 4 — Build the intuition

Process bars left to right. The stack stores `(start_index, height)` in
increasing order. When a new bar is shorter than the stack's top:
- Pop the top — its right boundary is the current index
- Compute its area
- The new bar's start index extends back to where the popped bar began
  (because the new bar is shorter and will cover that range)

At the end, every bar remaining in the stack extends to the rightmost position.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** For every pair `(i, j)`, the rectangle height is the minimum
in that range. Track the maximum area seen.

**Steps:**
1. For each starting index `i`, track `min_height` as `j` expands rightward
2. Area at each `(i, j)` = `min_height * (j - i + 1)`

**Complexity:**
- Time: O(n²) — nested loops
- Space: O(1)

**Code:**
```python
def largestRectangleArea_brute(heights):
    max_area = 0
    n = len(heights)
    for i in range(n):
        min_h = heights[i]
        for j in range(i, n):
            min_h = min(min_h, heights[j])
            max_area = max(max_area, min_h * (j - i + 1))
    return max_area
```

---

### Approach 2 — Optimal (Monotonic Stack)

**Intuition:** Use a monotonically increasing stack. When a shorter bar
is encountered, every taller bar being popped can form a maximal rectangle
— the current bar is its right boundary and the previous stack entry is its
left boundary.

**Steps:**
1. Maintain `stack = [(start, height)]` in increasing height order
2. For each bar `(i, h)`:
   - `start = i`
   - While `stack[-1].height > h`: pop, compute area, extend `start` left
   - Append `(start, h)`
3. After the loop, process remaining stack entries (they extend to `n`)

**Illustration:**
```
heights = [2, 1, 5, 6, 2, 3]
stack = []

i=0, h=2: stack=[(0,2)]
i=1, h=1: stack top (0,2) > 1 → pop (0,2): area=2*(1-0)=2, start=0
          stack=[], push (0,1) → stack=[(0,1)]
i=2, h=5: 5>1 → push (2,5) → stack=[(0,1),(2,5)]
i=3, h=6: 6>5 → push (3,6) → stack=[(0,1),(2,5),(3,6)]
i=4, h=2: top (3,6) > 2 → pop: area=6*(4-3)=6, start=3
          top (2,5) > 2 → pop: area=5*(4-2)=10, start=2  ← max so far
          top (0,1) ≤ 2 → stop
          push (2,2) → stack=[(0,1),(2,2)]
i=5, h=3: 3>2 → push (5,3) → stack=[(0,1),(2,2),(5,3)]

End of array — drain stack (all extend to n=6):
  pop (5,3): area=3*(6-5)=3
  pop (2,2): area=2*(6-2)=8
  pop (0,1): area=1*(6-0)=6

max_area = 10 ✓
```

**Complexity:**
- Time: O(n) — each bar pushed and popped at most once
- Space: O(n) — stack

**Code:**
```python
def largestRectangleArea(heights):
    stack = []  # (start, height)
    max_area = 0

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))

    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))

    return max_area
```

---

## Solution Breakdown — Step by Step

```python
def largestRectangleArea(heights: list[int]) -> int:
    stack = []
    max_area = 0

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))

    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))

    return max_area
```

**Line by line:**

`stack = []`
- Stores `(start_index, height)` pairs in monotonically increasing height order
- `start_index` is where this height's maximal rectangle can begin (may extend left
  through previously popped shorter-or-equal bars)

`start = i`
- Initialize the start of the current bar's potential rectangle to its own index

`while stack and stack[-1][1] > h:`
- Current bar is shorter — the popped bar's rectangle cannot extend past this point
- The current bar defines the right boundary for everything being popped

`idx, height = stack.pop()`
- `idx` is where the popped bar's rectangle can start (it already accounts for
  any earlier bars that were shorter and caused this bar to be pushed later)

`max_area = max(max_area, height * (i - idx))`
- Rectangle width = `i - idx` (from start to current index, not including current)
- Height = the popped bar's height

`start = idx`
- Critical: the current (shorter) bar can extend back to where the popped bar started
  because it's shorter and can cover that range too

`stack.append((start, h))`
- Push the current bar with the potentially extended start

`for idx, height in stack:`
- After iterating all bars, any remaining stack entries extend to the right edge
- Width = `len(heights) - idx`

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (nested loops) | O(n²) | O(1) |
| Optimal (monotonic stack) | O(n) | O(n) |

---

## Common Mistakes

**1. Not extending `start` when popping**
```python
# WRONG — the new bar should be able to extend as far left as the popped bar
start = i           # always starts at current index
stack.append((i, h))

# CORRECT
start = idx         # extend left to where the popped bar started
stack.append((start, h))
```
Without extending `start`, shorter bars that follow can't utilize the full
width they're entitled to.

**2. Using width `i - idx + 1` instead of `i - idx`**
```python
# WRONG — off by one: the rectangle runs from idx to i-1 (not including i)
area = height * (i - idx + 1)

# CORRECT — current index i is the right boundary (excluded)
area = height * (i - idx)
```
The current (shorter) bar at `i` is the right wall that stops the rectangle —
it is not part of the rectangle.

**3. Forgetting to drain the stack after the loop**
```python
# WRONG — bars that never found a shorter right boundary are skipped
for i, h in enumerate(heights):
    ...
# Missing: for idx, height in stack: ...
```
Bars remaining in the stack extend to the rightmost position — their area
must be computed with width `len(heights) - idx`.

---

## Pattern Recognition

### How to Recognize
- Finding the largest rectangle under a histogram or skyline
- Each element's contribution is bounded by the nearest smaller element on each side
- "Nearest smaller element" to the left and right — classic monotonic stack setup

### How to Identify
- For each element, does the answer depend on finding the closest element
  that is smaller (or larger) on each side?
- Can you process left to right and use a stack to track "unresolved" elements?

### How to Remember
> **Mental model:** Stack bars like trays. When a shorter tray comes in, all
> taller trays behind it are forced out — their rectangle closes here. The
> shorter tray may inherit the leftward reach of everything it cleared.

**Similar problems:**
- **Maximal Rectangle (LeetCode #85)** — apply this exact problem row-by-row in a matrix
- **Trapping Rain Water (LeetCode #42)** — monotonic stack variant
- **Daily Temperatures (LeetCode #739)** — nearest larger element, same stack pattern

---

## Real World Use Cases

### 1. Building skyline analysis in urban planning
City planners compute the maximum rectangular usable space within a skyline
profile (floor plan cross-section) for zoning and shadow modeling. This
algorithm gives the largest contiguous rectangular area in O(n).

### 2. Memory allocation in operating systems
When managing a pool of memory blocks of varying sizes (the histogram is
free-block sizes by address), finding the largest contiguous block that fits
a given shape uses the same largest-rectangle logic.

### 3. Billboard placement along a road profile
Advertising companies maximize billboard area along a highway with terrain
height restrictions. The histogram of permitted heights maps directly to this
problem — the optimal billboard is the largest rectangle in that histogram.

---

## Key Takeaways

- Each bar is the height of exactly one maximal rectangle — binary search for its left/right limits
- Monotonic stack finds "nearest smaller element" for all bars in O(n) total
- When popping, extend `start` leftward — the shorter bar can use the same range
- Width formula is `i - idx` (right boundary excluded), not `i - idx + 1`
- Drain remaining stack at the end with width `n - idx`

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Largest Rectangle in Histogram | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
