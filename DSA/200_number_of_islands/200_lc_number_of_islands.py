"""
LeetCode 200: Number of Islands
Difficulty: Medium
Topics: Graph, DFS, BFS, Union-Find, Matrix

Time Complexity: O(m * n)
Space Complexity: O(m * n)
"""

from typing import List
from collections import deque


def numIslands(grid: List[List[str]]) -> int:
    """
    Count the number of islands using DFS.
    An island is surrounded by water and formed by connecting adjacent lands.
    
    Args:
        grid: A 2D grid of '0' (water) and '1' (land)
        
    Returns:
        The number of islands
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        grid[r][c] = '0'  # Mark as visited
        
        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    
    return count


def numIslandsBFS(grid: List[List[str]]) -> int:
    """
    Count the number of islands using BFS.
    
    Args:
        grid: A 2D grid of '0' (water) and '1' (land)
        
    Returns:
        The number of islands
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = '0'
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                bfs(i, j)
                count += 1
    
    return count


# Test cases
if __name__ == "__main__":
    # Test 1: Multiple islands
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    assert numIslands([row[:] for row in grid1]) == 1
    
    # Test 2: Disconnected islands
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    assert numIslands([row[:] for row in grid2]) == 3
    
    print("All tests passed!")
