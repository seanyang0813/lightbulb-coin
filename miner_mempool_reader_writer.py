from blocks_reader import SignedTransaction

def read_mempool():
    # read from mempool/mempool.txt
    open('mempool/mempool.txt', 'r')
    # build transactions list from the file
    transactions = []
    for line in open('mempool/mempool.txt', 'r'):
        transactions.append(SignedTransaction.parse_transaction_line(line))
    return transactions
def main():
    # read
    transactions = read_mempool()
    for t in transactions:
        print(t)

if __name__ == '__main__':
    main()