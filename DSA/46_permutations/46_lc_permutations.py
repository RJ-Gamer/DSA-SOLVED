"""
LeetCode 46: Permutations
Difficulty: Medium
Topics: Backtracking, Array

Time Complexity: O(n! * n)
Space Complexity: O(n!)
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations of a list of unique integers.

    Args:
        nums: A list of unique integers

    Returns:
        A list containing all permutations
    """
    result = []

    def backtrack(path, remaining):
        # Base case: no more numbers to add
        if not remaining:
            result.append(path[:])
            return

        # Recursive case: try each remaining number as next
        for i in range(len(remaining)):
            # Choose
            path.append(remaining[i])

            # Explore
            new_remaining = remaining[:i] + remaining[i + 1 :]
            backtrack(path, new_remaining)

            # Unchoose
            path.pop()

    backtrack([], nums)
    return result


def permuteSwap(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations using in-place swapping (more efficient).

    Args:
        nums: A list of unique integers

    Returns:
        A list containing all permutations
    """
    result = []

    def backtrack(first=0):
        # Base case: all numbers are fixed
        if first == len(nums):
            result.append(nums[:])
            return

        for i in range(first, len(nums)):
            # Swap
            nums[first], nums[i] = nums[i], nums[first]

            # Explore
            backtrack(first + 1)

            # Swap back
            nums[first], nums[i] = nums[i], nums[first]

    backtrack()
    return result


# Test cases
if __name__ == "__main__":
    # Test 1: Single element
    result1 = permute([1])
    assert len(result1) == 1
    assert [1] in result1

    # Test 2: Two elements
    result2 = permute([1, 2])
    assert len(result2) == 2
    assert [1, 2] in result2
    assert [2, 1] in result2

    # Test 3: Three elements
    result3 = permute([1, 2, 3])
    assert len(result3) == 6

    # Test 4: Using swap method
    result4 = permuteSwap([1, 2, 3])
    assert len(result4) == 6

    print("All tests passed!")
