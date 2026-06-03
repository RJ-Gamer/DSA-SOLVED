# LeetCode Problem #295: Find Median from Data Stream

import heapq


class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap for lower half (store negated values)
        self.large = []  # min-heap for upper half

    def addNum(self, num: int) -> None:
        # Always push to small first
        heapq.heappush(self.small, -num)

        # Ensure max of small <= min of large
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes: small can have at most one more than large
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0
mf.addNum(4)
print(mf.findMedian())  # 2.5
