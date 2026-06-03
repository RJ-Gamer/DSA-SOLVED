# 547. Number of Provinces

**LeetCode:** [https://leetcode.com/problems/number-of-provinces/](https://leetcode.com/problems/number-of-provinces/)
**Difficulty:** Medium
**Topics:** [Union-Find] [Graph] [DFS]

---

## Problem Statement

There are `n` cities. Some of them are connected, while some are not. If city `a` is connected to city `b`, and city `b` is connected to city `c`, then city `a` is connected to city `c`.

A province is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the ith city and jth city are directly connected, and `isConnected[i][j] = 0` otherwise.

Return the total number of provinces.

### Constraints
- `1 <= n <= 200`
- `n == isConnected.length`
- `n == isConnected[i].length`
- `isConnected[i][i] == 1`
- `isConnected[i][j] == isConnected[j][i]`

### Example
```
Input:  isConnected = [[1,1,0],[1,1,0],[0,0,1]]
        
        City 0 - City 1
        
        City 2

Output: 2

Input:  isConnected = [[1,0,0],[0,1,0],[0,0,1]]
        
        City 0    City 1    City 2

Output: 3
```

---

## How to Think About This Problem

### Step 1 — Recognize this as a connected components problem
A province is a group of directly or indirectly connected cities. This is identical to finding the number of connected components in a graph.

### Step 2 — Identify the graph representation
The adjacency matrix `isConnected[i][j] = 1` means there's an edge between city i and city j. This is an undirected graph.

### Step 3 — Choose detection strategy
Two main approaches: DFS (traverse each component) or Union-Find (union connected cities, count distinct roots).

### Step 4 — Determine which is simpler
Both work equally well. DFS is more intuitive; Union-Find is more elegant for connectivity problems.

---

## Approaches

### Approach 1 — DFS (Graph Traversal)
**Intuition:** For each unvisited city, start DFS and mark all connected cities as visited. Each DFS call represents one province.

**Steps:**
1. Create visited array to track visited cities
2. Initialize province counter = 0
3. For each city:
   - If not visited:
     - Start DFS from that city
     - Mark all connected cities as visited
     - Increment province counter
4. Return province counter

**DFS Logic:**
- Mark current city as visited
- For each neighbor connected to current city:
  - If not visited, recursively visit

**Illustration:** Example 1 with adjacency matrix
```
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]

City 0 (visited=false): Start DFS
  DFS(0): visited[0]=true, check neighbors
    Neighbor 1: connected (isConnected[0][1]=1), DFS(1)
    DFS(1): visited[1]=true, check neighbors
      Neighbor 0: already visited
      Neighbor 2: not connected (isConnected[1][2]=0)
  Province count = 1

City 1 (visited=true): Skip

City 2 (visited=false): Start DFS
  DFS(2): visited[2]=true, check neighbors
    No connected neighbors
  Province count = 2

Return 2
```

**Complexity:** Time O(n²) check all adjacency matrix entries / Space O(n) for visited array

---

### Approach 2 — Union-Find (Disjoint Set Union)
**Intuition:** Union all connected cities, then count the number of distinct root parents. Each distinct root is a province.

**Union-Find Operations:**
- `find(x)`: Find root parent of x (with path compression)
- `union(x, y)`: Connect x and y's components (with union by rank)

**Steps:**
1. Initialize Union-Find with n cities (each city is its own parent)
2. For each pair (i, j) where isConnected[i][j] = 1:
   - Union cities i and j
3. Count the number of distinct roots (provinces)

**Illustration:** Same example
```
Initial: parent = [0, 1, 2] (each city is own parent)

isConnected[0][1] = 1: Union(0, 1)
  parent[1] = 0 -> parent = [0, 0, 2]
  (City 1's root becomes 0)

isConnected[0][2] = 0: Skip

isConnected[1][2] = 0: Skip

Count distinct roots: find(0)=0, find(1)=0, find(2)=2
Distinct roots: {0, 2} = 2 provinces
```

**Complexity:** Time O(n² * α(n)) where α is inverse Ackermann (nearly O(n²)) / Space O(n)

---

## Solution Breakdown — Step by Step

### DFS Solution
```python
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = [False] * n
    provinces = 0
    
    def dfs(city):
        visited[city] = True
        
        for neighbor in range(n):
            # If connected and not visited
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)
    
    for i in range(n):
        if not visited[i]:
            dfs(i)           # Explore this province
            provinces += 1   # Found one province
    
    return provinces
```

**Line-by-line:**
- `visited = [False] * n`: Track visited cities
- `provinces = 0`: Province counter
- `def dfs(city):`: DFS explores all cities in one province
- `visited[city] = True`: Mark as visited
- `for neighbor in range(n):`: Check all potential neighbors
- `if isConnected[city][neighbor] == 1`: Is there an edge?
- `and not visited[neighbor]`: Not yet visited?
- `dfs(neighbor)`: Recursively explore
- Main loop: For each unvisited city, start DFS and count province

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| DFS | O(n²) | O(n) |
| Union-Find | O(n² * α(n)) | O(n) |

Both are essentially O(n²) for this problem

---

## Common Mistakes

### Mistake 1 — Forgetting adjacency matrix is 1-indexed for self-loops
❌ **Wrong:**
```python
for i in range(n):
    for j in range(n):
        if isConnected[i][j] == 1:  # This includes i==j (self-loop)!
            # May cause issues
```

✅ **Correct:**
```python
for i in range(n):
    for j in range(i+1, n):  # Only check j > i to avoid duplicates
        if isConnected[i][j] == 1:
            union(i, j)
```

### Mistake 2 — Not marking as visited in DFS
❌ **Wrong:**
```python
def dfs(city):
    for neighbor in range(n):
        if isConnected[city][neighbor] == 1:
            dfs(neighbor)  # Missing: visited[city] = True at start!
```

✅ **Correct:**
```python
def dfs(city):
    visited[city] = True  # Mark FIRST to avoid infinite loop
    for neighbor in range(n):
        if isConnected[city][neighbor] == 1 and not visited[neighbor]:
            dfs(neighbor)
```

### Mistake 3 — Union-Find without path compression
❌ **Wrong:**
```python
def find(x):
    if parent[x] != x:
        return find(parent[x])  # No path compression
    return x
```

✅ **Correct:**
```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression!
    return parent[x]
```

---

## Pattern Recognition

> Use this pattern when you see: Connected components, provinces, clusters, connected groups, or any problem asking "how many groups of connected elements?"

**Similar problems:**
- LeetCode 200: Number of Islands
- LeetCode 684: Redundant Connection
- LeetCode 1579: Remove Max Number of Edges to Keep Graph Fully Connected

---

## Real World Use Cases

### 1. Social Network Analysis
Finding friend groups or communities (connected users).

### 2. Network Routing
Identifying connected network segments for routing protocols.

### 3. Computer Vision
Finding connected regions in image processing and object detection.

### 4. Mesh Networks
Identifying connected devices or regions in wireless networks.

---

## Key Takeaways

- Provinces are connected components in an undirected graph
- DFS approach: mark cities as visited, count connected components
- Union-Find approach: union connected cities, count distinct roots
- Both approaches have the same time complexity for this problem
- Union-Find is typically preferred for "connectivity" problems due to elegance
- Understanding when to use each approach is crucial for interview success

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | Number of Provinces | Medium |
| [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | Number of Islands | Medium |
| [LeetCode #684](https://leetcode.com/problems/redundant-connection/) | Redundant Connection | Medium |

> Excellent Union-Find introduction — master this before advanced Union-Find problems.
