# LeetCode Problem #76: Minimum Window Substring

from collections import Counter


def minWindow_brute_force(s: str, t: str) -> str:
    if not t:
        return ""
    need = Counter(t)
    result = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            window = Counter(s[i:j])
            if all(window[c] >= need[c] for c in need):
                if not result or j - i < len(result):
                    result = s[i:j]
    return result


def minWindow(s: str, t: str) -> str:
    if not t:
        return ""

    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)

    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]

            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return result


print(minWindow("ADOBECODEBANC", "ABC"))  # "BANC"
print(minWindow("a", "a"))               # "a"
print(minWindow("a", "aa"))              # ""
