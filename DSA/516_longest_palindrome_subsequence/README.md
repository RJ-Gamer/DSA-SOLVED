# 516. Longest Palindromic Subsequence

**LeetCode:** [Problem #516](https://leetcode.com/problems/longest-palindromic-subsequence/)
**Difficulty:** Medium
**Topics:** `String` `Dynamic Programming`

---

## Problem Statement

Given a string `s`, find the longest subsequence of `s` that is a palindrome.
Return its length.

A **subsequence** is derived from a string by deleting some (or no) characters
without changing the order of the remaining characters.

**Constraints:**
- `1 <= s.length <= 1000`
- `s` consists only of lowercase English letters

### Example
```
Input:  s = "bbbab"
Output: 4
Explanation: One possible longest palindromic subsequence is "bbbb".
```

```
Input:  s = "cbbd"
Output: 2
Explanation: One possible longest palindromic subsequence is "bb".
```

```
Input:  s = "total"
Output: 3
Explanation: The longest palindromic subsequence is "tot".
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need the longest subsequence of a single string that reads the same forwards
and backwards. Unlike substrings, subsequences allow skipping characters. Unlike
Longest Common Subsequence, we only have one string — we are comparing it
against itself.

### Step 2 — Identify the constraint that matters

The key observation: check the outermost characters of any interval `[i, j]`.
- If `s[i] == s[j]` — they can form the outer shell of a palindrome. The best
  answer is `grid[i+1][j-1] + 2`.
- If `s[i] != s[j]` — at most one of them can be in the palindrome's outer
  shell. Try excluding each and take the better result: `max(grid[i+1][j], grid[i][j-1])`.

This is **Interval DP**: the answer for interval `[i, j]` depends on strictly
smaller intervals inside it.

### Step 3 — Think about data structures

We need an `n × n` grid where `grid[i][j]` = length of the longest palindromic
subsequence of `s[i..j]`. We must fill shorter intervals before longer ones.
The two-row space optimization reduces space from O(n²) to O(n).

### Step 4 — Build the intuition

Imagine a necklace of lettered beads. You can remove beads but not rearrange
them. You want the longest remaining necklace that looks the same forwards and
backwards. Start by checking the outermost beads: if they match, they form the
shell of a palindrome and you recurse inward. If they don't, try removing one
end and solve the smaller problem.

---

## Approaches

For a string of length `n`, we create an `n × n` grid:

```python
size = len(word)
grid = [[0] * size for _ in range(size)]
```

**What `grid[i][j]` means:** The length of the longest palindromic subsequence of `word[i..j]`.

For `word = "total"` (size=5), the grid has 5 rows and 5 columns. Only the **upper triangle** (where `j >= i`) is valid and meaningful:

```
      t    o    t    a    l
  t  [i=0  ?    ?    ?    ?  ]   (j=0..4)
  o  [ ×  i=1   ?    ?    ?  ]   (j=1..4)
  t  [ ×   ×   i=2   ?    ?  ]   (j=2..4)
  a  [ ×   ×    ×   i=3   ?  ]   (j=3..4)
  l  [ ×   ×    ×    ×   i=4 ]   (j=4)
```

- `×` = lower triangle (j < i) — invalid, stays 0
- `i=k` on the diagonal = `grid[k][k]` (single character)
- `?` = cells to fill
- **Top-right corner** `grid[0][4]` = the answer for the full string

---

## Step 1: Base Cases — Single Characters

Every single character is a palindrome of length 1 by itself.

```python
for i in range(size):
    grid[i][i] = 1
```

After base cases, the grid diagonal is all 1s:

```
      t    o    t    a    l
  t  [ 1    0    0    0    0 ]
  o  [ 0    1    0    0    0 ]
  t  [ 0    0    1    0    0 ]
  a  [ 0    0    0    1    0 ]
  l  [ 0    0    0    0    1 ]
```

---

## Step 2: Fill by Interval Length — The Core Loop

We fill the grid **diagonal by diagonal**, starting from intervals of length 2 and growing to the full string.

```python
for length in range(2, size + 1):  # length of the current interval
    for i in range(size - length + 1):  # starting index
        j = i + length - 1  # ending index
```

For `word = "total"`:
- `length=2`: (i=0,j=1), (i=1,j=2), (i=2,j=3), (i=3,j=4)
- `length=3`: (i=0,j=2), (i=1,j=3), (i=2,j=4)
- `length=4`: (i=0,j=3), (i=1,j=4)
- `length=5`: (i=0,j=4)   ← the full problem

---

## Step 3: The Decision at Each Cell

At each cell `grid[i][j]`, we compare the **outer characters**: `word[i]` and `word[j]`.

---

### Case A: Outer Characters Match

```
word[i] == word[j]
```

The two outer characters can form the **shell** of a palindrome. The best we can do is:
> Take the longest palindrome from the **inner** substring `word[i+1..j-1]` and wrap these two matching characters around it.

```python
grid[i][j] = grid[i + 1][j - 1] + 2
```

```
  word:  [ t  ...inner...  t ]
                              ↑ these two match
  grid[i][j] = grid[i+1][j-1] + 2
```

**Special case — length 2, matching characters:**
If `j = i + 1` (adjacent characters), the inner interval `[i+1, j-1]` = `[i+1, i]` is **empty**.
An empty interval has palindrome length 0 (already in the grid as 0).
So: `grid[i][j] = 0 + 2 = 2`. ✓ Two identical adjacent characters form a palindrome of length 2.

---

### Case B: Outer Characters Don't Match

```
word[i] != word[j]
```

The two outer characters can't both be the outer shell. We try **two options** and take the better one:

**Option 1:** Exclude `word[i]` — solve `word[i+1..j]`
```python
grid[i + 1][j]  # skip the left character
```

**Option 2:** Exclude `word[j]` — solve `word[i..j-1]`
```python
grid[i][j - 1]  # skip the right character
```

```python
grid[i][j] = max(grid[i + 1][j], grid[i][j - 1])
```

---

## Warm-Up Trace: "bab" (length 3)

Let's trace through a short example completely before tackling "total".

`word = "bab"`, indices: b=0, a=1, b=2

**After base cases:**
```
      b    a    b
  b  [ 1    0    0 ]
  a  [ 0    1    0 ]
  b  [ 0    0    1 ]
```

---

**Length 2:**

**(i=0, j=1): `word[0]='b'`, `word[1]='a'` → b ≠ a**
```
max( grid[1][1]=1, grid[0][0]=1 ) = 1
grid[0][1] = 1
```

**(i=1, j=2): `word[1]='a'`, `word[2]='b'` → a ≠ b**
```
max( grid[2][2]=1, grid[1][1]=1 ) = 1
grid[1][2] = 1
```

Grid so far:
```
      b    a    b
  b  [ 1    1    0 ]
  a  [ 0    1    1 ]
  b  [ 0    0    1 ]
```

---

**Length 3:**

**(i=0, j=2): `word[0]='b'`, `word[2]='b'` → b == b ✓ Match!**
```
grid[0][2] = grid[1][1] + 2 = 1 + 2 = 3
```
> The inner character `'a'` gives a palindrome of length 1. Wrapping both `b`s around it: `b-a-b` = palindrome of length 3. ✓

Final grid:
```
      b    a    b
  b  [ 1    1    3 ]   ← grid[0][2] = 3
  a  [ 0    1    1 ]
  b  [ 0    0    1 ]
```

**Answer: `grid[0][2]` = 3 → `"bab"` is itself a palindrome, LPS = 3.** ✓

---

## Full Trace: "total" (length 5)

`word = "total"`, indices: t=0, o=1, t=2, a=3, l=4

**After base cases:**
```
      t    o    t    a    l
  t  [ 1    0    0    0    0 ]
  o  [ 0    1    0    0    0 ]
  t  [ 0    0    1    0    0 ]
  a  [ 0    0    0    1    0 ]
  l  [ 0    0    0    0    1 ]
```

---

### Length 2: Check every adjacent pair

| (i, j) | word[i] | word[j] | Match? | Calculation | Result |
|---|---|---|---|---|---|
| (0, 1) | t | o | ✗ | max(grid[1][1]=1, grid[0][0]=1) = 1 | **1** |
| (1, 2) | o | t | ✗ | max(grid[2][2]=1, grid[1][1]=1) = 1 | **1** |
| (2, 3) | t | a | ✗ | max(grid[3][3]=1, grid[2][2]=1) = 1 | **1** |
| (3, 4) | a | l | ✗ | max(grid[4][4]=1, grid[3][3]=1) = 1 | **1** |

Grid after length 2:
```
      t    o    t    a    l
  t  [ 1    1    0    0    0 ]
  o  [ 0    1    1    0    0 ]
  t  [ 0    0    1    1    0 ]
  a  [ 0    0    0    1    1 ]
  l  [ 0    0    0    0    1 ]
```

---

### Length 3: Check every 3-character window

**(i=0, j=2): `word[0]='t'`, `word[2]='t'` → t == t ✓ Match!**
```
grid[0][2] = grid[1][1] + 2 = 1 + 2 = 3
```
> The inner character at index 1 is `'o'`. Best palindrome in `"o"` is length 1.
> Wrapping both `t`s: `t-o-t` = **3**. ✓

**(i=1, j=3): `word[1]='o'`, `word[3]='a'` → o ≠ a**
```
grid[1][3] = max( grid[2][3]=1, grid[1][2]=1 ) = 1
```

**(i=2, j=4): `word[2]='t'`, `word[4]='l'` → t ≠ l**
```
grid[2][4] = max( grid[3][4]=1, grid[2][3]=1 ) = 1
```

Grid after length 3:
```
      t    o    t    a    l
  t  [ 1    1    3    0    0 ]
  o  [ 0    1    1    1    0 ]
  t  [ 0    0    1    1    1 ]
  a  [ 0    0    0    1    1 ]
  l  [ 0    0    0    0    1 ]
```

---

### Length 4: Check every 4-character window

**(i=0, j=3): `word[0]='t'`, `word[3]='a'` → t ≠ a**
```
grid[0][3] = max( grid[1][3]=1, grid[0][2]=3 ) = 3
```
> Including `word[1..3]` = `"ota"` gives LPS = 1.
> Including `word[0..2]` = `"tot"` gives LPS = 3. → Take 3.

**(i=1, j=4): `word[1]='o'`, `word[4]='l'` → o ≠ l**
```
grid[1][4] = max( grid[2][4]=1, grid[1][3]=1 ) = 1
```

Grid after length 4:
```
      t    o    t    a    l
  t  [ 1    1    3    3    0 ]
  o  [ 0    1    1    1    1 ]
  t  [ 0    0    1    1    1 ]
  a  [ 0    0    0    1    1 ]
  l  [ 0    0    0    0    1 ]
```

---

### Length 5: The Full String

**(i=0, j=4): `word[0]='t'`, `word[4]='l'` → t ≠ l**
```
grid[0][4] = max( grid[1][4]=1, grid[0][3]=3 ) = 3
```
> Including `word[1..4]` = `"otal"` gives LPS = 1.
> Including `word[0..3]` = `"tota"` gives LPS = 3. → Take 3.

**Final grid:**
```
      t    o    t    a    l
  t  [ 1    1    3    3    3 ]   ← grid[0][4] = 3
  o  [ 0    1    1    1    1 ]
  t  [ 0    0    1    1    1 ]
  a  [ 0    0    0    1    1 ]
  l  [ 0    0    0    0    1 ]
```

**Answer: `grid[0][4]` = 3 → LPS of `"total"` is `"tot"` (length 3).** ✓

---

### Approach 1 — Full Grid (Tabulation)

```python
class Solution:
    def longest_palindrome_subsequence(self, word: str) -> int:
        """
        Time Complexity: O(n^2) — fill every cell in the upper triangle
        Space Complexity: O(n^2) — the full n×n grid
        """
        size = len(word)
        grid = [[0] * size for _ in range(size)]

        for i in range(size):
            grid[i][i] = 1  # base case: single characters are palindromes of length 1

        for length in range(2, size + 1):  # length of the substring
            for i in range(size - length + 1):  # starting index of the substring
                j = i + length - 1  # ending index of the substring
                if word[i] == word[j]:
                    grid[i][j] = (
                        grid[i + 1][j - 1] + 2
                    )  # if characters match, add 2 to the result from the inner substring
                else:
                    grid[i][j] = max(
                        grid[i + 1][j], grid[i][j - 1]
                    )  # if characters don't match, take the maximum from either excluding the left character or the right character

        return grid[0][
            size - 1
        ]  # the result for the whole string is in the top-right corner


sol = Solution()
print(sol.longest_palindrome_subsequence("total"))  # Output: 3
print(sol.longest_palindrome_subsequence("loop"))  # Output: 2
```

---

### Approach 2 — Optimal (Two-Row Space Optimization)

### The Key Insight

Look at the dependencies when computing `grid[i][j]`:

```
grid[i][j] depends on:
  grid[i+1][j-1]   ← one row BELOW, one column LEFT
  grid[i+1][j]     ← one row BELOW, same column
  grid[i][j-1]     ← same row, one column LEFT (already computed)
```

All needed values come from:
1. The row **below** the current row (`i+1`) — **but only the part we've already filled**
2. The **current row** to the left (already computed left-to-right)

This means if we process the grid **bottom-to-top** (from `i = size-1` down to `i = 0`), we only need to keep track of:
- `prev_row` — the row we just finished (row `i+1`) 
- `curr_row` — the row we're currently filling (row `i`)

Think of it like peeling a necklace layer by layer from the bottom: once you've built a row, you only need it to build the row above it — then you can reuse the paper.

### Mapping the 2D Grid to Two 1D Rows

| 2D grid access | 1D equivalent |
|---|---|
| `grid[i+1][j]` | `prev_row[j]` |
| `grid[i+1][j-1]` | `prev_row[j-1]` |
| `grid[i][j-1]` | `curr_row[j-1]` (already written) |

### How the Loop Works

We process **row by row from bottom to top** (`i` from `size-1` down to `0`).

For each row `i`:
1. Set `curr_row[i] = 1` (diagonal base case — `word[i..i]`)
2. Fill `curr_row[j]` for `j` from `i+1` to `size-1` (left to right)
3. Swap `prev_row` and `curr_row`, then reset `curr_row` to zeros

After each swap:
- What was `curr_row` (just filled for row `i`) becomes the new `prev_row`
- A fresh `curr_row` is ready for row `i-1`

After the final iteration (`i=0`) and the final swap, the completed row 0 has moved into `prev_row`. So the answer is `prev_row[size-1]`.

---

### Step-by-Step Trace: "bab" (size=3)

**Initial:** `prev_row = [0, 0, 0]`, `curr_row = [0, 0, 0]`

---

**i=2 (bottom row — just the last character `b`):**
```
curr_row[2] = 1       (base case: word[2..2] = "b", LPS = 1)
No j loop (range(3, 3) is empty)
```
Swap: `prev_row = [0, 0, 1]`, `curr_row = [0, 0, 0]`

---

**i=1 (second-to-last row — starting at `a`):**
```
curr_row[1] = 1       (base case: word[1..1] = "a", LPS = 1)

j=2: word[1]='a', word[2]='b' → a ≠ b
     curr_row[2] = max(prev_row[2]=1, curr_row[1]=1) = 1
```
Swap: `prev_row = [0, 1, 1]`, `curr_row = [0, 0, 0]`

---

**i=0 (top row — starting at `b`):**
```
curr_row[0] = 1       (base case: word[0..0] = "b", LPS = 1)

j=1: word[0]='b', word[1]='a' → b ≠ a
     curr_row[1] = max(prev_row[1]=1, curr_row[0]=1) = 1

j=2: word[0]='b', word[2]='b' → b == b  ✓ Match!
     curr_row[2] = prev_row[j-1] + 2
               = prev_row[1] + 2
               = 1 + 2 = 3
```
Swap: `prev_row = [1, 1, 3]`, `curr_row = [0, 0, 0]`

---

**Answer: `prev_row[2]` = 3** ✓

> **Why `prev_row[j-1]` and not `curr_row[j-1]` for the match case?**
>
> When characters match, we need `grid[i+1][j-1]` — that's the row **below** us (row `i+1`), one column to the left. In our two-row system, row `i+1` is stored in `prev_row`. So we access `prev_row[j-1]`. ✓

---

### The Code

```python
class Solution:
    def longest_palindrome_subsequence_optimized(self, word: str) -> int:
        size = len(word)

        curr_row = [0] * size
        prev_row = [0] * size

        for i in range(size - 1, -1, -1):
            curr_row[i] = (
                1  # base case: single characters are palindromes of length 1 which is a diagonal in the grid
            )
            for j in range(i + 1, size):
                if word[i] == word[j]:
                    curr_row[j] = (
                        prev_row[j - 1] + 2
                    )  # if characters match, add 2 to the result from the inner substring
                else:
                    curr_row[j] = max(
                        prev_row[j], curr_row[j - 1]
                    )  # if characters don't match, take the maximum from either excluding the left character or the right character

            prev_row, curr_row = (
                curr_row,
                prev_row,
            )  # swap the rows for the next iteration
        return prev_row[
            size - 1
        ]  # the result for the whole string is in the last cell of the previous row after the final swap


sol = Solution()
print(sol.longest_palindrome_subsequence_optimized("total"))  # Output: 3
print(sol.longest_palindrome_subsequence_optimized("loop"))  # Output: 2
```

> **Why `prev_row[size-1]` and not `curr_row[size-1]` at the end?**
>
> At the end of the last iteration (`i=0`), the swap instruction moves the completed row into `prev_row` and the stale old `prev_row` into `curr_row`. Then `curr_row` gets reset. The answer was just written into what is now `prev_row`. So we return `prev_row[size-1]`.

---

---

## Solution Breakdown — Step by Step

```python
def longest_palindrome_subsequence(word: str) -> int:
    size = len(word)
    prev_row = [0] * size
    curr_row = [0] * size
    for i in range(size - 1, -1, -1):
        curr_row[i] = 1
        for j in range(i + 1, size):
            if word[i] == word[j]:
                curr_row[j] = prev_row[j - 1] + 2
            else:
                curr_row[j] = max(prev_row[j], curr_row[j - 1])
        prev_row, curr_row = curr_row, prev_row
        curr_row = [0] * size
    return prev_row[size - 1]
```

**Line by line:**

`for i in range(size - 1, -1, -1):`
- Process rows from bottom to top — shorter intervals before longer ones
- Row `i` represents all intervals starting at index `i`

`curr_row[i] = 1`
- Base case: a single character `word[i..i]` is always a palindrome of length 1

`if word[i] == word[j]: curr_row[j] = prev_row[j-1] + 2`
- Characters match — wrap them around the best palindrome in the inner interval
- `prev_row[j-1]` = `grid[i+1][j-1]` (row below, one column left)

`curr_row[j] = max(prev_row[j], curr_row[j-1])`
- Characters don't match — take the better of excluding the left or right character
- `prev_row[j]` = `grid[i+1][j]` (skip left), `curr_row[j-1]` = `grid[i][j-1]` (skip right)

`prev_row, curr_row = curr_row, prev_row; curr_row = [0] * size`
- Promote the finished row to `prev_row`, reset `curr_row` for the next iteration

`return prev_row[size - 1]`
- After the final swap, the completed top row lives in `prev_row`; its last element is the answer

---

## Common Mistakes

**1. Returning `prev_row[size-1]` vs `curr_row[size-1]`**
```python
prev_row, curr_row = curr_row, prev_row
curr_row = [0] * size
return curr_row[size - 1]  # WRONG — curr_row was just reset to zeros
```
After the swap, the completed row is in `prev_row`. Always return `prev_row[size-1]`.

**2. Using `curr_row[j-1]` instead of `prev_row[j-1]` for the match case**
```python
curr_row[j] = curr_row[j - 1] + 2  # WRONG — this is the left neighbor, not the diagonal
```
When characters match, we need `grid[i+1][j-1]` — the row below, one column left.
In the two-row system that is `prev_row[j-1]`, not `curr_row[j-1]`.

**3. Filling the grid left-to-right instead of bottom-to-top**
Interval DP requires solving shorter intervals before longer ones. Processing
bottom-to-top (decreasing `i`) ensures `grid[i+1][...]` is always ready when
we compute `grid[i][...]`.

**4. Confusing LPS with Palindromic Substrings**
LPS allows skipping characters (subsequence). Palindromic Substrings counts
contiguous slices only. They use different recurrences.

---

## Pattern Recognition

> Use the **interval DP** pattern when you see:
> - "Longest palindromic subsequence of a string"
> - A single-string problem where the subproblem is defined by a start and end index
> - The answer for `[i, j]` depends on strictly smaller intervals inside it

**Similar problems:**
- **Palindromic Substrings** — same interval structure, count palindromes instead of finding the longest
- **Minimum Insertions to Make a String Palindrome** — `n - LPS(s)` gives the answer
- **Longest Common Subsequence** — LPS of `s` equals LCS of `s` and `reverse(s)`
- **Burst Balloons** — interval DP where the subproblem is also defined by `[i, j]`

---

## Real World Use Cases

### 1. RNA secondary structure prediction in bioinformatics
RNA molecules fold back on themselves to form palindromic base-pair structures.
Finding the longest palindromic subsequence of an RNA sequence identifies the
most stable folding configuration — a direct application of this algorithm in
computational biology.

### 2. Data compression — symmetric pattern detection
Identifying the longest palindromic subsequence in a data stream helps
compression algorithms detect symmetric redundancy. Regions with long LPS
can be encoded more compactly using back-references.

### 3. Cryptographic sequence analysis
In certain cipher analysis tasks, finding the longest palindromic subsequence
of an encoded message helps identify repeating symmetric patterns that may
reveal structural properties of the encryption key.

---

## Key Takeaways

- `grid[i][j]` = length of the longest palindromic subsequence of `s[i..j]`
- Matching outer characters extend the inner palindrome by 2; mismatches take the max of two sub-intervals
- Fill order must be bottom-to-top (shorter intervals first) — not top-to-bottom
- The two-row optimization reduces space from O(n²) to O(n) with no time penalty
- LPS of `s` equals LCS of `s` and `reverse(s)` — a useful alternative formulation

---

|---|---|
| Single character `word[i..i]` | Base case: LPS = 1 |
| `word[i] == word[j]` | `grid[i][j] = grid[i+1][j-1] + 2` |
| `word[i] != word[j]` | `grid[i][j] = max(grid[i+1][j], grid[i][j-1])` |
| Fill order | By interval length: short → long |
| Final answer (full grid) | `grid[0][n-1]` — top-right corner |
| Final answer (optimized) | `prev_row[n-1]` — after last swap |

---

## Complexity

| Solution | Time | Space |
|---|---|---|
| Full Grid | O(n²) | O(n²) — stores the full n×n grid |
| Space-Optimized | O(n²) | O(n) — only two rows at a time |

Where `n` = length of `word`.

> Time remains O(n²) in both solutions because we still visit every cell in the upper triangle exactly once. Space improves from O(n²) to O(n) by keeping only two rows.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #516](https://leetcode.com/problems/longest-palindromic-subsequence/) | Longest Palindromic Subsequence | Medium |

> This problem is part of the **NeetCode 150** interview prep list.
