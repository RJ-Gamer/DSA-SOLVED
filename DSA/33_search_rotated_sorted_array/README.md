# 33. Search in Rotated Sorted Array

**LeetCode:** [Problem #33](https://leetcode.com/problems/search-in-rotated-sorted-array/)  
**Difficulty:** Medium  
**Topics:** `Binary Search` `Array`

---

## Problem Statement

Suppose an array sorted in ascending order is rotated at some unknown pivot. For example, `[0,1,2,4,5,6,7]` might become `[4,5,6,7,0,1,2]`.

You are given the rotated array `nums` and an integer `target`. Return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

### Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is sorted and rotated at some unknown pivot.
- `-10^4 <= target <= 10^4`

### Example
```
Input:  nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Input:  nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Input:  nums = [1], target = 1
Output: 0
```

---

## How to Think About This Problem

### Step 1 — Understand what makes this special
This is NOT a simple sorted array. It's rotated at an unknown point. The key insight is that even though the entire array isn't sorted, **one half of it is always sorted at any point during binary search**.

### Step 2 — Identify which half is sorted
At each binary search step, we can determine which half is sorted by comparing `nums[left]`, `nums[mid]`, and `nums[right]`.

### Step 3 — Use the sorted half to eliminate possibilities
If one half is sorted, we can check if the target is within that sorted half's range. If it is, search there. If not, search the other half.

### Step 4 — Standard binary search framework
Apply binary search principles with the twist that we first determine which half is sorted before deciding where to search next.

---

## Approaches

### Approach 1 — Brute Force (Not Optimal)
**Intuition:** Linear search through the array.

**Steps:**
1. Iterate through the array
2. Return index if target is found
3. Return -1 if not found

**Complexity:** Time O(n) / Space O(1)

This violates the O(log n) requirement, so it's not acceptable.

---

### Approach 2 — Binary Search (Optimal)
**Intuition:** Determine which half is sorted, then check if target is in that range.

**Steps:**
1. Initialize `left = 0`, `right = len(nums) - 1`
2. While `left <= right`:
   - Calculate `mid = (left + right) // 2`
   - If `nums[mid] == target`, return `mid`
   - Determine which half is sorted:
     - If `nums[left] <= nums[mid]`: left half is sorted
     - Otherwise: right half is sorted
   - Check if target is within the sorted half's range
   - Adjust pointers accordingly
3. Return -1 if target not found

**Illustration:** For `[4,5,6,7,0,1,2]`, target = `0`
```
         left=0, right=6, mid=3
         nums[mid]=7, not target
         Left half [4,5,6,7] is sorted
         target(0) not in [4,7] range
         Move to right half
         
         left=4, right=6, mid=5
         nums[mid]=1, not target
         Right half [0,1,2] is sorted
         target(0) is in [0,2] range
         
         left=4, right=4, mid=4
         nums[mid]=0, found!
         Return 4
```

**Complexity:** Time O(log n) / Space O(1)

---

## Solution Breakdown — Step by Step

```python
def search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Found target
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # Left half is sorted
            # Check if target is in the sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # Search left
            else:
                left = mid + 1   # Search right
        
        else:  # Right half is sorted
            # Check if target is in the sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # Search right
            else:
                right = mid - 1  # Search left
    
    return -1
```

**Line-by-line:**
- `left, right = 0, len(nums) - 1`: Initialize binary search pointers
- `while left <= right`: Continue while search space exists
- `mid = (left + right) // 2`: Find midpoint
- `if nums[mid] == target: return mid`: Early exit if found
- `if nums[left] <= nums[mid]`: Check if left half is sorted
- `if nums[left] <= target < nums[mid]`: Is target in the sorted left range?
- `right = mid - 1`: Move right pointer to search left half
- `left = mid + 1`: Move left pointer to search right half
- `return -1`: Target not found

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force | O(n) | O(1) |
| Binary Search | O(log n) | O(1) |

---

## Common Mistakes

### Mistake 1 — Comparing with wrong boundary
❌ **Wrong:**
```python
if nums[mid] < target <= nums[right]:  # Wrong boundary
    left = mid + 1
```

✅ **Correct:**
```python
if nums[mid] < target <= nums[right]:  # Use < not <=
    left = mid + 1
```

### Mistake 2 — Not handling the rotation point
❌ **Wrong:** Assuming the array is fully sorted
```python
if target > nums[mid]:
    left = mid + 1  # This doesn't work for rotated arrays
```

✅ **Correct:** First determine which half is sorted
```python
if nums[left] <= nums[mid]:  # Check which half is sorted
    if nums[left] <= target < nums[mid]:
        right = mid - 1
```

---

## Pattern Recognition

### How to Recognize
- O(log n) search is required on a sorted array with a twist
- The array is sorted but rotated (shifted) at an unknown pivot
- You need to find an element without a linear scan

### How to Identify
- At any binary search midpoint, is exactly one half always fully sorted?
- Can you use the sorted half's range to determine which half to eliminate?

### How to Remember
> **Mental model:** In a rotation, one half always behaves — search the half you can trust

**Similar problems:**
- LeetCode 81: Search in Rotated Sorted Array II (with duplicates)
- LeetCode 153: Find Minimum in Rotated Sorted Array
- Binary search variations

---

## Real World Use Cases

### 1. Database Query Optimization
When a database index is rotated (stored in circular buffers), binary search helps find records efficiently without scanning the entire dataset.

### 2. Inventory Management
In rotated circular buffers storing inventory data, finding items quickly is crucial for real-time systems.

### 3. Time Series Analysis
Historical data stored in circular buffers (rotating based on time) needs efficient search for specific time periods.

---

## Key Takeaways

- Rotated sorted arrays still maintain sortedness in at least one half at any given time
- Binary search is still O(log n) even with rotation; key is identifying which half is sorted
- Always compare target with the boundaries of the sorted half, not with the middle value alone
- The "rotated" property is the twist that makes this problem harder than standard binary search

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #33](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Search in Rotated Sorted Array | Medium |
| [LeetCode #81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | Search in Rotated Sorted Array II | Medium |
| [LeetCode #153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Find Minimum in Rotated Sorted Array | Medium |

> Part of the **Blind 75** list — essential for interview preparation.
