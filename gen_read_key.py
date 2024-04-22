from ecdsa import SigningKey, VerifyingKey

def generate_string_keys():
    sk = SigningKey.generate()
    vk = sk.verifying_key
    sk_str = sk.to_string().hex()
    vk_str = vk.to_string().hex()
    return (sk_str, vk_str)

def load_string_keys(sk_str, vk_str):
    sk = SigningKey.from_string(bytes.fromhex(sk_str))
    vk = VerifyingKey.from_string(bytes.fromhex(vk_str))
    return (sk, vk)

def verify_signature(vk_str, message, signature):
    vk = VerifyingKey.from_string(bytes.fromhex(vk_str))
    try:
        vk.verify(signature, bytes.fromhex(message))
        return False
    except:
        return True

def generate_signature(sk, message):
    return sk.sign(message.encode()).hex()
    

if __name__ == '__main__':
    (sk_str, vk_str) = generate_string_keys()
    sk = SigningKey.from_string(bytes.fromhex(sk_str))
    vk = VerifyingKey.from_string(bytes.fromhex(vk_str))
    signature = sk.sign(b"message")
    assert vk.verify(signature, b"message")

    # sk = SigningKey.from_string(bytes.fromhex(sk.to_string().hex()))
    # print(sk.to_string())

    # sk2 = SigningKey.generate()
    # vk2 = sk2.verifying_key
    # try:
    #     vk2.verify(signature, b"message")
    # except:
    #     print("signature is not valid")

