"""
LeetCode 20: Valid Parentheses
Difficulty: Easy
Topics: Stack, String

Time Complexity: O(n)
Space Complexity: O(n)
"""


def isValid(s: str) -> bool:
    """
    Check if a string containing parentheses, brackets, and braces is valid.
    Valid means every opening bracket has a corresponding closing bracket in the correct order.

    Args:
        s: A string containing parentheses, brackets, and braces

    Returns:
        True if the string is valid, False otherwise
    """
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in mapping:
            # Closing bracket
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # Opening bracket
            stack.append(char)

    return len(stack) == 0


# Test cases
if __name__ == "__main__":
    # Test 1: Valid simple parentheses
    assert isValid("()") == True

    # Test 2: Valid nested parentheses
    assert isValid("()[]{}") == True

    # Test 3: Invalid - unmatched opening
    assert isValid("(") == False

    # Test 4: Invalid - wrong order
    assert isValid("(]") == False

    # Test 5: Invalid - extra closing
    assert isValid("())") == False

    # Test 6: Complex valid case
    assert isValid("({[]})") == True

    # Test 7: Empty string
    assert isValid("") == True

    print("All tests passed!")
