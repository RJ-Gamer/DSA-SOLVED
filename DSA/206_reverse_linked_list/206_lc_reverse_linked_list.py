"""
LeetCode 206: Reverse Linked List
Difficulty: Easy
Topics: Linked List, Recursion

Time Complexity: O(n)
Space Complexity: O(1) iterative / O(n) recursive
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse a singly linked list iteratively.

    Args:
        head: The head node of the linked list

    Returns:
        The new head node of the reversed linked list
    """
    prev = None
    current = head

    while current:
        # Store next node
        next_temp = current.next

        # Reverse the link
        current.next = prev

        # Move prev and current one step forward
        prev = current
        current = next_temp

    return prev


def reverseListRecursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse a singly linked list recursively.

    Args:
        head: The head node of the linked list

    Returns:
        The new head node of the reversed linked list
    """
    # Base case: empty list or single node
    if not head or not head.next:
        return head

    # Recursively reverse the rest of the list
    new_head = reverseListRecursive(head.next)

    # Make the next node point back to current
    head.next.next = head
    head.next = None

    return new_head


# Test cases
if __name__ == "__main__":
    # Helper function to create linked list from list
    def create_list(arr):
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    # Helper function to convert linked list to list
    def list_to_array(head):
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    # Test 1: Normal case
    head = create_list([1, 2, 3, 4, 5])
    reversed_head = reverseList(head)
    assert list_to_array(reversed_head) == [5, 4, 3, 2, 1]

    # Test 2: Single node
    head = create_list([1])
    reversed_head = reverseList(head)
    assert list_to_array(reversed_head) == [1]

    # Test 3: Two nodes
    head = create_list([1, 2])
    reversed_head = reverseListRecursive(head)
    assert list_to_array(reversed_head) == [2, 1]

    print("All tests passed!")
