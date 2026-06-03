# 46. Permutations

**LeetCode:** [https://leetcode.com/problems/permutations/](https://leetcode.com/problems/permutations/)
**Difficulty:** Medium
**Topics:** [Backtracking] [Array]

---

## Problem Statement

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

A permutation is an arrangement of all elements where order matters.

### Constraints
- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All integers of `nums` are unique

### Example
```
Input:  nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Input:  nums = [0,1]
Output: [[0,1],[1,0]]

Input:  nums = [1]
Output: [[1]]
```

---

## How to Think About This Problem

### Step 1 — Understand what permutations are
Permutations are all possible orderings of elements. For n elements, there are n! permutations. Order matters (unlike combinations).

### Step 2 — Recognize the recursive structure
To build permutations of [1,2,3]:
- Choose 1 first, then find all permutations of [2,3]
- Choose 2 first, then find all permutations of [1,3]
- Choose 3 first, then find all permutations of [1,2]

### Step 3 — Identify backtracking pattern
Choose a number → recursively build rest → backtrack (undo choice) → try next number.

### Step 4 — Implement base case and recursive case
Base: when all numbers are chosen, add to result. Recursive: for each remaining number, choose it and recurse.

---

## Approaches

### Approach 1 — Backtracking (Using Remaining List)
**Intuition:** Build permutations by choosing one element at a time from remaining elements.

**Steps:**
1. Base case: if no remaining elements, add current path to result
2. For each element in remaining:
   - Choose: add to path
   - Explore: recursively build with remaining elements
   - Unchoose: remove from path (backtrack)

**Illustration:** Building permutations of [1,2,3]
```
backtrack([], [1,2,3])
├─ Choose 1: backtrack([1], [2,3])
│  ├─ Choose 2: backtrack([1,2], [3])
│  │  └─ Choose 3: backtrack([1,2,3], []) -> add [1,2,3]
│  └─ Choose 3: backtrack([1,3], [2])
│     └─ Choose 2: backtrack([1,3,2], []) -> add [1,3,2]
├─ Choose 2: backtrack([2], [1,3])
│  ├─ Choose 1: backtrack([2,1], [3])
│  │  └─ Choose 3: backtrack([2,1,3], []) -> add [2,1,3]
│  └─ Choose 3: backtrack([2,3], [1])
│     └─ Choose 1: backtrack([2,3,1], []) -> add [2,3,1]
└─ ... and so on
```

**Complexity:** Time O(n! * n) - n! permutations, n work per permutation / Space O(n!)

---

### Approach 2 — Backtracking (Using Swapping)
**Intuition:** More efficient - swap elements in-place instead of creating new lists.

**Steps:**
1. Base case: if we've placed all elements, add a copy to result
2. For each position from current to end:
   - Swap current with position
   - Recursively build the rest
   - Swap back (undo)

**Illustration:** Same problem with swapping
```
Array: [1,2,3]

Swap pos 0: [1,2,3] -> backtrack([1,2,3], 1)
├─ Swap pos 1: [1,2,3] -> backtrack([1,2,3], 2)
│  └─ Swap pos 2: [1,2,3] -> backtrack([1,2,3], 3)
│     └─ All positioned, add [1,2,3]
├─ Swap pos 2: [1,3,2] -> backtrack([1,3,2], 2)
│  └─ All positioned, add [1,3,2]

Swap pos 1: [2,1,3] -> backtrack([2,1,3], 1)
├─ Swap pos 1: [2,1,3] -> backtrack([2,1,3], 2)
│  └─ All positioned, add [2,1,3]
└─ ... and so on
```

**Complexity:** Time O(n! * n) / Space O(n!) but slightly more efficient in practice

---

## Solution Breakdown — Step by Step

### Approach 1: Using Remaining List
```python
def permute(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:  # Base case: all numbers used
            result.append(path[:])  # Add a copy of path
            return
        
        for i in range(len(remaining)):
            # Choose: take element at index i
            path.append(remaining[i])
            
            # Explore: recurse with remaining elements
            new_remaining = remaining[:i] + remaining[i+1:]
            backtrack(path, new_remaining)
            
            # Unchoose: backtrack
            path.pop()
    
    backtrack([], nums)
    return result
```

**Line-by-line:**
- `if not remaining: result.append(path[:])`: Add complete permutation (copy path!)
- `for i in range(len(remaining))`: Try each remaining element
- `path.append(remaining[i])`: Choose this element
- `new_remaining = remaining[:i] + remaining[i+1:]`: Create list without this element
- `backtrack(path, new_remaining)`: Recursively build rest
- `path.pop()`: Undo choice (backtrack)

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Backtracking (List) | O(n! * n) | O(n!) |
| Backtracking (Swap) | O(n! * n) | O(n!) |

---

## Common Mistakes

### Mistake 1 — Forgetting to copy the path
❌ **Wrong:**
```python
if not remaining:
    result.append(path)  # Adds reference, not copy!
    # Later modifications to path affect all results
```

✅ **Correct:**
```python
if not remaining:
    result.append(path[:])  # Add copy of path
    # or result.append(list(path))
```

### Mistake 2 — Not backtracking
❌ **Wrong:**
```python
for i in range(len(remaining)):
    path.append(remaining[i])
    backtrack(path, new_remaining)
    # Missing: path.pop() - now path has extra elements
```

✅ **Correct:**
```python
for i in range(len(remaining)):
    path.append(remaining[i])
    backtrack(path, new_remaining)
    path.pop()  # Essential! Reset for next iteration
```

### Mistake 3 — Creating new list incorrectly
❌ **Wrong:**
```python
new_remaining = remaining.remove(remaining[i])
# remove() returns None, not the modified list!
```

✅ **Correct:**
```python
new_remaining = remaining[:i] + remaining[i+1:]
# or: new_remaining = [x for j, x in enumerate(remaining) if j != i]
```

---

## Pattern Recognition

> Use this pattern when you see: Generate all permutations, arrangements, orderings, or any problem requiring exploration of all possibilities.

**Similar problems:**
- LeetCode 47: Permutations II (with duplicates)
- LeetCode 77: Combinations
- LeetCode 39: Combination Sum
- LeetCode 78: Subsets

---

## Real World Use Cases

### 1. Task Scheduling
Given tasks, find all possible execution orders (respecting dependencies).

### 2. Tournament Brackets
Generate all possible seeding orders or bracket arrangements for competitions.

### 3. Password Testing
Security testing explores all possible character orderings to test strength against permutation-based attacks.

---

## Key Takeaways

- Permutations require exploring all n! orderings - backtracking is the natural approach
- Always copy results when adding to result list (append by reference is common bug)
- Remember to backtrack (undo) after recursing - this resets state for next iteration
- With duplicates, sorting and skipping repeated choices becomes necessary
- Backtracking pattern: Choose → Explore → Unchoose

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #46](https://leetcode.com/problems/permutations/) | Permutations | Medium |
| [LeetCode #47](https://leetcode.com/problems/permutations-ii/) | Permutations II | Medium |
| [LeetCode #77](https://leetcode.com/problems/combinations/) | Combinations | Medium |

> Fundamental backtracking problem — master this pattern for all backtracking problems.
