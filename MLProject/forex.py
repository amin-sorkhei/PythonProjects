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
    return 100*(currentPoint - startPoint)/abs(float(startPoint))


def patternStorage(bid, ask, printDetails= False):
    avgLine = (bid+ask)/2
    x = len(avgLine) - 30
    y = 11
    current_status = 'none'
    while y < x:
        pattern = []
        p1 = percentChange(avgLine[y-10], avgLine[y-9])
        p2 = percentChange(avgLine[y-10], avgLine[y-8])
        p3 = percentChange(avgLine[y-10], avgLine[y-7])
        p4 = percentChange(avgLine[y-10], avgLine[y-6])
        p5 = percentChange(avgLine[y-10], avgLine[y-5])
        p6 = percentChange(avgLine[y-10], avgLine[y-4])
        p7 = percentChange(avgLine[y-10], avgLine[y-3])
        p8 = percentChange(avgLine[y-10], avgLine[y-2])
        p9 = percentChange(avgLine[y-10], avgLine[y-1])
        p10 = percentChange(avgLine[y-10], avgLine[y])

        outcomeRange = avgLine[y+20:y+30]
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
    date = data[data_label]
    rate = data[rate_label]
    ask = data[ask_label]
    bid = data[bid_label]
    plot_rate(date, rate)
    '''date, bid, ask = np.genfromtxt('1d.txt', unpack=True, delimiter=',',
                                   converters={0: mdates.strpdate2num('%Y%m%d%H%M%S')})'''
    # plot(date[0:30], bid[0:30], ask[0:30])
    # patternStorage(bid, ask)
    # print(patternArray[0])
    # print(performanceArray[0])

if __name__ == '__main__':
    main()

