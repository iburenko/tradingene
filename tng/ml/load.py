import numpy as np
import sys
sys.path.append('./../../')
from tng.algorithm_backtest.tng import TNG


def import_data(ticker, timeframe, start_date, end_date):
    def on_bar(instrument):
        pass

    name = "import_data"
    regime = "SP"
    alg = TNG(name, regime, start_date, end_date)
    alg.addInstrument(ticker)
    alg.addTimeframe(ticker, timeframe)
    alg.run_backtest(on_bar, pre_load=False)
    hist = list(alg.instruments)[0].rates[1:]
    del alg
    return hist


def load(fileName,
         startYear=None,
         endYear=None,
         startMonth=1,
         endMonth=12,
         startDay=1,
         endDay=None):
    readError = False
    fileOpened = False

    linesRead = 0
    linesSkipped = 0

    if startYear is None:
        startYear = 1900
    if endYear is None:
        endYear = 2200
    if endDay is None:
        endDay = getEndDayOfMonth(endYear, endMonth)

    from datetime import datetime

    startDate = datetime.strptime(
        str(startYear) + ":" + str(startMonth) + ":" + str(startDay),
        "%Y:%m:%d")
    endDate = datetime.strptime(
        str(endYear) + ":" + str(endMonth) + ":" + str(endDay), "%Y:%m:%d")

    op = []
    hi = []
    lo = []
    cl = []
    vol = []
    dtm = []

    try:
        fileHandle = open(fileName, "r")
        fileOpened = True

        for line in fileHandle:

            lineSplitted = line.split(",")
            if len(lineSplitted) < 6:
                linesSkipped += 1
                continue

            strDatetime = lineSplitted[0]
            dateTime = datetime.strptime(strDatetime, '%Y%m%d%H%M%S%f')

            if dateTime < startDate:
                continue
            if dateTime > endDate:
                continue

            dtm.append(dateTime)
            op.append(float(lineSplitted[1]))
            hi.append(float(lineSplitted[2]))
            lo.append(float(lineSplitted[3]))
            cl.append(float(lineSplitted[4]))
            vol.append(float(lineSplitted[5].rstrip()))

            linesRead += 1
    except IOError:
        readError = True

    if fileOpened:
        fileHandle.close()

    if readError:
        return (None)

    op = np.array(op[::-1], dtype='float')
    hi = np.array(hi[::-1], dtype='float')
    lo = np.array(lo[::-1], dtype='float')
    cl = np.array(cl[::-1], dtype='float')
    vol = np.array(vol[::-1], dtype='float')
    dtm = dtm[::-1]

    return {
        'op': op,
        'hi': hi,
        'lo': lo,
        'cl': cl,
        'vol': vol,
        'dtm': dtm,
        'length': linesRead,
        'skipped': linesSkipped
    }


# end of readFinam


def getEndDayOfMonth(year, month):
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        endDay = 31
    elif month == 2:
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    endDay = 29
                else:
                    endDay = 28
            else:
                endDay = 29
        else:
            endDay = 28
    else:
        endDay = 30
    return endDay


# end of def
