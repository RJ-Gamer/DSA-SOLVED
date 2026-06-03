# 215. Kth Largest Element in an Array

**LeetCode:** [Problem #215](https://leetcode.com/problems/kth-largest-element-in-an-array/)  
**Difficulty:** Medium  
**Topics:** `Heap` `Quick Select` `Sorting`

---

## Problem Statement

Given an integer array `nums` and an integer `k`, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

### Constraints
- `1 <= k <= nums.length <= 3 * 10^4`
- `-10^4 <= nums[i] <= 10^4`

### Example
```
Input:  nums = [3,2,1,5,6,4], k = 2
Output: 5

Input:  nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

Input:  nums = [1], k = 1
Output: 1
```

---

## How to Think About This Problem

### Step 1 — Understand what "kth largest" means
It's not kth distinct, so duplicates count. For `[3,2,1,5,6,4]` sorted descending: `[6,5,4,3,2,1]`, the 2nd largest is 5.

### Step 2 — Identify three approaches
1. Sort and pick (simple, O(n log n))
2. Use a heap of size k (efficient, O(n log k))
3. Quick select (optimal average, O(n) on average)

### Step 3 — Choose based on constraints
For most interviews, heap approach balances simplicity and efficiency.

### Step 4 — Implement your chosen approach
Each has different tradeoffs in code complexity and space.

---

## Approaches

### Approach 1 — Min Heap of Size k (Most Practical)
**Intuition:** Maintain a min heap of k largest elements. When heap size > k, remove the smallest (heap root). Final root is kth largest.

**Why min heap?** We need the smallest in our k elements (the kth largest), so min heap makes it easy to remove.

**Steps:**
1. Create empty heap
2. For each number:
   - Add to heap
   - If heap size > k, remove heap minimum
3. After processing all, heap top is kth largest

**Illustration:** For `nums=[3,2,1,5,6,4]`, k=2
```
Add 3: heap=[3], size=1
Add 2: heap=[2,3], size=2
Add 1: heap=[1,3,2], size=3 > k=2, remove min -> heap=[2,3]
Add 5: heap=[2,3,5], size=3 > k=2, remove min -> heap=[3,5]
Add 6: heap=[3,5,6], size=3 > k=2, remove min -> heap=[5,6]
Add 4: heap=[4,5,6], size=3 > k=2, remove min -> heap=[5,6]

Return heap[0] = 5 ✓
```

**Complexity:** Time O(n log k) - n adds, each is O(log k) / Space O(k)

---

### Approach 2 — Sorting (Simplest)
**Intuition:** Sort in descending order, return kth element.

**Steps:**
1. Sort array in descending order
2. Return element at index k-1

**Complexity:** Time O(n log n) / Space O(1) if in-place, O(n) if not

---

### Approach 3 — Quick Select (Most Optimal Average)
**Intuition:** Like quicksort but stop early. Partition until pivot is at position (n-k).

**Steps:**
1. Randomly pick pivot
2. Partition: smaller on left, larger on right
3. If pivot at index n-k, return pivot value
4. If pivot index < n-k, search right
5. If pivot index > n-k, search left

**Complexity:** Time O(n) average, O(n²) worst / Space O(1)

---

## Solution Breakdown — Step by Step

### Min Heap Solution (Most Practical)
```python
import heapq

def findKthLargest(nums, k):
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)  # Add to heap
        
        if len(heap) > k:
            heapq.heappop(heap)     # Remove smallest (heap min)
    
    return heap[0]                  # Return kth largest
```

**Line-by-line:**
- `heap = []`: Initialize empty min heap
- `for num in nums`: Process each number
- `heapq.heappush(heap, num)`: Add number to heap (maintains heap property)
- `if len(heap) > k`: If heap exceeds k elements
- `heapq.heappop(heap)`: Remove heap minimum (smallest of our k)
- `return heap[0]`: Root of min heap is kth largest element

**Why this works:**
- After processing all numbers, heap contains k largest elements
- Min heap root is the smallest of those k elements
- Which is exactly the kth largest!

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Sorting | O(n log n) | O(1) |
| Min Heap | O(n log k) | O(k) |
| Quick Select | O(n) avg | O(1) |

---

## Common Mistakes

### Mistake 1 — Using max heap instead of min heap
❌ **Wrong:**
```python
heap = []
for num in nums:
    heapq.heappush(heap, -num)  # Max heap simulation
    # Problem: heap grows unbounded, we don't remove anything
```

✅ **Correct:**
```python
heap = []
for num in nums:
    heapq.heappush(heap, num)   # Min heap
    if len(heap) > k:
        heapq.heappop(heap)     # Remove smallest to keep k largest
```

### Mistake 2 — Returning wrong element
❌ **Wrong:**
```python
nums.sort()
return nums[k]  # Off by one! Should be k-1 for 0-indexed
```

✅ **Correct:**
```python
nums.sort(reverse=True)
return nums[k-1]  # kth largest at index k-1
```

### Mistake 3 — Not understanding heap property
❌ **Wrong:**
```python
heap = []
for num in nums:
    heapq.heappush(heap, num)
# If len(heap) == k, return heap[0]
# This works but inefficient - why not remove smaller elements?
```

✅ **Correct:**
```python
# Keep heap at size k, removing smallest to keep only k largest
if len(heap) > k:
    heapq.heappop(heap)
```

---

## Pattern Recognition

### How to Recognize
- Problem asks for the kth largest or smallest element, or the top k elements
- Full sorting is possible but the constraint hints at a more efficient approach
- k is much smaller than n

### How to Identify
- Can you maintain a min-heap of exactly k elements, evicting the smallest when size exceeds k?
- After processing all elements, does the heap root hold the kth largest?

### How to Remember
> **Mental model:** Keep the top k in a min heap — kick out the weakest until only the elite remain

**Similar problems:**
- LeetCode 347: Top K Frequent Elements
- LeetCode 703: Kth Largest Element in a Stream
- LeetCode 692: Top K Frequent Words

---

## Real World Use Cases

### 1. Leaderboards
Gaming systems efficiently maintain top k players without storing entire rankings.

### 2. Stream Processing
Continuously find top k items in an infinite stream without storing all items.

### 3. Database Query Optimization
Find top k results efficiently instead of sorting entire dataset.

---

## Key Takeaways

- Min heap approach maintains exactly k largest elements, removing smallest as needed
- Heap gives O(n log k) which beats sorting's O(n log n) for small k
- Quick select is theoretically optimal O(n) average but more complex to implement
- For kth largest, use min heap (smallest of the k); for kth smallest, use max heap
- Three valid approaches with different complexity tradeoffs

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Kth Largest Element in an Array | Medium |
| [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | Top K Frequent Elements | Medium |
| [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Kth Largest Element in a Stream | Easy |

> Demonstrates heap efficiency — essential for optimization interview questions.
