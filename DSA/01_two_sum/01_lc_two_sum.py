# LeetCode Problem #1: Two Sum


def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]


def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    visited = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in visited:
            return [visited[complement], i]

        visited[nums[i]] = i


print(two_sum_brute_force(nums=[2, 7, 11, 15], target=9))
print(two_sum_hash_map(nums=[2, 7, 11, 15], target=9))
