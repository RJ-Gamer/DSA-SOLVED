# 72. Edit Distance

**LeetCode:** [Problem #72](https://leetcode.com/problems/edit-distance/)
**Difficulty:** Medium
**Topics:** `String` `Dynamic Programming`

---

## Problem Statement

Given two strings `word1` and `word2`, return the minimum number of operations
required to convert `word1` into `word2`.

You have three operations, each costing 1:
- **Insert** a character
- **Delete** a character
- **Replace** a character

This minimum is known as the **Levenshtein distance**.

**Constraints:**
- `0 <= word1.length, word2.length <= 500`
- `word1` and `word2` consist of lowercase English letters

### Example
```
Input:  word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse → rorse (replace 'h' with 'r')
rorse → rose  (delete 'r')
rose  → ros   (delete 'e')
```

```
Input:  word1 = "intention", word2 = "execution"
Output: 5
```

```
Input:  word1 = "", word2 = "abc"
Output: 3
Explanation: Three insertions needed.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need the minimum number of single-character edits (insert, delete, replace)
to transform one string into another. The order of operations matters, but we
don't need to track the actual sequence — only the minimum count.

### Step 2 — Identify the constraint that matters

At each position, we compare one character from each string. If they match,
no operation is needed. If they don't, we must choose the cheapest of three
operations. The cost of each choice depends on the costs of smaller subproblems
— this is the classic overlapping subproblem structure of DP.

### Step 3 — Think about data structures

We build a 2D grid where `grid[i][j]` = minimum edits to convert the first `j`
characters of `word1` into the first `i` characters of `word2`. Each cell
depends on three neighbors: diagonal (replace/match), left (delete), above (insert).

### Step 4 — Build the intuition

Think of the grid as a scoreboard tracking partial progress. The first row
represents converting any prefix of `word1` into an empty string (all deletes).
The first column represents converting an empty string into any prefix of `word2`
(all inserts). Every other cell picks the cheapest of three operations.

---

## The Three Operations and Their Neighbors

```
┌───────────┬───────────┐
│ diagonal  │   above   │
│ [i-1][j-1]│  [i-1][j] │
│  REPLACE  │  INSERT   │
├───────────┼───────────┤
│   left    │  current  │
│  [i][j-1] │   [i][j]  │
│  DELETE   │           │
└───────────┴───────────┘
```

- **Diagonal** = both characters consumed (replace or free match)
- **Above** = only the target character consumed (insert into source)
- **Left** = only the source character consumed (delete from source)

---

## Why This Is a Grid Pattern Problem

You already know the **Grid Pattern**: fill a 2D table where each cell's answer depends on its neighbors. Edit Distance is the most powerful application of this pattern.

Here's the big idea:

> `grid[i][j]` = the minimum edits needed to convert the first `j` letters of `first_word` into the first `i` letters of `second_word`.

- **Rows** = characters of `second_word` (the target)
- **Columns** = characters of `first_word` (the source)
- **Each cell** answers a smaller version of the problem
- **Bottom-right corner** = the answer to the full problem

---

## The Analogy: The Editor's Scoreboard

Think of the grid as a scoreboard tracking partial progress:

> "If I've only looked at the first few letters of each word — how cheaply can I transform one into the other?"

You fill the scoreboard top-to-bottom, left-to-right. Each small answer feeds into bigger ones — until the full problem is solved.

---

## Setting Up the Grid

For `first_word = "horse"` (m=5) and `second_word = "ros"` (n=3):

- The grid has **n+1 = 4 rows** (one extra for the empty string case)
- The grid has **m+1 = 6 columns** (one extra for the empty string case)

```python
grid = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
```

Visualized before filling:

```
          ""   h    o    r    s    e
     ""  [ _    _    _    _    _    _ ]
      r  [ _    _    _    _    _    _ ]
      o  [ _    _    _    _    _    _ ]
      s  [ _    _    _    _    _    _ ]
```

---

## Step 1: Fill the Base Cases

### First row: What if `second_word` is empty?

If the target is an empty string `""`, the only way to reach it from any prefix of `first_word` is to **delete all its letters**.

- Convert `"h"` to `""` → 1 delete
- Convert `"ho"` to `""` → 2 deletes
- Convert `"hor"` to `""` → 3 deletes
- ...and so on

```python
for i in range(m + 1):
    grid[0][i] = i  # row 0: cost is the column index
```

### First column: What if `first_word` is empty?

If the source is an empty string `""`, the only way to build any prefix of `second_word` is to **insert all its letters**.

- Convert `""` to `"r"` → 1 insert
- Convert `""` to `"ro"` → 2 inserts
- Convert `""` to `"ros"` → 3 inserts

```python
for i in range(n + 1):
    grid[i][0] = i  # column 0: cost is the row index
```

After filling base cases:

```
          ""   h    o    r    s    e
     ""  [ 0    1    2    3    4    5 ]
      r  [ 1    _    _    _    _    _ ]
      o  [ 2    _    _    _    _    _ ]
      s  [ 3    _    _    _    _    _ ]
```

**Read the first row:** Converting `"horse"` (any prefix) into `""` costs 1, 2, 3, 4, 5 deletions.
**Read the first column:** Converting `""` into `"ros"` (any prefix) costs 1, 2, 3 insertions.

---

## Step 2: The Heart of the Solution — Three Neighbors, Three Operations

Now we fill every interior cell. At cell `grid[i][j]`, we compare:
- `first_word[j-1]` — the current character from the source
- `second_word[i-1]` — the current character from the target

We have **two cases**:

---

### Case A: Characters Match — Free Pass

If `first_word[j-1] == second_word[i-1]`, these two characters are already aligned. **No operation needed!**

We simply carry over whatever the cost was **before we looked at either of these characters** — that's the diagonal neighbor.

```python
if first_word[j - 1] == second_word[i - 1]:
    grid[i][j] = grid[i - 1][j - 1]  # diagonal: free — characters already match
```

Think of it as: *"These two characters cancel each other out. Pretend they were never there."*

---

### Case B: Characters Don't Match — Pick the Cheapest Operation

When `first_word[j-1] != second_word[i-1]`, we **must** use one operation. We have three choices, each corresponding to a different neighbor:

```
┌───────────┬───────────┐
│ diagonal  │   above   │
│ [i-1][j-1]│  [i-1][j] │
├───────────┼───────────┤
│   left    │  current  │
│  [i][j-1] │   [i][j]  │
└───────────┴───────────┘
```

Each neighbor tells a different story about which operation we just performed:

---

#### Option 1: Replace (look at the diagonal)

> **Story:** "I converted `first_word[:j-1]` to `second_word[:i-1]` (cost = `grid[i-1][j-1]`), and then I **replaced** `first_word[j-1]` with `second_word[i-1]`."

Cost = `grid[i-1][j-1] + 1`

```
horse → ros
At cell (r, h): We know cost("" → "") = 0 [diagonal].
Replace 'h' with 'r' → cost = 0 + 1 = 1.
```

---

#### Option 2: Delete (look left)

> **Story:** "I converted `first_word[:j-1]` to `second_word[:i]` (cost = `grid[i][j-1]`), and then I **deleted** `first_word[j-1]` — I didn't need that extra character."

Cost = `grid[i][j-1] + 1`

```
horse → ros
At cell (r, h): left neighbor = grid[r][""] = 1.
Delete 'h' → cost = 1 + 1 = 2.
```

---

#### Option 3: Insert (look above)

> **Story:** "I converted `first_word[:j]` to `second_word[:i-1]` (cost = `grid[i-1][j]`), and then I **inserted** `second_word[i-1]` at the end — I needed that extra character in the target."

Cost = `grid[i-1][j] + 1`

```
horse → ros
At cell (r, h): above neighbor = grid[""][h] = 1.
Insert 'r' → cost = 1 + 1 = 2.
```

---

#### The decision:

```python
else:
    grid[i][j] = 1 + min(
        grid[i - 1][j - 1],  # replace
        grid[i][j - 1],      # delete
        grid[i - 1][j],      # insert
    )
```

We take whichever operation leads to the smallest total cost.

---

## Step 3: Complete Grid Walkthrough — "horse" → "ros"

Let's fill every cell, row by row.

### Row `r` (i=1): Converting `first_word` prefixes → `"r"`

**Cell (r, h):** `h ≠ r`
```
min( replace: grid[0][0]=0, delete: grid[1][0]=1, insert: grid[0][1]=1 ) = 0
grid[1][1] = 1 + 0 = 1
```
> Cheapest: replace `h` with `r`. Cost: 1.

**Cell (r, o):** `o ≠ r`
```
min( replace: grid[0][1]=1, delete: grid[1][1]=1, insert: grid[0][2]=2 ) = 1
grid[1][2] = 1 + 1 = 2
```
> Cheapest: replace `h→r` then delete `o`. Cost: 2.

**Cell (r, r):** `r == r` — **Free pass!**
```
grid[1][3] = grid[0][2] = 2
```
> `r` and `r` already match. Cost stays at 2 (same as converting `"ho"` to `""`).

**Cell (r, s):** `s ≠ r`
```
min( replace: grid[0][3]=3, delete: grid[1][3]=2, insert: grid[0][4]=4 ) = 2
grid[1][4] = 1 + 2 = 3
```

**Cell (r, e):** `e ≠ r`
```
min( replace: grid[0][4]=4, delete: grid[1][4]=3, insert: grid[0][5]=5 ) = 3
grid[1][5] = 1 + 3 = 4
```

Row `r` filled:
```
          ""   h    o    r    s    e
     ""  [ 0    1    2    3    4    5 ]
      r  [ 1    1    2    2    3    4 ]
```

---

### Row `o` (i=2): Converting `first_word` prefixes → `"ro"`

**Cell (o, h):** `h ≠ o`
```
min( replace: grid[1][0]=1, delete: grid[2][0]=2, insert: grid[1][1]=1 ) = 1
grid[2][1] = 1 + 1 = 2
```

**Cell (o, o):** `o == o` — **Free pass!**
```
grid[2][2] = grid[1][1] = 1
```
> `o` matches `o`. Carry forward the cost of converting `"h"` → `"r"` which was 1.

**Cell (o, r):** `r ≠ o`
```
min( replace: grid[1][2]=2, delete: grid[2][2]=1, insert: grid[1][3]=2 ) = 1
grid[2][3] = 1 + 1 = 2
```

**Cell (o, s):** `s ≠ o`
```
min( replace: grid[1][3]=2, delete: grid[2][3]=2, insert: grid[1][4]=3 ) = 2
grid[2][4] = 1 + 2 = 3
```

**Cell (o, e):** `e ≠ o`
```
min( replace: grid[1][4]=3, delete: grid[2][4]=3, insert: grid[1][5]=4 ) = 3
grid[2][5] = 1 + 3 = 4
```

Row `o` filled:
```
          ""   h    o    r    s    e
     ""  [ 0    1    2    3    4    5 ]
      r  [ 1    1    2    2    3    4 ]
      o  [ 2    2    1    2    3    4 ]
```

---

### Row `s` (i=3): Converting `first_word` prefixes → `"ros"`

**Cell (s, h):** `h ≠ s`
```
min( replace: grid[2][0]=2, delete: grid[3][0]=3, insert: grid[2][1]=2 ) = 2
grid[3][1] = 1 + 2 = 3
```

**Cell (s, o):** `o ≠ s`
```
min( replace: grid[2][1]=2, delete: grid[3][1]=3, insert: grid[2][2]=1 ) = 1
grid[3][2] = 1 + 1 = 2
```

**Cell (s, r):** `r ≠ s`
```
min( replace: grid[2][2]=1, delete: grid[3][2]=2, insert: grid[2][3]=2 ) = 1
grid[3][3] = 1 + 1 = 2
```

**Cell (s, s):** `s == s` — **Free pass!**
```
grid[3][4] = grid[2][3] = 2
```
> `s` matches `s`. Inherit cost of converting `"hor"` → `"ro"` which was 2.

**Cell (s, e):** `e ≠ s`
```
min( replace: grid[2][4]=3, delete: grid[3][4]=2, insert: grid[2][5]=4 ) = 2
grid[3][5] = 1 + 2 = 3
```
> Cheapest: delete `e` from `"horse"` (left neighbor), cost = 2 + 1 = **3**. ✓

---

## Fully Filled Grid

```
          ""   h    o    r    s    e
     ""  [ 0    1    2    3    4    5 ]
      r  [ 1    1    2    2    3    4 ]
      o  [ 2    2    1    2    3    4 ]
      s  [ 3    3    2    2    2    3 ]
                                   ↑
                               Answer: 3
```

`grid[3][5]` = **3** — it takes exactly 3 operations to transform `"horse"` into `"ros"`.

The actual 3-step path we traced:
1. Replace `h` → `r`
2. Delete `r` (the second one in `"rorse"`)
3. Delete `e`

---

## Solution Breakdown — Step by Step

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    grid = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        grid[0][i] = i
    for i in range(n + 1):
        grid[i][0] = i
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[j - 1] == word2[i - 1]:
                grid[i][j] = grid[i - 1][j - 1]
            else:
                grid[i][j] = 1 + min(grid[i - 1][j - 1], grid[i][j - 1], grid[i - 1][j])
    return grid[n][m]
```

**Line by line:**

`grid = [[0] * (m + 1) for _ in range(n + 1)]`
- Creates an `(n+1) × (m+1)` grid — one extra row and column for the empty string base cases

`for i in range(m + 1): grid[0][i] = i`
- First row: converting any prefix of `word1` to an empty string costs `i` deletions

`for i in range(n + 1): grid[i][0] = i`
- First column: converting an empty string to any prefix of `word2` costs `i` insertions

`if word1[j-1] == word2[i-1]: grid[i][j] = grid[i-1][j-1]`
- Characters match — no operation needed, carry the diagonal cost forward

`grid[i][j] = 1 + min(grid[i-1][j-1], grid[i][j-1], grid[i-1][j])`
- Characters differ — add 1 for the operation, pick the cheapest neighbor
- Diagonal = replace, left = delete, above = insert

`return grid[n][m]`
- Bottom-right corner holds the answer for the full strings

---

## Common Mistakes

**1. Confusing which dimension is rows vs columns**
```python
grid = [[0] * (n + 1) for _ in range(m + 1)]  # rows = word1, cols = word2
# vs
grid = [[0] * (m + 1) for _ in range(n + 1)]  # rows = word2, cols = word1
```
Both work as long as you are consistent. The convention here is rows = `word2`
(target), columns = `word1` (source). Mixing them up produces wrong answers.

**2. Forgetting to fill the base cases**
```python
grid = [[0] * (m + 1) for _ in range(n + 1)]
# Missing: grid[0][i] = i and grid[i][0] = i
```
Without the base cases, the first row and column stay 0, making every cell
computed from them wrong.

**3. Using `grid[i-1][j-1]` for the mismatch case instead of `+1`**
```python
grid[i][j] = min(grid[i-1][j-1], ...)  # WRONG — forgets to add 1 for the operation
```
Every mismatch costs exactly 1 operation. Always add 1 before taking the min.

**4. Returning `grid[m][n]` when rows=word2, cols=word1**
```python
return grid[m][n]  # WRONG if grid has n+1 rows and m+1 columns
```
Return `grid[n][m]` when rows correspond to `word2` (length `n`) and columns
correspond to `word1` (length `m`).

---

## Pattern Recognition

> Use the **edit distance grid DP** pattern when you see:
> - "Minimum operations to transform string A into string B"
> - "Similarity score between two sequences"
> - Any problem where the cost at position `(i, j)` depends on three neighbors

**Similar problems:**
- **Longest Common Subsequence** — same grid structure, maximize matches instead of minimizing edits
- **One Edit Distance** — check if two strings are exactly 1 edit apart
- **Delete Operation for Two Strings** — minimize deletions to make strings equal (variant of LCS)
- **Minimum ASCII Delete Sum** — weighted edit distance using character ASCII values

---

## Real World Use Cases

### 1. Spell-checking and autocorrect in text editors
Autocorrect systems rank candidate corrections by their edit distance from the
typed word. Words within distance 1 or 2 are suggested first. The grid DP runs
once per keystroke against a dictionary of thousands of words — O(m × n) per
candidate.

### 2. DNA sequence alignment in bioinformatics
Comparing two DNA sequences to find mutations uses edit distance as the core
metric. Insertions, deletions, and substitutions in the genome correspond
directly to the three operations. Tools like BLAST use variants of this DP
to align sequences with billions of base pairs.

### 3. Plagiarism and diff detection in version control
Git's diff algorithm is based on the longest common subsequence (the complement
of edit distance). Finding the minimum edits between two versions of a file
produces the compact diff output shown in pull requests.

---

## Key Takeaways

- `grid[i][j]` = minimum edits to convert the first `j` chars of `word1` into the first `i` chars of `word2`
- Matching characters are free — copy the diagonal
- Mismatching characters cost 1 — take the minimum of replace (diagonal), delete (left), insert (above)
- The first row and column are the base cases: pure deletions and pure insertions
- The bottom-right corner is always the answer

---

        m, n = len(first_word), len(second_word)

        grid = [
            [0 for _ in range(m + 1)] for _ in range(n + 1)
        ]  # create a grid of size (n+1) x (m+1)

        for i in range(m + 1):
            grid[0][i] = i  # fill the first row with the column index

        for i in range(n + 1):
            grid[i][0] = i  # fill the first column with the row index

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if first_word[j - 1] == second_word[i - 1]:
                    grid[i][j] = grid[i - 1][
                        j - 1
                    ]  # if characters match, take the diagonal value
                else:
                    grid[i][j] = (
                        1
                        + min(
                            grid[i - 1][j],
                            grid[i][j - 1],
                            grid[i - 1][
                                j - 1
                            ],  # if characters don't match, take the minimum of the three adjacent values and add 1
                        )
                    )
        return grid[n][m]  # the bottom-right cell contains the minimum distance


sol = Solution()
print(sol.min_distance("horse", "ros"))  # Output: 3
print(sol.min_distance("intention", "execution"))  # Output: 5
```

---

## The Three Neighbors: A Quick Reference

```
┌──────────────────────────────────────────────────┐
│  grid[i-1][j-1]  │  grid[i-1][j]                │
│   (diagonal)     │   (above)                     │
│   = REPLACE      │   = INSERT second_word[i-1]   │
├──────────────────┼────────────────────────────── │
│  grid[i][j-1]   │   grid[i][j]  ← computing now │
│   (left)         │                               │
│   = DELETE first_word[j-1]                       │
└──────────────────────────────────────────────────┘
```

**Memory trick:**
- **Diagonal** = both characters consumed (replace or match)
- **Above** = only the target character consumed (insert)
- **Left** = only the source character consumed (delete)

---

## Quick Summary

| Situation | What we do | Neighbor used |
|---|---|---|
| Characters match | Copy diagonal — no operation | `grid[i-1][j-1]` |
| Characters differ | Replace `grid[i-1][j-1] + 1` | diagonal |
| Characters differ | Delete from source `grid[i][j-1] + 1` | left |
| Characters differ | Insert into source `grid[i-1][j] + 1` | above |
| Either string empty | Number of deletions or insertions | base case |
| Final answer | `grid[n][m]` — bottom-right corner | — |

---

## Complexity

| Type | Value | Why |
|---|---|---|
| Time | O(m × n) | We visit every cell in the grid exactly once |
| Space | O(m × n) | We store the entire grid |

Where `m` = length of `first_word`, `n` = length of `second_word`.

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #72](https://leetcode.com/problems/edit-distance/) | Edit Distance | Medium |

> This problem is part of the **Blind 75** and **NeetCode 150** interview prep lists.
