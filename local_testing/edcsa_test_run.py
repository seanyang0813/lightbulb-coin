from ecdsa import SigningKey

sk = SigningKey.generate()
vk = sk.verifying_key
signature = sk.sign(b"message")
assert vk.verify(signature, b"message")

sk = SigningKey.from_string(bytes.fromhex(sk.to_string().hex()))
print(sk.to_string())

sk2 = SigningKey.generate()
vk2 = sk2.verifying_key
try:
    vk2.verify(signature, b"message")
except:
    print("signature is not valid")