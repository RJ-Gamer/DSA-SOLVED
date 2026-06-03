# 239. Sliding Window Maximum

**LeetCode:** [Problem #239](https://leetcode.com/problems/sliding-window-maximum/)  
**Difficulty:** Hard  
**Topics:** `Array` `Sliding Window` `Queue` `Monotonic Queue`

---

## Problem Statement

Given an integer array `nums` and an integer `k`, return an array of the
**maximum value** in each sliding window of size `k` as it moves from left
to right.

**Constraints:**
- `1 <= nums.length <= 10⁵`
- `-10⁴ <= nums[i] <= 10⁴`
- `1 <= k <= nums.length`

### Example
```
Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [3, 3, 5, 5, 6, 7]
Explanation:
  Window [1,3,-1]  → max 3
  Window [3,-1,-3] → max 3
  Window [-1,-3,5] → max 5
  Window [-3,5,3]  → max 5
  Window [5,3,6]   → max 6
  Window [3,6,7]   → max 7
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

For every position where a window of size `k` fits, report the maximum.
There are `n - k + 1` such windows. The naive approach re-scans each window
in O(k), giving O(nk) total — too slow for large inputs.

### Step 2 — Identify the constraint that matters

When the window slides one step right, one element leaves on the left and
one enters on the right. We need a structure that lets us:
- Find the maximum in O(1)
- Remove the element that just left the window
- Insert the new element

A sorted structure with O(log n) operations gives O(n log n) total.
But we can do better.

### Step 3 — Think about data structures

Ask: "Can we throw away elements that will never be a maximum?"

If a new element `x` enters and `x >= nums[j]` for some earlier index `j`
still in the window, then `nums[j]` can never be the maximum while `x` is
present (x covers the same or larger window and is bigger). We can remove
`nums[j]` permanently.

This gives us a **monotonic decreasing deque** — the front always holds
the index of the current window's maximum.

### Step 4 — Build the intuition

Maintain a deque of indices. The deque is always decreasing in value
(front = largest). Before adding a new index:
1. Pop from the front if it's outside the window (expired)
2. Pop from the back while the back's value is ≤ the new value (useless)
3. Push the new index

When the window is full (`i >= k - 1`), `nums[deque[0]]` is the answer.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** For every window position, scan all `k` elements to find the max.

**Steps:**
1. Slide a window of size `k` across `nums`
2. For each position, take `max(nums[i:i+k])`

**Complexity:**
- Time: O(nk) — k-element scan per window
- Space: O(1) — aside from the output array

**Code:**
```python
def maxSlidingWindow_brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
```

---

### Approach 2 — Optimal (Monotonic Deque)

**Intuition:** Maintain a deque of indices in decreasing value order.
The front of the deque is always the index of the current maximum.

**Steps:**
1. Iterate through `nums` with index `i`
2. Pop the front if `dq[0] < i - k + 1` (out of window)
3. Pop the back while `nums[dq[-1]] < nums[i]` (can never be max)
4. Append `i`
5. If `i >= k - 1`, record `nums[dq[0]]` as the window's max

**Illustration:**
```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

i=0, num=1:  dq=[]         → append 0 → dq=[0]
i=1, num=3:  nums[0]=1 < 3 → pop 0   → dq=[1]
i=2, num=-1: nums[1]=3 > -1 → keep   → dq=[1,2]   window full → result=[nums[1]]=[3]
i=3, num=-3: nums[2]=-1 > -3 → keep  → dq=[1,2,3] window full, dq[0]=1 in range [1,3] → result=[3,nums[1]]=[3,3]
i=4, num=5:  pop 3(-3), pop 2(-1), pop 1(3) all < 5 → dq=[4]
             dq[0]=4, window=[2,4] → result=[3,3,nums[4]]=[3,3,5]
i=5, num=3:  nums[4]=5 > 3 → keep → dq=[4,5]
             window=[3,5] → result=[3,3,5,nums[4]]=[3,3,5,5]
i=6, num=6:  nums[5]=3 < 6 → pop 5; nums[4]=5 < 6 → pop 4 → dq=[6]
             window=[4,6] → result=[3,3,5,5,6]
i=7, num=7:  nums[6]=6 < 7 → pop 6 → dq=[7]
             window=[5,7] → result=[3,3,5,5,6,7] ✓
```

**Complexity:**
- Time: O(n) — each index is pushed and popped at most once
- Space: O(k) — deque holds at most k indices

**Code:**
```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()
    result = []
    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## Solution Breakdown — Step by Step

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    dq = deque()
    result = []

    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Line by line:**

`dq = deque()`
- Stores indices (not values) so we can check if the front has expired
- Python's `deque` supports O(1) pop from both ends — critical for this approach

`while dq and dq[0] < i - k + 1: dq.popleft()`
- `i - k + 1` is the leftmost valid index for the current window
- If the front index is older than that, it has slid out — remove it

`while dq and nums[dq[-1]] < num: dq.pop()`
- Maintain the monotonic decreasing property: any element smaller than
  the incoming one is useless — it's in the same or earlier window and smaller
- Pop from the back (smaller end) until the back is ≥ current value

`dq.append(i)`
- Add the current index — it's a candidate for future windows

`if i >= k - 1: result.append(nums[dq[0]])`
- Window is complete only once we've processed at least `k` elements
- `dq[0]` is always the index of the current window's maximum

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (scan each window) | O(nk) | O(1) |
| Optimal (monotonic deque) | O(n) | O(k) |

---

## Common Mistakes

**1. Storing values in the deque instead of indices**
```python
# WRONG — can't check if the front element has expired
dq.append(num)  # we lose the index

# CORRECT
dq.append(i)    # store index, retrieve value with nums[dq[0]]
```
Without indices, there's no way to know whether the front element is still
inside the current window.

**2. Checking strict inequality wrong in the expiry condition**
```python
# WRONG — expiry condition is off by one
while dq and dq[0] <= i - k:      # same as i - k + 1, but less readable
while dq and dq[0] < i - k:       # WRONG — keeps one expired element
```
The leftmost valid index is `i - k + 1`. If `dq[0] < i - k + 1`, it's expired.

**3. Popping the back when value is strictly less vs. less-or-equal**
```python
# Using <= removes equal elements — still correct but loses info unnecessarily
while dq and nums[dq[-1]] <= num:
    dq.pop()
```
Using `<` (strict) is safer — equal elements don't hurt, and keeping them
means we prefer the earlier index as the window max, which is fine.

---

## Pattern Recognition

### How to Recognize
- Sliding window problem asking for min or max within each window
- Brute force is O(nk), need O(n)
- Elements that become "dominated" by a newer element can be discarded permanently

### How to Identify
- Is there a way to permanently discard elements that can never be the answer?
- Would a data structure that maintains a monotonic order over the window work?

### How to Remember
> **Mental model:** A bouncer at a club — when a bigger guest arrives, all smaller guests
> at the back of the line are removed because they'll never get in first.

**Similar problems:**
- **Sliding Window Minimum** — same pattern, but monotonic increasing deque
- **Shortest Subarray with Sum at Least K (LeetCode #862)** — monotonic deque on prefix sums
- **Jump Game VI (LeetCode #1696)** — DP with monotonic deque for window max

---

## Real World Use Cases

### 1. Real-time stock price monitoring
Financial dashboards compute rolling maximums over time windows (e.g., the
52-week high) on tick-by-tick price feeds. The monotonic deque makes this
O(n) across millions of ticks instead of O(nk).

### 2. Network traffic spike detection
Intrusion detection systems compute the peak packet rate in rolling time
windows. Using a monotonic deque allows real-time alerting without rescanning
the entire window on every new packet.

### 3. Sensor anomaly detection in IoT
Industrial sensors report readings continuously. Anomaly thresholds are based
on the maximum in the last N readings. The deque-based approach processes
high-frequency sensor streams without lagging.

---

## Key Takeaways

- Store indices, not values, in the deque — you need them to detect expiry
- Two cleanup steps: expire old front, remove dominated back elements
- The deque's front is always the current window maximum
- Each element is pushed and popped at most once — total O(n) across all windows
- This monotonic deque pattern appears in sliding window min, DP range queries, and more

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/) | Sliding Window Maximum | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
