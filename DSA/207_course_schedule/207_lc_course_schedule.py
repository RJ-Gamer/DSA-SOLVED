"""
LeetCode 207: Course Schedule
Difficulty: Medium
Topics: Graph, Topological Sort, DFS, BFS

Time Complexity: O(V + E)
Space Complexity: O(V + E)
"""

from typing import List
from collections import defaultdict, deque


def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Determine if all courses can be finished given prerequisites using DFS.
    Detects if there's a cycle in the directed graph.
    
    Args:
        numCourses: Total number of courses
        prerequisites: List of [course, prerequisite] pairs
        
    Returns:
        True if all courses can be finished, False if there's a cycle
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # States: 0 = unvisited, 1 = visiting, 2 = visited
    states = [0] * numCourses
    
    def hasCycle(course):
        if states[course] == 1:  # Currently visiting - cycle detected
            return True
        if states[course] == 2:  # Already visited
            return False
        
        states[course] = 1  # Mark as visiting
        
        for prereq in graph[course]:
            if hasCycle(prereq):
                return True
        
        states[course] = 2  # Mark as visited
        return False
    
    # Check each course for cycles
    for course in range(numCourses):
        if states[course] == 0:
            if hasCycle(course):
                return False
    
    return True


def canFinishBFS(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Determine if all courses can be finished using BFS (Kahn's algorithm for topological sort).
    
    Args:
        numCourses: Total number of courses
        prerequisites: List of [course, prerequisite] pairs
        
    Returns:
        True if all courses can be finished, False if there's a cycle
    """
    # Build graph and in-degree map
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        course = queue.popleft()
        count += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we processed all courses, no cycle exists
    return count == numCourses


# Test cases
if __name__ == "__main__":
    # Test 1: No cycle
    assert canFinish(2, [[1, 0]]) == True
    
    # Test 2: Cycle exists
    assert canFinish(2, [[1, 0], [0, 1]]) == False
    
    # Test 3: No prerequisites
    assert canFinish(3, []) == True
    
    # Test 4: Complex case - BFS
    assert canFinishBFS(4, [[1, 0], [2, 1], [3, 2]]) == True
    
    # Test 5: Complex cycle
    assert canFinishBFS(3, [[0, 1], [1, 2], [2, 0]]) == False
    
    print("All tests passed!")
