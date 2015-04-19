import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Quandl


# Contains each pattern the pattern finder restores
patternArray = []
performanceArray = []


def plot(date, bid, ask):
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.subplot2grid((40, 40), (0, 0), rowspan=40, colspan=40)
    ax1.plot(date, bid)
    ax1.plot(date, ask)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('time')
    plt.ylabel('price')
    plt.legend(['bid', 'ask'], loc='upper left')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.subplots_adjust(bottom=0.3)
    plt.grid(True)
    plt.show()


def percentChange(startPoint, currentPoint):
    return 100 * (currentPoint - startPoint) / abs(float(startPoint))


def patternStorage(bid, ask, printDetails=False):
    avgLine = (bid + ask) / 2
    x = len(avgLine) - 30
    y = 11
    current_status = 'none'
    while y < x:
        pattern = []
        p1 = percentChange(avgLine[y - 10], avgLine[y - 9])
        p2 = percentChange(avgLine[y - 10], avgLine[y - 8])
        p3 = percentChange(avgLine[y - 10], avgLine[y - 7])
        p4 = percentChange(avgLine[y - 10], avgLine[y - 6])
        p5 = percentChange(avgLine[y - 10], avgLine[y - 5])
        p6 = percentChange(avgLine[y - 10], avgLine[y - 4])
        p7 = percentChange(avgLine[y - 10], avgLine[y - 3])
        p8 = percentChange(avgLine[y - 10], avgLine[y - 2])
        p9 = percentChange(avgLine[y - 10], avgLine[y - 1])
        p10 = percentChange(avgLine[y - 10], avgLine[y])

        outcomeRange = avgLine[y + 20:y + 30]
        avgOutcome = reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)

        currentPoint = avgLine[y]
        futureOutcome = percentChange(currentPoint, avgOutcome)

        if printDetails:
            print 'where we are historically:', currentPoint
            print 'soft outcome of the horizon:', avgOutcome
            print 'This pattern brings a future change of:', futureOutcome

        pattern.append(p1)
        pattern.append(p2)
        pattern.append(p3)
        pattern.append(p4)
        pattern.append(p5)
        pattern.append(p6)
        pattern.append(p7)
        pattern.append(p8)
        pattern.append(p9)
        pattern.append(p10)

        y += 1

        patternArray.append(pattern)
        performanceArray.append(futureOutcome)


# ----------------------------------------------------------------


def rolling_window(one_dim_data_set, size):
    shape = one_dim_data_set.shape[:-1] + (one_dim_data_set.shape[-1] - size + 1, size)
    strides = one_dim_data_set.strides + (one_dim_data_set.strides[-1],)
    return np.lib.stride_tricks.as_strided(one_dim_data_set, shape=shape, strides=strides)


def instantiation_counter(one_dim_data_set, instantiation):
    one_dim_data_set_slices = rolling_window(one_dim_data_set, len(instantiation))
    return np.sum(True == np.apply_along_axis(np.array_equal, 1, one_dim_data_set_slices, instantiation))


def plot_rate(date, rate):
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.subplot2grid((40, 40), (0, 0), rowspan=40, colspan=40)
    ax1.plot(date, rate, color='blue')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('time', color='blue')
    plt.ylabel('EUR/USD rate', color='blue')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.subplots_adjust(bottom=0.3)
    plt.grid(True)
    plt.show()


def main():
    data = Quandl.get("CURRFX/EURUSD",
                      authtoken="8eLZCik36beb-NpTA_ht",
                      returns='numpy',
                      trim_start='2012-01-1',
                      trim_end='2014-12-31',
                      collapse='daily')

    print 'this is the data that the training set contains ' + str(data.dtype.names)
    data_label, rate_label, ask_label, bid_label = data.dtype.names
    # date = data[data_label]
    rate = data[rate_label]
    # ask = data[ask_label]
    # bid = data[bid_label]



    rate_change = np.zeros(data.size)
    for i in range(1, rate.size):
        if rate[i] >= rate[i - 1]:
            rate_change[i] = True
        else:
            rate_change[i] = False

    training_data = rate_change[0:627]
    test_data = rate_change[627:]

    # print rate_change
    # ------------- Order One Markov Model ------------- #
    order_one_initial_probability = {'True': instantiation_counter(training_data[:-1], [True]),
                                     'False': instantiation_counter(training_data[:-1], [False])}
    print 'First Order Markov Model results :'
    order_one_CPT = {'O_t = True | O_(t-1) = True': float(instantiation_counter(training_data, [True, True]))/ order_one_initial_probability['True'],
                     'O_t = False | O_(t-1) = True': float(instantiation_counter(training_data, [True, False]))/ order_one_initial_probability['True'],
                     'O_t = False | O_(t-1) = False': float(instantiation_counter(training_data, [False, False]))/ order_one_initial_probability['False'],
                     'O_t = True | O_(t-1) = False': float(instantiation_counter(training_data, [False, True]))/ order_one_initial_probability['False']}
    for item in order_one_CPT.items():
        print item
    predicted_y = np.zeros(test_data.size)


if __name__ == '__main__':
    main()

