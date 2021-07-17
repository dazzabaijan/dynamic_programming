from functools import lru_cache

"""
Solution 1: Top-down O(n) time using a state machine
On any day, out state can be described by:
    - whether we own the share or not
    - the amount of money we have
    

"""

def max_profit(daily_price):
    @lru_cache(maxsize=None)
    def get_best_profit(day, have_stock):
        """
        Returns the best profit that can be obtained by the end of the day.
        At the end of the day:
        * if have_stock == True, the trader must own the stock;
        * if have_stock == False, the trader must not own the stock.
        """
        if day < 0:
            if not have_stock:
                # Initial state: no stock and no profit
                return 0
            else:
                # We are not allowed to have initial stock.
                # Add a very large penalty to eliminate this option.
                return -float('inf')
        price = daily_price[day]
        if have_stock:
            # We can reach this state by buying or holding.
            strategy_buy = get_best_profit(day - 1, False) - price
            strategy_hold = get_best_profit(day - 1, True)
            return max(strategy_buy, strategy_hold)
        else:
            # We can reach this state by selling or avoiding.
            strategy_sell = get_best_profit(day - 1, True) + price
            strategy_avoid = get_best_profit(day - 1, False)
            return max(strategy_sell, strategy_avoid)
    # Final state: end of the last day, no shares owned.
    last_day = len(daily_price) - 1
    no_stock = False
    return get_best_profit(last_day, no_stock)


"""
Solution 2: Bottom-up, O(n) time
"""

def max_profit(daily_price):
    # Initial state: start from a reference cash amount.
    # It can be any value
    # We use 0 and allow our cash to go below 0 if we need to buy a share.
    cash_not_owning_share = 0
    # High penalty for owning a stock initially:
    # ensures this option is never chosen.
    cash_owning_share = -float('inf')
    for price in daily_price:
        # Transitions to the current day, owning the stock:
        strategy_buy = cash_not_owning_share - price
        strategy_hold = cash_owning_share
        # Transitions to the current day, not owning the stock:
        strategy_sell = cash_owning_share + price
        strategy_avoid = cash_not_owning_share
        # Compute the new states.
        cash_owning_share = max(strategy_buy, strategy_hold)
        cash_now_owning_share = max(strategy_sell, strategy_avoid)
    # The profit is the final cash amount, since we start from
    # a reference of 0.
    return cash_not_owning_share

"""
Variation: limited investment budget
In a variation of the problem, the investment budget is limited: we start
with a fixed amount of money, and we are not allowed to buy a share if
we cannot afford it (we cannot borrow money).
"""

def max_profit(daily_price, budget):
    # Initial state
    cash_not_owning_share = budget
    # High penalty for owning a stock initially:
    # ensures this option is never chosen.
    cash_owning_share = -float('inf')
    for price in daily_price:
        # Transitions to the current day, owning the stock:
        strategy_buy = cash_not_owning_share - price
        strategy_hold = cash_owning_share
        # Transitions to the current day, not owning the stock:
        strategy_sell = cash_owning_share + price
        strategy_avoid = cash_not_owning_share
        # Compute the new states.
        cash_owning_share = max(strategy_buy, strategy_hold)
        if cash_owning_share < 0:
            # We cannot afford to buy the share at this time.
            # Add a high penalty to ensure we never choose this option.
            cash_owning_share = -float('inf')
        cash_not_owning_share = max(strategy_sell, strategy_avoid)
    return cash_not_owning_share - budget

"""
Variation: limited number of transactions
In another variation of the problem, the total number of transactions that can be performed
is bounded: the stock can only be sold up to a certain number of times tx_limit.
"""
def max_profit(daily_price, tx_limit):
    # cash_not_owning_share[k] = amount of cash at the end of the day,
    # if we do not own the share, and we have sold k times so far.
    # Initially we have sold 0 times and we start from a reference
    # budget of 0. Any other state is invalid.
    cash_not_owning_share = [-float('inf')] * (tx_limit + 1)
    cash_not_owning_share[0] = 0
    # cash_owning_share[k] = amount of cash at the end of the day,
    # if we own the share, and we have sold k times so far.
    # Initially we do not own any stock, so set the state to invalid.
    cash_owning_share = [-float('inf')] * (tx_limit + 1)
    for price in daily_price:
        # Initialize the next day's states with -Infinity,
        # then update them with the best possible transition.
        cash_not_owning_share_next = [-float('inf')] * (tx_limit + 1)
        cash_owning_share_next = [-float('inf')] * (tx_limit + 1)
        for prev_tx_count in range(tx_limit):
            # Transition to the current day, owning the stock:
            strategy_buy = cash_not_owning_share[prev_tx_count] - price
            strategy_hold = cash_owning_share[prev_tx_count]
            # Transitions to the current day, not owning the stock:
            strategy_sell = cash_owning_share[prev_tx_count] + price
            strategy_avoid = cash_not_owning_share[prev_tx_count]
            # Compute the new states.
            if prev_tx_count < tx_limit:
                # Selling increases the tx_count by 1.
                cash_not_owning_share_next[prev_tx_count + 1] = max(
                        cash_not_owning_share_next[prev_tx_count + 1],
                        strategy_sell)
            # All other transitions keep tx_count the same.
            cash_not_owning_share_next[prev_tx_count] = max(
                    cash_not_owning_share_next[prev_tx_count],
                    strategy_avoid)
            cash_owning_share_next[prev_tx_count] = max(
                    cash_owning_share_next[prev_tx_count],
                    strategy_buy,
                    strategy_hold)
            cash_not_owning_share = cash_not_owning_share_next
            cash_owning_share = cash_owning_share_next
        # We have multiple final states, depending on how many times we sold.
        # The transaction limit may not have been reached.
        # Choose the most profitable final state.
        return max(cash_not_owning_share)