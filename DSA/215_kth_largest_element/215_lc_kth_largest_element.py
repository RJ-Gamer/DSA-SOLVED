"""
LeetCode 215: Kth Largest Element in an Array
Difficulty: Medium
Topics: Heap, Quick Select, Sorting

Time Complexity: O(n log k) heap / O(n) quick select average
Space Complexity: O(k) heap / O(1) quick select
"""

import heapq
from typing import List


def findKthLargest(nums: List[int], k: int) -> int:
    """
    Find the kth largest element using a min heap of size k.

    Args:
        nums: A list of integers
        k: The position (1-indexed) of the largest element to find

    Returns:
        The kth largest element
    """
    # Maintain a min heap of size k
    heap = []

    for num in nums:
        # Add element to heap
        heapq.heappush(heap, num)

        # Remove smallest if heap size exceeds k
        if len(heap) > k:
            heapq.heappop(heap)

    # The root of the min heap is the kth largest
    return heap[0]


def findKthLargestSort(nums: List[int], k: int) -> int:
    """
    Find the kth largest element using sorting.

    Args:
        nums: A list of integers
        k: The position (1-indexed) of the largest element to find

    Returns:
        The kth largest element
    """
    nums.sort(reverse=True)
    return nums[k - 1]


def findKthLargestQuickSelect(nums: List[int], k: int) -> int:
    """
    Find the kth largest element using quick select algorithm.

    Args:
        nums: A list of integers
        k: The position (1-indexed) of the largest element to find

    Returns:
        The kth largest element
    """

    def quickSelect(left, right, k_smallest):
        # k_smallest is 0-indexed position from the right
        if left == right:
            return nums[left]

        # Partition
        pivot_index = partition(left, right)

        if pivot_index == k_smallest:
            return nums[pivot_index]
        elif pivot_index < k_smallest:
            return quickSelect(pivot_index + 1, right, k_smallest)
        else:
            return quickSelect(left, pivot_index - 1, k_smallest)

    def partition(left, right):
        pivot = nums[right]
        i = left

        for j in range(left, right):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1

        nums[i], nums[right] = nums[right], nums[i]
        return i

    # Find kth largest means finding (n-k)th smallest
    return quickSelect(0, len(nums) - 1, len(nums) - k)


# Test cases
if __name__ == "__main__":
    # Test 1: Simple case
    assert findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5

    # Test 2: Single element
    assert findKthLargest([1], 1) == 1

    # Test 3: k = len(nums)
    assert findKthLargest([3, 2, 1, 5, 6, 4], 6) == 1

    # Test 4: Using sort method
    assert findKthLargestSort([3, 2, 1, 5, 6, 4], 2) == 5

    # Test 5: Using quick select
    nums = [3, 2, 1, 5, 6, 4]
    assert findKthLargestQuickSelect(nums.copy(), 2) == 5

    print("All tests passed!")
