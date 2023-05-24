from base64 import (
    a85decode,
    a85encode,
    b16decode,
    b16encode,
    b32decode,
    b32encode,
    b32hexdecode,
    b32hexencode,
    b64decode,
    b64encode,
    b85decode,
    b85encode,
)
from binascii import hexlify, unhexlify
from hashlib import (
    blake2b,
    blake2s,
    md5,
    sha1,
    sha3_224,
    sha3_256,
    sha3_384,
    sha3_512,
    sha224,
    sha256,
    sha384,
    sha512,
)

ENCODING_ALGORITHMS = {
    "a85": a85encode,
    "base16": b16encode,
    "base32": b32encode,
    "base32hex": b32hexencode,
    "base64": b64encode,
    "base85": b85encode,
    "hexlify": hexlify,
}

DECODING_ALGORITHMS = {
    "a85": a85decode,
    "base16": b16decode,
    "base32": b32decode,
    "base32hex": b32hexdecode,
    "base64": b64decode,
    "base85": b85decode,
    "hexlify": unhexlify,
}


HASHING_ALGORITHMS = {
    "blake2b": blake2b,
    "blake2s": blake2s,
    "md5": md5,
    "sha1": sha1,
    "sha224": sha224,
    "sha256": sha256,
    "sha384": sha384,
    "sha3_224": sha3_224,
    "sha3_256": sha3_256,
    "sha3_384": sha3_384,
    "sha3_512": sha3_512,
    "sha512": sha512,
}
