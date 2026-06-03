# LeetCode Problem #84: Largest Rectangle in Histogram

from typing import List


def largestRectangleArea_brute_force(heights: List[int]) -> int:
    max_area = 0
    n = len(heights)
    for i in range(n):
        min_height = heights[i]
        for j in range(i, n):
            min_height = min(min_height, heights[j])
            max_area = max(max_area, min_height * (j - i + 1))
    return max_area


def largestRectangleArea(heights: List[int]) -> int:
    stack = []  # (start_index, height)
    max_area = 0

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))

    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))

    return max_area


print(largestRectangleArea([2, 1, 5, 6, 2, 3]))  # 10
print(largestRectangleArea([2, 4]))               # 4
print(largestRectangleArea([1]))                  # 1
print(largestRectangleArea([1, 2, 3, 4, 5]))      # 9
