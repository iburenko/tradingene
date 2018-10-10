import numpy as np


# AD-indicator
def ad(period=1, shift=0, hi=None, lo=None, cl=None, vol=None, prev=None):
    if hi is None or lo is None or cl is None or vol is None:
        return None

    adValue = None
    if prev is not None:
        if shift < len(cl):
            adValue = prev + ad1(hi[shift], lo[shift], cl[shift], vol[shift])
    else:
        startIndex = shift + period - 1
        if startIndex < len(cl):
            prevAdValue = 0.0
            for i in range(startIndex, shift - 1, -1):
                adValue = prevAdValue + ad1(hi[i], lo[i], cl[i], vol[i])
                prevAdValue = adValue

    return adValue


# end of AD


def ad1(hi, lo, cl, vol):
    highLessLow = hi - lo
    if highLessLow > 0.0:
        closeLessLow = cl - lo
        highLessClose = hi - cl
        return ((vol * (closeLessLow - highLessClose)) / highLessLow)
    return 0


# end of ad1


# ADX-indicator
def adx(periodADX=14,
        periodDI=-1,
        shift=0,
        hi=None,
        lo=None,
        cl=None,
        prev=None):
    if hi is None or lo is None or cl is None:
        return None
    if shift >= len(cl) - 1:
        return None

    if periodDI < 0:
        periodDI = periodADX

    prevSmoothedTr = None
    prevSmoothedPlusDM = None
    prevSmoothedMinusDM = None
    prevADX = None
    if prev is not None:
        prevSmoothedTr = prev['smoothedTr']
        prevSmoothedPlusDM = prev['smoothedPlusDM']
        prevSmoothedMinusDM = prev['smoothedMinusDM']
        prevADX = prev['adx']

    plusDM = 0.0
    minusDM = 0.0
    upMove = hi[shift] - hi[shift + 1]
    downMove = lo[shift + 1] - lo[shift]
    if upMove > downMove and upMove > 0.0:
        plusDM = upMove
    if downMove > upMove and downMove > 0.0:
        minusDM = downMove

    smoothedPlusDM = smma(
        period=periodDI, shift=0, rates=[plusDM], prev=prevSmoothedPlusDM)
    if smoothedPlusDM is None:
        return None
    smoothedMinusDM = smma(
        period=periodDI, shift=0, rates=[minusDM], prev=prevSmoothedMinusDM)
    if smoothedMinusDM is None:
        return None

    tr = max(hi[shift] - lo[shift], abs(hi[shift] - cl[shift + 1]),
             abs(lo[shift] - cl[shift + 1]))
    smoothedTr = smma(
        period=periodDI, shift=0, rates=[tr], prev=prevSmoothedTr)

    plusDI = None
    minusDI = None
    adx = None
    dx = None
    if smoothedTr is not None:
        if smoothedTr > 0.0:
            plusDI = (smoothedPlusDM * 100.0 / smoothedTr)
            minusDI = (smoothedMinusDM * 100.0 / smoothedTr)
            sumDI = plusDI + minusDI
            if sumDI > 0.0:
                dx = 100.0 * (abs(plusDI - minusDI) / sumDI)
                adx = smma(period=periodADX, shift=0, rates=[dx], prev=prevADX)

    return ({
        'smoothedTr': smoothedTr,
        'smoothedPlusDM': smoothedPlusDM,
        'smoothedMinusDM': smoothedMinusDM,
        "pdi": plusDI,
        "mdi": minusDI,
        'dx': dx,
        'adx': adx,
    })


# end of ADX


# Absolute Price Oscillator
def apo(periodFast=12, periodSlow=26, shift=0, rates=None, prev=None):
    if rates is None:
        return None

    prevFast = None
    prevSlow = None
    if prev is not None:
        prevFast = prev['fast']
        prevSlow = prev['slow']

    if prevFast is not None and prevSlow is not None:
        emaFast = ema(
            period=periodFast, rates=rates, shift=shift, prev=prevFast)
        emaSlow = ema(
            period=periodSlow, rates=rates, shift=shift, prev=prevSlow)
        if emaFast is None or emaSlow is None:
            apo = None
        else:
            apo = emaFast - emaSlow
    else:
        emaFast = ema(period=periodFast, shift=shift, rates=rates)
        emaSlow = ema(period=periodSlow, shift=shift, rates=rates)
        if emaFast is None or emaSlow is None:
            apo = None
        else:
            apo = emaFast - emaSlow

    if apo is None:
        return None
    return ({'slow': emaSlow, 'fast': emaFast, 'apo': apo})


# end of apo


def aroon(period=14, shift=0, rates=None):
    global _close
    if rates is None:
        rates = _close
    if rates is None:
        return None

    notAssigned = True
    highest = -1.0  # Highest high to be stored here
    highestIndex = -1.0  # The highest high index to be stored here
    lowest = -1.0  # Lowest low to be stored here
    lowestIndex = -1.0  # The lowest low index to be stored here

    endIndex = shift + period + 1
    if endIndex > len(rates):
        return None

    for i in range(shift, endIndex):
        priceValue = rates[i]
        if notAssigned:
            highest = priceValue
            highestIndex = i
            lowest = priceValue
            lowestIndex = i
            notAssigned = False
        else:
            if highest < priceValue:
                highest = priceValue
                highestIndex = i
            elif lowest > priceValue:
                lowest = priceValue
                lowestIndex = i

    if notAssigned:
        return None

    up = (period - (highestIndex - shift)) * 100.0 / period
    down = (period - (lowestIndex - shift)) * 100.0 / period

    return ({'up': up, 'down': down})


# end of aroon


# ATR - Average True Range
def atr(period=14, shift=0, hi=None, lo=None, cl=None):
    if hi is None or lo is None or cl is None:
        return None

    startIndex = shift + period - 1
    if startIndex >= len(cl):
        startIndex = len(cl) - 1
    trValues = []
    for i in range(startIndex, shift - 1, -1):
        trValues.append(tr(hi, lo, cl, i))
    if len(trValues) > 0:
        return np.mean(trValues)
    else:
        return None


# end of atr


def tr(hi, lo, cl, shift):
    trValue = None
    lenCl = len(cl)
    if shift + 1 < lenCl:
        trValue = max(hi[shift] - lo[shift], abs(hi[shift] - cl[shift + 1]),
                      abs(lo[shift] - cl[shift + 1]))
    elif shift < lenCl:
        trValue = hi[shift] - lo[shift]
    return trValue


#end of tr


# Bollinger Bands
def bollinger(period=20, shift=0, nStds=2.0, rates=None):
    if rates is None:
        return None

    en = shift + period
    if en > len(rates):
        return None

    bandMiddle = np.mean(rates[shift:en])
    bandStd = np.std(rates[shift:en])

    top = (bandMiddle + nStds * bandStd)
    bottom = (bandMiddle - nStds * bandStd)
    return ({'ma': bandMiddle, 'std': bandStd, 'top': top, 'bottom': bottom})


# end of bollinger


# CCI indicator
def cci(period=20, shift=0, hi=None, lo=None, cl=None, cciConst=0.015):
    if hi is None or lo is None or cl is None:
        return None

    if shift + period - 1 >= len(cl):
        return None

    typicalPrices = np.empty(shape=period, dtype='float')
    for i in range(shift + period - 1, shift - 1, -1):
        typicalPrices[shift - i] = (hi[i] + lo[i] + cl[i]) / 3.0

    meanTypicalPrice = np.mean(typicalPrices)

    sumDeviation = 0.0
    for i in range(shift + period - 1, shift - 1, -1):
        sumDeviation = sumDeviation + abs(meanTypicalPrice -
                                          typicalPrices[shift - i])
    if not (sumDeviation > 0.0):
        return None
    meanDeviation = sumDeviation / period

    cciValue = (typicalPrices[0] - meanTypicalPrice) / (
        cciConst * meanDeviation)

    return {
        'cci': cciValue,
        'meanTypicalPrice': meanTypicalPrice,
        'meanDeviation': meanDeviation
    }


# end of CCI


# Chande Momentum Oscillator
def chande(period=10, shift=0, rates=None):
    if rates is None:
        return None

    if shift + period >= len(rates):
        return None

    up = 0.0
    down = 0.0
    pricePrev = None
    for i in range(shift + period, shift - 1, -1):
        if pricePrev is not None:
            diff = rates[i] - pricePrev
            if diff > 0.0:
                up += diff
            elif diff < 0.0:
                down += (-diff)
        pricePrev = rates[i]

    summed = up + down
    if not (summed > 0.0):
        return None
    return ((up - down) * 100.0) / summed


# end of Chande Momentum Oscillator


# EMA - Exponential Moving Average
def ema(period=10, shift=0, alpha=None, rates=None, prev=None, history=-1):
    if rates is None:
        return None

    if alpha is None:
        alpha = 2.0 / (period + 1.0)

    emaValue = None
    lenRates = len(rates)

    # Previously calculated ema is given
    if prev is not None:
        #if shift < lenRates:
        emaValue = (rates[shift] - prev) * alpha + prev
    else:
        if history == -1:
            if shift < lenRates:
                emaValue = rates[shift]
        elif history == 0:
            end = shift + period
            if shift < lenRates:
                if end > lenRates:
                    end = lenRates
                emaValue = np.mean(rates[shift:end])
        else:
            end = shift + period + history - 1
            if end >= len(rates):
                end = len(rates) - 1
            if end >= shift:
                emaValue = np.mean(rates[shift + history:end + 1])
                for i in range(shift + history - 1, shift - 1, -1):
                    emaValue = (rates[i] - emaValue) * alpha + emaValue
    return emaValue


# end of ema


# Keltner Channels
def keltner(period=20,
            multiplier=1.0,
            shift=0,
            hi=None,
            lo=None,
            cl=None,
            prev=None):
    if hi is None or lo is None or cl is None:
        return None
    lenRates = len(cl)
    if lenRates <= shift:
        return None

    if prev is not None:
        hlc = (hi[shift] + lo[shift] + cl[shift]) / 3.0
        priceList = [hlc]
        emaBasis = ema(
            period=period, rates=priceList, shift=0, prev=prev['basis'])
        if lenRates > shift + 1:
            trList = [tr(hi, lo, cl, shift)]
            atr = ema(period=period, rates=trList, shift=0, prev=prev['atr'])
        else:
            atr = None
    else:
        priceList = []
        trList = []
        firstIndex = shift + period - 1
        if firstIndex > lenRates - 1:
            firstIndex = lenRates - 1
        for i in range(firstIndex, shift - 1, -1):
            hlc = (hi[i] + lo[i] + cl[i]) / 3.0
            priceList.append(hlc)
        if firstIndex > lenRates - 2:
            firstIndex = lenRates - 2
        for i in range(firstIndex, shift - 1, -1):
            trList.append(tr(hi, lo, cl, i))
        emaBasis = ema(period=period, rates=priceList, shift=0)
        atr = ema(period=period, rates=trList, shift=0)

    if emaBasis is None or atr is None:
        upper = None
        lower = None
    else:
        upper = emaBasis + atr * multiplier
        lower = emaBasis - atr * multiplier

    return ({'basis': emaBasis, 'upper': upper, 'lower': lower, 'atr': atr})


# end of keltners


# MACD - Moving Average Convergence/Divergence Oscillator
def macd(periodFast=12,
         periodSlow=26,
         periodSignal=9,
         shift=0,
         rates=None,
         prev=None):
    global _close
    if rates is None:
        rates = _close
    if rates is None:
        return None

    if prev is not None:
        emaFast = ema(
            period=periodFast, rates=rates, shift=shift, prev=prev['fast'])
        emaSlow = ema(
            period=periodSlow, rates=rates, shift=shift, prev=prev['slow'])
        if emaFast is None or emaSlow is None:
            macd = None
            emaSignal = None
        else:
            macd = emaFast - emaSlow
            emaSignal = ema(
                period=periodSignal,
                rates=[macd],
                shift=0,
                prev=prev['signal'])
    else:
        emaFast = ema(period=periodFast, shift=shift, rates=rates)
        emaSlow = ema(period=periodSlow, shift=shift, rates=rates)
        if emaFast is None or emaSlow is None:
            macd = None
            emaSignal = None
        else:
            macd = emaFast - emaSlow
            emaSignal = ema(period=periodSignal, shift=shift, rates=[macd])
    if macd is not None and emaSignal is not None:
        histogram = (macd - emaSignal)
    else:
        histogram = None

    #if macd is None or emaSignal is None or histogram is None:
    #    return None
    return ({
        'slow': emaSlow,
        'fast': emaFast,
        'macd': macd,
        'signal': emaSignal,
        'histogram': histogram
    })


# end of macd


# Momentum indicator
def momentum(period=9, shift=0, rates=None):
    if rates is None:
        return None

    nPeriodsAgoIndex = shift + period
    if nPeriodsAgoIndex >= len(rates):
        return None
    if not (rates[nPeriodsAgoIndex] > 0):
        return None

    return (rates[shift] - rates[nPeriodsAgoIndex])


# end of momentum


# PPO - Percent Price Oscillator
def ppo(periodFast=12, periodSlow=26, shift=0, rates=None):
    if rates is None:
        return None

    lenRates = len(rates)
    endIndexFast = shift + periodFast
    endIndexSlow = shift + periodSlow
    if endIndexSlow > lenRates:
        return None

    meanFast = np.mean(rates[shift:endIndexFast])
    meanSlow = np.mean(rates[shift:endIndexSlow])
    if (not (meanSlow > 0.0)):
        return None

    return ((meanFast - meanSlow) * 100.0) / meanSlow


# end of ppo


# RSI - Relative Strength Index
def rsi(period=14, shift=0, rates=None, prev=None):
    if rates is None:
        return None
    lenRates = len(rates)

    if shift + 1 >= lenRates:
        return None

    averagePosPrev = None  # 0.00491656 # None
    averageNegPrev = None  # 0.00132679 # None
    if prev is not None:
        averagePosPrev = prev['averagePos']
        averageNegPrev = prev['averageNeg']

    # if (averageGainPrev is not None) and (averageLossPrev is not None):
    difference = rates[shift] - rates[shift + 1]
    currentPos = 0.0
    currentNeg = 0.0
    if difference > 0.0:
        currentPos = difference
    if difference < 0.0:
        currentNeg = -difference

    averagePos = rma(
        period=period, rates=[currentPos], shift=0, prev=averagePosPrev)
    averageNeg = rma(
        period=period, rates=[currentNeg], shift=0, prev=averageNegPrev)
    if not (averageNeg > 0.0):
        rsiValue = 100.0
    elif not (averagePos > 0.0):
        rsiValue = 0.0
    else:
        rsiValue = 100.0 - (100.0 / (1.0 + averagePos / averageNeg))

    return ({
        'rsi': rsiValue,
        'averagePos': averagePos,
        'averageNeg': averageNeg
    })


# end of rsi


# ROC - Rate Of Change Oscillator
def roc(period=9, shift=0, rates=None):
    if rates is None:
        return None

    nPeriodsAgoIndex = shift + period
    if nPeriodsAgoIndex >= len(rates):
        return None
    if not (rates[nPeriodsAgoIndex] > 0):
        return None

    return (rates[shift] -
            rates[nPeriodsAgoIndex]) * 100.0 / rates[nPeriodsAgoIndex]


# end of roc


# SMA - Simple Moving Average
def sma(period=10, shift=0, rates=None, source=None, newValue=None):
    if rates is None:
        return None

    if source is None:
        lenRates = len(rates)
        endIndex = shift + period
        if endIndex > lenRates:
            return None
        return np.mean(rates[shift:endIndex])
    else:
        if newValue is not None:
            source.insert(0, newValue)
        else:
            source.insert(0, rates[shift])
        if len(source) > period:
            source.pop()
        return np.mean(source)


# end of sma


# SMMA - Smooothed Moving Average
def smma(period, shift=0, rates=None, prev=None):
    return ema(
        period=period, shift=shift, alpha=1.0 / period, rates=rates, prev=prev)


# end of smma


# RMA - A EMA for RSI
def rma(period, shift=0, rates=None, prev=None):
    return ema(
        period=period, shift=shift, alpha=1.0 / period, rates=rates, prev=prev)


# end of rma


# Stochastic (FSI) - Stochastic Oscillator
def stochastic(period=14,
               periodD=3,
               smoothing=1,
               shift=0,
               hi=None,
               lo=None,
               cl=None):
    if hi is None or lo is None or cl is None:
        return None

    ratesLen = len(cl)
    if shift + period + periodD - 1 >= ratesLen:
        if shift + period - 1 >= ratesLen:  # The 'K' value is also impossible to calculate?
            return None
        valueK = stochasticK(
            hi, lo, cl, shift,
            shift + period - 1)  # Calculating the 'K' value only
        if valueK is None:
            return None
        return ({'k': valueK, 'd': None})

    valuesK = np.empty(shape=periodD, dtype='float')
    for i in range(periodD):
        valueK = stochasticK(hi, lo, cl, shift + i, shift + i + period - 1)
        if valueK is None:
            return None
        valuesK[i] = valueK

    return ({'k': valuesK[0], 'd': np.mean(valuesK)})


# end of stochastic


def stochasticK(hi, lo, cl, st, en):
    minLow = lo[st]
    maxHigh = hi[st]
    for i in range(st + 1, en + 1):
        if lo[i] < minLow:
            minLow = lo[i]
        if hi[i] > maxHigh:
            maxHigh = hi[i]
    difference = maxHigh - minLow
    if not (difference > 0):
        return None

    return (cl[st] - minLow) * 100.0 / difference


# end of stochasticK


# TRIMA
def trima(period=10, shift=0, rates=None):
    if rates is None:
        return None

    ratesLen = len(rates)

    interval = period / 2.0 + 0.5
    interval = int(interval)

    arrayOfSma = []
    for i in range(interval):
        valueOfSma = sma(period=interval, rates=rates, shift=shift + i)
        if valueOfSma is None:
            break
        arrayOfSma.append(valueOfSma)

    valueOfTrima = None
    if len(arrayOfSma) > 0:
        valueOfTrima = sma(period=interval, rates=arrayOfSma)
    return valueOfTrima


# end of stochastic


def williams(period=14, shift=0, hi=None, lo=None, cl=None):
    if hi is None or lo is None or cl is None:
        return None

    endIndex = shift + period
    if endIndex > len(cl):
        return None

    lowestLow = np.min(lo[shift:endIndex])
    highestHigh = np.max(hi[shift:endIndex])
    diff = highestHigh - lowestLow
    if not (diff > 0.0):
        return None

    return (-100.0 * (highestHigh - cl[shift])) / diff


# end of williams


def wma(period=10, shift=0, rates=None, prev=None):
    if rates is None:
        return None
    numSummed = 0
    summed = 0.0
    smoothed = 0.0
    if prev is not None:
        numSummed = prev['num']
        summed = prev['sum']
        smoothed = prev['wma']

    if numSummed < period:
        summed = summed + rates[shift]
        numSummed += 1
        smoothed = summed / numSummed
    else:
        smoothed = (smoothed * (period - 1.0) + rates[shift]) / period

    return ({'wma': smoothed, 'num': numSummed, 'sum': summed})


# end of wma


def awesome(period1=5, period2=34, shift=0, hi=None, lo=None):
    if hi is None or lo is None:
        return None

    endIndex = shift + period1
    if endIndex > len(hi):
        return None
    v1 = (hi[shift:endIndex] + lo[shift:endIndex]) / 2.0

    endIndex = shift + period2
    if endIndex > len(hi):
        return None
    v2 = (hi[shift:endIndex] + lo[shift:endIndex]) / 2.0

    return (v1 - v2)


# end of awesome


def pNextHigher(period, rates):
    if rates is None:
        return None

    if len(rates) < period or period < 2:
        return None

    numH = 0.0
    for i in range(1, period):
        if rates[i - i] > rates[i]:
            numH += 1.0

    return numH / (period - 1.0)


# end of def


def pNextLower(period, rates):
    if rates is None:
        return None

    if len(rates) < period or period < 2:
        return None

    numL = 0.0
    for i in range(1, period):
        if rates[i - 1] < rates[i]:
            numL += 1.0

    return numL / (period - 1.0)


# end of def
