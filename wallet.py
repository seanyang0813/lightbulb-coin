'''
this is a cli for wallet funcationalities
Get wallet coin or balance of a public key
read public or private key from a file 
generate a new public private key pair into credentials 
submit transaction to the block chain
'''

from blocks_reader import read_blocks
from balance_mapping import get_balance, get_all_balances
import os
import argparse
from Crypto.PublicKey import RSA


def generate_key_pair():
    from Crypto.PublicKey import RSA

def main():
    parser = argparse.ArgumentParser(description = "Your lightcoin wallet")
    parser.add_argument("-c", "--credential", type = str, nargs = 1,
                    metavar = "file_name", default = None,
                    help = "Opens and reads the credentials file")
    args = parser.parse_args()

    if args.credential is not None:
        # geenrate a new rsa key value pair
        credentials = open(args.credential[0], 'r')
        public_key = credentials.readline()
        private_key = credentials.readline()
    else :
        print("generated a new credential for you")



    # check the folder blocks_tracker and read the first file in the list
    if not os.path.exists('blocks_tracker'):
        print("there is not active node")
        exit()
    else :
        # find all files in the folder blocks_tracker
        files = os.listdir('blocks_tracker')
        # read the first file in the list
        file = files[0]
        blocks = read_blocks('blocks_tracker/' + file)
        print(get_balance('PK2', blocks))
        print(get_balance('PK1', blocks))
        print(get_all_balances(blocks))
if __name__ == '__main__':
    main()