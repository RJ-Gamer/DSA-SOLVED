# 1143. Longest Common Subsequence

**LeetCode:** [Problem #1143](https://leetcode.com/problems/longest-common-subsequence/)
**Difficulty:** Medium
**Topics:** `String` `Dynamic Programming`

---

## Problem Statement

Given two strings `text1` and `text2`, return the length of their **longest
common subsequence**. If there is no common subsequence, return `0`.

A **subsequence** is a sequence derived from a string by deleting some (or no)
characters without changing the order of the remaining characters.

A **common subsequence** is a subsequence that appears in both strings.

**Constraints:**
- `1 <= text1.length, text2.length <= 1000`
- `text1` and `text2` consist of lowercase English letters

### Example
```
Input:  text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" (length 3).
```

```
Input:  text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" (length 3).
```

```
Input:  text1 = "abc", text2 = "def"
Output: 0
Explanation: No common subsequence exists.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need the longest sequence of characters that appears in both strings in the
same relative order, but not necessarily contiguously. Unlike substrings,
subsequences allow skipping characters.

### Step 2 — Identify the constraint that matters

At each pair of positions `(i, j)`, we compare one character from each string.
If they match, we extend the best subsequence found before either character.
If they don't, we take the best result from skipping one character in either
string. This overlapping subproblem structure requires DP.

### Step 3 — Think about data structures

We build a 2D grid where `grid[i][j]` = length of the LCS of `text1[:i]` and
`text2[:j]`. Each cell depends on the diagonal (match) or the max of above/left
(skip). The full grid uses O(m × n) space; the two-row optimization reduces
this to O(n).

### Step 4 — Build the intuition

Think of filling a treasure map grid. Rows represent characters of `text1`,
columns represent characters of `text2`. Each cell answers: "What is the
longest matching chain I can build using only the characters up to this point
in both strings?" Fill left-to-right, top-to-bottom. The bottom-right corner
holds the answer.

---

## Approaches

### Step 1: Set Up the Grid

We create a grid with one **extra row and column** filled with zeros. Why? Because if either album is empty, there are zero matching stickers — easy!

```python
m = len(text1)  # number of stickers in your album
n = len(text2)  # number of stickers in your friend's album

grid = [[0] * (n + 1) for _ in range(m + 1)]
```

For `"abcde"` vs `"ace"`, the initial grid looks like this (6 rows x 4 columns):

```
     ""  a   c   e
""  [ 0   0   0   0 ]
a   [ 0   _   _   _ ]
b   [ 0   _   _   _ ]
c   [ 0   _   _   _ ]
d   [ 0   _   _   _ ]
e   [ 0   _   _   _ ]
```

The `_` cells are what we'll fill in next.

---

### Step 2: Fill the Border with Zeros

The first row and first column are already 0 (from our grid initialization). This represents:

- **First row:** Your friend's stickers vs an empty album = 0 matches
- **First column:** Your stickers vs an empty album = 0 matches

```python
for j in range(1, n):
    grid[0][j] = 0  # empty album vs friend's album = no matches

for i in range(1, m):
    grid[i][0] = 0  # your album vs empty album = no matches
```

> These are already 0 by default — this step just makes the logic explicit.

---

### Step 3: Fill the Grid — The Heart of the Solution

Now we go through every sticker in your album (row by row) and every sticker in your friend's album (column by column).

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
```

At each cell `(i, j)`, we compare sticker `text1[i-1]` (yours) and sticker `text2[j-1]` (your friend's).

---

#### Case A: The Stickers Match! 🎉

If the two stickers are the same letter, we found a new match! We take the number of matches found **before this sticker** (the diagonal cell) and add **1**.

```python
if text1[i - 1] == text2[j - 1]:
    grid[i][j] = 1 + grid[i - 1][j - 1]
```

Think of the diagonal cell as: *"What was the best chain I had before I considered either of these two stickers?"* Now I can extend that chain by 1.

```
     ""  a   c   e
""  [ 0   0   0   0 ]
a   [ 0   1   _   _ ]   ← 'a' == 'a', so diagonal (0) + 1 = 1
```

---

#### Case B: The Stickers Don't Match 😔

If the stickers are different, we can't extend any chain. Instead, we **borrow the best answer** we've seen so far by looking at either:
- The cell **above** `grid[i-1][j]` → best chain if we skip your current sticker
- The cell **to the left** `grid[i][j-1]` → best chain if we skip your friend's current sticker

We take whichever is **bigger**.

```python
else:
    grid[i][j] = max(grid[i - 1][j], grid[i][j - 1])
```

---

### Step 4: Read the Answer

After filling every cell, the **bottom-right corner** of the grid holds the answer — the length of the longest common subsequence of both full strings.

```python
return grid[m][n]
```

---

## Fully Filled Grid Example

For `"abcde"` vs `"ace"`:

```
     ""  a   c   e
""  [ 0   0   0   0 ]
a   [ 0   1   1   1 ]
b   [ 0   1   1   1 ]
c   [ 0   1   2   2 ]
d   [ 0   1   2   2 ]
e   [ 0   1   2   3 ]  ← answer is 3
```

The bottom-right cell is **3**, which matches `a-c-e`.

---

### Approach 1 — Full Grid (Tabulation)

```python
class Solution:
    def longest_common_subsequence_mxn(self, text1: str, text2: str) -> int:
        """
        Time: O(m × n)
        Space: O(m × n)
        """
        m = len(text1)
        n = len(text2)

        # Create a grid of zeros with an extra row and column
        grid = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill the grid
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    # Letters match! Extend the chain from diagonal
                    grid[i][j] = 1 + grid[i - 1][j - 1]
                else:
                    # No match — borrow the best from above or left
                    grid[i][j] = max(grid[i - 1][j], grid[i][j - 1])

        # Bottom-right corner has our answer
        return grid[m][n]


sol = Solution()
print(sol.longest_common_subsequence_mxn("abcde", "ace"))           # Output: 3
print(sol.longest_common_subsequence_mxn("september", "december"))  # Output: 6
```

---

### Approach 2 — Optimal (Two-Row Space Optimization)

### The Key Insight

Look at the recurrence again:

```
if match:     grid[i][j] = 1 + grid[i-1][j-1]   ← needs the row above, one column left
else:         grid[i][j] = max(grid[i-1][j], grid[i][j-1])  ← needs the row above, same column
```

When we're filling row `i`, we only ever look at **row `i-1`** (the previous row) and the **current row so far**. We never go further back. So we don't need to keep the entire grid — just **two rows**: `prev` (the row above) and `curr` (the row we're filling right now).

Think of it like updating a **two-line scoreboard**. Once you've used a line to compute the next one, you can erase it and reuse it.

### How It Works

```
prev  →  [row we just finished]
curr  →  [row we're building now]

After each row: swap prev ↔ curr, then reset curr to all zeros.
```

For `"abcde"` vs `"ace"`, after processing row `a` (i=1):

```
prev = [0, 1, 1, 1]   ← result of row 'a'
curr = [0, 0, 0, 0]   ← ready for row 'b'
```

After row `b` (i=2):

```
prev = [0, 1, 1, 1]   ← result of row 'b' (same as 'a' — no new matches)
curr = [0, 0, 0, 0]   ← ready for row 'c'
```

After row `c` (i=3):

```
prev = [0, 1, 2, 2]   ← 'c' matched! diagonal extended to 2
```

...and so on until `prev = [0, 1, 2, 3]` after row `e`. The answer is `prev[n]` = **3**.

### The Code

```python
class Solution:
    def longest_common_subsequence_optimal(self, first: str, second: str) -> int:
        """
        Time: O(m × n)
        Space: O(n)  — only two rows instead of the full grid
        """
        m = len(first)
        n = len(second)

        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if first[i - 1] == second[j - 1]:
                    curr[j] = 1 + prev[j - 1]  # extend chain from diagonal
                else:
                    curr[j] = max(prev[j], curr[j - 1])  # borrow best from above or left

            prev, curr = curr, prev   # finished this row — promote it to "prev"
            curr = [0] * (n + 1)      # reset curr for the next row

        return prev[n]   # prev holds the last completed row


sol = Solution()
print(sol.longest_common_subsequence_optimal("abcde", "ace"))           # Output: 3
print(sol.longest_common_subsequence_optimal("september", "december"))  # Output: 6
```

> **Why `prev[n]` and not `curr[n]`?**
> After the last iteration, we do `prev, curr = curr, prev` — which moves the finished row into `prev`. So the answer lives in `prev[n]`, not `curr[n]`.

---

---

## Solution Breakdown — Step by Step

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = 1 + prev[j - 1]
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
        curr = [0] * (n + 1)
    return prev[n]
```

**Line by line:**

`prev = [0] * (n + 1); curr = [0] * (n + 1)`
- Two rows of length `n + 1` — the extra cell at index 0 represents the empty string base case
- All zeros: LCS with an empty string is always 0

`for i in range(1, m + 1):`
- Process each character of `text1` one row at a time

`if text1[i-1] == text2[j-1]: curr[j] = 1 + prev[j-1]`
- Characters match — extend the chain from the diagonal (before either character was considered)
- `prev[j-1]` is `grid[i-1][j-1]` in the full grid — the row above, one column left

`curr[j] = max(prev[j], curr[j-1])`
- Characters don't match — take the best from skipping `text1[i-1]` (above: `prev[j]`)
  or skipping `text2[j-1]` (left: `curr[j-1]`)

`prev, curr = curr, prev; curr = [0] * (n + 1)`
- Promote the finished row to `prev`, reset `curr` for the next row

`return prev[n]`
- After the last swap, the completed row lives in `prev`; its last element is the answer

---

## Common Mistakes

**1. Returning `curr[n]` instead of `prev[n]` in the two-row approach**
```python
prev, curr = curr, prev
curr = [0] * (n + 1)
return curr[n]  # WRONG — curr was just reset to zeros
```
After the swap, the completed row is in `prev`. Always return `prev[n]`.

**2. Forgetting the extra row and column for the empty string base case**
```python
grid = [[0] * n for _ in range(m)]  # WRONG — missing the +1
```
The grid must be `(m+1) × (n+1)`. Row 0 and column 0 represent empty string
base cases and must stay 0.

**3. Using `grid[i][j-1]` for the diagonal instead of `grid[i-1][j-1]`**
```python
curr[j] = 1 + curr[j - 1]  # WRONG — this is the left neighbor, not the diagonal
```
When characters match, we need the diagonal: `prev[j-1]` (row above, column left).

**4. Confusing LCS with Longest Common Substring**
LCS allows skipping characters (subsequence). Longest Common Substring requires
contiguous characters. They use different recurrences — don't mix them up.

---

## Pattern Recognition

### How to Recognize
- Problem asks for the longest common subsequence of two strings
- Characters can be skipped — order matters but gaps are allowed
- Comparing two sequences where the subproblem is defined by one index per string

### How to Identify
- Does `LCS(i, j)` reduce to `1 + LCS(i-1, j-1)` on a character match, or `max(LCS(i-1,j), LCS(i,j-1))` on mismatch?
- Can you reduce space from O(m × n) to O(n) by keeping only the previous row?

### How to Remember
> **Mental model:** Match = extend the chain from the diagonal; mismatch = borrow the best from above or left

**Similar problems:**
- **Edit Distance** — same grid structure, counts operations instead of matches
- **Shortest Common Supersequence** — build on LCS: `len(s1) + len(s2) - LCS`
- **Delete Operation for Two Strings** — minimum deletions = `len(s1) + len(s2) - 2 * LCS`
- **Longest Increasing Subsequence** — LCS of the array with its sorted version

---

## Real World Use Cases

### 1. Diff tools and version control
Git's diff algorithm finds the longest common subsequence of lines between two
file versions. Lines in the LCS are unchanged; everything else is an insertion
or deletion. The two-row optimization is critical for diffing large files.

### 2. DNA sequence alignment in bioinformatics
Comparing two DNA or protein sequences to find conserved regions uses LCS as
the foundation. The longest common subsequence of two genomes identifies
evolutionarily conserved segments across species.

### 3. Plagiarism detection in academic systems
Plagiarism detectors compare the LCS of a submitted document against a
corpus of known works. A high LCS ratio relative to document length is a
strong signal of copied content, even when words are reordered or paraphrased.

---

## Key Takeaways

- `grid[i][j]` = LCS length of `text1[:i]` and `text2[:j]`
- Matching characters extend the diagonal; mismatches take the max of above or left
- The two-row optimization reduces space from O(m × n) to O(n) with no time penalty
- After the final row swap, the answer is in `prev[n]`, not `curr[n]`
- LCS is the foundation for edit distance, diff tools, and sequence alignment

---

|---|---|
| Letters match | Diagonal value + 1 |
| Letters don't match | Max of above or left |
| Either string is empty | 0 (no match possible) |
| Final answer (full grid) | Bottom-right cell: `grid[m][n]` |
| Final answer (optimized) | Last element of prev row: `prev[n]` |

---

## Complexity

| Solution | Time | Space |
|---|---|---|
| Full Grid | O(m × n) | O(m × n) — stores every cell |
| Space-Optimized | O(m × n) | O(n) — only two rows at a time |

Where `m` = length of `text1` / `first`, `n` = length of `text2` / `second`.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/) | Longest Common Subsequence | Medium |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
