__author__ = 'sorkhei'

import scipy as sp
import matplotlib.pyplot as plt

def error(f, x, y):
    return sp.sum((f(x) - y) ** 2)


def main():
    data = sp.genfromtxt('./data/web_traffic.tsv', delimiter='\t')
    x = data[:, 0]
    y = data[:, 1]
    x = x[~sp.isnan(y)]
    y = y[~sp.isnan(y)]
    fp1 = sp.polyfit(x, y, 1)
    print('Model parameters for fp1 %s' % fp1)
    f1 = sp.poly1d(fp1)
    print('This is the error rate for fp1 %f' % error(f1, x, y))

    fp2 = sp.polyfit(x, y, 2)
    print('Model parameters for fp2 %s' % fp2)
    f2 = sp.poly1d(fp2)
    print('This is the error rate for fp2 %f' % error(f2, x, y))

    plt.scatter(x, y,color= 'pink')
    plt.title('My first impression')
    plt.xlabel('Time')
    plt.ylabel('#Hits')
    plt.xticks([w * 7 * 24 for w in range(10)], ['week %i' % w for w in range(10)])
    fx = sp.linspace(0, x[-1], 1000)
    plt.plot(fx, f1(fx), linewidth=3,color='cyan')


    plt.plot(fx, f2(fx), linewidth=3, linestyle='--',color= 'red')
    plt.legend(['d = %i' %f1.order, 'd = %i' %f2.order], loc='upper left')
    plt.autoscale(tight=True)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
