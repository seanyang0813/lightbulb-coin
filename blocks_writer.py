import binascii
import hashlib
import blocks_reader
import datetime
from ecdsa import SigningKey

class BlockWriter:
    def __init__(self, prev_block):
        # create header
        self.header = hashlib.md5(binascii.hexlify(prev_block.encode()))

    @staticmethod 
    def create_transaction(sk1, pk1, pk2, payment, transaction_fee):
        uid = datetime.time
        transaction = blocks_reader.Transaction(uid, pk1, pk2, payment, transaction_fee)
        signature = sk1.sign(str(transaction).encode('utf-8'))
        return blocks_reader.SignedTransaction(uid, pk1, pk2, payment, transaction_fee, signature)
        
    # Creates the entire block with exception of the mined component
    def create_block(self, signed_transactions):
        self.block = ""
        self.block += self.header
        for transaction in signed_transactions:
            self.block += str(transaction)