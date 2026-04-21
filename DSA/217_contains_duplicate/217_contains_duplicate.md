# 217. Contains Duplicate

**LeetCode:** [Problem #217](https://leetcode.com/problems/contains-duplicate/)  
**Difficulty:** Easy  
**Topics:** `Array` `Hash Map`

---

## Problem Statement

Given an integer array `nums`, return `true` if any value appears **at least twice**
in the array, and return `false` if every element is distinct.

**Constraints:**
- `1 <= nums.length <= 10⁵`
- `-10⁹ <= nums[i] <= 10⁹`

### Example
```
Input:  nums = [1, 2, 3, 1]
Output: true
Explanation: 1 appears at index 0 and index 3
```

```
Input:  nums = [1, 2, 3, 4]
Output: false
Explanation: all elements are distinct
```

```
Input:  nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: true
Explanation: multiple duplicates exist
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to detect whether any number shows up more than once. The moment we find
**a single repeat**, we can return `true` immediately. If we finish scanning the
entire array without finding one, we return `false`.

Notice: we don't need to find ALL duplicates, count them, or report their positions.
We just need to answer "yes or no — does any duplicate exist?"

### Step 2 — Identify the constraint that matters

The constraint that makes this interesting is **scale**: up to 100,000 elements.
A naive approach that checks every element against every other element requires
O(n²) comparisons — up to 10 billion operations for the largest inputs. That's
too slow.

The real question becomes: **how do we check "have I seen this number before?"
in less than O(n) time per lookup?**

### Step 3 — Think about data structures

When you need fast membership testing ("is X already in my collection?"), a
**hash set** is the right tool.

- List membership check: O(n) — scans the entire list
- Hash set membership check: O(1) — computes a hash and checks one bucket

By maintaining a set of numbers we've already seen, we can answer "seen before?"
in constant time for every element.

### Step 4 — Build the intuition

Imagine you're a bouncer at a club with a guest list. As people arrive, you check
their name against your notepad. If the name is on the notepad, they've already
been in — that's a duplicate. If not, you write it down and let them through.

The notepad is your hash set. You never scan the whole notepad — you just check
the relevant entry. That's the O(1) lookup guarantee.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Compare every possible pair of elements and check if any two are equal.

**Steps:**
1. For each element at index `i`, loop through all elements at index `j > i`
2. If `nums[i] == nums[j]`, a duplicate exists — return `true`
3. If no match found after all pairs, return `false`

**Illustration:**
```
nums = [1, 2, 3, 1]

i=0 (num=1):
  j=1: 1 == 2? No
  j=2: 1 == 3? No
  j=3: 1 == 1? YES → return True ✓

(If no match:)
i=1 (num=2):
  j=2: 2 == 3? No
  j=3: 2 == 1? No
i=2 (num=3):
  j=3: 3 == 1? No
→ return False
```

**Complexity:**
- Time: O(n²) — for each of n elements, we scan up to n-1 others
- Space: O(1) — no extra data structure used

**Code:**
```python
def contains_duplicates_brute_force(nums: list[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
```

---

### Approach 2 — Optimal (Hash Set)

**Intuition:** Walk through the array once, tracking every number in a set; the
moment we encounter a number already in the set, we have our duplicate.

**Steps:**
1. Create an empty set `seen`
2. For each number in `nums`:
   - If `num` is already in `seen` → return `True`
   - Otherwise → add `num` to `seen`
3. If the loop completes → return `False`

**Illustration:**
```
nums = [1, 2, 3, 1]

num=1: seen={}       → 1 not in seen → seen={1}
num=2: seen={1}      → 2 not in seen → seen={1, 2}
num=3: seen={1, 2}   → 3 not in seen → seen={1, 2, 3}
num=1: seen={1,2,3}  → 1 IS in seen  → return True ✓
```

```
nums = [1, 2, 3, 4]

num=1: seen={}         → seen={1}
num=2: seen={1}        → seen={1, 2}
num=3: seen={1, 2}     → seen={1, 2, 3}
num=4: seen={1, 2, 3}  → seen={1, 2, 3, 4}
Loop ends             → return False ✓
```

**Complexity:**
- Time: O(n) — single pass, O(1) lookup and insert per element
- Space: O(n) — set grows up to n elements in the worst case (all unique)

**Code:**
```python
def contains_duplicates_hash_map(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

---

### Approach 3 — Length Comparison (One-Liner)

**Intuition:** A set automatically removes duplicates; if the set is smaller than
the original array, at least one duplicate existed.

**Steps:**
1. Convert `nums` to a set (all duplicates removed)
2. Compare the length of the set with the original array length
3. If lengths differ, duplicates existed

**Illustration:**
```
nums = [1, 2, 3, 1]

set(nums) = {1, 2, 3}   → length 3
len(nums) = 4

3 != 4 → True ✓

nums = [1, 2, 3, 4]

set(nums) = {1, 2, 3, 4} → length 4
len(nums) = 4

4 == 4 → False ✓
```

**Complexity:**
- Time: O(n) — building the set requires one pass
- Space: O(n) — the set holds up to n elements

**Code:**
```python
def contains_duplicates_len(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))
```

> **Note:** This approach always processes the entire array before returning,
> even if a duplicate appears at index 1. Approach 2 short-circuits on the
> first duplicate found. For most interview settings, Approach 2 is preferred.

---

## Solution Breakdown — Step by Step

```python
def contains_duplicates_hash_map(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

**Line by line:**

`seen = set()`
- A hash set that tracks every distinct number we've visited
- Unlike a list, membership testing (`in`) is O(1) — hash-based lookup
- We don't need to store indices here (contrast with Two Sum), just presence

`for num in nums:`
- Iterate directly over values — we don't need indices, so no `enumerate`
- Each iteration processes one number and makes an O(1) decision

`if num in seen:`
- O(1) hash set lookup — Python computes `hash(num)` and checks one bucket
- If this returns `True`, we found the same number twice — work is done

`return True`
- Early exit: we return the moment the first duplicate is confirmed
- No need to scan the rest of the array

`seen.add(num)`
- Record this number so future iterations can detect it as a duplicate
- **Critical:** this comes AFTER the membership check — if we added first,
  every number would falsely appear to be a duplicate of itself

`return False`
- Only reached if the loop finishes without finding any duplicate
- Means all elements in `nums` were distinct

---

## Common Mistakes

**1. Using a list instead of a set**
```python
# WRONG — O(n) lookup, total becomes O(n²)
seen = []
if num in seen:  # scans every element of seen
    return True
seen.append(num)
```
Always use `set()` for membership testing. This is the entire performance difference.

**2. Adding before checking**
```python
# WRONG — every number immediately "duplicates" itself
seen.add(num)
if num in seen:  # always True!
    return True
```
Always check membership before adding. Add is the fallback when no match is found.

**3. Checking length without understanding the trade-off**
```python
# Works but doesn't short-circuit
return len(nums) != len(set(nums))
```
This is fine for correctness but builds the full set even when `nums[0] == nums[1]`.
In interviews, mention this trade-off — it shows depth of understanding.

---

## Pattern Recognition

> Use the **"have I seen this before?"** hash set pattern when you see:
> - "Does any element appear more than once?"
> - "Find the first repeated element"
> - "Check for membership in O(1)"

**Similar problems:**
- **Two Sum** — same hash-lookup pattern, but stores index alongside value (uses dict not set)
- **Longest Substring Without Repeating Characters** — sliding window + set to track current window
- **Happy Number** — detect cycle by tracking seen values in a set
- **Find the Duplicate Number** — duplicate detection with space constraint (O(1) space solution)
- **Intersection of Two Arrays** — set membership across two arrays

---

## Real World Use Cases

### 1. Idempotency key deduplication in distributed payment systems
Payment APIs use idempotency keys to prevent duplicate charges when a client
retries a failed request. The server stores processed keys in a Redis set and
checks membership on every incoming request — the exact "have I seen this before?"
pattern. Processing 50,000 requests per second makes O(1) lookup non-negotiable.

### 2. Event deduplication in Kafka consumer pipelines
In high-throughput event streaming, network retries often cause the same message
to be delivered more than once. Consumers maintain a sliding-window set of
recently processed message IDs and check for membership before processing each
event, preventing duplicate writes to the database.

### 3. Username/email uniqueness validation during user registration
When a user registers, the system checks whether their chosen username or email
already exists in the database. Database systems implement this with unique
indexes (hash-based internally), which perform the same O(1) duplicate detection
at storage scale rather than in-memory scale.

---

## Key Takeaways

- A hash set gives O(1) membership testing — use it whenever you need "have I seen X?"
- Early return on first duplicate is more efficient than building the full set first
- Trading O(n) space for O(n) time (instead of O(n²) time with O(1) space) is almost always the right call
- The `in` operator on a Python list is O(n); on a set it is O(1) — this distinction defines your algorithm's complexity
