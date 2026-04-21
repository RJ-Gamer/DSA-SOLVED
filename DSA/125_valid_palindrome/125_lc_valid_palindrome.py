# LeetCode Problem #125: Valid Palindrome


def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


print(is_palindrome(s="A man, a plan, a canal: Panama"))
print(is_palindrome(s="race a car"))
print(is_palindrome(s=" "))
print(is_palindrome(s="0P"))
