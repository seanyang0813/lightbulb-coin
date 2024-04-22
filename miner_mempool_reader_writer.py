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
    transactions_to_remove = [transactions[1]]
    remove_finished_transactions_from_mempool(transactions_to_remove)

def remove_finished_transactions_from_mempool(transactions_list):
    # remove transactions that are finished from mempool
    signature_to_remove_set = set()
    for transaction in transactions_list:
        signature_to_remove_set.add(transaction.sig1)
    # open mempool txt 
    with open('mempool/mempool.txt', 'r') as file:
        lines = file.readlines()
        # Filter lines; keep lines that do not start with '1'
        filtered_lines = [line for line in lines if not line.split(' ')[-1] not in signature_to_remove_set]
        # Write the filtered lines back to the file
        with open('mempool/mempool.txt', 'w') as file:
            file.writelines(filtered_lines)





if __name__ == '__main__':
    main()