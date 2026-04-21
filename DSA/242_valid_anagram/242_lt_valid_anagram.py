# LeetCode Problem #242 Valid Anagram
from collections import Counter

def valid_anagram_linear(s: str, t: str) -> bool:
    """
    Space Complexity: O(1)
    Time Complexity: O(n)
    """
    if len(s) != len(t):
        return False

    count_s, count_t = {}, {}

    for letter in s:
        count_s[letter] = 1 + count_s.get(letter, 0)

    for letter in t:
        count_t[letter] = 1 + count_t.get(letter, 0)

    if count_s == count_t:
        return True

    return False


def valid_anagram_sort(s: str, t: str) -> bool:
    """
    Space Complexity: O(1)
    Time Complexity: O(n*log(n))
    """
    return sorted(s) == sorted(t)

def valid_anagram_counter(s: str, t: str) -> bool:
    """
    Space Complexity: O(1)
    Time Complexity: O(n)
    """
    return Counter(s) == Counter(t)


if __name__ == "__main__":
    print(valid_anagram_linear("anagram", "nagaram"))
    print(valid_anagram_linear("rat", "car"))

    print(valid_anagram_sort("anagram", "nagaram"))
    print(valid_anagram_sort("rat", "car"))

    print(valid_anagram_counter("anagram", "nagaram"))
    print(valid_anagram_counter("rat", "car"))


