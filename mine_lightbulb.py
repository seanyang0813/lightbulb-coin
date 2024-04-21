import hashlib
import binascii
from bitstring import BitArray

match_length = 8
match_binary = [0] * match_length # Uses a simple binary


def is_next_block(message):
    res = BitArray(hex=message.hexdigest())
    check = res[0:match_length] ^ BitArray(match_binary)
    is_next_block = True
    for i in range(match_length):
        if (check[i]):
            is_next_block = False
            break
    return is_next_block


# mine assuming that the new block is valid
def mine_lightbulb_coin(prev_block, new_block):
    base_message = prev_block + new_block #Join the strings
    mined_hash = 0
    message_binary = base_message.encode()
    # next block is valid only if the hash's first bits match the 'match binary'
    while (not is_next_block(hashlib.md5(binascii.hexlify(message_binary + str(mined_hash).encode())))):
        mined_hash += 1
    return mined_hash

print(mine_lightbulb_coin('', 'Test ledger'))