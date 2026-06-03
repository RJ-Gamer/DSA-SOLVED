"""
LeetCode 46: Permutations
Difficulty: Medium
Topics: Backtracking, Array

Time Complexity: O(n! * n)
Space Complexity: O(n!)
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    res = []

    def backtrack(start=0):
        if start == len(nums):
            res.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    backtrack()
    return res


print(permute([1, 2, 3]))
