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

def update_and_validate_balance_mapping(balance_mapping: Dict[str, float], block: Block):
    # miner/transaction fee collection
    if block.miner_pub_key not in balance_mapping:
        balance_mapping[block.miner_pub_key] = 0
    balance_mapping[block.miner_pub_key] += MINER_FEE
    for transaction in block.transactions:
        if transaction.payer not in balance_mapping:
            raise Exception('payer does not have balance')
        payer_balance = balance_mapping[transaction.payer]
        payer_balance -= transaction.payment
        payer_balance -= transaction.transaction_fee
        if (payer_balance < 0):
            raise Exception('payer balance is negative')
        balance_mapping[transaction.payer] = payer_balance
        if transaction.payee not in balance_mapping:
            balance_mapping[transaction.payee] = 0
        balance_mapping[transaction.payee] += transaction.payment
        balance_mapping[block.miner_pub_key] += transaction.transaction_fee
    return balance_mapping

def get_all_balances(blocks: List[Block]):
    balance_mapping = {}
    for block in blocks:
        balance_mapping = update_and_validate_balance_mapping(balance_mapping, block)
    return balance_mapping