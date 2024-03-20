import cryptography
from .EncodingApi import (
    EncodingManager,
    ENCODE,
    DECODE,
)  # EncodingManager(Func: callable, s: str | bytes, Op: int)
from .HashingApi import Hasher  # Hasher(HashingFunc: callable, s: str | bytes) -> str:
from binascii import hexlify, unhexlify

from hashlib import (
    blake2b,
    blake2s,
    md5,
    sha1,
    sha224,
    sha256,
    sha384,
    sha3_224,
    sha3_256,
    sha3_384,
    sha3_512,
    sha512,
)
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

Encoding_Algorithms = [
    "aA85",
    "base16",
    "base32",
    "base32hex",
    "base64",
    "base85",
    "hexlify",
]

ENCODING = {
    "A85": [a85encode, a85decode],
    "BASE16": [b16encode, b16decode],
    "BASE32": [b32encode, b32decode],
    "BASE32HEX": [b32hexencode, b32hexdecode],
    "BASE64": [b64encode, b64decode],
    "BASE85": [b85encode, b85decode],
    "HEXLIFY": [hexlify, unhexlify],
    "Doc": [
        f"""
  Syntax: Encode <InputText> < {" | ".join(Encoding_Algorithms)} >
""",
        f"""
  Syntax: Decode <InputText> < {" | ".join(Encoding_Algorithms)} >
""",
    ],
}

Hashing_Algorithms = [
    "blake2s",
    "blake2b",
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "sha512",
]

HASHING = {
    "BLAKE2B": blake2b,
    "BLAKE2S": blake2s,
    "MD5": md5,
    "SHA1": sha1,
    "SHA224": sha224,
    "SHA256": sha256,
    "SHA384": sha384,
    "SHA3_224": sha3_224,
    "SHA3_256": sha3_256,
    "SHA3_384": sha3_384,
    "SHA3_512": sha3_512,
    "SHA512": sha512,
    "Doc": f"""
  Syntax: Hash <InputText> < {" | ".join(Hashing_Algorithms)} >
	""",
}
