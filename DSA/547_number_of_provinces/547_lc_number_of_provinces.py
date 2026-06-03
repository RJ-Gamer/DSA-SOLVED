"""
LeetCode 547: Number of Provinces
Difficulty: Medium
Topics: Union-Find, Graph, DFS

Time Complexity: O(n^2) for DFS / O(n^2 * α(n)) for Union-Find
Space Complexity: O(n)
"""

from typing import List


def findCircleNum(isConnected: List[List[int]]) -> int:
    """
    Find the number of provinces using DFS.
    A province is a group of directly or indirectly connected cities.

    Args:
        isConnected: Adjacency matrix where isConnected[i][j] = 1 means city i and j are connected

    Returns:
        The number of provinces
    """
    n = len(isConnected)
    visited = [False] * n
    provinces = 0

    def dfs(city):
        visited[city] = True
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            dfs(i)
            provinces += 1

    return provinces


class UnionFind:
    """Union-Find data structure for efficient connectivity queries."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Find the root parent of element x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union two elements by their roots with union by rank."""
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            return

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def findCircleNumUnionFind(isConnected: List[List[int]]) -> int:
    """
    Find the number of provinces using Union-Find.

    Args:
        isConnected: Adjacency matrix where isConnected[i][j] = 1 means city i and j are connected

    Returns:
        The number of provinces
    """
    n = len(isConnected)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    # Count number of unique roots
    return len(set(uf.find(i) for i in range(n)))


# Test cases
if __name__ == "__main__":
    # Test 1: All cities connected
    assert findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2

    # Test 2: All cities separate
    assert findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

    # Test 3: Single city
    assert findCircleNum([[1]]) == 1

    # Test 4: Using Union-Find
    assert findCircleNumUnionFind([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2

    # Test 5: Complex case
    assert (
        findCircleNumUnionFind([[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1]])
        == 1
    )

    print("All tests passed!")
