# 295. Find Median from Data Stream

**LeetCode:** [Problem #295](https://leetcode.com/problems/find-median-from-data-stream/)  
**Difficulty:** Hard  
**Topics:** `Heap` `Design` `Sorting` `Two Pointers`

---

## Problem Statement

Design a data structure that supports adding integers from a data stream and
returning the median of all elements seen so far.

Implement the `MedianFinder` class:
- `MedianFinder()` — initializes the object
- `void addNum(int num)` — adds `num` to the data structure
- `double findMedian()` — returns the median of all elements

**Constraints:**
- `-10⁵ <= num <= 10⁵`
- At most `5 * 10⁴` calls to `addNum` and `findMedian`
- At least one element before calling `findMedian`

### Example
```
Input:  ["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
        [[],[1],[2],[],[3],[]]
Output: [null,null,null,1.5,null,2.0]

Explanation:
  addNum(1) → stream: [1]
  addNum(2) → stream: [1,2]
  findMedian() → (1+2)/2 = 1.5
  addNum(3) → stream: [1,2,3]
  findMedian() → 2.0
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

The median of a sorted list is the middle element (odd count) or the average
of the two middle elements (even count). Numbers arrive one at a time in any
order, so we can't pre-sort. We need an efficient structure to insert and
query the median repeatedly.

### Step 2 — Identify the constraint that matters

Sorting after every insert is O(n log n) per query — too expensive for
frequent calls. We need O(log n) inserts and O(1) median queries.

### Step 3 — Think about data structures

The median depends only on the middle element(s). If we split the stream
into a lower half and an upper half:
- The lower half's maximum and the upper half's minimum define the median
- A **max-heap** on the lower half gives the largest lower-half element in O(1)
- A **min-heap** on the upper half gives the smallest upper-half element in O(1)

Keep the two heaps balanced in size (differ by at most 1).

### Step 4 — Build the intuition

Picture two piles of numbers:
- `small` (max-heap): the smaller half — you can always peek at its largest
- `large` (min-heap): the larger half — you can always peek at its smallest

The median is either `small`'s top (odd total, `small` has one extra) or
the average of both tops (even total). Every `addNum` call maintains:
1. `small.max <= large.min` — the split is correct
2. `|len(small) - len(large)| <= 1` — the halves are balanced

---

## Approaches

### Approach 1 — Brute Force (Sorted List)

**Intuition:** Keep all numbers in a sorted list; find the median directly.

**Steps:**
1. Insert `num` in sorted position using bisect
2. Compute median from the middle index(es)

**Complexity:**
- Time: O(n) per `addNum` (shifting elements for insertion), O(1) for `findMedian`
- Space: O(n)

**Code:**
```python
import bisect

class MedianFinder:
    def __init__(self):
        self.data = []

    def addNum(self, num):
        bisect.insort(self.data, num)

    def findMedian(self):
        n = len(self.data)
        if n % 2 == 1:
            return float(self.data[n // 2])
        return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0
```

---

### Approach 2 — Optimal (Two Heaps)

**Intuition:** Maintain a max-heap for the lower half and a min-heap for
the upper half. Keep them balanced — median is always readable from the tops.

**Steps:**
1. Push `num` to `small` (max-heap, stored negated)
2. If `small`'s max exceeds `large`'s min, move the overflow to `large`
3. Rebalance sizes so `small` has at most one more element than `large`
4. For `findMedian`: if sizes differ, return `-small[0]`; else return the
   average of `-small[0]` and `large[0]`

**Illustration:**
```
addNum(1): small=[-1], large=[]   sizes: 1,0 → ok
addNum(2):
  push to small: small=[-1], then -(-1)=1 ≤ 2=large[0]? large is empty.
  push 2 to small → small=[-2,-1]
  small.max=2, large empty → no cross-balance needed
  |small|=2 > |large|+1=1 → move max(2) to large
  small=[-1], large=[2]   sizes: 1,1 → balanced
findMedian(): equal sizes → (-(-1) + 2) / 2 = 1.5 ✓

addNum(3):
  push -3 to small → small=[-3,-1]
  small.max=3 > large.min=2 → move 3 to large
  small=[-1], large=[2,3]
  |large|=2 > |small|=1 → move min(2) from large to small
  small=[-2,-1], large=[3]   sizes: 2,1
findMedian(): small bigger → -small[0] = 2.0 ✓
```

**Complexity:**
- Time: O(log n) per `addNum`, O(1) per `findMedian`
- Space: O(n)

**Code:**
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

---

## Solution Breakdown — Step by Step

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []
        self.large = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

**Line by line:**

`self.small = []` / `self.large = []`
- `small` is a max-heap (Python only has min-heaps; negate values to simulate max-heap)
- `large` is a min-heap — stores the upper half as-is

`heapq.heappush(self.small, -num)`
- Always insert into `small` first — we'll move elements around to fix ordering

`if (-self.small[0]) > self.large[0]:`
- Cross-check: the top of the lower half must never exceed the bottom of the upper half
- If violated, the partition is wrong — move the overflow to `large`

`if len(self.small) > len(self.large) + 1:`
- `small` can have at most one more element than `large` (holds the median in odd case)
- If more, move the max of `small` to `large`

`elif len(self.large) > len(self.small):`
- `large` must never be bigger than `small` (we want `small` to hold the median)
- If violated, move the min of `large` to `small`

`return float(-self.small[0])`
- Odd total: the median is the top of the larger heap (always `small`)

`return (-self.small[0] + self.large[0]) / 2.0`
- Even total: average the two middle elements (tops of both heaps)

---

## Quick Summary

| Approach | Time (addNum) | Time (findMedian) | Space |
|---|---|---|---|
| Brute Force (sorted list) | O(n) | O(1) | O(n) |
| Optimal (two heaps) | O(log n) | O(1) | O(n) |

---

## Common Mistakes

**1. Forgetting to negate when pushing/popping from the max-heap**
```python
# WRONG — Python's heapq is a min-heap; storing positives gives min behavior
heapq.heappush(self.small, num)
max_of_small = self.small[0]  # this is the MIN, not the max

# CORRECT
heapq.heappush(self.small, -num)
max_of_small = -self.small[0]
```

**2. Skipping the cross-balance check**
```python
# WRONG — only rebalancing sizes without ensuring small.max <= large.min
if len(self.small) > len(self.large) + 1:
    ...
# If small's max is 10 and large's min is 5, partition is invalid even if sizes are equal
```
Always check the ordering invariant before checking the size invariant.

**3. Allowing `large` to be larger than `small`**
```python
# WRONG — when total is odd, median should come from small (the larger heap)
# If large > small, findMedian returns large[0], but that's the wrong element
```
Maintain the invariant: `len(small) >= len(large)` at all times.

---

## Pattern Recognition

### How to Recognize
- Streaming data with repeated median (or k-th quantile) queries
- Need O(1) median access after O(log n) inserts
- Problem involves splitting a dynamic set into two halves

### How to Identify
- Does the answer depend only on the middle element(s) of a sorted sequence?
- Is the data arriving one element at a time (not pre-sorted)?

### How to Remember
> **Mental model:** Two mirror teams — the bigger players on one side,
> smaller on the other. The captains (heap tops) determine the score (median).

**Similar problems:**
- **Sliding Window Median (LeetCode #480)** — same two-heap idea with removal
- **IPO (LeetCode #502)** — two heaps to greedily pick the best available project
- **K Closest Points to Origin (LeetCode #973)** — heap for dynamic top-k queries

---

## Real World Use Cases

### 1. Real-time analytics dashboards
Monitoring systems that display the median response time of API calls need
to update the statistic as each new request arrives. Two heaps make this
O(log n) per event, enabling live dashboards without batching.

### 2. Streaming financial data
Trading systems compute the median price of trades within a rolling session.
New trades arrive continuously — the heap structure provides instant median
access without storing a sorted list of all trades.

### 3. Load balancer health monitoring
Infrastructure systems track median CPU or memory usage across a fleet of
servers that reports metrics continuously. The two-heap structure handles
the dynamic insertion stream without resorting on every new metric.

---

## Key Takeaways

- Python's `heapq` is a min-heap — simulate a max-heap by negating values
- Always maintain two invariants: ordering (`small.max <= large.min`) and balance (`|sizes| <= 1`)
- Check ordering before size — fixing ordering may change sizes, making a separate size fix necessary
- `findMedian` is O(1) because both heap tops are instantly accessible
- This two-heap pattern generalizes to any dynamic k-th quantile query

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #295](https://leetcode.com/problems/find-median-from-data-stream/) | Find Median from Data Stream | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
