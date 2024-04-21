from blocks_reader import read_blocks
from balance_mapping import get_balance, get_all_balances
if __name__ == '__main__':
    blocks = read_blocks('sample-blocks.txt')
    for block in blocks:
        print(block)
    print(get_balance('PK2', blocks))
    print(get_balance('PK1', blocks))
    print(get_all_balances(blocks))

    blocks = read_blocks('sample-blocks-invalid.txt')
    for block in blocks:
        print(block)
    try:
        print(get_all_balances(blocks))
    except Exception as e:
        print(e)
