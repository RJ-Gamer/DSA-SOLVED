# LeetCode Problem # 1299: Replace Elements with Greatest Element on Right Side

**LeetCode:** [Problem #1299](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)  
**Difficulty:** Easy  
**Topics:** `Array`

---

## Problem Statement

Given an array `arr`, replace every element in that array with the **greatest element** among the elements to its right, and replace the last element with `-1`.

After doing so, return the array.

**Constraints:**
- `1 <= arr.length <= 10⁴`
- `1 <= arr[i] <= 10⁵`

### Example
```
Input:  arr = [17, 18, 5, 4, 6, 1]
Output: [18, 6, 6, 6, 1, -1]
Explanation: 
- index 0 --> greatest element to the right of 17 is 18.
- index 1 --> greatest element to the right of 18 is 6.
- index 2 --> greatest element to the right of 5 is 6.
- index 3 --> greatest element to the right of 4 is 6.
- index 4 --> greatest element to the right of 6 is 1.
- index 5 --> there are no elements to the right of 1, so we put -1.
```

```
Input:  arr = [400]
Output: [-1]
Explanation: There are no elements to the right of index 0.
```

---

## How to Think About This Problem

This problem is a classic example of where the **direction of iteration** changes everything.

### Step 1 — Understand what's being asked

For every position `i`, we need the maximum of `arr[i+1], arr[i+2], ..., arr[n-1]`.

If we look at it from left to right, for every element, we'd have to scan the entire remaining array to find the maximum. This feels repetitive.

### Step 2 — Identify the redundancy

When we move from index `i` to `i+1`, the set of "elements to the right" only changes by *removing* `arr[i+1]`.
However, finding a new maximum after removing an element is hard. 

**What if we go backwards?**
When we move from index `i` to `i-1` (right to left), the set of "elements to the right" changes by *adding* `arr[i]`.
Finding a new maximum after adding an element is easy: `new_max = max(old_max, added_element)`.

### Step 3 — Think about state

We need to remember one thing as we walk backwards: **What is the largest number we have seen so far?**

### Step 4 — Build the intuition

Imagine you are standing at the end of a line of people of different heights. You walk towards the front of the line. At each person:
1. You tell them the height of the tallest person you've seen *behind* them.
2. You then check if the current person is taller than your current "tallest seen" and update your memory if they are.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** For every element, scan everything to its right to find the max.

**Steps:**
1. Loop `i` from `0` to `n-1`.
2. For each `i`, start a second loop `j` from `i+1` to `n-1`.
3. Find the max in that sub-range.
4. Replace `arr[i]` with that max.
5. Set the last element to `-1`.

**Complexity:**
- Time: O(n²) — nested loops, searching for max takes O(n) for each of the n elements.
- Space: O(1) — modifying in place.

---

### Approach 2 — Optimal (Reverse Iteration)

**Intuition:** Iterate from right to left, maintaining the "greatest seen so far".

**Steps:**
1. Initialize `greatest_so_far = -1`.
2. Start from the last index and move to the first.
3. For the current element `arr[i]`:
    - Save its original value in a `temp` variable.
    - Set `arr[i] = greatest_so_far`.
    - Update `greatest_so_far = max(greatest_so_far, temp)`.
4. Return the modified array.

**Illustration:**
```
arr = [17, 18, 5, 4, 6, 1], greatest_so_far = -1

i = 5 (val: 1)
  temp = 1
  arr[5] = -1
  greatest_so_far = max(-1, 1) = 1
  arr is now [17, 18, 5, 4, 6, -1]

i = 4 (val: 6)
  temp = 6
  arr[4] = 1
  greatest_so_far = max(1, 6) = 6
  arr is now [17, 18, 5, 4, 1, -1]

i = 3 (val: 4)
  temp = 4
  arr[3] = 6
  greatest_so_far = max(6, 4) = 6
  ...and so on
```

**Complexity:**
- Time: O(n) — single pass through the array.
- Space: O(1) — we only use a few variables regardless of array size.

---

## Solution Breakdown — Step by Step

```python
def replaceElements(arr: List[int]) -> List[int]:
    # 1. Initialize the 'right-side max' for the very last element
    greatest_so_far = -1

    # 2. Iterate backwards from the end of the array to the start
    for i in range(len(arr) - 1, -1, -1):
        # 3. Keep track of current value before we overwrite it
        current_val = arr[i]

        # 4. Replace current element with the max of elements to its right
        arr[i] = greatest_so_far

        # 5. Update the max for the NEXT element (the one to our left)
        # It will be the max of the current element we just processed
        # and the max of everything to its right.
        if current_val > greatest_so_far:
            greatest_so_far = current_val

    return arr
```

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (Forward) | O(n²) | O(1) |
| Optimal (Backward) | O(n) | O(1) |

---

## Common Mistakes

**1. Overwriting the max before using it**
If you update `greatest_so_far` using `arr[i]` *before* you assign the old `greatest_so_far` to `arr[i]`, you'll be including the current element in its own "right side max" calculation.

**2. Off-by-one in range**
When iterating backwards in Python, `range(start, stop, step)` stops *before* the `stop` value. To include index `0`, you must use `-1` as the `stop` value.

---

## Pattern Recognition

### How to Recognize
- The result for each element depends on elements to its right (a suffix property)
- Iterating left-to-right requires re-scanning from each position — O(n²)
- Keywords: "replace with greatest/smallest on right", "next greater element", "suffix max/min"

### How to Identify
- Does iterating right-to-left let you maintain a running maximum you already know?
- When moving left by one step, does the new "right side" simply add one more element?

### How to Remember
> **Mental model:** Walk backwards and carry the max — by the time you arrive, you already know the answer

**Similar problems:**
- **Next Greater Element I/II** — same right-to-left scan with a stack
- **Daily Temperatures** — find next warmer day; same suffix-scan thinking
- **Trapping Rain Water** — precompute left-max and right-max arrays using the same reverse pass

---

## Real World Use Cases

### 1. Stock Market "Sell High" analysis
If you want to know, for every day in the past, what the highest price was *after* that day (to see how much profit you missed out on), this is exactly the algorithm you'd use.

### 2. Leaderboard/Ranking Systems
Identifying "leaders" in a stream of data where a leader is someone who has a higher score than everyone who came after them.

### 3. Rendering Engines
In some 2D rendering scenarios, you might need to know the highest Z-index (layer) of objects "behind" or "to the side" of a current object to determine visibility or shadows.

---

## Key Takeaways

- **Direction Matters:** Sometimes a problem that is hard from left-to-right is trivial from right-to-left.
- **In-place updates:** We saved space by modifying the input array directly.
- **Temporary storage:** When overwriting data you'll need for the next step, a `temp` variable is your best friend.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #1299](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/) | Replace Elements with Greatest Element on Right Side | Easy |
