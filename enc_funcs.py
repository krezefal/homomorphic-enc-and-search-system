import math

from phe import paillier, encoding


class EncodedNumber(encoding.EncodedNumber):
    BASE = 64
    LOG2_BASE = math.log(BASE, 2)


class BytesIntEncoder:

    @staticmethod
    def encode(b: bytes) -> int:
        return int.from_bytes(b, byteorder='big')

    @staticmethod
    def decode(i: int) -> bytes:
        return i.to_bytes(((i.bit_length() + 7) // 8), byteorder='big')


def generate_keypair():
    return paillier.generate_paillier_keypair()


def encode_and_encrypt(number, public_key):
    encoded = EncodedNumber.encode(public_key, number)
    encrypted = public_key.encrypt(encoded)
    return encrypted


def decode_and_decrypt(number, private_key):
    decrypted_but_encoded = \
        private_key.decrypt_encoded(number, EncodedNumber)
    return decrypted_but_encoded.decode()


def calc_difference(x, y):
    encrypted_c = x - y
    return encrypted_c
