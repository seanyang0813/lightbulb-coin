'''
this is a cli for wallet funcationalities
Get wallet coin or balance of a public key
read public or private key from a file 
generate a new public private key pair into credentials 
submit transaction to the block chain
the public private key pair is always stored with the name being public key and the file containing both public and private key
'''

from blocks_reader import read_blocks, Transaction
from balance_mapping import get_balance, get_all_balances
from gen_read_key import load_string_keys, generate_string_keys, generate_signature
import os
import sys
import uuid

def main():
    public_key = None
    private_key = None
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
    else :
        print("generated a new credential for you")
        (private_key_str, public_key_str) = generate_string_keys()
        print(f'public key: {public_key_str} \nprivate key: {private_key_str}')
        credentials_file = open(f'credentials/{public_key_str}', 'w')
        credentials_file.write(public_key_str)
        credentials_file.write('\n')
        credentials_file.write(private_key_str)
        credentials_file.close()
        (private_key, public_key) = load_string_keys(private_key_str, public_key_str)



    # check the folder blocks_tracker and read the first file in the list
    if not os.path.exists('blocks_tracker'):
        print("there is no active node")
        exit()
    else :
        # find all files in the folder blocks_tracker
        files = os.listdir('blocks_tracker')
        # read the first file in the list
        file = files[0]
        blocks = read_blocks('blocks_tracker/' + file)
        print("your balance is: ", get_balance(public_key.to_string().hex(), blocks))
    while True:
        print("Select the menu options below with the number (ex: 1)")
        print("1. Get current balance")
        print("2. Submit transaction")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("your balance is: ", get_balance(public_key.to_string().hex(), blocks))
        elif choice == 2:
            payee = input("Enter the public key of the person who you want to pay:\n")
            amount = float(input("Enter the amount you want to pay:\n"))
            fee = float(input("Enter the transaction fee (can be 0, the higher fee gets priority):\n"))
            id = uuid.uuid1()
            print(private_key.to_string().hex())
            signature = generate_signature(private_key, f'{id} {public_key.to_string().hex()} {payee}  {amount} {fee}')
            transaction = Transaction(id, public_key.to_string().hex(), payee, amount, fee, signature)
            print(transaction)
            print("Submitted transaction")
        elif choice == 3:
            print("exiting")
            exit()
        else:
            print("invalid choice")

if __name__ == '__main__':
    main()