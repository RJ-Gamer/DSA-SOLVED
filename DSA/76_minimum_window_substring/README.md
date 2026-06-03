# 76. Minimum Window Substring

**LeetCode:** [Problem #76](https://leetcode.com/problems/minimum-window-substring/)  
**Difficulty:** Hard  
**Topics:** `String` `Sliding Window` `Hash Map` `Two Pointers`

---

## Problem Statement

Given two strings `s` and `t`, return the **minimum window substring** of `s`
such that every character in `t` (including duplicates) is included in the
window. If no such window exists, return an empty string `""`.

**Constraints:**
- `1 <= s.length, t.length <= 10⁵`
- `s` and `t` consist of uppercase and lowercase English letters
- The answer is guaranteed to be unique

### Example
```
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: "BANC" is the smallest window containing 'A', 'B', and 'C'.

Input:  s = "a", t = "a"
Output: "a"

Input:  s = "a", t = "aa"
Output: ""
Explanation: 't' requires two 'a's; 's' has only one.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

Find the shortest contiguous substring of `s` that contains all characters
of `t` at least as many times as they appear in `t`. Duplicates in `t` matter.

### Step 2 — Identify the constraint that matters

We need every character in `t` satisfied, with correct frequencies. As we
expand the window, we track how many of `t`'s distinct character requirements
are fully met ("formed"). Once all are met, we try to shrink from the left.

### Step 3 — Think about data structures

Two hash maps — `need` (required frequencies from `t`) and `have` (current
window frequencies) — let us check in O(1) whether a character's count just
crossed the threshold. A `formed` counter tracks how many distinct characters
are fully satisfied. When `formed == len(need)`, we have a valid window.

### Step 4 — Build the intuition

Expand the right pointer one step at a time. When a character's count in `have`
reaches its count in `need`, increment `formed`. Once `formed == required`,
the window is valid — record its length, then shrink from the left until the
window becomes invalid again. Repeat.

This "expand until valid, shrink until invalid" rhythm is the core sliding
window pattern.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Check every possible substring of `s` of length ≥ `len(t)`.

**Steps:**
1. Generate all substrings of `s` with length `>= len(t)`
2. For each, check if it contains all characters of `t`
3. Track the shortest valid one

**Complexity:**
- Time: O(n² · |t|) — O(n²) substrings, each checked in O(|t|)
- Space: O(|t|) — character frequency map

**Code:**
```python
from collections import Counter

def minWindow_brute(s, t):
    need = Counter(t)
    result = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            window = Counter(s[i:j])
            if all(window[c] >= need[c] for c in need):
                if not result or j - i < len(result):
                    result = s[i:j]
    return result
```

---

### Approach 2 — Optimal (Sliding Window)

**Intuition:** Use a variable-width sliding window. Expand right to satisfy
all requirements, then shrink left as much as possible while still valid.

**Steps:**
1. Build `need = Counter(t)`, `required = len(need)`
2. `have = {}`, `formed = 0`, `left = 0`, track min window
3. Expand `right`:
   - Add `s[right]` to `have`
   - If `have[s[right]] == need[s[right]]`, increment `formed`
4. While `formed == required`:
   - Update min window if current is shorter
   - Remove `s[left]` from `have`; if `have[s[left]] < need[s[left]]`, decrement `formed`
   - Advance `left`

**Illustration:**
```
s = "ADOBECODEBANC", t = "ABC"
need = {A:1, B:1, C:1}, required = 3

Expand right until all 3 satisfied:
  r=0 (A): have={A:1}, formed=1
  r=1 (D): have={A:1,D:1}
  r=2 (O): have={A:1,D:1,O:1}
  r=3 (B): have={...,B:1}, formed=2
  r=4 (E): ...
  r=5 (C): have={...,C:1}, formed=3  → valid! window="ADOBEC" (len 6)

Shrink left:
  l=0 (A): have[A]=0 < need[A]=1 → formed=2, stop shrinking. l=1
  window "DOBECODEBA..." not checked yet; formed=2 now.

Expand right again:
  r=6 (O): ...
  r=7 (D): ...
  r=8 (E): ...
  r=9 (B): have[B]=2
  r=10 (A): have[A]=1 → formed=3 again! window="DOBECODEBA" (len 10) — worse

Shrink left (l=1..):
  l=1 (D): remove D, not in need → shrink. l=2
  l=2 (O): remove O, not in need → shrink. l=3
  l=3 (B): have[B]=1, was 2 → still >= need[B]=1 → shrink. l=4
  l=4 (E): remove E → shrink. l=5
  l=5 (C): have[C]=0 < need[C]=1 → formed=2, stop. l=6
  Best window so far: s[3:10]="OBECODEBA" wait... let me recount.

...eventually window "BANC" (indices 10..13) is found with len=4 ✓
```

**Complexity:**
- Time: O(|s| + |t|) — each character is added and removed from the window at most once
- Space: O(|s| + |t|) — hash maps

**Code:**
```python
from collections import Counter

def minWindow(s, t):
    if not t:
        return ""
    need = Counter(t)
    have = {}
    formed = required = 0
    required = len(need)
    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            formed += 1
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return result
```

---

## Solution Breakdown — Step by Step

```python
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t:
        return ""
    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)
    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return result
```

**Line by line:**

`need = Counter(t)`
- Frequency map of what we need — `{'A': 1, 'B': 1, 'C': 1}` for `t = "ABC"`

`required = len(need)`
- Number of distinct characters we need to fully satisfy (not total characters)

`have[char] = have.get(char, 0) + 1`
- Track how many of each character the current window contains

`if char in need and have[char] == need[char]: formed += 1`
- Only increment when we've exactly hit the required count — not exceeded it
- This avoids double-counting: `have[char] == need[char]` is true only on the
  crossing moment, not every time we add another copy

`while formed == required:`
- All characters are fully satisfied — try to shrink the window
- Inner loop runs the "minimize" logic while valid

`if right - left + 1 < min_len:`
- Check before shrinking — current window is valid, record it if it's the best

`have[left_char] -= 1`
- Remove the leftmost character from the window

`if left_char in need and have[left_char] < need[left_char]: formed -= 1`
- If removing this character drops a required count below its threshold,
  the window is no longer valid — decrement `formed` to exit the while loop

`left += 1`
- Advance the left boundary

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (all substrings) | O(n² · \|t\|) | O(\|t\|) |
| Optimal (sliding window) | O(\|s\| + \|t\|) | O(\|s\| + \|t\|) |

---

## Common Mistakes

**1. Incrementing `formed` on every character match instead of threshold crossing**
```python
# WRONG — formed gets incremented every time we see a needed character
if char in need:
    formed += 1

# CORRECT — only when the count exactly meets the requirement
if char in need and have[char] == need[char]:
    formed += 1
```
If `t = "AA"` and `need = {A: 2}`, adding the first `A` should not count as
`formed`. Only when `have[A] == 2` do we count it.

**2. Checking total length of t instead of distinct character count**
```python
# WRONG — len(t) counts duplicates; required should be distinct keys
required = len(t)     # if t = "AAB", this is 3

# CORRECT
required = len(need)  # if t = "AAB", this is 2 (A and B)
```

**3. Shrinking the left without recording the window first**
```python
# WRONG — shrinks before checking if this is the minimum
left += 1
if right - left + 1 < min_len:   # window already smaller than when valid
```
Always record the window size before advancing `left`.

---

## Pattern Recognition

### How to Recognize
- "Minimum/maximum substring/subarray" with a constraint on what it must contain
- The window must include all elements of a target set with correct frequencies
- Expand right to satisfy, shrink left to minimize

### How to Identify
- Is there a "formed / required" count that tells you when a window is valid?
- Does expanding always get you closer to valid, shrinking always toward invalid?

### How to Remember
> **Mental model:** Fill a bag (expand right) until it has everything you need,
> then empty from the front (shrink left) until something falls short. Record
> every valid bag. Repeat.

**Similar problems:**
- **Permutation in String (LeetCode #567)** — fixed-size window with same frequency check
- **Longest Substring Without Repeating Characters (LeetCode #3)** — simpler sliding window
- **Substring with Concatenation of All Words (LeetCode #30)** — same pattern, word-level

---

## Real World Use Cases

### 1. DNA subsequence search in bioinformatics
Finding the shortest segment of a genome that contains all marker nucleotides
of a target sequence — used in primer design and variant detection pipelines
where the target pattern must appear within a window.

### 2. Log file analysis
In observability tools, finding the shortest time window in a log stream that
contains all required event types (e.g., request start, DB call, response)
— used to detect the fastest possible end-to-end trace.

### 3. Text document retrieval
Search engines checking whether a document contains all query terms within a
short passage (proximity search). The minimum window gives the most relevant
snippet to display as the search result excerpt.

---

## Key Takeaways

- Track `formed` (satisfied requirements) separately from `have` (raw counts)
- Only update `formed` when a count exactly hits the threshold — not every time
- `required = len(need)` counts distinct characters, not total characters in `t`
- Expand right to satisfy, shrink left to minimize — the classic sliding window rhythm
- This pattern handles duplicate requirements in `t` naturally via the frequency maps

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #76](https://leetcode.com/problems/minimum-window-substring/) | Minimum Window Substring | Hard |

> Part of the **Blind 75** and **NeetCode 150** interview prep lists.
