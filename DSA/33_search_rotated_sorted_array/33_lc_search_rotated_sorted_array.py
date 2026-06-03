"""
LeetCode 33: Search in Rotated Sorted Array
Difficulty: Medium
Topics: Binary Search, Array

Time Complexity: O(log n)
Space Complexity: O(1)
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search for a target value in a rotated sorted array.
    
    Args:
        nums: A rotated sorted array of unique integers
        target: The target value to search for
        
    Returns:
        The index of target if found, otherwise -1
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # Left half is sorted
            # Check if target is in the sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            # Check if target is in the sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# Test cases
if __name__ == "__main__":
    # Test 1: Target in right half
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    
    # Test 2: Target not found
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    
    # Test 3: Single element
    assert search([1], 1) == 0
    
    # Test 4: Target at start
    assert search([4, 5, 6, 7, 0, 1, 2], 4) == 0
    
    # Test 5: Target in left half
    assert search([4, 5, 6, 7, 0, 1, 2], 5) == 1
    
    print("All tests passed!")
