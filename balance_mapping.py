from typing import Dict, List
from blocks_reader import Block, Transaction
from consts import MINER_FEE

def get_balance(pub_key: str, blocks: List[Block]):
    balance = 0
    # miner/transaction fee collection
    for block in blocks:
        if block.miner_pub_key == pub_key:
            balance += MINER_FEE
            for transaction in block.transactions:
                balance += transaction.transaction_fee
    # payer and payee transactions
    for block in blocks:
        for transaction in block.transactions:
            if transaction.payer == pub_key:
                balance -= transaction.payment
                balance -= transaction.transaction_fee
            if transaction.payee == pub_key:
                balance += transaction.payment
    return balance