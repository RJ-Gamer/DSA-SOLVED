# LeetCode Problem #4: Median of Two Sorted Arrays

from typing import List


def findMedianSortedArrays_brute_force(nums1: List[int], nums2: List[int]) -> float:
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n) // 2
    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = half - i

        max_left1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right1 = float('inf') if i == m else nums1[i]
        max_left2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right2 = float('inf') if j == n else nums2[j]

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 1:
                return float(min(min_right1, min_right2))
            return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            right = i - 1
        else:
            left = i + 1


print(findMedianSortedArrays([1, 3], [2]))        # 2.0
print(findMedianSortedArrays([1, 2], [3, 4]))     # 2.5
print(findMedianSortedArrays([0, 0], [0, 0]))     # 0.0
print(findMedianSortedArrays([], [1]))             # 1.0
