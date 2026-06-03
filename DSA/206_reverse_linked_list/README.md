# 206. Reverse Linked List

**LeetCode:** [Problem #206](https://leetcode.com/problems/reverse-linked-list/)  
**Difficulty:** Easy  
**Topics:** `Linked List` `Recursion`

---

## Problem Statement

Given the `head` of a singly linked list, reverse the list, and return the reversed list.

### Constraints
- The number of nodes in the list is the range `[0, 5000]`
- `-5000 <= Node.val <= 5000`

### Example
```
Input:  head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Input:  head = [1,2]
Output: [2,1]

Input:  head = []
Output: []
```

---

## How to Think About This Problem

### Step 1 — Visualize what reversal means
In a linked list, each node points to the next node. Reversing means each node should point to the previous node instead.

### Step 2 — Understand the pointer manipulation
To reverse:
- Current node's `next` should point to the previous node
- But we need to save the next node before changing the pointer, or we'll lose it
- Move forward after reversing the current node

### Step 3 — Choose your approach
Two main ways: iterative (change pointers as you go) or recursive (let recursion handle the traversal, then fix pointers on the way back).

### Step 4 — Trace through manually
Always trace a small example (3-4 nodes) to verify logic before coding.

---

## Approaches

### Approach 1 — Iterative (Optimal)
**Intuition:** Maintain three pointers: previous, current, and next. Reverse as you traverse.

**Steps:**
1. Initialize `prev = None`, `current = head`
2. While `current` exists:
   - Save `next_node = current.next` (don't lose it!)
   - Reverse: `current.next = prev`
   - Move forward: `prev = current`, `current = next_node`
3. Return `prev` (new head)

**Illustration:** Reversing `1 -> 2 -> 3 -> None`
```
Initial:  prev=None, current=1
          1 -> 2 -> 3 -> None

Step 1:   prev=1, current=2
          None <- 1    2 -> 3 -> None

Step 2:   prev=2, current=3
          None <- 1 <- 2    3 -> None

Step 3:   prev=3, current=None
          None <- 1 <- 2 <- 3

Return prev (3) which is the new head
```

**Complexity:** Time O(n) / Space O(1)

---

### Approach 2 — Recursive
**Intuition:** Recursively reach the end, then reverse pointers on the way back.

**Steps:**
1. Base case: if `head` is None or has no next node, return `head`
2. Recursively reverse the rest of the list: `new_head = reverse(head.next)`
3. Make `head.next.next = head` (the next node points back to current)
4. Break the old link: `head.next = None`
5. Return `new_head`

**Illustration:** Same list, recursive approach
```
Recursion goes down:
  reverse(1) -> reverse(2) -> reverse(3) -> return 3

Coming back up:
  3.next = 3 (no change)
  2.next.next = 2, so 3->2, then 2.next = None
  1.next.next = 1, so 2->1, then 1.next = None
  
Result: 3 -> 2 -> 1 -> None
```

**Complexity:** Time O(n) / Space O(n) due to recursion stack

---

## Solution Breakdown — Step by Step

### Iterative Solution
```python
def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None          # Previous node (initially nothing)
    current = head       # Start at head
    
    while current:       # While there are nodes to process
        next_temp = current.next  # Save next node (DON'T LOSE IT)
        current.next = prev       # Reverse: point to previous
        prev = current            # Move prev forward
        current = next_temp       # Move current forward
    
    return prev          # New head is prev
```

**Line-by-line:**
- `prev = None`: Starting with no previous node
- `current = head`: Current starts at head
- `next_temp = current.next`: Save the next node before we change current.next
- `current.next = prev`: Reverse the pointer
- `prev = current`: Move prev to current position
- `current = next_temp`: Move current to saved next
- `return prev`: prev is now the head of reversed list

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Iterative | O(n) | O(1) |
| Recursive | O(n) | O(n) |

---

## Common Mistakes

### Mistake 1 — Losing the next node
❌ **Wrong:**
```python
current.next = prev  # Changed the pointer
next_node = current.next  # Already lost! This is None or prev
```

✅ **Correct:**
```python
next_node = current.next  # Save BEFORE changing
current.next = prev       # Now change safely
```

### Mistake 2 — Infinite loop in recursion
❌ **Wrong:**
```python
head.next.next = head
head.next = None
return reverseList(head)  # Recursing again? Why?
```

✅ **Correct:**
```python
head.next.next = head
head.next = None
return new_head  # Return the actual new head from recursion
```

---

## Pattern Recognition

### How to Recognize
- Problem requires reversing a linked list or redirecting its pointers
- In-place pointer manipulation is expected (O(1) extra space)
- Need to traverse the list while modifying direction

### How to Identify
- Do you need three pointers (`prev`, `cur`, `next`) to safely flip each link without losing the chain?
- Does the recursive solution fix pointers on the way back up the call stack?

### How to Remember
> **Mental model:** Save next, flip arrow, slide forward — never lose the thread

**Similar problems:**
- LeetCode 92: Reverse Linked List II (reverse only part)
- LeetCode 25: Reverse Nodes in k-Group
- LeetCode 206 with recursion variations

---

## Real World Use Cases

### 1. Undo Functionality
Many applications use linked lists for undo stacks. Reversing helps display history in correct order.

### 2. Polynomial Arithmetic
Polynomials stored in linked lists (lowest to highest degree or vice versa) often need reversal for specific operations.

### 3. Network Packet Processing
Some protocols process packets in reverse order; linked list reversal enables efficient reordering.

---

## Key Takeaways

- Always save the next node before modifying the current node's pointer
- Iterative approach is generally preferred (O(1) space) over recursive (O(n) space)
- Pointer manipulation requires careful thinking; manual tracing prevents bugs
- Understanding linked list reversal is fundamental for many advanced list problems

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #206](https://leetcode.com/problems/reverse-linked-list/) | Reverse Linked List | Easy |
| [LeetCode #92](https://leetcode.com/problems/reverse-linked-list-ii/) | Reverse Linked List II | Medium |
| [LeetCode #25](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Reverse Nodes in k-Group | Hard |

> Fundamental linked list problem — appears in nearly every interview.
