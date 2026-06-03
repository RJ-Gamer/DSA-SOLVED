# 647. Palindromic Substrings

**LeetCode:** [Problem #647](https://leetcode.com/problems/palindromic-substrings/)
**Difficulty:** Medium
**Topics:** `String` `Dynamic Programming`

---

## Problem Statement

Given a string `s`, return the number of **palindromic substrings** in it.

A string is a palindrome when it reads the same backward as forward. A substring
is a contiguous sequence of characters within the string.

**Constraints:**
- `1 <= s.length <= 1000`
- `s` consists of lowercase English letters

### Example
```
Input:  s = "abc"
Output: 3
Explanation: Three palindromic substrings: "a", "b", "c"
```

```
Input:  s = "aaa"
Output: 6
Explanation: Six palindromic substrings: "a", "a", "a", "aa", "aa", "aaa"
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to count every contiguous slice of the string that reads the same
forwards and backwards. Every single character counts as a palindrome. We
need to count all of them, including overlapping ones.

### Step 2 — Identify the constraint that matters

A substring `s[i..j]` is a palindrome if and only if `s[i] == s[j]` AND
`s[i+1..j-1]` is also a palindrome. This recursive structure means smaller
subproblems feed into larger ones — the hallmark of interval DP.

The brute force of checking every substring from scratch is O(n³). Both DP
and the expand-around-center approach bring this down to O(n²).

### Step 3 — Think about data structures

Three approaches:
1. **Memoized recursion** — top-down, O(n²) time and space
2. **Interval DP table** — bottom-up boolean grid, O(n²) time and space
3. **Expand around center** — O(n²) time, O(1) space

The expand-around-center approach is the most space-efficient and the most
commonly expected in interviews.

### Step 4 — Build the intuition

Every palindrome has a center. Odd-length palindromes have a single character
at the center; even-length palindromes have a gap between two characters.
For each of the `2n - 1` possible centers, expand outward as long as the
characters on both sides match. Each successful expansion is one more
palindromic substring.

---

## Approaches

For a string of length `n`, create an `n × n` boolean grid:

```python
size = len(word)
dp = [[False] * size for _ in range(size)]
```

**What `dp[i][j]` means:** `True` if `word[i..j]` is a palindrome, `False` otherwise.

For `word = "madam"` (size=5):

```
      m    a    d    a    m
  m  [i=0  ?    ?    ?    ?  ]
  a  [ ×  i=1   ?    ?    ?  ]
  d  [ ×   ×   i=2   ?    ?  ]
  a  [ ×   ×    ×   i=3   ?  ]
  m  [ ×   ×    ×    ×   i=4 ]
```

- `×` = lower triangle (`j < i`) — invalid, a substring can't end before it starts
- `i=k` on the diagonal = single-character substrings (always `True`)
- Final answer = count all `True` cells in the upper triangle + diagonal

---

## Step 1: Base Cases — Single Characters

Every single character is a palindrome of length 1.

```python
for i in range(size):
    dp[i][i] = True
    count += 1
```

After base cases for `"madam"`:

```
      m    a    d    a    m
  m  [ T    F    F    F    F ]
  a  [ ×    T    F    F    F ]
  d  [ ×    ×    T    F    F ]
  a  [ ×    ×    ×    T    F ]
  m  [ ×    ×    ×    ×    T ]
```

Count so far: **5** (one per character).

---

## Step 2: Fill by Interval Length

Fill diagonal by diagonal, length 2 up to length `n`.

```python
for length in range(2, size + 1):
    for i in range(size - length + 1):
        j = i + length - 1
```

---

### Length 2: Adjacent Pairs

`dp[i][i+1]` is `True` if and only if `word[i] == word[i+1]`.

> Note: For length 2, `dp[i+1][j-1]` = `dp[i+1][i]` — that cell is in the lower triangle (invalid). So we handle length 2 as a special case: no inner substring, just check whether the two characters match.

| (i, j) | word[i] | word[j] | Match? | dp[i][j] |
|---|---|---|---|---|
| (0, 1) | m | a | ✗ | False |
| (1, 2) | a | d | ✗ | False |
| (2, 3) | d | a | ✗ | False |
| (3, 4) | a | m | ✗ | False |

No new palindromes. Count still: **5**.

---

### Length 3

`dp[i][j]` = `True` if `word[i] == word[j]` AND `dp[i+1][j-1]` is `True`.

| (i, j) | word[i] | word[j] | Match? | Inner dp[i+1][j-1] | dp[i][j] |
|---|---|---|---|---|---|
| (0, 2) | m | d | ✗ | — | False |
| (1, 3) | a | a | ✓ | dp[2][2] = True | **True** ✓ → `"ada"` |
| (2, 4) | d | m | ✗ | — | False |

Count: **6** (`"ada"` added).

---

### Length 4

| (i, j) | word[i] | word[j] | Match? | Inner dp[i+1][j-1] | dp[i][j] |
|---|---|---|---|---|---|
| (0, 3) | m | a | ✗ | — | False |
| (1, 4) | a | m | ✗ | — | False |

Count still: **6**.

---

### Length 5: The Full String

| (i, j) | word[i] | word[j] | Match? | Inner dp[i+1][j-1] | dp[i][j] |
|---|---|---|---|---|---|
| (0, 4) | m | m | ✓ | dp[1][3] = True (`"ada"`) | **True** ✓ → `"madam"` |

Count: **7**.

---

**Final grid for `"madam"`:**

```
      m    a    d    a    m
  m  [ T    F    F    F    T ]   ← "madam" is a palindrome
  a  [ ×    T    F    T    F ]   ← "ada" is a palindrome
  d  [ ×    ×    T    F    F ]
  a  [ ×    ×    ×    T    F ]
  m  [ ×    ×    ×    ×    T ]
```

Count all `True` cells: 5 (diagonal) + 1 (`"ada"`) + 1 (`"madam"`) = **7**. ✓

---

### Approach 1 — Memoized Recursion (Top-Down)

The most direct approach: write `is_palindrome` as a recursive function and let memoization avoid recomputing the same `(i, j)` pair twice.

```python
from functools import lru_cache


class Solution:
    def palindromic_substrings(self, word: str) -> int:
        """
        Time: O(n^2) — each (i, j) pair computed once
        Space: O(n^2) — cache stores all (i, j) results + recursion stack
        """
        size = len(word)
        count = 0

        for i in range(size):
            for j in range(i, size):
                if self.is_palindrome(word, i, j):
                    count += 1

        return count

    @lru_cache(maxsize=None)
    def is_palindrome(self, word: str, left: int, right: int) -> bool:
        if left >= right:
            return True
        if word[left] != word[right]:
            return False
        return self.is_palindrome(word, left + 1, right - 1)
```

**Why it works:** `is_palindrome(word, i, j)` peels one layer at a time — checks the outer characters, then asks the same question for `word[i+1..j-1]`. The `@lru_cache` ensures each `(word, i, j)` trio is only computed once.

---

### Approach 2 — Interval DP Table (Bottom-Up)

Instead of recursing top-down, fill the `dp` table from shorter intervals to longer ones.

```python
class Solution:
    def palindromic_substrings_dp(self, word: str) -> int:
        """
        Time: O(n^2) — fill every cell in the upper triangle
        Space: O(n^2) — the full n×n boolean grid
        """
        size = len(word)
        dp = [[False] * size for _ in range(size)]
        count = 0

        # Base case: single characters
        for i in range(size):
            dp[i][i] = True
            count += 1

        # Length 2: handled separately (inner interval would be invalid)
        for i in range(size - 1):
            if word[i] == word[i + 1]:
                dp[i][i + 1] = True
                count += 1

        # Length 3 and above
        for length in range(3, size + 1):
            for i in range(size - length + 1):
                j = i + length - 1
                if word[i] == word[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    count += 1

        return count
```

**Why length 2 is handled separately:** For `length = 2`, `j = i + 1`, so `dp[i+1][j-1]` = `dp[i+1][i]`. That cell is in the lower triangle — it's invalid and stays `False`. But two identical adjacent characters *do* form a palindrome. Separating length 2 avoids reading an invalid cell and keeps the main loop clean.

---

### Approach 3 — Optimal (Expand Around Center)

Every palindrome has a **center**:
- Odd-length palindromes (`"aba"`, `"madam"`) have a single center character.
- Even-length palindromes (`"aa"`, `"abba"`) have a center *gap* between two characters.

Instead of checking intervals from outside in, we go the other direction: **start at every possible center and expand outward** as long as the characters match.

For a string of length `n`, there are `2n - 1` possible centers:
- `n` single-character centers (for odd-length palindromes)
- `n - 1` gap centers (for even-length palindromes)

```python
class Solution:
    def palindromic_substrings_center(self, word: str) -> int:
        """
        Time: O(n^2) — n centers × up to n expansions each
        Space: O(1) — no grid needed
        """
        size = len(word)
        count = 0

        for center in range(size):
            # Odd-length: single character at center
            left, right = center, center
            while left >= 0 and right < size and word[left] == word[right]:
                count += 1
                left -= 1
                right += 1

            # Even-length: gap between center and center+1
            left, right = center, center + 1
            while left >= 0 and right < size and word[left] == word[right]:
                count += 1
                left -= 1
                right += 1

        return count
```

### Trace for `"madam"`

| Center | Type | Expansions | Palindromes found |
|---|---|---|---|
| 0 (`m`) | Odd | `"m"` only — `word[-1]` out of bounds | `"m"` |
| 0–1 (`m`/`a`) | Even | `m ≠ a` — stop immediately | — |
| 1 (`a`) | Odd | `"a"`, then `word[0]='m' ≠ word[2]='d'` — stop | `"a"` |
| 1–2 (`a`/`d`) | Even | `a ≠ d` — stop | — |
| 2 (`d`) | Odd | `"d"`, `"ada"` (k=1), `"madam"` (k=2), then out of bounds | `"d"`, `"ada"`, `"madam"` |
| 2–3 (`d`/`a`) | Even | `d ≠ a` — stop | — |
| 3 (`a`) | Odd | `"a"`, then `word[2]='d' ≠ word[4]='m'` — stop | `"a"` |
| 3–4 (`a`/`m`) | Even | `a ≠ m` — stop | — |
| 4 (`m`) | Odd | `"m"` only — `word[5]` out of bounds | `"m"` |

Total: `"m"`, `"a"`, `"d"`, `"a"`, `"m"`, `"ada"`, `"madam"` = **7** ✓

---

---

## Solution Breakdown — Step by Step

```python
def palindromic_substrings_center(s: str) -> int:
    size = len(s)
    count = 0
    for center in range(size):
        left, right = center, center
        while left >= 0 and right < size and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
        left, right = center, center + 1
        while left >= 0 and right < size and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count
```

**Line by line:**

`for center in range(size):`
- Iterate over every possible center position
- There are `n` single-character centers and `n-1` gap centers — we handle both in each iteration

`left, right = center, center`
- Start both pointers at the same character — odd-length palindrome expansion

`while left >= 0 and right < size and s[left] == s[right]:`
- Expand outward as long as the characters match and we stay in bounds
- Each iteration of this loop confirms one more palindromic substring

`count += 1`
- Every successful expansion is a valid palindromic substring — count it immediately

`left -= 1; right += 1`
- Move both pointers outward to check the next larger palindrome centered here

`left, right = center, center + 1`
- Reset for even-length expansion — the center is the gap between `center` and `center + 1`

---

## Common Mistakes

**1. Only checking odd-length palindromes**
```python
for center in range(size):
    left, right = center, center
    while ...:  # only odd-length
        count += 1
# Missing the even-length expansion entirely
```
Always run both expansions per center: one starting at `(center, center)` and
one at `(center, center + 1)`.

**2. Counting after the loop instead of inside it**
```python
while left >= 0 and right < size and s[left] == s[right]:
    left -= 1
    right += 1
count += 1  # WRONG — only counts one palindrome per center
```
Increment `count` inside the while loop — each successful expansion is a
separate palindromic substring.

**3. Handling length-2 separately in the DP approach**
For `length = 2`, `dp[i+1][j-1]` = `dp[i+1][i]` which is in the lower triangle
(invalid). Always handle length 2 as a special case before the main loop.

**4. Confusing substrings with subsequences**
Substrings must be contiguous. `"ace"` is a subsequence of `"abcde"` but not
a substring. This problem counts substrings only.

---

## Pattern Recognition

### How to Recognize
- Problem asks to count or find palindromic substrings (contiguous, not subsequences)
- Every possible center (character or gap) must be considered
- Expanding outward from each center is more space-efficient than a full DP table

### How to Identify
- For each center, can you expand `left` and `right` while `s[left] == s[right]`?
- Do you need two expansions per center: one for odd-length, one for even-length palindromes?

### How to Remember
> **Mental model:** Every palindrome has a center — expand from all 2n − 1 possible centers

**Similar problems:**
- **Longest Palindromic Substring** — same expand-around-center, track the longest instead of counting
- **Longest Palindromic Subsequence** — interval DP, but characters can be skipped
- **Palindrome Partitioning** — use the same palindrome check as a subroutine for partitioning
- **Minimum Cuts for Palindrome Partitioning** — DP using palindrome check results

---

## Real World Use Cases

### 1. DNA motif detection in bioinformatics
Palindromic sequences in DNA (where the reverse complement matches the original)
are recognition sites for restriction enzymes. Counting and locating all
palindromic substrings in a genome sequence is a direct application of this
algorithm at scale.

### 2. Natural language processing — symmetry detection
NLP pipelines that detect symmetric or repetitive patterns in text (for
stylometric analysis or authorship attribution) use palindrome-counting as
one signal. The expand-around-center approach processes large corpora efficiently.

### 3. Data compression — run-length encoding preprocessing
Identifying palindromic regions in data streams helps compression algorithms
find redundant patterns. Palindromic substrings indicate local symmetry that
can be encoded more compactly.

---

## Key Takeaways

- Every palindrome has a center — expand outward from all `2n - 1` possible centers
- Odd-length palindromes expand from a single character; even-length from a gap between two characters
- Count inside the expansion loop, not after it — each successful expansion is a distinct palindrome
- The expand-around-center approach achieves O(n²) time with O(1) space — better than the DP table
- This problem differs from Longest Palindromic Subsequence: substrings are contiguous, subsequences are not

---

|---|---|
| `word[i] == word[j]` AND inner is palindrome | `dp[i][j] = True`, increment count |
| `word[i] != word[j]` | `dp[i][j] = False` — no need to check inside |
| Length 1 (`i == j`) | Always `True` — base case |
| Length 2 (`j == i + 1`) | `True` iff `word[i] == word[j]` |
| Fill order (tabulated) | By interval length: short → long |
| Final answer | Count of all `True` cells |

---

## Complexity

| Solution | Time | Space |
|---|---|---|
| Memoized Recursion | O(n²) | O(n²) — cache for all (i, j) pairs |
| Interval DP (table) | O(n²) | O(n²) — full n×n boolean grid |
| Expand Around Center | O(n²) | **O(1)** — no grid needed |

Where `n` = length of `word`.

> Time is O(n²) for all three: each (i, j) pair is visited at most once. Space improves from O(n²) to O(1) with the center-expansion approach.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #647](https://leetcode.com/problems/palindromic-substrings/) | Palindromic Substrings | Medium |

> This problem is part of the **NeetCode 150** interview prep list.
