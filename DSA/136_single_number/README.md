# 136. Single Number

**LeetCode:** [Problem #136](https://leetcode.com/problems/single-number/)  
**Difficulty:** Easy  
**Topics:** `Bit Manipulation` `Array`

---

## Problem Statement

Given a non-empty array of integers `nums`, every element appears twice except for one element that appears once. Find that single element.

You must implement a solution with a linear time complexity and without using extra space (constant space).

### Constraints
- `1 <= nums.length <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`
- Each element in the array appears twice except for one element which appears once

### Example
```
Input:  nums = [2,2,1]
Output: 1

Input:  nums = [4,1,2,1,2]
Output: 4

Input:  nums = [1]
Output: 1
```

---

## How to Think About This Problem

### Step 1 — Identify the constraint
Every number appears exactly twice except one. This specific constraint is the key - it's not random, it's structured.

### Step 2 — Recall XOR properties
- `a ^ a = 0` (any number XORed with itself is 0)
- `a ^ 0 = a` (any number XORed with 0 is itself)
- XOR is commutative: `a ^ b ^ a = (a ^ a) ^ b = 0 ^ b = b`

### Step 3 — Connect the constraint to XOR
If we XOR all numbers together, duplicates cancel out (become 0), leaving only the single number!

### Step 4 — The solution emerges
One line: XOR all numbers, the result is the single number.

---

## Approaches

### Approach 1 — XOR Bit Manipulation (Optimal)
**Intuition:** XOR has the magical property that `a ^ a = 0` and `a ^ 0 = a`. When we XOR all numbers, pairs cancel to 0, leaving only the single number.

**Steps:**
1. Initialize result = 0
2. For each number in array: result = result ^ number
3. Return result

**Illustration:** For `[2,2,1]`
```
result = 0
result = 0 ^ 2 = 2
result = 2 ^ 2 = 0       (pair cancels)
result = 0 ^ 1 = 1       (single number remains)
Return 1
```

**For `[4,1,2,1,2]`:**
```
result = 0
result = 0 ^ 4 = 4
result = 4 ^ 1 = 5 (binary: 100 ^ 001 = 101)
result = 5 ^ 2 = 7 (binary: 101 ^ 010 = 111)
result = 7 ^ 1 = 6 (binary: 111 ^ 001 = 110, one 1 cancels)
result = 6 ^ 2 = 4 (binary: 110 ^ 010 = 100, both cancel)
Return 4
```

**Complexity:** Time O(n) / Space O(1) - no extra space!

---

### Approach 2 — Using Set (Alternative, not optimal)
**Intuition:** Add unique numbers to set, sum twice the set, subtract from total. `2 * sum(set) - sum(array) = single_number`

**Steps:**
1. Create a set of unique numbers
2. Calculate: `2 * sum(set) - sum(array)`

**Mathematical logic:**
- Let single number = s, let each duplicate be d
- `sum(set) = s + all_d_once`
- `sum(array) = s + 2*all_d_twice`
- `2*sum(set) - sum(array) = 2*(s + all_d) - (s + 2*all_d) = s`

**Complexity:** Time O(n) / Space O(n) - uses extra space, so not optimal

---

## Solution Breakdown — Step by Step

### XOR Solution
```python
def singleNumber(nums):
    result = 0              # Initialize result
    
    for num in nums:        # XOR each number
        result ^= num       # XOR assignment
    
    return result           # Single number remains
```

**Line-by-line:**
- `result = 0`: Start with 0 (neutral element for XOR)
- `for num in nums`: Iterate through each number
- `result ^= num`: XOR current number with result
  - First iteration: `0 ^ nums[0] = nums[0]`
  - When we XOR a pair: they cancel to 0
  - When we XOR the single: it remains
- `return result`: Returns the single number

**Binary View (Why it works):**
```
Example: [2, 2, 1]
2 in binary: 010
2 in binary: 010
1 in binary: 001

XOR:    010
      ^ 010
      -----
        000   (pair cancels)
      ^ 001
      -----
        001   (single number = 1)
```

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| XOR Bit Manipulation | O(n) | O(1) |
| Set Math | O(n) | O(n) |

---

## Common Mistakes

### Mistake 1 — Using wrong initialization
❌ **Wrong:**
```python
result = nums[0]  # Starting with 1st element
for num in nums[1:]:
    result ^= num
# Only works if we're lucky, not general
```

✅ **Correct:**
```python
result = 0  # Neutral element for XOR
for num in nums:
    result ^= num
# Works for all cases, handles all elements uniformly
```

### Mistake 2 — Not understanding XOR properties
❌ **Wrong:**
```python
# Thinking: "I need to track which numbers are duplicated"
seen = set()
for num in nums:
    if num in seen:
        # ... try to track duplicates
```

✅ **Correct:**
```python
# Let XOR handle it automatically
result = 0
for num in nums:
    result ^= num
```

---

## Pattern Recognition

### How to Recognize
- Every element appears exactly twice except one (or a similar pairing constraint)
- O(1) space is required — no hash map or extra array allowed
- The problem exploits a mathematical self-cancellation property

### How to Identify
- Does XOR's `a ^ a = 0` and `a ^ 0 = a` mean all pairs cancel out, leaving only the singleton?
- Can you fold the entire array into a single value by XOR-ing all elements?

### How to Remember
> **Mental model:** XOR is a self-destruct button for pairs — flip all, pairs vanish, singleton survives

**Similar problems:**
- LeetCode 260: Single Number III (two single numbers)
- LeetCode 137: Single Number II (element appears 3 times)
- LeetCode 268: Missing Number (variation with XOR)

---

## Real World Use Cases

### 1. Error Detection
XOR is used in error detection/correction codes (checksums, parity bits).

### 2. Efficient Swapping
Swap two variables without temp: `a ^= b; b ^= a; a ^= b`

### 3. Memory Efficient Algorithms
When space is critical, XOR tricks help solve problems with O(1) memory.

---

## Key Takeaways

- XOR properties: `a ^ a = 0` and `a ^ 0 = a` are fundamental
- XOR is commutative and associative - order doesn't matter
- The constraint "one element appears once, others twice" perfectly matches XOR's cancellation property
- This solution is optimal: O(n) time, O(1) space
- Bit manipulation often provides elegant solutions to seemingly complex problems

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #136](https://leetcode.com/problems/single-number/) | Single Number | Easy |
| [LeetCode #260](https://leetcode.com/problems/single-number-iii/) | Single Number III | Medium |
| [LeetCode #137](https://leetcode.com/problems/single-number-ii/) | Single Number II | Medium |

> Elegant bit manipulation problem — demonstrates power of knowing XOR properties.
