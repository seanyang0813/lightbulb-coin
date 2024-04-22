import binascii
import hashlib
import blocks_reader
import datetime
from ecdsa import SigningKey

class BlockWriter:
    def __init__(self, prev_block):
        # create header
        self.header = hashlib.md5(binascii.hexlify(prev_block.encode()))

        
    # Creates the entire block with exception of the mined component
    def create_block(self, signed_transactions):
        self.block = ""
        self.block += self.header
        for transaction in signed_transactions:
            self.block += str(transaction)