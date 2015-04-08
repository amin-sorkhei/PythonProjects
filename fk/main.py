import itertools


def merge(list_of_items):
    result = []
    for i in xrange(len(list_of_items) - 1):
        j = i + 1
        while list_of_items[i][:-1] == list_of_items[j][:-1]:
                result.append(list_of_items[i][:-1] + list(list_of_items[i][-1]) + list(list_of_items[j][-1]))
                j += 1
    return result


def support_count(list_of_items, transactions, threshold):
    result = []
    for item in list_of_items:
        count = 0
        for transaction in transactions:
            if set(item) <= set(transaction):
                    count += 1
        support = float(count) / len(transactions)
        print str(item) + ' ' + str(support)
        if support >= threshold:
            result.append(item)

    for item in result:
        if type(item) == list:
            item.sort()
    result.sort()
    return result


def main():
    transactions = []
    for line in open('in.txt', 'r').readlines():
        transactions.append([wrd.strip() for wrd in line.split()])

    items = ['T', 'W', 'H', 'I', 'P', 'E', 'O']
    items.sort()
    candidates = support_count(items, transactions, 0.6)
    candidates = map(list, list(itertools.combinations(candidates, 2)))
    print candidates
    final_items = candidates
    while candidates:
        candidates = support_count(candidates, transactions, 0.6)
        if not candidates:
            break
        print 'this is candidates after support ' + str(candidates)
        candidates = merge(candidates)
        print 'this is the current candidate: ' + str(candidates)
    print 'this is the final answer ' + str(final_items)

if __name__ == '__main__':
    main()
