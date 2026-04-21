# 125. Valid Palindrome

**LeetCode:** [Problem #125](https://leetcode.com/problems/valid-palindrome/)  
**Difficulty:** Easy  
**Topics:** `String` `Two Pointers`

---

## Problem Statement

Given a string `s`, return `true` if it is a palindrome, or `false`
otherwise.

A palindrome reads the same forward and backward **after converting all
uppercase letters into lowercase letters and removing all non-alphanumeric
characters**.

Alphanumeric characters include letters and numbers.

**Constraints:**
- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters

### Example
```
Input:  s = "A man, a plan, a canal: Panama"
Output: true
Explanation: After removing spaces and punctuation, the string becomes
"amanaplanacanalpanama", which reads the same forward and backward.
```

```
Input:  s = "race a car"
Output: false
Explanation: After normalization, the string becomes "raceacar", which is
not the same in reverse.
```

```
Input:  s = " "
Output: true
Explanation: After removing non-alphanumeric characters, nothing remains.
An empty string is still considered a palindrome.
```

---

## How to Think About This Problem

### Step 1 - Understand what's being asked

We are not checking the raw string exactly as written. We first need to
**ignore punctuation**, **ignore spaces**, and **ignore case**. Only then do we
check whether the remaining characters read the same from both ends.

So this is really:

> "After normalization, is the string symmetric?"

### Step 2 - Identify the constraint that matters

The important part is that the string can be quite large. If we repeatedly
rebuild strings or scan sections again and again, we do extra work we do not
need.

Also, many characters may be irrelevant. A direct left-to-right comparison on
the original string fails because punctuation and casing should not count.

### Step 3 - Think about data structures

There are two natural ideas:

1. Build a cleaned version of the string containing only lowercase
   alphanumeric characters, then compare it with its reverse
2. Use **two pointers** on the original string and skip invalid characters in
   place

The first idea is easier to understand. The second avoids building a separate
string and is therefore more space-efficient.

### Step 4 - Build the intuition

Imagine two people standing at opposite ends of the string.

- The left person keeps moving right until they find a useful character
- The right person keeps moving left until they find a useful character
- Once both are standing on letters or digits, compare them case-insensitively
- If they differ, the string cannot be a palindrome
- If they match, both move inward and continue

The key insight: **characters that are not alphanumeric never affect the answer,
so we can skip them entirely.**

---

## Approaches

### Approach 1 - Brute Force

**Intuition:** Build a normalized string first, then compare it with its reverse.

**Steps:**
1. Create an empty list to store cleaned characters
2. Scan each character in `s`
3. If the character is alphanumeric, append its lowercase form
4. Join the cleaned characters into a string
5. Compare the cleaned string with its reverse

**Illustration:**
```
s = "A man, a plan, a canal: Panama"

Scan characters:
A   -> keep as 'a'
    -> skip
m   -> keep
a   -> keep
n   -> keep
,   -> skip
...

cleaned = "amanaplanacanalpanama"
reverse = "amanaplanacanalpanama"

cleaned == reverse -> True
```

**Complexity:**
- Time: O(n) - one pass to clean, another pass to reverse/compare
- Space: O(n) - the normalized string is stored separately

**Code:**
```python
def is_palindrome_brute_force(s: str) -> bool:
    cleaned = []

    for ch in s:
        if ch.isalnum():
            cleaned.append(ch.lower())

    cleaned = "".join(cleaned)
    return cleaned == cleaned[::-1]
```

---

### Approach 2 - Optimal

**Intuition:** Use two pointers on the original string and skip characters that
do not matter.

**Steps:**
1. Set `left = 0` and `right = len(s) - 1`
2. Move `left` rightward until it points to an alphanumeric character
3. Move `right` leftward until it points to an alphanumeric character
4. Compare `s[left].lower()` and `s[right].lower()`
5. If they differ, return `False`
6. If they match, move both pointers inward and continue
7. If the pointers cross, return `True`

**Illustration:**
```
s = "A man, a plan, a canal: Panama"

left='A', right='a'
compare 'a' vs 'a' -> match

left=' ' -> skip
left='m'
right='m'
compare 'm' vs 'm' -> match

left='a', right='a' -> match
left='n', right='n' -> match
...

All valid character pairs match -> True
```

```
s = "0P"

left='0', right='P'
compare '0' vs 'p' -> mismatch
return False
```

**Complexity:**
- Time: O(n) - each pointer moves inward at most n times total
- Space: O(1) - no extra normalized string is created

**Code:**
```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

---

## Solution Breakdown - Step by Step

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

**Line by line:**

`left, right = 0, len(s) - 1`
- We place one pointer at the beginning and one at the end
- These pointers will move inward as we compare mirrored characters

`while left < right:`
- We only need to compare while the pointers have not crossed
- Once they meet or cross, every needed comparison has already succeeded

`while left < right and not s[left].isalnum():`
- Skip over spaces, punctuation, and any other non-alphanumeric character
- `left < right` is included to avoid walking past the other pointer
- This also safely handles inputs like `" "` or `".,,"`

`left += 1`
- Move the left pointer to the next character
- This continues until `left` lands on a valid character or crosses `right`

`while left < right and not s[right].isalnum():`
- Same idea on the right side
- We keep skipping characters that do not matter for palindrome checking

`right -= 1`
- Move the right pointer leftward until it lands on a valid character

`if s[left].lower() != s[right].lower():`
- Compare the useful characters after converting both to lowercase
- This makes `'A'` and `'a'` count as equal
- If they differ, the normalized string is not symmetric

`return False`
- The first mismatch is enough to prove the answer is false
- No further scanning is needed

`left += 1`
- After a successful match, move inward from the left

`right -= 1`
- After a successful match, move inward from the right

`return True`
- If the loop completes without a mismatch, all mirrored valid characters matched
- That means the normalized string is a palindrome

---

## Common Mistakes

- Forgetting to ignore non-alphanumeric characters. Comparing the raw string
  directly will fail on inputs like `"A man, a plan, a canal: Panama"`.
- Forgetting to normalize case. `'A'` and `'a'` should be treated as equal.
- Skipping invalid characters without checking pointer bounds. On inputs made
  entirely of spaces or punctuation, this can cause an index error.
- Building a cleaned string correctly, but then forgetting that an empty cleaned
  string should still return `True`.

---

## Pattern Recognition

> Use this pattern when you see: "compare from both ends", "ignore irrelevant
> characters while checking symmetry", or "validate a string after normalization"

**Similar problems:**
- **Valid Palindrome II** - same two-pointer idea, but allows deleting one
  character
- **Reverse String** - same mirrored two-pointer traversal
- **Palindrome Linked List** - palindrome check with different storage
  constraints

---

## Real World Use Cases

### 1. Input normalization in search systems
Search engines often normalize user queries by ignoring casing and certain
punctuation before matching or comparing text patterns. The idea is similar:
remove irrelevant formatting noise, then compare the meaningful characters.

### 2. Data validation in OCR pipelines
Optical character recognition systems frequently clean scanned text by stripping
symbols and standardizing letter case before running quality checks. A palindrome
validator is a small example of the same normalization-first workflow.

### 3. Log and identifier sanitization in backend systems
Production systems often compare identifiers that may arrive with separators,
mixed case, or formatting artifacts from external sources. A two-pointer
normalization approach helps validate equivalence without allocating large
intermediate strings.

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force (clean + reverse) | O(n) | O(n) |
| Optimal (two pointers) | O(n) | O(1) |

---

## Key Takeaways

- The real problem is not "is the raw string a palindrome?" but "is the
  normalized string a palindrome?"
- Two pointers are a strong fit when you need to compare mirrored characters
  from both ends
- Skipping irrelevant characters in place gives O(1) extra space
- Always guard pointer movement when skipping characters to avoid edge-case
  index errors

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #125](https://leetcode.com/problems/valid-palindrome/) | Valid Palindrome | Easy |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
