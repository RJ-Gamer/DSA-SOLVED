# LeetCode Problem #239: Sliding Window Maximum

from typing import List
from collections import deque


def maxSlidingWindow_brute_force(nums: List[int], k: int) -> List[int]:
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    dq = deque()  # monotonic decreasing deque of indices
    result = []

    for i, num in enumerate(nums):
        # Remove indices that have left the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove indices whose values are smaller than current (they can never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


print(maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
print(maxSlidingWindow([1], 1))                            # [1]
print(maxSlidingWindow([1, -1], 1))                        # [1, -1]
