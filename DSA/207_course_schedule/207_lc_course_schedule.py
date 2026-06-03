def can_finish_dfs(numCourses, prerequisites):
    from collections import defaultdict

    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[a].append(b)
    state = [0] * numCourses

    def dfs(u):
        if state[u] == 1:
            return True
        if state[u] == 2:
            return False
        state[u] = 1
        for v in graph[u]:
            if dfs(v):
                return True
        state[u] = 2
        return False

    for i in range(numCourses):
        if state[i] == 0 and dfs(i):
            return False
    return True


def can_finish_bfs(numCourses, prerequisites):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indeg = [0] * numCourses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return cnt == numCourses


print(can_finish_dfs(2, [[1, 0]]))
