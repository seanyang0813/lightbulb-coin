from blocks_reader import read_blocks
from balance_mapping import get_balance
if __name__ == '__main__':
    blocks = read_blocks('sample-blocks.txt')
    for block in blocks:
        print(block)
    print(get_balance('PK2', blocks))
    