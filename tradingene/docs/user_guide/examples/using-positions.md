### Using multiple positions

Full ```python``` code [here](https://github.com/iburenko/tradingene/blob/master/tradingene/examples/first_alg.py); ```ipython``` notebook [here](https://github.com/iburenko/tradingene/blob/master/tradingene/examples/nn_2classes.ipynb)

Along with ```buy()``` and ```sell()``` the Tradingene framework provides you with more tools for making trades including ```openLong()``` and ```openShort()``` functions. With these ones you may have two positions of opposite side opened at the same time. Opening a "counter-trade" while holding another one still opened may serve several purposes, e.g. temporarily hedging while surviving a drawdown, saving commission expanses payed to exchange etc.

When opening a trade with either ```openLong()``` or ```openShort()``` you must specified the number of lots to use:
```python
	long_position = alg.openLong(1) # ...buying 1 lot.
```
The function returns the identifier of a position just been opened. We may use this identifier to control position in the future. For example we may specify a function to be called when the position is closed:
```python
	alg.onPositionClose(long_position, onLongPositionClose) # Specifying the function to be called when the position is
```
