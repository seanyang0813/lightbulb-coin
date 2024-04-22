import sys
import os 
from gen_read_key import load_string_keys
from miner_mempool_reader_writer import read_mempool
from blocks_reader import read_blocks
from balance_mapping import  get_all_balances
from gen_read_key import verify_signature

# get the copy of the blocks 

def check_transaction_is_valid(balance_mapping, blocks, transaction, payer):
    # check if the user has enough balance to support both payment and transaction fee
    if (payer not in balance_mapping):
        return False
    payer_balance = balance_mapping[payer]
    if (payer_balance < transaction.payment + transaction.transaction_fee):
        return False
    # check for the signature is good
    if verify_signature(payer, transaction) == False:
        return False
    # check if the transaction already exists in the block chain
    for block in blocks:
        for b_transaction in block.transactions:
            if b_transaction.signature == transaction.signature:
                return False
    return True
def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        if not os.path.exists(file_name):
            print(f'{file_name} does not exist')
            exit()
        else:
            credentials = open(file_name, 'r')
            public_key = credentials.readline()
            private_key = credentials.readline()
            (private_key, public_key) = load_string_keys(private_key, public_key)
            print("loaded credentials from file: " + file_name)
            print(f'public key: {public_key.to_string().hex()}')
    else:
        print("You need to provide a file with your credentials")
        exit()
    
    # load the longest chain fro m the blocs_tracker folder
    # open directory and find the file with the highest block height
    files = os.listdir('blocks_tracker')
    highest_block_height = 0
    file_to_use = None
    for file_name in files:
        # check the file length
        num_lines = len(open('blocks_tracker/' + file_name, 'r').readlines())
        if num_lines > highest_block_height or file_to_use == None:
            highest_block_height = num_lines
            # get the file name
            file_to_use = file_name
        
    if (file_to_use == None):
        print("no blocks historyfound")
        exit()
    
    # open the file with the highest block height
    file = 'blocks_tracker/' + file_to_use
    print("using file: " + file)
    blocks = read_blocks(file)
    print(blocks)

    balance_mapping = get_all_balances(blocks)
    
    # pull from mempool
    while True:
        transactions = read_mempool()
        print("mempool: ", transactions)
        transactions.sort()
        good_transactions = []
        for transaction in transactions:
            if check_transaction_is_valid(balance_mapping, blocks, transaction, transaction.payer):
                good_transactions.append(transaction)
        print("good transactions: ", good_transactions)





if __name__ == '__main__':
    main()