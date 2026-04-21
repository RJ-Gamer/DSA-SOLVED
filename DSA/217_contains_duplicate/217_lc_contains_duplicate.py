# LeetCode Problem #217: Contains Duplicates


def contains_duplicates_brute_force(nums: list[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


def contains_duplicates_hash_map(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def contains_duplicates_len(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))


print(contains_duplicates_brute_force(nums=[1, 2, 3, 1]))
print(contains_duplicates_hash_map(nums=[1, 2, 3, 1]))
print(contains_duplicates_len(nums=[1, 2, 3, 1]))
