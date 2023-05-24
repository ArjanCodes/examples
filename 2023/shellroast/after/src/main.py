"""
Author: Hossin azmoud (Moody0101)
Date: 10/18/2022
LICENCE: MIT
Language: Python3.10
"""

from time import sleep

from colorama import Fore as f
from shell.api import (
    decode,
    decoding_algos,
    encode,
    encoding_algos,
    has_decoding_algo,
    has_encoding_algo,
    has_hashing_algo,
    hash_val,
    hashing_algos,
)
from shell.core import add_command, run_shell

STARTUP_DOC = f"""{f.YELLOW}
    Author: Hossin azmoud (Moody0101)
    Date: 10/18/2022
    LICENCE: MIT
    Language: {f.CYAN}Python3.10{f.YELLOW}
    Description: A tool to hash, encode, decode text
    Commands: hash, encode, decode, help, exit
"""

ENCODING_DOC = f"""
    Syntax: Encode <InputText> < {" | ".join(encoding_algos())} >
"""

DECODING_DOC = f"""
    Syntax: Decode <InputText> < {" | ".join(decoding_algos())} >
"""

HASHING_DOC = f"""
    Syntax: Hash <InputText> < {" | ".join(hashing_algos())} >
"""

HELP_DOC = """
    Usage:
		To encode/Decode:
			Encode/Decode <Text> <Algorithm>
			Encode/Decode only for help.
		To hash:
			Hash <Text> <Algorithm>
			Hash only for help.
"""


def exit_shell(_: list[str]) -> None:
    for i in [".", "..", "..."]:
        print(f"  Exiting{i}", end="\r")
        sleep(1)
    exit(0)


def help_shell(_: list[str]) -> None:
    print(HELP_DOC)


def process_hash(args: list[str]) -> None:
    if len(args) != 2:
        print(HASHING_DOC)
        return
    [text, hashing_algo] = args
    if not has_hashing_algo(hashing_algo):
        print(f"Unknown algorithm name: {hashing_algo}.")
        print(HASHING_DOC)
        return
    hashed_text = hash_val(text, hashing_algo)
    print(hashed_text)


def process_decode(args: list[str]) -> None:
    if len(args) != 2:
        print(DECODING_DOC)
        return
    [text, decoder_algo] = args
    if not has_decoding_algo(decoder_algo):
        print(f"Unknown algorithm name: {decoder_algo}.")
        print(DECODING_DOC)
        return
    decoded_text = decode(text, decoder_algo)
    print(decoded_text)


def process_encode(args: list[str]) -> None:
    if len(args) != 2:
        print(ENCODING_DOC)
        return
    [text, encoder_algo] = args
    if not has_encoding_algo(encoder_algo):
        print(f"Unknown algorithm name: {encoder_algo}.")
        print(ENCODING_DOC)
        return
    encoded_text = encode(text, encoder_algo)
    print(encoded_text)


def main() -> None:
    add_command("exit", exit_shell)
    add_command("help", help_shell)
    add_command("hash", process_hash)
    add_command("encode", process_encode)
    add_command("decode", process_decode)

    print(STARTUP_DOC)
    run_shell()


if __name__ == "__main__":
    main()
