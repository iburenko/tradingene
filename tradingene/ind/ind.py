import tradingene.ind.ti as ti
from tradingene.algorithm_backtest.limits import LOOKBACK_PERIOD
import numpy as np


class Indicators:
    def __init__(self, _timeframeMin):
        self._timeframe = _timeframeMin
        self._indicators = list()

    @property
    def timeframe(self):
        return self._timeframe

    @timeframe.setter
    def timeframe(self, value):
        self._timeframe = value

    @timeframe.deleter
    def timeframe(self):
        self._timeframe = 0

    @property
    def indicators(self):
        return self._indicators

    @indicators.setter
    def indicators(self, value):
        self._indicators = value

    @indicators.deleter
    def indicator(self):
        self._indicators = list()

    def ad(self, period=1):
        indParameters = {'name': 'ad', 'period': period}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndAD(period)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def adx(self, periodADX=14, periodDI=-1):
        indParameters = {
            'name': 'adx',
            'periodADX': periodADX,
            'periodDI': periodDI
        }
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndADX(periodADX, periodDI)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def apo(self, periodFast=26, periodSlow=12, priceType='close'):
        indParameters = {'name': 'apo', 'periodFast': periodFast, \
                         'periodSlow': periodSlow, 'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndAPO(periodFast, periodSlow, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def aroon(self, period=1, priceType='close'):
        indParameters = {'name': 'aroon', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndAroon(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def atr(self, period=1):
        indParameters = {'name': 'atr', 'period': period}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndATR(period)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def bollinger(self, period=14, priceType='close', nStds=2.0):
        indParameters = {'name': 'bollinger', 'period': period, \
                         'priceType': priceType, 'nStds': nStds}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndBollinger(period, priceType, nStds)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def cci(self, period=14, cciConst=0.015):
        indParameters = {'name': 'cci', 'period': period, 'cciConst': cciConst}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndCCI(period, cciConst)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def chande(self, period=10, priceType='close'):
        indParameters = {'name': 'chande', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndChande(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def ema(self, period=9, priceType='close'):
        indParameters = {'name': 'ema', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndEMA(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def keltner(self, period=14, multiplier=1.0):
        indParameters = {
            'name': 'keltner',
            'period': period,
            'multiplier': multiplier
        }
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndKeltner(period, multiplier)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None


    def macd(self, periodFast=26, periodSlow=12, periodSignal=9, \
                   priceType='close'):
        indParameters = {'name': 'macd', 'periodFast': periodFast, \
                         'periodSlow': periodSlow, 'periodSignal':periodSignal,\
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndMACD(periodFast, periodSlow, periodSignal, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def momentum(self, period=9, priceType='close'):
        indParameters = {'name': 'momentum', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndMomentum(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def ppo(self, periodFast=12, periodSlow=26, priceType='close'):
        indParameters = {'name': 'ppo', 'periodFast': periodFast, \
                         'periodSlow': periodSlow, 'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndPPO(periodFast, periodSlow, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def roc(self, period=9, priceType='close'):
        indParameters = {'name': 'roc', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndROC(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def sma(self, period=9, priceType='close'):
        indParameters = {'name': 'sma', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndSMA(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def rsi(self, period=14, priceType='close'):
        indParameters = {'name': 'rsi', 'period': period, \
                         'priceType': priceType}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndRSI(period, priceType)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def stochastic(self, period=14, periodD=3, smoothing=1):
        indParameters = {'name': 'stochastic', 'period': period, \
                         'periodD':periodD, 'smoothing':smoothing}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndStochastic(period, periodD, smoothing)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def trima(self, period=10):
        indParameters = {'name': 'trima', 'period': period}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndTrima(period)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None

    def williams(self, period=14):
        indParameters = {'name': 'williams', 'period': period}
        ind = IndHlp.findIndicator(self.indicators, indParameters)
        if ind is None:
            ind = IndWilliams(period)
            indParameters['ind'] = ind
            self.indicators.append(indParameters)
        if ind is not None:
            ind.recalculate(self.rates)
            return ind.getValues()
        return None


# end of Indicators


class IndHlp:

    historySize = 50 + 3  # LOOKBACK_PERIOD # UNCOMMENT!!!!

    @staticmethod
    def getRatesByPriceType(rates, priceType):
        if priceType == 'open':
            return rates['open']
        elif priceType == 'high' or priceType == 'max':
            return rates['high']
        elif priceType == 'high' or priceType == 'max':
            return rates['high']
        elif priceType == 'low' or priceType == 'min':
            return rates['low']
        else:
            return rates['close']

    # end of def

    @staticmethod
    def getIndexToCalculate(dtmsInd, dtmsRates):
        indexStart = -1
        indexToOverwrite0 = -1
        if len(dtmsInd) == 0:
            return IndHlp.historySize - 1, indexToOverwrite0

        if dtmsInd[0] < dtmsRates[0]:
            for i in range(1, len(dtmsRates)):
                if dtmsInd[0] == dtmsRates[i]:
                    indexStart = i
                    indexToOverwrite0 = i
                    break
        return indexStart, indexToOverwrite0

    # end of getIndexToCalculate

    @staticmethod
    def findIndicator(indicators, keyValuePairs):
        ind = None
        for i in range(len(indicators)):
            failed = False
            for key in keyValuePairs:
                if not (key in indicators[i]):
                    failed = True
                    break
                if keyValuePairs[key] != indicators[i][key]:
                    failed = True
                    break
            if not failed:
                ind = indicators[i]['ind']
                break
        return ind

    @staticmethod
    def insertTime(dtmsIndex, dtms, timeIndex, time):
        if timeIndex < len(time):
            dtms.insert(dtmsIndex, time[timeIndex])
        else:
            dtms.insert(dtmsIndex, None)

    @staticmethod
    def getPrev(values, overwrite):
        if overwrite:
            prevIndex = 1
        else:
            prevIndex = 0
        if len(values) > prevIndex:
            return values[prevIndex]
        return None


# end of IndHlp


class IndVals:
    def __init__(self):
        return

    def __setattr__(self, name, value):
        self.__dict__[name] = value


# end of class IndicatorValues


class Indicator:
    def __init__(self, period=9, priceType="close"):
        self.period = period
        self.priceType = priceType
        self.values = []
        self.dtms = []

    def getValues(self):
        return self.values

    def calculateAll(
            self, rates
    ):  # To calculate indicator value(s) for every candle bar in price&volume history.
        indexStart = len(rates['close']) - 1
        for i in range(indexStart, -1, -1):
            self.calculate(rates, i, useHistorySize=False)  #

    def recalculate(self, rates):
        indexStart, indexToOverwrite0 = IndHlp.getIndexToCalculate(
            self.dtms, rates['time'])
        for i in range(indexStart, -1, -1):
            self.calculate(rates, i, indexToOverwrite0 == i)  #

    def calculate(self, rates, shift=0, overwrite=False):
        raise NotImplementedError("Must override calculate()")


# end of class Indicator


class IndAD(Indicator):
    def __init__(self, period=1):
        Indicator.__init__(self, period)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.values, overwrite)
        new = ti.ad(period=self.period, shift=shift, prev=prev,\
                        hi=rates['high'], lo=rates['low'], \
                        cl=rates['close'], vol=rates['vol'])
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        values = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.ad(period=self.period, shift=i, prev=prev,\
                            hi=rates['high'], lo=rates['low'], \
                            cl=rates['close'], vol=rates['vol'])
            values[i] = new
            prev = new
        return {'ad': values}


# end of IndAD


class IndADX(Indicator):
    def __init__(self, periodADX=14, periodDI=-1):
        Indicator.__init__(self, 0)
        self.raw = []
        self.periodADX = periodADX
        self.periodDI = periodDI
        self.indVals = IndVals()
        self.indVals.adx = []
        self.indVals.pdi = []
        self.indVals.mdi = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.raw.pop()
            self.indVals.adx.pop()
            self.indVals.pdi.pop()
            self.indVals.mdi.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.raw, overwrite)
        new = ti.adx(periodADX=self.periodADX, periodDI=self.periodDI, shift=shift, prev=prev, \
                        hi=rates['high'], lo=rates['low'], cl=rates['close'])
        newADX = None
        newPDI = None
        newMDI = None
        if new is not None:
            if new['adx'] is not None:
                newADX = new['adx']
            if new['pdi'] is not None:
                newPDI = new['pdi']
            if new['mdi'] is not None:
                newMDI = new['mdi']
        if overwrite:
            self.indVals.adx[0] = newADX
            self.indVals.pdi[0] = newPDI
            self.indVals.mdi[0] = newMDI
            self.raw[0] = new
        else:
            self.indVals.adx.insert(0, newADX)
            self.indVals.pdi.insert(0, newPDI)
            self.indVals.mdi.insert(0, newMDI)
            self.raw.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time
        #print( str(self.dtms[0]) + ":" + str(self.indVals.adx[0]) )

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        adx = np.empty(lenRates)
        pdi = np.empty(lenRates)
        mdi = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.adx(periodADX=self.periodADX, periodDI=self.periodDI, shift=i, prev=prev, \
                hi=rates['high'], lo=rates['low'], cl=rates['close'])
            if new is not None:
                adx[i] = new['adx']
                pdi[i] = new['pdi']
                mdi[i] = new['mdi']
            prev = new
        return {'adx.adx': adx, 'adx.pdi': pdi, 'adx.mdi': mdi}


# end of IndADX


class IndAPO(Indicator):
    def __init__(self, periodFast=12, periodSlow=26, priceType='close'):
        Indicator.__init__(self, 0, priceType)
        self.periodFast = periodFast
        self.periodSlow = periodSlow
        self.raw = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.raw.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.raw, overwrite)
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.apo(periodFast=self.periodFast, periodSlow=self.periodSlow, \
                    shift=shift, rates=rates1d, prev=prev)
        newAPO = None
        if new is not None:
            if new['apo'] is not None:
                newAPO = new['apo']
        if overwrite:
            self.values[0] = newAPO
            self.raw[0] = new
        else:
            self.values.insert(0, newAPO)
            self.raw.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.apo(periodFast=self.periodFast, periodSlow=self.periodSlow, \
                    shift=i, rates=rates1d, prev=prev)
            values[i] = new['apo']
            prev = new
        return {'apo': values}


# end of IndAPO


class IndAroon(Indicator):
    def __init__(self, period=14, priceType="close"):
        Indicator.__init__(self, period, priceType)
        self.indVals = IndVals()
        self.indVals.up = []
        self.indVals.down = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.indVals.up.pop()
            self.indVals.down.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.aroon(period=self.period, shift=shift, rates=rates1d)
        newUp = None
        newDown = None
        if new is not None:
            if new['up'] is not None:
                newUp = new['up']
            if new['down'] is not None:
                newDown = new['down']
        if overwrite:
            self.indVals.up[0] = newUp
            self.indVals.down[0] = newDown
        else:
            self.indVals.up.insert(0, newUp)
            self.indVals.down.insert(0, newDown)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        up = np.empty(lenRates)
        down = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            new = ti.aroon(period=self.period, shift=i, rates=rates1d)
            if new is not None:
                up[i] = new['up']
                down[i] = new['down']
            else:
                up[i] = None
                down[i] = None
        return {'aroon.up': up, 'aroon.down': down}


# end of IndAroon


class IndATR(Indicator):
    def __init__(self, period=14):
        Indicator.__init__(self, period)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        new = ti.atr(period=self.period, shift=shift, \
                          hi=rates['high'], lo=rates['low'], cl=rates['close'])
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.atr(period=self.period, shift=i, \
                            hi=rates['high'], lo=rates['low'], cl=rates['close'])
        return {'atr': values}


# end of IndATR


class IndBollinger(Indicator):
    def __init__(self, period=1, priceType='close', nStds=2.0):
        Indicator.__init__(self, period, priceType)
        self.nStds = nStds
        self.indVals = IndVals()
        self.indVals.ma = []
        self.indVals.top = []
        self.indVals.bottom = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.indVals.ma.pop()
            self.indVals.top.pop()
            self.indVals.bottom.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.bollinger(
            period=self.period, shift=shift, nStds=self.nStds, rates=rates1d)
        newMA = None
        newTop = None
        newBottom = None
        if new is not None:
            if new['ma'] is not None:
                newMA = new['ma']
            if new['top'] is not None:
                newTop = new['top']
            if new['bottom'] is not None:
                newBottom = new['bottom']
        if overwrite:
            self.indVals.ma[0] = newMA
            self.indVals.top[0] = newTop
            self.indVals.bottom[0] = newBottom
        else:
            self.indVals.ma.insert(0, newMA)
            self.indVals.top.insert(0, newTop)
            self.indVals.bottom.insert(0, newBottom)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        ma = np.empty(lenRates)
        top = np.empty(lenRates)
        bottom = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            new = ti.bollinger(
                period=self.period, shift=i, nStds=self.nStds, rates=rates1d)
            if new is not None:
                ma[i] = new['ma']
                top[i] = new['top']
                bottom[i] = new['bottom']
            else:
                ma[i] = None
                top[i] = None
                bottom[i] = None
        return {'ma': ma, 'top': top, 'bottom': bottom}


# end of IndBollinger


class IndCCI(Indicator):
    def __init__(self, period=9, cciConst=0.015):
        Indicator.__init__(self, period)
        self.cciConst = cciConst

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        new = ti.cci(period=self.period, cciConst=self.cciConst, shift=shift, \
                     hi=rates['high'], lo=rates['low'], cl=rates['close'])
        newCCI = None
        if new is not None:
            if new['cci'] is not None:
                newCCI = new['cci']
        if overwrite:
            self.values[0] = newCCI
        else:
            self.values.insert(0, newCCI)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            new = ti.cci(period=self.period, cciConst=self.cciConst, shift=i, \
                     hi=rates['high'], lo=rates['low'], cl=rates['close'])
            if new is not None:
                values[i] = new['cci']
            else:
                values[i] = None
        return {'cci': values}


# end of IndCCI


class IndChande(Indicator):
    def __init__(self, period=10, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.chande(period=self.period, shift=shift, rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.chande(period=self.period, shift=i, rates=rates1d)
        return {'chande': values}


# end of IndChande


class IndEMA(Indicator):
    def __init__(self, period=9, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.values, overwrite)
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.ema(period=self.period, shift=shift, rates=rates1d, prev=prev)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.ema(
                period=self.period, shift=i, rates=rates1d, prev=prev)
            prev = values[i]
        return {'ema': values}


# end of IndEMA


class IndKeltner(Indicator):
    def __init__(self, period=20, multiplier=1.0):
        Indicator.__init__(self, period)
        self.multiplier = multiplier
        self.indVals = IndVals()
        self.indVals.basis = []
        self.indVals.upper = []
        self.indVals.lower = []
        self.raw = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.indVals.basis.pop()
            self.indVals.upper.pop()
            self.indVals.lower.pop()
            self.raw.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.raw, overwrite)
        new = ti.keltner(period=self.period, multiplier=self.multiplier, shift=shift, prev=prev, \
                        hi=rates['high'], lo=rates['low'], cl=rates['close'])
        newBasis = None
        newUpper = None
        newLower = None
        if new is not None:
            if new['basis'] is not None:
                newBasis = new['basis']
            if new['upper'] is not None:
                newUpper = new['upper']
            if new['lower'] is not None:
                newLower = new['lower']
        if overwrite:
            self.indVals.basis[0] = newBasis
            self.indVals.upper[0] = newUpper
            self.indVals.lower[0] = newLower
            self.raw[0] = new
        else:
            self.indVals.basis.insert(0, newBasis)
            self.indVals.upper.insert(0, newUpper)
            self.indVals.lower.insert(0, newLower)
            self.raw.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        basis = np.empty(lenRates)
        upper = np.empty(lenRates)
        lower = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.keltner(period=self.period, multiplier=self.multiplier, shift=i, prev=prev, \
                        hi=rates['high'], lo=rates['low'], cl=rates['close'])
            if new is not None:
                basis[i] = new['basis']
                upper[i] = new['upper']
                lower[i] = new['lower']
            else:
                basis[i] = None
                upper[i] = None
                lower[i] = None
            prev = new
        return {
            'keltner.basis': basis,
            'keltner.upper': upper,
            'keltner.lower': lower
        }


# end of IndKeltner


class IndMACD(Indicator):
    def __init__(self,
                 periodFast=12,
                 periodSlow=26,
                 periodSignal=9,
                 priceType='close'):
        Indicator.__init__(self, 0, priceType)
        self.periodFast = periodFast
        self.periodSlow = periodSlow
        self.periodSignal = periodSignal
        self.indVals = IndVals()
        self.indVals.macd = []
        self.indVals.signal = []
        self.indVals.histogram = []
        self.raw = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.indVals.macd.pop()
            self.indVals.signal.pop()
            self.indVals.histogram.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.raw, overwrite)
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.macd(periodFast=self.periodFast, periodSlow=self.periodSlow, \
                      periodSignal=self.periodSignal, shift=shift, \
                      rates=rates1d, prev=prev)
        newMACD = None
        newSignal = None
        newHistogram = None
        if new is not None:
            if new['macd'] is not None:
                newMACD = new['macd']
            if new['signal'] is not None:
                newSignal = new['signal']
            if new['histogram'] is not None:
                newHistogram = new['histogram']
        if overwrite:
            self.indVals.macd[0] = newMACD
            self.indVals.signal[0] = newSignal
            self.indVals.histogram[0] = newHistogram
            self.raw[0] = new
        else:
            self.indVals.macd.insert(0, newMACD)
            self.indVals.signal.insert(0, newSignal)
            self.indVals.histogram.insert(0, newHistogram)
            self.raw.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        macd = np.empty(lenRates)
        signal = np.empty(lenRates)
        histogram = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.macd(periodFast=self.periodFast, periodSlow=self.periodSlow, \
                          periodSignal=self.periodSignal, shift=i, \
                          rates=rates1d, prev=prev)
            if new is not None:
                macd[i] = new['macd']
                signal[i] = new['signal']
                histogram[i] = new['histogram']
            else:
                macd[i] = None
                signal[i] = None
                histogram[i] = None
            prev = new
        return {
            'macd.macd': macd,
            'macd.signal': signal,
            'macd.histogram': histogram
        }


# end of IndMACD


class IndMomentum(Indicator):
    def __init__(self, period=9, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.momentum(period=self.period, shift=shift, rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.momentum(period=self.period, shift=i, rates=rates1d)
        return {'momentum': values}


# end of IndMomentum


class IndPPO(Indicator):
    def __init__(self, periodFast=12, periodSlow=26, priceType="close"):
        Indicator.__init__(self, 0, priceType)
        self.periodFast = periodFast
        self.periodSlow = periodSlow

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.ppo(
            periodFast=self.periodFast,
            periodSlow=self.periodSlow,
            shift=shift,
            rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.ppo( periodFast=self.periodFast, periodSlow=self.periodSlow,\
                shift=i, rates=rates1d)
        return {'ppo': values}


# end of IndPPO


class IndROC(Indicator):
    def __init__(self, period=9, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.roc(period=self.period, shift=shift, rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.roc(period=self.period, shift=i, rates=rates1d)
        return {'roc': values}


# end of IndROC


class IndRSI(Indicator):
    def __init__(self, period=14, priceType="close"):
        Indicator.__init__(self, period, priceType)
        self.raw = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        prev = IndHlp.getPrev(self.raw, overwrite)
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.rsi(period=self.period, shift=shift, rates=rates1d, prev=prev)
        newRSI = None
        if new is not None:
            if new['rsi'] is not None:
                newRSI = new['rsi']
        if overwrite:
            self.values[0] = newRSI
            self.raw[0] = new
        else:
            self.values.insert(0, newRSI)
            self.raw.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        prev = None
        for i in range(lenRates - 1, -1, -1):
            new = ti.rsi(period=self.period, shift=i, rates=rates1d, prev=prev)
            if new is not None:
                values[i] = new['rsi']
            else:
                values[i] = None
            prev = new

        return {'rsi': values}


# end of IndRSI


class IndSMA(Indicator):
    def __init__(self, period=9, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.sma(period=self.period, shift=shift, rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.sma(period=self.period, shift=i, rates=rates1d)
        return {'sma': values}


# end of IndSMA


class IndStochastic(Indicator):
    def __init__(self, period=14, periodD=3, smoothing=1):
        Indicator.__init__(self, period, "")
        self.periodD = periodD
        self.smoothing = smoothing
        self.indVals = IndVals()
        self.indVals.k = []
        self.indVals.d = []

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.indVals.k.pop()
            self.indVals.d.pop()
            self.dtms.pop()

        new = ti.stochastic(period=self.period, periodD=self.periodD, \
                            smoothing=self.smoothing, shift=shift, \
                            hi=rates['high'],lo=rates['low'],cl=rates['close'])
        newK = None
        newD = None
        if new is not None:
            if new['k'] is not None:
                newK = new['k']
            if new['d'] is not None:
                newD = new['d']
        if overwrite:
            self.indVals.k[0] = newK
            self.indVals.d[0] = newD
        else:
            self.indVals.k.insert(0, newK)
            self.indVals.d.insert(0, newD)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def getValues(self):
        return self.indVals

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        k = np.empty(lenRates)
        d = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            new = ti.stochastic(period=self.period, periodD=self.periodD, \
                                smoothing=self.smoothing, shift=i, \
                                hi=rates['high'],lo=rates['low'],cl=rates['close'])
            if new is not None:
                k[i] = new['k']
                d[i] = new['d']
            else:
                k[i] = None
                d[i] = None

        return {'stochastic.k': k, 'stochastic.d': d}


# end of IndStochastic


class IndTrima(Indicator):
    def __init__(self, period=10, priceType="close"):
        Indicator.__init__(self, period, priceType)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        new = ti.trima(period=self.period, shift=shift, rates=rates1d)
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        rates1d = IndHlp.getRatesByPriceType(rates, self.priceType)
        lenRates = len(rates1d)
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.trima(period=self.period, shift=i, rates=rates1d)
        return {'trima': values}


# end of IndChande


class IndWilliams(Indicator):
    def __init__(self, period=14):
        Indicator.__init__(self, period)

    def calculate(self, rates, shift=0, overwrite=False, useHistorySize=True):
        if len(self.values) >= IndHlp.historySize and useHistorySize:
            self.values.pop()
            self.dtms.pop()

        new = ti.williams(
            period=self.period,
            shift=shift,
            hi=rates['high'],
            lo=rates['low'],
            cl=rates['close'])
        if overwrite:
            self.values[0] = new
        else:
            self.values.insert(0, new)
            IndHlp.insertTime(
                0, self.dtms, shift,
                rates['time'])  # dtmsIndex, dtms, timeIndex, time

    def calculateRates(self, rates):
        lenRates = len(rates['close'])
        values = np.empty(lenRates)
        for i in range(lenRates - 1, -1, -1):
            values[i] = ti.williams( period=self.period, shift=i,\
                hi=rates['high'], lo=rates['low'], cl=rates['close'])
        return {'williams': values}


# end of IndWilliams

#######################################################################################################################################
