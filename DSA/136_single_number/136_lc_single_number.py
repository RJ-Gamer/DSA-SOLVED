"""
LeetCode 136: Single Number
Difficulty: Easy
Topics: Bit Manipulation, Array

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


def singleNumber(nums: List[int]) -> int:
    """
    Find the single number in an array where every other number appears twice.
    Uses XOR bit manipulation: a ^ a = 0, a ^ 0 = a
    
    Args:
        nums: A list of integers where every number appears twice except one
        
    Returns:
        The single number that appears only once
    """
    result = 0
    for num in nums:
        result ^= num  # XOR each number
    return result


def singleNumberSet(nums: List[int]) -> int:
    """
    Find the single number using set (not optimal but shows alternative approach).
    
    Args:
        nums: A list of integers where every number appears twice except one
        
    Returns:
        The single number that appears only once
    """
    seen = set()
    for num in nums:
        if num in seen:
            seen.remove(num)
        else:
            seen.add(num)
    return seen.pop()


# Test cases
if __name__ == "__main__":
    # Test 1: Simple case
    assert singleNumber([2, 2, 1]) == 1
    
    # Test 2: Different order
    assert singleNumber([4, 1, 2, 1, 2]) == 4
    
    # Test 3: Single element
    assert singleNumber([1]) == 1
    
    # Test 4: Larger array
    assert singleNumber([0, 1, 0, 1, 99]) == 99
    
    # Test 5: Using set approach
    assert singleNumberSet([2, 2, 1]) == 1
    
    print("All tests passed!")
