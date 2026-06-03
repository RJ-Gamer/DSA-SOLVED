# LeetCode Problem #20: Valid Parentheses


def is_valid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in mapping:
            if not stack or stack[-1] != mapping[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack


print(is_valid("()"))
print(is_valid("([)]"))
