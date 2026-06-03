def single_number(nums):
    res = 0
    for n in nums:
        res ^= n
    return res


print(single_number([2, 2, 1]))
