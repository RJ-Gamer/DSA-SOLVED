# 208. Implement Trie (Prefix Tree)

**LeetCode:** [https://leetcode.com/problems/implement-trie-prefix-tree/](https://leetcode.com/problems/implement-trie-prefix-tree/)
**Difficulty:** Medium
**Topics:** [Trie] [Design] [Hash Map]

---

## Problem Statement

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class with the following functions:
- `insert(word)`: Inserts the string word into the trie
- `search(word)`: Returns true if the string word is in the trie, false otherwise
- `startsWith(prefix)`: Returns true if there is a previously inserted string word that has the prefix prefix, false otherwise

### Constraints
- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters
- At most 3 * 10^4 calls in total to insert, search, and startsWith

### Example
```
Input:  
  Trie trie = new Trie();
  trie.insert("apple");
  trie.search("apple");    // return True
  trie.search("app");      // return False
  trie.startsWith("app");  // return True
  trie.insert("app");
  trie.search("app");      // return True
```

---

## How to Think About This Problem

### Step 1 — Understand the Trie structure
A Trie is a tree where each node represents a character. Paths from root to node spell out prefixes/words. This naturally supports prefix matching.

### Step 2 — Recognize the data structure design
Each node needs: a dictionary/map of children (character -> node) and a flag indicating if this completes a word.

### Step 3 — Trace through operations
- Insert "apple": Create nodes for a-p-p-l-e, mark 'e' as word end
- Search "apple": Follow a-p-p-l-e, check if 'e' is marked as word end
- StartsWith "app": Follow a-p-p, return true (even if "app" itself isn't a word)

### Step 4 — Implement each operation
Each operation follows the same path-traversal logic.

---

## Approaches

### Approach 1 — Dictionary-based Trie Nodes (Standard)
**Intuition:** Each node stores character children as a dictionary and a boolean flag for word endings.

**Structure:**
```
class TrieNode:
    - children: Dict[char, TrieNode]
    - is_word: Boolean (marks end of word)
```

**Steps:**

**Insert:**
1. Start at root
2. For each character:
   - If not in children, create new node
   - Move to child node
3. Mark final node as word ending

**Search:**
1. Start at root
2. For each character:
   - If not in children, return False
   - Move to child node
3. Return true only if final node is marked as word ending

**StartsWith:**
1. Start at root
2. For each character:
   - If not in children, return False
   - Move to child node
3. Return True (we found the prefix path)

**Illustration:** Inserting "apple", "app"
```
                root
                 |
                 a
                 |
                 p
                /  \
               p    (is_word=True for "app")
               |
               l
               |
               e
             (is_word=True for "apple")

search("apple"): a->p->p->l->e, is_word=True ✓
search("app"): a->p->p, is_word=True ✓
startsWith("ap"): a->p, path exists ✓
search("ap"): a->p, is_word=False ✗
```

**Complexity:**
- Insert: O(m) where m = word length (at most m new nodes)
- Search: O(m) traverse at most m nodes
- StartsWith: O(m) traverse at most m nodes
- Space: O(ALPHABET_SIZE * N * M) for N words of avg length M

---

### Approach 2 — Array-based Trie (Optimization)
**Intuition:** Instead of dictionaries, use arrays of size 26 (for lowercase letters).

**Pros:** Faster lookup (array access vs hash map)
**Cons:** Extra space for empty slots

This approach has same time complexity but slightly faster in practice.

---

## Solution Breakdown — Step by Step

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_word = False    # marks end of word

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Root node
    
    def insert(self, word: str) -> None:
        node = self.root
        
        for char in word:
            # Create node if doesn't exist
            if char not in node.children:
                node.children[char] = TrieNode()
            
            # Move to child
            node = node.children[char]
        
        # Mark end of word
        node.is_word = True
    
    def search(self, word: str) -> bool:
        node = self.root
        
        for char in word:
            # Character not found in path
            if char not in node.children:
                return False
            
            # Move to child
            node = node.children[char]
        
        # Return true only if path ends with a word
        return node.is_word
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        
        for char in prefix:
            # Character not found in path
            if char not in node.children:
                return False
            
            # Move to child
            node = node.children[char]
        
        # Return true (prefix path exists)
        return True
```

**Line-by-line Insert:**
- `node = self.root`: Start at root
- `for char in word`: Process each character
- `if char not in node.children`: Character not yet in tree
- `node.children[char] = TrieNode()`: Create new node for character
- `node = node.children[char]`: Move to child node
- `node.is_word = True`: Mark this node as end of word

**Key Difference: Search vs StartsWith**
- `search`: Must reach a node marked `is_word=True`
- `startsWith`: Just needs to reach the node (even if not marked)

---

## Quick Summary

| Operation | Time | Space |
|---|---|---|
| Insert | O(m) | O(1) per word |
| Search | O(m) | O(1) |
| StartsWith | O(m) | O(1) |

(m = word/prefix length)

---

## Common Mistakes

### Mistake 1 — Confusing search and startsWith
❌ **Wrong:**
```python
def search(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return True  # Forgot to check is_word!
```

✅ **Correct:**
```python
def search(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_word  # Must be marked as complete word
```

### Mistake 2 — Not creating nodes on insert
❌ **Wrong:**
```python
def insert(self, word):
    node = self.root
    for char in word:
        node = node.children[char]  # Crashes if char not in children!
        node.is_word = True
```

✅ **Correct:**
```python
def insert(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()  # Create if needed
        node = node.children[char]
    node.is_word = True
```

---

## Pattern Recognition

> Use this pattern when you see: Autocomplete, spell checker, IP routing, prefix matching, or any problem requiring efficient prefix queries.

**Similar problems:**
- LeetCode 211: Design Add and Search Words Data Structure
- LeetCode 212: Word Search II
- LeetCode 1166: Design File System

---

## Real World Use Cases

### 1. Autocomplete Systems
Search engines, IDEs, and text editors use tries for efficient prefix-based suggestions.

### 2. Spell Checkers
Dictionaries stored in tries enable fast word validation and suggestions.

### 3. IP Routing
Internet routers use tries to match and route IP prefixes efficiently.

### 4. Phone Directory
Phone numbers stored in tries enable fast lookup by prefix.

---

## Key Takeaways

- Trie structure: each node has children dictionary and is_word flag
- Insert: create nodes as needed, mark end with is_word flag
- Search: must find path AND node must be marked as word
- StartsWith: just find path (don't check is_word flag)
- Space efficient for many strings with common prefixes
- Essential data structure for prefix-based queries

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/) | Implement Trie | Medium |
| [LeetCode #211](https://leetcode.com/problems/add-and-search-word-data-structure-design/) | Add and Search Word | Medium |
| [LeetCode #212](https://leetcode.com/problems/word-search-ii/) | Word Search II | Hard |

> Fundamental data structure for prefix problems — understanding this enables many advanced problems.
