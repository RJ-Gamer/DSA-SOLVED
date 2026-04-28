# LeetCode Problem # 1299: Replace with Greatest Element on Right Side

from typing import List
class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        
        # Edge case: empty array
        if not arr: 
            return []
        
        # Edge case: single element array
        if len(arr) == 1: 
            arr[0] = -1
            return arr
        
        # General case: more than one element
        # Approach: iterate from right to left, keeping track of greatest element seen so far
        greatest_so_far = -1
        for i in range(len(arr) - 1, -1, -1):
            temp = arr[i]
            arr[i] = greatest_so_far
            greatest_so_far = max(greatest_so_far, temp)
            
        return arr
    
sol = print(Solution().replaceElements([17,18,5,4,6,1]))
sol = print(Solution().replaceElements([400]))
            
