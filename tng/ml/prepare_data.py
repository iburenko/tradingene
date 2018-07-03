import numpy as np


# Calculates (inputs, label, profit) for each data index by index
#def prepare_data(rates, calc_inp, calc_out, params=None, normalize=False):
def prepare_data(rates, calc_inp, calc_out, params=None):
    return_value = None
    op = rates['open']
    hi = rates['high']
    lo = rates['low']
    cl = rates['close']
    length = len(rates['open'])
    vol = rates['vol']
    dtm = rates['time']
    return_op = []
    return_dtm = []
    return_inputs = []
    return_labels = []
    return_profit = []
    return_rate_indexes = []
    return_custom_out = []
    for i in range(1, length):
        # Inputs
        pastRates = {
            'open': op[i:],
            'high': hi[i:],
            'low': lo[i:],
            'close': cl[i:],
            'vol': vol[i:],
            'time': dtm[i:]
        }
        futureRates = {
            'open': op[i - 1::-1],
            'high': hi[i - 1::-1],
            'low': lo[i - 1::-1],
            'close': cl[i - 1::-1],
            'vol': vol[i - 1::-1],
            'time': dtm[i - 1::-1]
        }

        inputs = calc_inp(pastRates, params)
        if inputs is None:
            continue

        res = calc_out(futureRates, params)
        if not isinstance(res, tuple):
            continue
        if len(res) == 2:  # No custom output added
            label, profit = res
            custom_out = None
        elif len(res) == 3:  # Custom output added
            label, profit, custom_out = res

        return_inputs.append(inputs)
        return_labels.append(label)
        return_profit.append(profit)
        return_dtm.append(dtm[i - 1])
        return_op.append(op[i - 1])
        return_rate_indexes.append(i - 1)
        if custom_out is not None:
            return_custom_out.append(custom_out)
    if len(return_inputs) == 0:
        return return_value
    if len(return_labels) == 0:
        return return_value

    return_inputs = np.array(return_inputs, dtype='float')
    return_rate_indexes = np.array(return_rate_indexes, dtype='int')
    num_samples, num_features = np.shape(return_inputs)
    return_labels = np.array(return_labels, dtype='float')
    shape = np.shape(return_labels)
    if len(shape) == 2:  # One Hot
        num_labels = shape[1]
    else:
        num_labels = int(np.max(return_labels) + 1)
    return_profit = np.array(return_profit, dtype='float')
    return_mean = np.zeros(shape=[num_features], dtype='float')
    return_std = np.zeros(shape=[num_features], dtype='float')

    # if normalize: # If normalization is required
    # 	for i in range(numFeatures):
    # 		status, mean, std = normalize(return_inputs[:,i])
    # 		if status is None:
    # 			log_message += "Can't normalize %d column\n." % (i)
    # 			return retErr
    # 		return_mean[i] = mean
    # 		return_std[i] = std
    # else:
    # 	log_message += "Normalization skipped.\n"
    # 	return_mean = None
    # 	return_std = None

    params['normalization'] = {'mean': return_mean, 'std': return_std}

    return_value = {
        'inputs': return_inputs,
        'labels': return_labels,
        'profit': return_profit,
        'custom_out': return_custom_out,
        'time': return_dtm,
        'open': return_op,
        'num_samples': num_samples,
        'num_features': num_features,
        'num_labels': num_labels,
        'mean': return_mean,
        'std': return_std,
        'rate_indexes': return_rate_indexes
    }

    return return_value


# end of def prepareData


def normalize(x, meanX=None, stdX=None, normInterval=[0, -1]):
    if meanX is None:
        if normInterval[1] == -1:
            meanX = np.mean(x)
        else:
            meanX = np.mean(x[normInterval[0]:normInterval[1]])
    if stdX is None:
        if normInterval[1] == -1:
            stdX = np.std(x)
        else:
            stdX = np.std(x[normInterval[0]:normInterval[1]])
    lenX = len(x)
    if lenX == 0:
        return None, None, None
    if not (stdX > 0.0):
        meanX = 1
        for i in range(lenX):
            x[i] = 1
    else:
        for i in range(lenX):
            x[i] = (x[i] - meanX) / stdX
    return lenX, meanX, stdX


# end of normalize


def count_labels(labels):
    shape = np.shape(labels)
    if len(shape) == 2:  # One-hot
        rows, cols = shape
        labelsCounter = np.zeros(shape=[cols])
        for i in range(rows):
            for j in range(cols):
                if labels[i][j] == 1:
                    labelsCounter[j] += 1
        return labelsCounter
    else:  # Not one-hot
        rows = shape[0]
        maxLabel = int(np.max(labels))
        labelsCounter = []
        for i in range(maxLabel + 1):
            labelsCounter.append(0)
        for i in range(rows):
            labelsCounter[int(labels[i])] += 1
        return labelsCounter


# end of def
