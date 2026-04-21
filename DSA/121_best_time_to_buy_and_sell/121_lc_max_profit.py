# LeetCode Problem #121: Best Time to Buy and Sell Stock


def max_profit_brute_force(prices: list[int]) -> int:
    max_profit = 0

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            profit = prices[j] - prices[i]

            if profit > max_profit:
                max_profit = profit

    return max_profit


def max_profit_linear(prices: list[int]) -> int:
    min_price = float("inf")
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit


print(max_profit_linear([7, 1, 5, 3, 6, 4]))
print(max_profit_linear([7, 6, 4, 3, 1]))
print(max_profit_linear([2, 4, 1]))
print(max_profit_brute_force([2, 1, 2, 1, 0, 1, 2]))
print(max_profit_brute_force([2, 4, 1]))
print(max_profit_brute_force([7, 1, 5, 3, 6, 4]))
