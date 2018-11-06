# List of methods

## backtest_results

### Description
This method calls all other methods for generating comprehensive list of algorithm's statistics.

**Arguments:**

    plot (boolean, default True): If True, after calling method
          will automatically open html file with backtest statistics.

    filename (str, default "stats"): Name of the file where backtest
          statistics will be saved.

**Returns:**

    None

**Examples:**

```python
#Statistics will be saved in stats.html and showed after calculations
stats = bs.BacktestStatistics(alg)
stats.backtest_results()
```

## calculate_PnL

### Description
Calculates cumulative profit over backtest period including profit of the last position whether it was closed or not.

**Arguments:**

    None

**Returns:**

    float: Cumulative profit.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    pnl = stats.calculate_PnL()

## calculate_number_of_trades

Calculates the number of closed position while backtest.

**Arguments:**

    None

**Returns:**

    int: The number of closed positions.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    number_of_trades = stats.calculate_number_of_trades()

## calculate_reliability

Calculates reliability, i.e. ratio of the number of profitable positions to the number of all positions.


**Arguments:**

    None

**Returns:**

    float: Reliability of an algorithm. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    reliability = stats.calculate_reliability()

## calculate_RRR

Calculates Risk Reward Ratio. RRR is defined as ratio of the mean of all losing positions to mean of all profitable positions:


**Arguments:**

    None

**Returns:**

    float: Risk reward ratio. If no profitable trades were while backtest returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    risk_reward_ratio = stats.calculate_RRR()

## calculate_drawdown

Calculates a drawdown and drawdown length.

**Arguments:**

    None

**Returns:**

    list: (drawdown, drawdown_length).

**Examples:**

    stats = bs.BacktestStatistics(alg)
    drawdown, drawdown_len = stats.calculate_drawdown()

## calculate_AT

Calculates an average profit over all positions in the backtest (Average Trade).

**Arguments:**

    None

**Returns:**

    float: Average profit.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_trade = stats.calculate_AT()

## calculate_ATT

Calculates an average duration over all positions (Average Time in Trade).

**Arguments:**

    None

**Returns:**

    float: Average duration.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_time = stats.calculate_ATT()

## calculate_ADPD

Calculates an average number of positions per day (Average Deals Per Day).

**Arguments:**

    None

**Returns:**

    float: Average number of positions. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_pos_per_day = stats.calculate_ADPD()

## calculate_profit

Calculates an overall profit of all profitable positions.

**Arguments:**

    None

**Returns:**

    float: Profit. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    profit = stats.calculate_profit()

## calculate_loss

Calculates an overall loss of all losing positions.

**Arguments:**

    None

**Returns:**

    float: Loss. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    loss = stats.calculate_loss()

## calculate_AWT

Calculates an average profit over all profitable positions (Average Winning Trade).

**Arguments:**

    None

**Returns:**

    float: Average profit. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_profit = stats.calculate_AWT()

## calculate_ALT

Calculates an average loss over all losing positions (Average Losing Trade).

**Arguments:**

    None

**Returns:**

    float: Average loss. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_loss = stats.calculate_ALT()

## calculate_WT

Calculates a number of profitable positions (Winning Trades).

**Arguments:**

    None

**Returns:**

    int: Number of profitable positions.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    winning_pos = stats.calculate_WT()

## calculate_LT

Calculates a number of losing positions (Losing Trades).

**Arguments:**

    None

**Returns:**

    int: Number of losing trades.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    losing_pos = stats.calculate_LT()

## calculate_LWT

Calculates a profit of the most profitable position (Largest Winning Trade).

**Arguments:**

    None

**Returns:**

    float: Largest profit. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    largest_profit = stats.calculate_LWT()

## calculate_LLT

Calculates a loss of the most losing position (Largest Losing Trade).

**Arguments:**

    None

**Returns:**

    float: The least loss. If no positions were opened returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    largest_loss = stats.calculate_LLT()

## calculate_ATWT

Calculates an average duration of profitable positions (Average Time in Winning Trade).

**Arguments:**

    None

**Returns:**

    float: Average duration. If no profitable positions were closed returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_win_time = stats.calculate_ATWT()


## calculate_ATLT

Calculates an average duration of losing positions (Average Time in Losing Trade).

**Arguments:**

    None

**Returns:**

    float: Average duration. If no losing positions were closed returns 0.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    average_los_time = stats.calculate_ATLT()

## calculate_MCW

Calculates the largest number of consequent profitable trades (Maximum Consecutive Winners).

**Arguments:**

    None

**Returns:**

    int: The largest number of consequent profitable trades.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    max_cons_win = stats.calculate_MCW()

## calculate_MCL

Calculates the largest number of consequent losing trades (Maximum Consecutive Losers).

**Arguments:**

    None

**Returns:**

    int: The largest number of consequent losing trades.

**Examples:**

    stats = bs.BacktestStatistics(alg)
    max_cons_los = stats.calculate_MCL()
