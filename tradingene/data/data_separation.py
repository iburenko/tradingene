import numpy as np


def separate_data(data, split, calculate_input, calculate_output, lookback,
                  lookforward, bootstrap):
    data = data[::-1]
    data = data.to_records()
    split_data = dict()
    input_parameters = np.empty((0, 0))
    output_parameters = np.empty((0, 0))
    output_timelimits = np.empty(
        (0, 2), dtype=int
    )  # For each output stores starting and ending indexes of candles involved.
    out_len = -1  # Stores the shape of output
    inp_len = -1  # Stores the shape of input
    for i in range(lookback, len(data) - lookforward - 1):
        inp = np.array([calculate_input(data[i - lookback:i + 1][::-1])])
        if inp is None:
            continue
        out = calculate_output(data[i:i + lookforward + 1])
        if out is None:
            continue
        # SH
        if bootstrap > 0:  # If bootstrapping is required...
            if isinstance(
                    out, tuple
            ):  # Tuple data type assumes an output having it's ending candle index at the end of the tuple.
                ending_candle_index = out[-1] + i  # The ending candle (the starting one is "i")
                output_timelimits = np.append(
                    output_timelimits, [[i - lookback, ending_candle_index]],
                    axis=0)  # Appending time span for a current output
                out = np.array([
                    out[:-1]
                ])  # The tuple without ending candle index serves as output
            else:  # Time span used to calculate output always equals the "lookforward"
                output_timelimits = np.append(
                    output_timelimits, [[i - lookback, i + lookforward]],
                    axis=0)  # Appending time span for a current output
                out = np.array([out])
        else:  # Nothing more than an "ordinary" output
            out = np.array([out])
        if out_len == -1:
            out_len = out.shape[-1]
        if inp_len == -1:
            inp_len = inp.shape[-1]
        input_parameters = np.append(input_parameters, inp)
        output_parameters = np.append(output_parameters, out)
    if out_len == -1:  # If no output has been received or parsed...
        return None  # ... leaving the function then.

    input_overall_len = len(input_parameters)
    input_parameters = np.reshape(input_parameters,
                                  (input_overall_len // inp_len, inp_len))
    output_overall_len = len(output_parameters)
    output_parameters = np.reshape(output_parameters,
                                   (output_overall_len // out_len, out_len))

    # SH START
    if np.shape(
            output_timelimits
    )[0] > 0 and bootstrap > 0:  # If time limits for output has been initialized - bootstrapping...

        import random
        from datetime import datetime
        random.seed(datetime.now())

        samples_num = np.shape(output_timelimits)[
            0]  # The total number of samples
        samples_drawn = np.zeros(
            samples_num, dtype=bool
        )  # To remember samples have been drawn and those that haven't
        indexes = np.arange(0, samples_num)  # An array of indexes to draw from
        probabilities = [
            1.0 / samples_num for i in range(samples_num)
        ]  # Assigning each sample the same probability to be drawn.

        #samples_to_draw_num = samples_num // (lookback+lookforward)//2 # The number of samples to draw from original sample set. It's 100% of the samples for now.
        samples_to_draw_num = samples_num // 3
        sample_indexes_drawn = np.full(
            samples_to_draw_num, -1)  # To store indexes of samples drawn.

        for samples_to_draw_counter in range(samples_to_draw_num):
            if (bootstrap == 2):  # If bootstrapping with probabilities update
                index = np.random.choice(indexes, 1,
                                         probabilities)  # Choosing a sample.
            else:
                index = random.randint(0, samples_num - 1)
            samples_drawn[index] = True  # To let us know it's chosen.
            sample_indexes_drawn[
                samples_to_draw_counter] = index  # Saving the index of a yet another sample drawn.

            # Updating probabilities
            if bootstrap == 2:
                uniquenesses = np.ones(
                    samples_num
                )  # An array to store uniqueness of each sample output
                for samples_counter in range(
                        samples_num):  # For each sample...
                    starting_candle_index = output_timelimits[samples_counter][
                        0]
                    ending_candle_index = output_timelimits[samples_counter][1]

                    overlaps_sum = 0.0
                    overlaps_num = 0
                    for t in range(
                            starting_candle_index, ending_candle_index + 1
                    ):  # For each t in the output interval of a current sample...
                        overlaps = 0
                        for i in range(
                                samples_num
                        ):  # Calculating overlaps with sample 'i' at time 't'
                            if not samples_drawn[i]:  # If a sample hasn't been drawn yet - passing it
                                continue
                            if output_timelimits[i][0] <= t and output_timelimits[i][1] >= t:  # If overlapping found...
                                overlaps += 1  # ...taking it into account.
                        overlaps_sum += 1.0 / (1.0 + overlaps)
                        overlaps_num += 1
                    uniquenesses[
                        samples_counter] = overlaps_sum / overlaps_num  # Average uniqueness of output along all it's "t"s
                sum_of_uniquenesses = np.sum(uniquenesses)  # The overall
                for samples_counter in range(samples_num):
                    probabilities[
                        samples_counter] = uniquenesses[samples_counter] / sum_of_uniquenesses  # Updating probability for each sample output
            # End of updating probabilities

        bootstrapped_input = np.empty(
            (0, inp_len))  # New bootstrapped arrays for inputs
        bootstrapped_output = np.empty((0, out_len))  # and outputs
        for samples_to_draw_counter in range(
                samples_to_draw_num):  # Initializing...
            index = sample_indexes_drawn[samples_to_draw_counter]
            bootstrapped_input = np.append(
                bootstrapped_input, [input_parameters[index]], axis=0)
            bootstrapped_output = np.append(
                bootstrapped_output, [output_parameters[index]], axis=0)
        input_parameters = bootstrapped_input  # From now on we deal with the bootstrapped inputs
        output_parameters = bootstrapped_output  # and outputs.

        # FOR DEBUGGING PURPOSES ONLY. TO BE DELETED LATER!
        # overlap = 0
        # for samples_to_draw_counter in range(samples_to_draw_num):
        # 	for samples_to_draw_counter2 in range(samples_to_draw_counter+1,samples_to_draw_num):
        # 		index1 = sample_indexes_drawn[samples_to_draw_counter]
        # 		index2 = sample_indexes_drawn[samples_to_draw_counter2]
        # 		l1 = output_timelimits[index1][0]
        # 		r1 = output_timelimits[index1][1]
        # 		l2 = output_timelimits[index2][0]
        # 		r2 = output_timelimits[index2][1]
        # 		if l1 > l2 and l1 < r2:
        # 			if r1 < r2:
        # 				overlap += r1 - l1
        # 			else:
        # 				overlap += r2 - l1
        # 		elif l2 > l1 and l2 < r1:
        # 			if r2 < r1:
        # 				overlap += r2 - l2
        # 			else:
        # 				overlap += r1 - l2

        # num_candles_to_cover = len(data)
        # candles_covered = np.zeros( num_candles_to_cover, dtype=int)
        # for samples_to_draw_counter in range(samples_to_draw_num):
        # 	index = sample_indexes_drawn[samples_to_draw_counter]
        # 	l = output_timelimits[index][0]
        # 	r = output_timelimits[index][1]
        # 	for counter in range(r-l+1):
        # 		candles_covered[counter+l] = 1
        # num_covered = 0
        # for counter in range(num_candles_to_cover):
        # 	if candles_covered[counter] == 1:
        # 		num_covered += 1
        # input("")
        # END OF "FOR DEBUGGING PURPOSES ONLY. TO BE DELETED LATER!"

    if len(split) == 2:
        train_len = input_parameters.shape[0] * split[0] // 100
        split_data['train_input'] = input_parameters[1:train_len]
        split_data['train_output'] = output_parameters[1:train_len]
        split_data['test_input'] = input_parameters[train_len:]
        split_data['test_output'] = output_parameters[train_len:]
    elif len(split) == 3:
        train_len = input_parameters.shape[0] * split[0] // 100
        validation_len = input_parameters.shape[0] * split[1] // 100
        split_data['train_input'] = input_parameters[0:train_len]
        split_data['train_output'] = output_parameters[0:train_len]
        split_data['validation_input'] = input_parameters[train_len:train_len +
                                                          validation_len]
        split_data['validation_output'] = output_parameters[
            train_len:train_len + validation_len]
        split_data['test_input'] = input_parameters[train_len +
                                                    validation_len:]
        split_data['test_output'] = output_parameters[train_len +
                                                      validation_len:]
    return split_data
