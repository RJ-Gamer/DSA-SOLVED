# LeetCode Problem #42: Trapping Rain Water

from typing import List


def trap_brute_force(height: List[int]) -> int:
    n = len(height)
    water = 0
    for i in range(1, n - 1):
        left_max = max(height[:i + 1])
        right_max = max(height[i:])
        water += min(left_max, right_max) - height[i]
    return water


def trap_precompute(height: List[int]) -> int:
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))


def trap(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water


print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6
print(trap([4, 2, 0, 3, 2, 5]))                       # 9
print(trap([3, 0, 2, 0, 4]))                          # 7
