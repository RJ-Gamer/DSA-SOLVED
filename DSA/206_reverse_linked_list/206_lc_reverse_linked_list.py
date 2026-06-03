# LeetCode Problem #206: Reverse Linked List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list_iter(head: ListNode) -> ListNode:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def reverse_list_recursive(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


def build_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for v in arr[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


head = build_list([1, 2, 3, 4, 5])
rev = reverse_list_iter(head)
print([rev.val, rev.next.val, rev.next.next.val, rev.next.next.next.val, rev.next.next.next.next.val])
