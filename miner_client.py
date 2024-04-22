import sys
import os 
from gen_read_key import load_string_keys
from miner_mempool_reader_writer import read_mempool, remove_finished_transactions_from_mempool
from blocks_reader import read_blocks, Block, SignedTransaction
from balance_mapping import  get_all_balances
import binascii
import hashlib
import mine_lightbulb
from gen_read_key import verify_signature

# get the copy of the blocks 

def check_transaction_is_valid(balance_mapping, blocks, transaction: SignedTransaction, payer):
    # check if the user has enough balance to support both payment and transaction fee
    if (payer not in balance_mapping):
        return False
    payer_balance = balance_mapping[payer]
    if (payer_balance < transaction.payment + transaction.transaction_fee):
        return False
    # check for the signature is good
    if verify_signature(payer, f'{transaction.uid} {transaction.payer} {transaction.payee}  {transaction.payment} {transaction.transaction_fee}', transaction.sig1) == False:
        return False
    # check if the transaction already exists in the block chain
    for block in blocks:
        for b_transaction in block.transactions:
            if b_transaction.sig1 == transaction.sig1:
                return False
    return True

def build_str_for_block_hash(public_key_str, good_transactions):
    new_block_hash_str = public_key_str + "\n"
    for transaction in good_transactions:
        new_block_hash_str += (str(transaction) + "\n")
    print("new block hash: ", new_block_hash_str)
    return new_block_hash_str

def main():
    public_key_str = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        if not os.path.exists(file_name):
            print(f'{file_name} does not exist')
            exit()
        else:
            credentials = open(file_name, 'r')
            public_key = credentials.readline().strip()
            public_key_str = public_key
            private_key = credentials.readline().strip()
            (private_key, public_key) = load_string_keys(private_key, public_key)
            print("loaded credentials from file: " + file_name)
            print(f'public key: {public_key.to_string().hex()}')
    else:
        print("You need to provide a file with your credentials")
        exit()
    

    
    # pull from mempool
    while True:
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
        transactions = read_mempool()
        print("mempool: ", transactions)
        transactions.sort()
        good_transactions = []
        for transaction in transactions:
            if check_transaction_is_valid(balance_mapping, blocks, transaction, transaction.payer):
                good_transactions.append(transaction)
        print("good transactions: ", good_transactions)
        prev_block_hash = blocks[-1].cur_block_hash

        new_block_hash_str = build_str_for_block_hash(public_key_str, good_transactions)
        hash_proof = mine_lightbulb.mine_lightbulb_coin(prev_block_hash, new_block_hash_str)
        print("hash proof: ", hash_proof)
        print("new height is: ", blocks[-1].height + 1)
        new_block = Block(blocks[-1].height + 1, prev_block_hash, hash_proof, public_key_str, len(good_transactions))
        for transaction in good_transactions:
            new_block.add_transaction(transaction)
        # check if block tracker has a file with name that is my public key
        blocks.append(new_block)
        print("made new block: ", new_block)
        if not os.path.exists('blocks_tracker/' + public_key_str + ".txt"):
            # create a new file with the name of the public key
            open('blocks_tracker/' + public_key_str + ".txt", 'w').writelines([x.build_string_for_block() for x in blocks])
        else:
            # open the file with the name of the public key
            file = open('blocks_tracker/' + public_key_str + ".txt", 'w')
            file.writelines([x.build_string_for_block() for x in blocks])
            file.close()
        # once commited remove from mempool
        remove_finished_transactions_from_mempool(good_transactions)

if __name__ == '__main__':
    main()