# LeetCode Problem #33: Search in Rotated Sorted Array

from typing import List


def search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def search_naive(nums: List[int], target: int) -> int:
    for i, v in enumerate(nums):
        if v == target:
            return i
    return -1


print(search([4, 5, 6, 7, 0, 1, 2], 0))
print(search_naive([4, 5, 6, 7, 0, 1, 2], 0))
