# LeetCode Problem #53: Maximum Subarray


def max_sub_array_brute_force(nums: list[int]) -> int:
    max_sum = float("-inf")
    for i in range(len(nums)):
        current_sum = 0
        for j in range(i, len(nums)):
            current_sum += nums[j]
            max_sum = max(max_sum, current_sum)
    return max_sum


def max_sub_array_optimal(nums: list[int]) -> int:
    max_sum = float("-inf")
    current_sum = 0

    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


print(max_sub_array(nums=[-2, 1, -3, 4, -1, 2, 1, -5, 4]))
print(max_sub_array(nums=[1]))
print(max_sub_array(nums=[5, 4, -1, 7, 8]))
print(max_sub_array(nums=[5, 7, -2, 1, 8, -7, -3]))
