# 121. Best Time to Buy and Sell Stock

**LeetCode:** [Problem #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)  
**Difficulty:** Easy  
**Topics:** `Array` `Two Pointers` `Greedy`

---

## Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock
on day `i`. You want to maximize your profit by choosing a **single day to buy**
and a **different day in the future to sell**.

Return the maximum profit you can achieve. If no profit is possible, return `0`.

**Constraints:**
- `1 <= prices.length <= 10⁵`
- `0 <= prices[i] <= 10⁴`
- You must buy before you sell (no short selling)
- Only one transaction allowed (one buy, one sell)

### Example
```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6 - 1 = 5
```

```
Input:  prices = [7, 6, 4, 3, 1]
Output: 0
Explanation: Prices only decrease. No profitable trade exists.
```

---

## How to Think About This Problem

### Step 1 — Understand what's being asked

We need to find two days — a buy day and a sell day — such that the sell day
comes **after** the buy day and the price difference `sell_price - buy_price`
is maximized. If all price differences are negative (prices only go down), we
return `0` (we simply don't trade).

### Step 2 — Identify the constraint that matters

The constraint that defines this problem is **temporal ordering**: you must buy
before you sell. You can't look ahead to see a low price coming and retroactively
buy at it. You can only decide to sell today based on a price you've already
observed in the past.

This rules out a simple "find the minimum and maximum of the array" approach —
what if the minimum occurs *after* the maximum?

```
prices = [7, 6, 4, 3, 1]
min = 1 (day 5), max = 7 (day 1)
But day 5 comes after day 1 — you can't buy at 1 and sell at 7.
```

### Step 3 — Think about data structures

No exotic data structure is needed. We need to track two things as we scan:

1. **The lowest price seen so far** — this is the best possible buy price for any
   future sell day we haven't visited yet
2. **The maximum profit achievable** — updated each day if selling today beats the
   current best

A single pass with two variables suffices.

### Step 4 — Build the intuition

Think of yourself as a trader reading a price feed left-to-right (day by day).
At each day's price, you ask two questions:

1. "If I could have bought at the cheapest point before today, how much profit
   would I make selling right now?" → update `max_profit` if this beats current best
2. "Is today cheaper than any previous day?" → if yes, update `min_price`
   (I'd rather have bought today if I could go back)

The key observation: **the best sell day for any given buy day is already captured
by tracking the running minimum.** If we're at day `i` and the minimum so far is
`min_price`, then `prices[i] - min_price` is the best profit achievable with a
sell on day `i`.

We never need to look backwards — the minimum has already been accumulated.

---

## Approaches

### Approach 1 — Brute Force

**Intuition:** Try every combination of buy day and sell day, keeping track of
the maximum profit seen.

**Steps:**
1. For each potential buy day `i`, consider all potential sell days `j > i`
2. Compute `profit = prices[j] - prices[i]`
3. If `profit > max_profit`, update `max_profit`
4. Return `max_profit`

**Illustration:**
```
prices = [7, 1, 5, 3, 6, 4]

Buy at i=0 (price=7):
  Sell j=1: 1-7 = -6   max=0
  Sell j=2: 5-7 = -2   max=0
  Sell j=3: 3-7 = -4   max=0
  Sell j=4: 6-7 = -1   max=0
  Sell j=5: 4-7 = -3   max=0

Buy at i=1 (price=1):
  Sell j=2: 5-1 =  4   max=4
  Sell j=3: 3-1 =  2   max=4
  Sell j=4: 6-1 =  5   max=5  ← best so far
  Sell j=5: 4-1 =  3   max=5

Buy at i=2 (price=5):
  Sell j=3: 3-5 = -2   max=5
  Sell j=4: 6-5 =  1   max=5
  Sell j=5: 4-5 = -1   max=5

... remaining buys at prices 3, 6, 4 yield ≤ 5

Return 5 ✓
```

**Complexity:**
- Time: O(n²) — every pair of (buy, sell) days is evaluated
- Space: O(1) — only `max_profit` tracked

**Code:**
```python
def max_profit_brute_force(prices: list[int]) -> int:
    max_profit = 0

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            profit = prices[j] - prices[i]

            if profit > max_profit:
                max_profit = profit

    return max_profit
```

---

### Approach 2 — Optimal (One Pass, Running Minimum)

**Intuition:** Track the minimum price seen so far as the best possible buy price;
at each step, compute the profit if we sold today and update the global maximum.

**Steps:**
1. Initialize `min_price = +∞` and `max_profit = 0`
2. For each `price`:
   - If `price < min_price`, update `min_price` (found a cheaper buy day)
   - Else if `price - min_price > max_profit`, update `max_profit` (found a better profit)
3. Return `max_profit`

**Illustration:**
```
prices = [7, 1, 5, 3, 6, 4]

price=7: 7 < inf  → min_price=7            max_profit=0
price=1: 1 < 7    → min_price=1            max_profit=0
price=5: 5-1=4    → 4 > 0  → max_profit=4
price=3: 3-1=2    → 2 < 4                  max_profit=4
price=6: 6-1=5    → 5 > 4  → max_profit=5
price=4: 4-1=3    → 3 < 5                  max_profit=5

Return 5 ✓ (buy at 1, sell at 6)
```

```
prices = [7, 6, 4, 3, 1]

price=7: 7 < inf  → min_price=7            max_profit=0
price=6: 6 < 7    → min_price=6            max_profit=0
price=4: 4 < 6    → min_price=4            max_profit=0
price=3: 3 < 4    → min_price=3            max_profit=0
price=1: 1 < 3    → min_price=1            max_profit=0

Return 0 ✓ (no profitable trade)
```

**Complexity:**
- Time: O(n) — single pass through the array
- Space: O(1) — two variables only

**Code:**
```python
def max_profit_linear(prices: list[int]) -> int:
    min_price = float("inf")
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit
```

---

## Solution Breakdown — Step by Step

```python
def max_profit_linear(prices: list[int]) -> int:
    min_price = float("inf")
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit
```

**Line by line:**

`min_price = float("inf")`
- Initialized to positive infinity so the very first price we see will always
  be recorded as the current minimum
- Using `prices[0]` would also work but `inf` is cleaner and more explicit

`max_profit = 0`
- Initialized to 0 because if no profitable trade exists, we return 0 (don't trade)
- This is the correct base case — the problem guarantees we can always choose
  not to trade

`for price in prices:`
- Single pass; we only need the price value, not the index

`if price < min_price:`
- Check if today is cheaper than any previous day
- If yes, this is the new best buy candidate — we update `min_price`
- We do NOT update `max_profit` here because selling at the cheapest day
  we've seen so far yields 0 profit

`min_price = price`
- Record the new floor — future sell days will compare against this

`elif price - min_price > max_profit:`
- If today is NOT a new minimum, check whether selling today is better than our
  current best
- `price - min_price` = profit if we had bought at the cheapest day seen and
  sold today
- `elif` is correct here: if `price < min_price`, we update the buy candidate,
  not the profit

`max_profit = price - min_price`
- Record the new best profit

`return max_profit`
- After the single pass, `max_profit` holds the answer

---

## Common Mistakes

**1. Not initializing `min_price` to infinity (or `prices[0]`)**
```python
# WRONG — if prices[0] = 0, everything looks like a new minimum
min_price = 0
```
Initialize to `float("inf")` so the first price always sets the minimum correctly.

**2. Using if instead of elif for the profit update**
```python
# Subtle but incorrect — both branches can run in the same iteration
if price < min_price:
    min_price = price
if price - min_price > max_profit:   # now min_price = price, profit = 0
    max_profit = price - min_price
```
When a new minimum is found, `price - min_price` equals 0 — we'd never erroneously
update `max_profit`, but we'd waste a comparison. More importantly, if `min_price`
is just updated, we know the profit calculation would use the same day as buy and
sell — `elif` is the semantically correct guard.

**3. Thinking you need to find the global min and max**
```python
# WRONG — ignores temporal ordering
return max(prices) - min(prices)
# prices = [7, 6, 4, 3, 1] → returns 7-1=6, but correct answer is 0
```
The minimum might come after the maximum — you can't sell before you buy.

**4. Using `>=` instead of `>` for the profit comparison**
```python
if price - min_price >= max_profit:  # updates unnecessarily on ties
```
This is not wrong (the problem doesn't ask for the specific days, just the profit),
but `>` is the standard convention.

---

## Pattern Recognition

> Use the **running minimum / running maximum** pattern when you see:
> - "Find maximum difference where larger element comes after smaller"
> - "Single-pass optimization with a tracked extreme value"
> - Greedy problems where the best choice at each step depends on the best seen so far

**Similar problems:**
- **Maximum Subarray** — equivalent: convert to daily differences, then find max subarray sum
- **Best Time to Buy and Sell Stock II** — multiple transactions; greedy: take every upswing
- **Best Time to Buy and Sell Stock III** — at most 2 transactions; DP approach
- **Best Time to Buy and Sell Stock with Cooldown** — DP with state machine

---

## Real World Use Cases

### 1. Infrastructure cost optimization in cloud resource scheduling
Cloud cost dashboards track per-hour pricing for spot instances. A scheduler
uses the "running minimum" pattern to find the cheapest provisioning window and
the optimal release window — effectively the same buy-low-sell-high calculation
applied to compute costs. This runs as a streaming scan over millions of
pricing data points per region per service.

### 2. Inventory replenishment in supply chain management
A warehouse management system tracks the unit cost of a commodity over time.
The "best buy window" logic — when to lock in procurement prices — mirrors this
exact problem: scan historical prices, maintain the lowest seen, compute the
maximum margin if sold at today's spot price. Logistics companies run this
continuously over live commodity feeds.

### 3. Session window analysis in user behavior analytics
An analytics pipeline processes per-second engagement scores for a user session.
Finding the "peak engagement window" — the period with the maximum improvement
from a local low to a later local high — uses the running minimum pattern.
Product teams use this to identify when users discover value in a feature.

---

## Key Takeaways

- You never need to look back — a running minimum accumulates the best buy price automatically
- The temporal ordering constraint ("must buy before sell") rules out the naive global min/max approach
- Use `elif` for the profit branch: if you're updating `min_price`, you're not selling that day
- Initialize `max_profit = 0` — the "no trade" option is always available
- This problem is equivalent to finding the max subarray sum on the array of daily price differences
