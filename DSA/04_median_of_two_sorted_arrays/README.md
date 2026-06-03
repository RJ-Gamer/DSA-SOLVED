# 04. Median of Two Sorted Arrays

**LeetCode:** [Problem #4](https://leetcode.com/problems/median-of-two-sorted-arrays/)
**Difficulty:** Hard
**Topics:** `Array` `Binary Search` `Divide and Conquer`

---

## Problem Statement

Given two sorted arrays `nums1` and `nums2` of sizes `m` and `n`, return the
**median** of the two sorted arrays.

The overall runtime complexity must be `O(log(m + n))`.

**Constraints:**
- `0 <= m, n <= 1000`
- `1 <= m + n <= 2000`
- `-10⁶ <= nums1[i], nums2[i] <= 10⁶`

### Example
```
Input:  nums1 = [1, 3], nums2 = [2]
Output: 2.0
Explanation: Merged array is [1, 2, 3], median is 2.

Input:  nums1 = [1, 2], nums2 = [3, 4]
Output: 2.5
Explanation: Merged array is [1, 2, 3, 4], median is (2 + 3) / 2 = 2.5
```

---

## How to Think About This Problem

### Step 1 — Understand what the median means in terms of partitions

The median splits a sorted sequence into two equal halves. In a merged array of
size `m + n`, the left half has `(m + n) // 2` elements. The median is the
largest element of the left half (odd total) or the average of the largest in
the left half and smallest in the right half (even total).

We don't need to build the merged array. We just need to find the right **split
point** across both arrays.

### Step 2 — Identify the constraint that matters

The `O(log(m + n))` requirement rules out merging the arrays. We need binary
search. The key insight: if we choose how many elements to take from `nums1`
(call it `i`), then we know exactly how many to take from `nums2` (`j = half - i`).
Binary search on `i`.

### Step 3 — Think about what a valid partition looks like

A partition is valid when:
- `maxLeft1 <= minRight2` — left part of nums1 ≤ right part of nums2
- `maxLeft2 <= minRight1` — left part of nums2 ≤ right part of nums1

If both conditions hold, the combined left half contains the correct elements.

### Step 4 — Build the intuition

Binary search on the shorter array. For each candidate partition of `nums1`,
compute the forced partition of `nums2`. Check the boundary conditions. Adjust
left/right pointers based on which side violates the condition.

---

## Approaches

### Approach 1 — Brute Force (Merge and Find)

**Intuition:** Merge both arrays, then find the median of the merged array.

**Steps:**
1. Concatenate both arrays and sort
2. If total length is odd, return the middle element
3. If even, return the average of the two middle elements

**Complexity:**
- Time: O((m + n) log(m + n)) — sorting dominates
- Space: O(m + n) — stores the merged array

**Code:**
```python
def findMedianSortedArrays_brute(nums1, nums2):
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
```

---

### Approach 2 — Optimal (Binary Search on Partition)

**Intuition:** Binary search on the smaller array to find the partition point
`i` such that `nums1[:i] + nums2[:j]` forms exactly the left half of the
merged array. Check the four boundary values to confirm a valid partition.

**Steps:**
1. Ensure `nums1` is the shorter array (swap if needed)
2. Binary search `i` in range `[0, m]`
3. Compute `j = half - i`
4. Compute the four boundary values: `maxLeft1`, `minRight1`, `maxLeft2`, `minRight2`
5. If partition is valid, compute and return the median
6. If `maxLeft1 > minRight2`, move `right = i - 1` (i is too large)
7. Otherwise `left = i + 1` (i is too small)

**Illustration:**
```
nums1 = [1, 3],  nums2 = [2, 4],  m=2, n=2, half=2

Try i=1, j=1:
  maxLeft1  = nums1[0] = 1
  minRight1 = nums1[1] = 3
  maxLeft2  = nums2[0] = 2
  minRight2 = nums2[1] = 4

  maxLeft1(1) <= minRight2(4) ✓
  maxLeft2(2) <= minRight1(3) ✓
  → valid partition!

Total even → median = (max(1,2) + min(3,4)) / 2 = (2 + 3) / 2 = 2.5 ✓
```

**Complexity:**
- Time: O(log(min(m, n))) — binary search on the shorter array
- Space: O(1) — only pointer variables

**Code:**
```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    half = (m + n) // 2
    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = half - i

        maxLeft1  = float('-inf') if i == 0 else nums1[i - 1]
        minRight1 = float('inf')  if i == m else nums1[i]
        maxLeft2  = float('-inf') if j == 0 else nums2[j - 1]
        minRight2 = float('inf')  if j == n else nums2[j]

        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            if (m + n) % 2 == 1:
                return float(min(minRight1, minRight2))
            return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0
        elif maxLeft1 > minRight2:
            right = i - 1
        else:
            left = i + 1
```

---

## Solution Breakdown — Step by Step

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    half = (m + n) // 2
    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = half - i

        maxLeft1  = float('-inf') if i == 0 else nums1[i - 1]
        minRight1 = float('inf')  if i == m else nums1[i]
        maxLeft2  = float('-inf') if j == 0 else nums2[j - 1]
        minRight2 = float('inf')  if j == n else nums2[j]

        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            if (m + n) % 2 == 1:
                return float(min(minRight1, minRight2))
            return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0
        elif maxLeft1 > minRight2:
            right = i - 1
        else:
            left = i + 1
```

**Line by line:**

`if len(nums1) > len(nums2): nums1, nums2 = nums2, nums1`
- Always binary search on the shorter array — reduces search space and prevents `j` from going out of bounds

`half = (m + n) // 2`
- The left half of the merged array always has exactly this many elements

`i = (left + right) // 2`
- `i` is the number of elements we take from `nums1` into the left half

`j = half - i`
- The remaining elements in the left half come from `nums2`

`maxLeft1 = float('-inf') if i == 0 else nums1[i - 1]`
- Edge case: if we take zero elements from `nums1`, treat the left boundary as -∞

`minRight1 = float('inf') if i == m else nums1[i]`
- Edge case: if we take all elements from `nums1`, treat the right boundary as +∞

`if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:`
- Both cross-conditions must hold — this is what makes the partition valid

`return float(min(minRight1, minRight2))`
- Odd total: median is the smallest element in the right half

`return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0`
- Even total: average of the largest in the left half and smallest in the right half

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (merge + sort) | O((m+n) log(m+n)) | O(m+n) |
| Optimal (binary search on partition) | O(log(min(m,n))) | O(1) |

---

## Common Mistakes

**1. Not swapping to ensure nums1 is shorter**
```python
# WRONG — j can become negative if nums1 is longer
i = (0 + len(nums1)) // 2
j = half - i  # may be negative if m > n
```
Always swap so that `m <= n`. This guarantees `j` stays in `[0, n]`.

**2. Using wrong boundary sentinels**
```python
# WRONG — using 0 instead of -inf / inf breaks the comparison
maxLeft1 = 0 if i == 0 else nums1[i - 1]
```
Use `float('-inf')` and `float('inf')` — the boundary comparison must be safe
even when one side contributes no elements.

**3. Adjusting the wrong pointer**
```python
# WRONG — when maxLeft1 > minRight2, i is too big, move right
left = i + 1   # should be: right = i - 1
```
If `maxLeft1 > minRight2`, `nums1`'s partition is too far right — decrease `i`.

**4. Off-by-one in `left` and `right` initialization**
```python
left, right = 0, m - 1  # WRONG — i == m must be reachable (take all of nums1)
```
Initialize `right = m`, not `m - 1`.

---

## Pattern Recognition

### How to Recognize
- Two sorted arrays, need a combined property in O(log n)
- Problem involves finding a specific rank/position across merged data
- Merging is too expensive — the sorted property must be exploited

### How to Identify
- Can you express the answer as "pick `i` elements from array 1 and `j` from array 2"?
- Does binary searching on the partition point satisfy the O(log n) constraint?

### How to Remember
> **Mental model:** Don't merge — partition. Binary search for the right cut point across both arrays simultaneously.

**Similar problems:**
- **Kth Smallest Element in a Sorted Matrix** — same idea extended to 2D
- **Find K-th Smallest Pair Distance** — binary search on the answer value
- **Split Array Largest Sum** — binary search on the answer, not an index

---

## Real World Use Cases

### 1. Distributed statistics aggregation
Data warehouses that process sorted event streams from multiple sources (e.g.,
two data centers sorted by timestamp) need to compute quantiles without merging
petabytes. The partition-based approach computes the median in O(log n) per query.

### 2. Real-time sensor fusion
In autonomous vehicles, two LiDAR sensors produce sorted distance readings. Computing
the median reading (to filter noise) in real time requires O(log n) rather than
sorting the combined feed.

### 3. Merge-sort based distributed search
Search engines that maintain sorted inverted index shards use the same partition
logic to find the globally-ranked kth document across shards without full merges.

---

## Key Takeaways

- The median partitions the merged array into two equal halves — binary search for the right partition instead of building the array
- Always binary search on the shorter array to keep `j` in bounds
- Four boundary values (`maxLeft1`, `minRight1`, `maxLeft2`, `minRight2`) define whether the partition is valid
- Edge cases (`i == 0` or `i == m`) require `-∞` / `+∞` sentinels
- This is the hardest application of binary search in the Blind 75 — master the partition invariant

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #4](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Median of Two Sorted Arrays | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
