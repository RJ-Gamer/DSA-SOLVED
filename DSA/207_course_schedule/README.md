# 207. Course Schedule

**LeetCode:** [https://leetcode.com/problems/course-schedule/](https://leetcode.com/problems/course-schedule/)
**Difficulty:** Medium
**Topics:** [Graph] [Topological Sort] [DFS] [BFS]

---

## Problem Statement

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course `b` before taking course `a`.

Return `true` if you can finish all courses. Otherwise, return `false`.

### Constraints
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- All prerequisites pairs are unique

### Example
```
Input:  numCourses = 2, prerequisites = [[1,0]]
Output: true
(Take course 0 first, then course 1)

Input:  numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
(Circular dependency - impossible!)

Input:  numCourses = 1, prerequisites = []
Output: true
```

---

## How to Think About This Problem

### Step 1 — Model as a graph problem
Courses are nodes. If course A requires course B, add edge B → A (B must come before A). The problem becomes: "Is there a cycle in this directed graph?"

### Step 2 — Understand why cycles matter
If there's a cycle (e.g., A requires B, B requires C, C requires A), it's impossible to satisfy all prerequisites. If no cycle, topological sort exists, and we can finish all courses.

### Step 3 — Choose detection strategy
Two approaches: DFS with states (visiting/visited) to detect cycles, or BFS with in-degrees (Kahn's algorithm for topological sort).

### Step 4 — Implementation approach
DFS is slightly more intuitive: if we visit a node that's currently being visited, we found a cycle.

---

## Approaches

### Approach 1 — DFS with State Tracking (Intuitive)
**Intuition:** Use three states: unvisited (0), currently visiting (1), visited (2). If we encounter a node in state 1, there's a cycle.

**Steps:**
1. Build adjacency list from prerequisites
2. Track states for each course
3. For each unvisited course:
   - Mark as visiting (state 1)
   - DFS to all prerequisite courses
   - If any course is in state 1, cycle detected (return False)
   - Mark as visited (state 2) after exploring
4. If all courses processed without finding cycle, return True

**Illustration:** For prerequisites [[1,0], [0,1]]:
```
Graph: 0 -> 1 -> 0 (cycle!)

DFS from course 0:
  Mark 0 as visiting (state 1)
  Go to prerequisite 1
  Mark 1 as visiting (state 1)
  Go to prerequisite 0
  Course 0 is visiting (state 1) - CYCLE DETECTED!
  Return False
```

**Complexity:** Time O(V + E) visits each course and edge once / Space O(V + E) for graph

---

### Approach 2 — BFS with In-degree (Kahn's Algorithm)
**Intuition:** Use topological sort. If we can sort all courses, no cycle exists. If not all courses are processed, cycle exists.

**Steps:**
1. Build adjacency list and calculate in-degrees
2. Add all courses with in-degree 0 to queue (no prerequisites)
3. While queue is not empty:
   - Dequeue a course
   - Decrement in-degree of all dependent courses
   - If in-degree becomes 0, enqueue that course
4. If we processed all courses, no cycle (return True)
5. If we processed fewer courses, cycle exists (return False)

**Illustration:** Same example with BFS
```
Prerequisites: [[1,0], [0,1]]
In-degree: 0->1, 1->1 (both depend on each other!)

Queue starts: [nothing] (no course with in-degree 0)
Process: 0 courses
Total courses: 2
Processed < Total -> Cycle detected, return False
```

**Complexity:** Time O(V + E) / Space O(V + E)

---

## Solution Breakdown — Step by Step

### DFS Solution
```python
def canFinish(numCourses, prerequisites):
    # Build graph
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # States: 0=unvisited, 1=visiting, 2=visited
    states = [0] * numCourses
    
    def hasCycle(course):
        if states[course] == 1:  # Currently visiting - CYCLE!
            return True
        if states[course] == 2:  # Already visited
            return False
        
        states[course] = 1  # Mark as visiting
        
        # Check all prerequisites
        for prereq in graph[course]:
            if hasCycle(prereq):  # Found cycle in subtree
                return True
        
        states[course] = 2  # Mark as visited
        return False
    
    # Check each course for cycles
    for course in range(numCourses):
        if states[course] == 0:  # Unvisited
            if hasCycle(course):
                return False
    
    return True
```

**Line-by-line:**
- `graph[course].append(prereq)`: Build adjacency list
- `states = [0] * numCourses`: Initialize all courses as unvisited
- `if states[course] == 1: return True`: Cycle detected (we're in current path)
- `if states[course] == 2: return False`: Already processed, no cycle here
- `states[course] = 1`: Mark as currently visiting
- `for prereq in graph[course]:`: Check all prerequisites
- `if hasCycle(prereq): return True`: If any prerequisite has cycle, return
- `states[course] = 2`: Mark as completely visited
- Main loop: Process all unvisited courses

---

## Quick Summary

| Approach | Time | Space |
|---|---|---|
| DFS State Tracking | O(V + E) | O(V + E) |
| BFS In-degree (Kahn) | O(V + E) | O(V + E) |

---

## Common Mistakes

### Mistake 1 — Wrong direction of edges
❌ **Wrong:**
```python
graph[prereq].append(course)  # B -> A (wrong direction!)
# This means: if B then A
# But we want: to do A, we need B first (A -> B)
```

✅ **Correct:**
```python
graph[course].append(prereq)  # A -> B (course depends on prereq)
# This means: to do course, we need prereq first
```

### Mistake 2 — Not distinguishing states properly
❌ **Wrong:**
```python
visited = set()
if course in visited:
    return False  # Can't distinguish between: "in current path" vs "already processed"
visited.add(course)
```

✅ **Correct:**
```python
states = [0, 1, 2]  # unvisited, visiting, visited
if states[course] == 1:  # Currently in path = cycle
    return True
```

### Mistake 3 — Forgetting to count processed courses (BFS approach)
❌ **Wrong:**
```python
while queue:
    course = queue.popleft()
    # ... process ...
return True  # Didn't verify ALL courses were processed
```

✅ **Correct:**
```python
count = 0
while queue:
    count += 1
    # ... process ...
return count == numCourses  # All courses must be processed
```

---

## Pattern Recognition

> Use this pattern when you see: Course prerequisites, task scheduling with dependencies, cycle detection in graphs, or topological sorting problems.

**Similar problems:**
- LeetCode 210: Course Schedule II (order courses, not just feasibility)
- LeetCode 310: Minimum Height Trees
- LeetCode 1203: Sort Items by Groups Respecting Dependencies

---

## Real World Use Cases

### 1. Build System Dependencies
Compilers detect circular dependencies in module imports.

### 2. Project Management
Task scheduling ensures dependencies are satisfied before execution.

### 3. Software Package Management
Package managers check if dependencies form cycles before installing.

---

## Key Takeaways

- This is fundamentally a cycle detection problem in a directed graph
- Cycles make task/course completion impossible; lack of cycles means all tasks can be completed
- DFS with state tracking naturally detects cycles (state 1 in current path)
- BFS/Kahn's algorithm also works: if topological sort completes all nodes, no cycle
- Understanding graph modeling is crucial: nodes = courses, edges = dependencies

---

## Where to Practice

| Platform | Problem | Difficulty |
|---|---|---|
| [LeetCode #207](https://leetcode.com/problems/course-schedule/) | Course Schedule | Medium |
| [LeetCode #210](https://leetcode.com/problems/course-schedule-ii/) | Course Schedule II | Medium |
| [LeetCode #310](https://leetcode.com/problems/minimum-height-trees/) | Minimum Height Trees | Hard |

> Excellent introduction to topological sorting and cycle detection in graphs.
