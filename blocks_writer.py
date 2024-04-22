import binascii
import hashlib
import blocks_reader
import datetime
from ecdsa import SigningKey

class BlockWriter:
    def __init__(self, block, prev_block):
        self.block = block
        # create header
        self.header = hashlib.md5(binascii.hexlify(prev_block.encode()))

    def create_transaction(self, sk1, pk1, pk2, payment, transaction_fee):
        uid = datetime.time
        transaction = blocks_reader.Transaction(uid, pk1, pk2, payment, transaction_fee)
        signature = sk1.sign(str(transaction).encode('utf-8'))
        self.signed_transaction = blocks_reader.SignedTransaction(uid, pk1, pk2, payment, transaction_fee, signature)
        