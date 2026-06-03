"""
LeetCode 208: Implement Trie (Prefix Tree)
Difficulty: Medium
Topics: Trie, Design

Time Complexity: O(m) for insert/search/startsWith where m is word length
Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """
    A Trie (prefix tree) data structure for efficient string searches.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Args:
            word: The word to insert
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        """
        Search for an exact word in the trie.

        Args:
            word: The word to search for

        Returns:
            True if the word exists, False otherwise
        """
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_word

    def startsWith(self, prefix: str) -> bool:
        """
        Check if there's any word in the trie starting with the given prefix.

        Args:
            prefix: The prefix to search for

        Returns:
            True if any word starts with prefix, False otherwise
        """
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True


# Test cases
if __name__ == "__main__":
    trie = Trie()

    # Test 1: Insert and search
    trie.insert("apple")
    assert trie.search("apple") == True

    # Test 2: Incomplete word
    assert trie.search("app") == False

    # Test 3: Prefix search
    assert trie.startsWith("app") == True

    # Test 4: Non-existent word
    assert trie.search("apricot") == False

    # Test 5: Multiple inserts
    trie.insert("app")
    assert trie.search("app") == True

    # Test 6: Non-existent prefix
    assert trie.startsWith("xyz") == False

    print("All tests passed!")
