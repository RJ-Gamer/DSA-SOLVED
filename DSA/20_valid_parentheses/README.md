# 20. Valid Parentheses

**LeetCode:** [https://leetcode.com/problems/valid-parentheses/](https://leetcode.com/problems/valid-parentheses/)
**Difficulty:** Easy
**Topics:** [Stack] [String]

---

## Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of bracket
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type

### Constraints
- `1 <= s.length <= 10^4`
- `s` consists of parentheses only: `'()[]{}' `

### Example
```
Input:  s = "()"
Output: true

Input:  s = "()[]{}"
Output: true

Input:  s = "([)]"
Output: false

Input:  s = "{[]}"
Output: true
```

---

## How to Think About This Problem

### Step 1 — Recognize the matching requirement
Each closing bracket must match its corresponding opening bracket. This suggests a data structure that tracks unmatched opening brackets.

### Step 2 — Understand the order requirement
If we see closing bracket, it must match the most recent unmatched opening bracket. This is LIFO (Last In First Out) behavior — a stack!

### Step 3 — Devise the algorithm
- For opening brackets: push to stack
- For closing brackets: check if it matches stack top, then pop
- At end: stack must be empty (all brackets matched)

### Step 4 — Handle edge cases
Empty string, odd length string, immediate closing bracket.

---

## Approaches

### Approach 1 — Stack (Optimal)
**Intuition:** Use a stack to track opening brackets. When we see a closing bracket, check if it matches the top of the stack.

**Steps:**
1. Create an empty stack
2. Create a mapping of closing -> opening brackets
3. For each character:
   - If opening bracket: push to stack
   - If closing bracket:
     - Stack must not be empty
     - Top of stack must be matching opening bracket
     - If not, return false
     - Pop from stack
4. Stack must be empty at end (all matched)
5. Return true if reached here

**Illustration:** For `"({[]})":`
```
Char: (
Stack: [(]

Char: {
Stack: [(, {]

Char: [
Stack: [(, {, []

Char: ]
Top is [, matches! Pop
Stack: [(, {]

Char: }
Top is {, matches! Pop
Stack: [(]

Char: )
Top is (, matches! Pop
Stack: []

End: Stack empty? YES
Return true
```

**Complexity:** Time O(n) each char processed once / Space O(n) worst case all opening brackets

---

### Approach 2 — Without HashMap (Alternative)
**Intuition:** Same as above, but use helper function to check matching instead of hashmap.

**Steps:** Same stack approach, but write matching logic differently.

**Complexity:** Time O(n) / Space O(n)

This is essentially the same algorithm with different implementation style.

---

## Solution Breakdown — Step by Step

```python
def isValid(s: str) -> bool:
    stack = []
    # Mapping closing bracket to opening bracket
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in mapping:  # Closing bracket
            # Stack must not be empty, and top must match
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:  # Opening bracket
            stack.append(char)
    
    return len(stack) == 0  # All brackets matched
```

**Line-by-line:**
- `stack = []`: Initialize empty stack
- `mapping = {')': '(', ...]`: Map each closing bracket to its opening
- `for char in s`: Process each character
- `if char in mapping`: Is this a closing bracket?
- `if not stack or stack[-1] != mapping[char]`: Check if stack is empty OR top doesn't match
  - Not empty AND matching = valid closing bracket
- `stack.pop()`: Remove the matched opening bracket
- `else: stack.append(char)`: Opening bracket, push to stack
- `return len(stack) == 0`: Valid if stack is empty (all matched)

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| Stack | O(n) | O(n) |

---

## Common Mistakes

### Mistake 1 — Not checking if stack is empty
❌ **Wrong:**
```python
if stack[-1] != mapping[char]:  # Crashes if stack is empty
    return False
```

✅ **Correct:**
```python
if not stack or stack[-1] != mapping[char]:  # Check empty first
    return False
```

### Mistake 2 — Forgetting to check stack at end
❌ **Wrong:**
```python
for char in s:
    # ... process ...
return True  # What if stack has unmatched opening brackets?
```

✅ **Correct:**
```python
for char in s:
    # ... process ...
return len(stack) == 0  # Ensure all brackets matched
```

### Mistake 3 — Wrong comparison logic
❌ **Wrong:**
```python
mapping = {'(': ')', '[': ']', '{': '}'}  # Wrong direction!
if char in mapping:  # This checks opening, not closing
```

✅ **Correct:**
```python
mapping = {')': '(', ']': '[', '}': '{'}  # Correct: closing -> opening
if char in mapping:  # This checks closing brackets
```

---

## Pattern Recognition

> Use this pattern when you see: Matching brackets/parentheses, balanced delimiters, or any problem requiring LIFO structure with matching logic.

**Similar problems:**
- LeetCode 1541: Minimum Insertions to Balance a Parentheses String
- LeetCode 921: Minimum Add to Make Parentheses Valid
- LeetCode 1249: Minimum Remove to Make Valid Parentheses
- LeetCode 856: Score of Parentheses

---

## Real World Use Cases

### 1. Compiler/Syntax Checking
All programming language compilers use this exact algorithm to validate bracket matching in source code.

### 2. Mathematical Expression Validation
Calculators and math libraries validate and parse expressions with nested brackets/parentheses.

### 3. HTML/XML Parser
Web browsers parse HTML/XML tags using stack-based matching to ensure proper nesting.

---

## Key Takeaways

- Stack is the natural choice for matching/bracketing problems due to LIFO property
- Always map closing brackets to opening brackets for easy comparison
- Check for both empty stack AND matching condition
- Don't forget to verify stack is empty at the end
- This is one of the most fundamental stack problems

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) | Valid Parentheses | Easy |
| [LeetCode #921](https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/) | Minimum Add to Make Parentheses Valid | Medium |
| [LeetCode #1541](https://leetcode.com/problems/minimum-insertions-to-balance-a-parentheses-string/) | Minimum Insertions to Balance | Medium |

> Part of the **Blind 75** — fundamental stack problem everyone should know.
