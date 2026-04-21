# 242. Valid Anagram

**LeetCode:** [Problem #242](https://leetcode.com/problems/valid-anagram/)  
**Difficulty:** Easy  
**Topics:** `String` `Hash Map`

---

## Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`,
and `false` otherwise.

An **anagram** is a word or phrase formed by rearranging the letters of another,
using all the original letters exactly once.

**Constraints:**
- `1 <= s.length, t.length <= 5 * 10⁴`
- `s` and `t` consist of lowercase English letters

### Example
```
Input:  s = "anagram", t = "nagaram"
Output: true
Explanation: Both strings contain exactly the same letters with the same
frequencies: a×3, n×1, g×1, r×1, m×1
```

```
Input:  s = "rat", t = "car"
Output: false
Explanation: "rat" has r×1, a×1, t×1 but "car" has c×1, a×1, r×1.
The letter 't' is missing from "car" and 'c' is missing from "rat".
```

```
Input:  s = "a", t = "ab"
Output: false
Explanation: Different lengths — "ab" has an extra 'b' that "a" does not.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

Two strings are anagrams if one is a rearrangement of the other. That means:
- They must have the **same length**
- They must contain the **exact same characters**
- Each character must appear the **exact same number of times**

Order does not matter. `"anagram"` and `"nagaram"` are anagrams because if you
sort both, you get the same string. The question is really:

> "Do both strings have identical character frequency distributions?"

### Step 2 — Identify the constraint that matters

The strings can be up to 50,000 characters long. Any approach that compares
characters in a nested fashion will be O(n²) — too slow at scale.

The key insight: we don't care about order, only about **counts**. If we can
build a frequency map for each string in O(n) and compare them in O(1), we
have an efficient solution.

### Step 3 — Think about data structures

There are three natural approaches:

1. **Sort both strings** and compare — if they're anagrams, sorted versions
   are identical. Simple, but O(n log n).
2. **Two hash maps** — count character frequencies in each string separately,
   then compare the maps. O(n) time, O(1) space (at most 26 keys for lowercase
   letters).
3. **Python's `Counter`** — a built-in that does exactly what approach 2 does,
   in one line.

The hash map approach is the most instructive because it makes the counting
logic explicit and is the pattern interviewers want to see you reason through.

### Step 4 — Build the intuition

Imagine you have two bags of Scrabble tiles. You want to know if both bags
contain the same tiles. You don't need to sort them — you just count each
letter in bag one, count each letter in bag two, and compare the tallies.

If every letter has the same count in both bags, they're anagrams. If any
letter's count differs — or if one bag has a letter the other doesn't — they're
not.

The hash map is the tally sheet. One pass per string to build it, one
comparison to check it.

---

## Approaches

### Approach 1 — Brute Force (Sort)

**Intuition:** If two strings are anagrams, sorting both produces the same
string. Compare the sorted versions directly.

**Steps:**
1. If `len(s) != len(t)`, return `False` immediately
2. Sort both strings
3. Return `True` if the sorted strings are equal, `False` otherwise

**Illustration:**
```
s = "anagram", t = "nagaram"

sorted(s) = "aaagmnr"
sorted(t) = "aaagmnr"

"aaagmnr" == "aaagmnr" → True ✓

s = "rat", t = "car"

sorted(s) = "art"
sorted(t) = "acr"

"art" == "acr" → False ✓
```

**Complexity:**
- Time: O(n log n) — sorting dominates
- Space: O(n) — Python's `sorted()` creates a new list

**Code:**
```python
def valid_anagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)
```

> **Note:** This is clean and readable, but sorting is unnecessary work when
> all we need is a frequency count. The hash map approach is strictly faster.

---

### Approach 2 — Optimal (Two Hash Maps)

**Intuition:** Count character frequencies in both strings using hash maps and
compare the maps. Two strings are anagrams if and only if their frequency maps
are identical.

**Steps:**
1. If `len(s) != len(t)`, return `False` — different lengths can never be anagrams
2. Build `count_s`: iterate over `s`, incrementing the count for each character
3. Build `count_t`: iterate over `t`, incrementing the count for each character
4. Return `True` if `count_s == count_t`, `False` otherwise

**Illustration:**
```
s = "anagram", t = "nagaram"

Build count_s:
a → 3, n → 1, g → 1, r → 1, m → 1
count_s = {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}

Build count_t:
n → 1, a → 3, g → 1, r → 1, m → 1
count_t = {'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}

count_s == count_t → True ✓

s = "rat", t = "car"

count_s = {'r': 1, 'a': 1, 't': 1}
count_t = {'c': 1, 'a': 1, 'r': 1}

count_s == count_t → False ✓
('t' is in count_s but not count_t; 'c' is in count_t but not count_s)
```

**Complexity:**
- Time: O(n) — two passes of length n, one comparison
- Space: O(1) — at most 26 keys per map (lowercase English letters only)

**Code:**
```python
def valid_anagram_linear(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    count_s, count_t = {}, {}

    for letter in s:
        count_s[letter] = 1 + count_s.get(letter, 0)

    for letter in t:
        count_t[letter] = 1 + count_t.get(letter, 0)

    return count_s == count_t
```

---

### Approach 3 — Pythonic (Counter)

**Intuition:** Python's `collections.Counter` builds a frequency map in one
call. Comparing two `Counter` objects is equivalent to comparing two frequency
maps.

**Steps:**
1. Build `Counter(s)` and `Counter(t)`
2. Return whether they are equal

**Illustration:**
```
s = "anagram", t = "nagaram"

Counter(s) = Counter({'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1})
Counter(t) = Counter({'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1})

Counter(s) == Counter(t) → True ✓
```

**Complexity:**
- Time: O(n) — `Counter` iterates over each string once
- Space: O(1) — bounded by the alphabet size (26 keys)

**Code:**
```python
def valid_anagram_counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)
```

> **Note:** This is the most concise version and perfectly correct. In an
> interview, prefer Approach 2 to demonstrate that you understand what
> `Counter` is doing under the hood.

---

## Solution Breakdown — Step by Step

```python
def valid_anagram_linear(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    count_s, count_t = {}, {}

    for letter in s:
        count_s[letter] = 1 + count_s.get(letter, 0)

    for letter in t:
        count_t[letter] = 1 + count_t.get(letter, 0)

    return count_s == count_t
```

**Line by line:**

`if len(s) != len(t):`
- An anagram must use all original letters exactly once, so both strings must
  have the same length
- This is a free O(1) early exit that eliminates a large class of inputs
  immediately — no need to build any maps

`return False`
- If lengths differ, no further work is needed — they cannot be anagrams

`count_s, count_t = {}, {}`
- Two empty dictionaries to hold character frequency counts
- Keys will be characters (`'a'`, `'b'`, etc.), values will be integer counts
- We use two separate maps so we can compare them at the end

`for letter in s:`
- Iterate directly over the characters of `s`
- No index needed — we only care about the characters themselves

`count_s[letter] = 1 + count_s.get(letter, 0)`
- `count_s.get(letter, 0)` returns the current count for `letter`, or `0` if
  it hasn't been seen yet — this avoids a `KeyError` on the first occurrence
- We add `1` to that count and store it back
- After this loop, `count_s` holds the exact frequency of every character in `s`

`for letter in t:`
- Same pass over `t` to build `count_t`

`count_t[letter] = 1 + count_t.get(letter, 0)`
- Identical logic — builds the frequency map for `t`

`return count_s == count_t`
- Python's dictionary equality check compares both keys and values
- Returns `True` only if every character appears the same number of times in
  both strings
- This single comparison replaces the need to manually iterate over both maps

---

## Common Mistakes

**1. Skipping the length check**
```python
# Works but does unnecessary work
count_s, count_t = {}, {}
for letter in s:
    count_s[letter] = 1 + count_s.get(letter, 0)
for letter in t:
    count_t[letter] = 1 + count_t.get(letter, 0)
return count_s == count_t
```
If `s = "ab"` and `t = "abc"`, the maps will differ anyway, but you've done
extra work building them. The length check is a free early exit — always include it.

**2. Using a list instead of a dict for frequency counting**
```python
# Fragile — only works for lowercase ASCII, and requires index arithmetic
count = [0] * 26
count[ord(letter) - ord('a')] += 1
```
This works for the given constraints but breaks the moment the input includes
uppercase letters, digits, or Unicode. A dictionary generalizes naturally to
any character set.

**3. Comparing sorted strings when you need O(n)**
```python
# Correct but suboptimal
return sorted(s) == sorted(t)
```
Sorting is O(n log n). If an interviewer asks for the optimal solution, this
won't satisfy the requirement. Know both approaches and be ready to explain
the trade-off.

**4. Mutating a single map instead of building two**
```python
# WRONG — increments for s, but then increments again for t instead of comparing
for letter in s:
    count[letter] = 1 + count.get(letter, 0)
for letter in t:
    count[letter] = 1 + count.get(letter, 0)  # should be decrementing, not incrementing
```
A valid single-map approach increments for `s` and **decrements** for `t`, then
checks that all values are zero. If you use two maps, keep them separate and
compare at the end.

---

## Pattern Recognition

> Use the **frequency map** pattern when you see:
> - "Are these two strings rearrangements of each other?"
> - "Do these two collections contain the same elements with the same counts?"
> - "Check if one string can be formed from the characters of another"

**Similar problems:**
- **Group Anagrams** — same frequency map idea, but group multiple strings that
  share the same character distribution
- **Find All Anagrams in a String** — sliding window + frequency map to find
  all anagram substrings
- **Minimum Window Substring** — frequency map with a sliding window to find
  the smallest window containing all required characters
- **Permutation in String** — check if any permutation of `s` exists as a
  substring of `t`; same frequency comparison, applied with a sliding window
- **Contains Duplicate** — simpler membership check using a set instead of a
  full frequency map

---

## Real World Use Cases

### 1. Plagiarism detection in document analysis
Academic plagiarism tools often check whether a submitted document is a
rearrangement or paraphrase of an existing one. At the character or word
frequency level, anagram detection is a building block: if two documents have
nearly identical word frequency distributions, they warrant deeper inspection.
The frequency map approach scales to millions of documents when combined with
hashing.

### 2. Spell-checking and autocorrect in text editors
When a user types an unknown word, spell-checkers look for valid words that
are anagrams or near-anagrams of the input. Building a frequency map of the
typed word and comparing it against a dictionary of frequency maps is far
faster than sorting every candidate word on each keystroke.

### 3. Cryptographic key validation
Some symmetric encryption schemes use character transposition as part of key
derivation. Validating that a derived key is a permutation of the original
seed material uses the same frequency comparison: same characters, same counts,
different order.

### 4. Log deduplication and normalization in observability pipelines
In distributed systems, log messages from different services often contain the
same fields in different orders. Normalizing log entries by treating them as
anagrams of a canonical form — comparing field frequency maps rather than raw
strings — allows deduplication before writing to storage, reducing log volume
significantly.

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (sort) | O(n log n) | O(n) |
| Optimal (two hash maps) | O(n) | O(1) |
| Pythonic (Counter) | O(n) | O(1) |

---

## Key Takeaways

- Two strings are anagrams if and only if their character frequency maps are
  identical — order is irrelevant, counts are everything
- Always do the length check first — it's a free O(1) early exit
- `dict.get(key, 0)` is the idiomatic way to safely increment a counter without
  a `KeyError` on the first occurrence
- The hash map approach is O(n) time and O(1) space (bounded by alphabet size),
  strictly better than the O(n log n) sort approach
- `Counter` from `collections` is the Pythonic shortcut, but understanding the
  manual implementation is what interviewers are testing

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #242](https://leetcode.com/problems/valid-anagram/) | Valid Anagram | Easy |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
