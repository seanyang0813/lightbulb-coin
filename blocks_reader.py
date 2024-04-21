'''
sample block format 
Block height starting from 0
Hash of previous block
Hash of the current block
Miner public key hash mined
trasnactions count: 1
UID PK1 gives PK2 payment transaction_fee sig1 


'''

class Transaction:
    def __init__(self, uid, pk1, pk2, payment, transaction_fee):
        self.uid = uid
        self.payer = pk1
        self.payee = pk2
        self.payment = payment
        self.transaction_fee = transaction_fee

    def __str__(self):
        return f'Transaction uid: {self.uid}, from: {self.payer}, to: {self.payee}, payment: {self.payment}, transaction_fee: {self.transaction_fee} \n'

class SignedTransaction(Transaction):
    def __init__(self, uid, pk1, pk2, payment, transaction_fee, sig1):
        Transaction.__init__(uid, pk1, pk2, payment, transaction_fee)
        self.sig1 = sig1

    def __str__(self):
        return f'{Transaction.__str__()}, sig1: {self.sig1} \n'

    def parse_transaction_line(line):
        line = line.split(' ')
        uid = line[0]
        payer = line[1]
        payee = line[2]
        payment = float(line[3])
        transaction_fee = float(line[4])
        sig1 = line[5]
        return SignedTransaction(uid, payer, payee, payment, transaction_fee, sig1)

class Block:
    def __init__(self, height, prev_block_hash, cur_block_hash, miner_pub_key, tx_count):
        self.height = height
        self.prev_block_hash = prev_block_hash
        self.cur_block_hash = cur_block_hash
        self.miner_pub_key = miner_pub_key
        self.tx_count = tx_count
        self.transactions = []
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        res = f'Block height: {self.height}, prev_block_hash: {self.prev_block_hash}, cur_block_hash: {self.cur_block_hash}, miner_pub_key: {self.miner_pub_key}, tx_count: {self.tx_count}'
        res += '\nTransactions:\n'
        for transaction in self.transactions:
            res += transaction.__str__()
        return res


def read_blocks(file):
    blocks = []
    with open(file, 'r') as f:
        lines_list = f.read().splitlines()
        index = 0
        if len(lines_list) == 0:
            return
        while index < len(lines_list):
            (index,block) = read_block(lines_list, index)
            blocks.append(block)
            index += 1
    return blocks
            
            
def read_block(lines_list, index):
    block = Block(int(lines_list[index]), lines_list[index + 1], lines_list[index + 2], lines_list[index + 3], int(lines_list[index + 4]))
    index += 5
    for i in range(block.tx_count):
        transaction = Transaction.parse_transaction_line(lines_list[index])
        block.add_transaction(transaction)
        index += 1
    return (index, block)


if __name__ == '__main__':
    read_blocks('sample-blocks.txt')