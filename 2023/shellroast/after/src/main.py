"""
Author: Hossin azmoud (Moody0101)
Date: 10/18/2022
LICENCE: MIT
Language: Python3.10
"""

from time import sleep

from colorama import Fore as f
from UtilPackage.Algorithms import ENCODING, HASHING
from UtilPackage.EncodingApi import DECODE, ENCODE, EncodingManager
from UtilPackage.Shell import shell_input

DOC = f"""{f.YELLOW}
	Author: Hossin azmoud (Moody0101)
	Date: 10/18/2022
	LICENCE: MIT
	Language: {f.CYAN}Python3.10 {f.YELLOW}
	Description: A tool to hash, encode, decode text
	Commands: hash, encode, decode, help, exit
"""


def exit_shell(_: list[str]) -> None:
    for i in [".", "..", "..."]:
        print(f"  Exiting{i}", end="\r")
        sleep(1)
    exit(0)


def help_shell(_: list[str]) -> None:
    print(
        """
	Usage: 
		To encode/Decode:
			Encode/Decode <Text> <Algorithm>
			Encode/Decode only for help.
		To hash:
			Hash <Text> <Algorithm>
			Hash only for help.
		"""
    )


def hash_val(args: list[str]) -> None:
    if len(args) != 2:
        print(HASHING["Doc"])
        return
    [text, hashing_algo] = args
    cleaned_hasher_name = hashing_algo.upper().strip()
    if cleaned_hasher_name not in HASHING:
        print(f"Unknown algorithm name: {hashing_algo}.")
        print(HASHING["Doc"])
        return
    encoded_text = text.encode()
    hashed_text: str = HASHING[cleaned_hasher_name](encoded_text).hexdigest()
    print(hashed_text)


def decode(args: list[str]) -> None:
    if len(args) != 2:
        print(ENCODING["Doc"][DECODE])
        return
    [text, decoder_algo] = args
    cleaned_decoder_name = decoder_algo.upper().strip()
    if cleaned_decoder_name not in ENCODING:
        print(f"Unknown algorithm name: {decoder_algo}.")
        print(ENCODING["Doc"][DECODE])
        return

    # Get Decoder function
    func_ = ENCODING[cleaned_decoder_name][DECODE]
    # Map the value
    decode_fn = EncodingManager(func_, DECODE)
    # return the value
    print(decode_fn(text))


def encode(args: list[str]) -> None:
    if len(args) != 2:
        print(ENCODING["Doc"][ENCODE])
        return
    [text, encoder_algo] = args
    cleaned_encoder_name = encoder_algo.upper().strip()
    if cleaned_encoder_name not in ENCODING:
        print(f"Unknown algorithm name: {encoder_algo}.")
        print(ENCODING["Doc"][ENCODE])
        return

    # Get Encoder function
    func_ = ENCODING[cleaned_encoder_name][ENCODE]
    # Map the value
    encode_fn = EncodingManager(func_, ENCODE)
    # return the value
    print(encode_fn(text))


COMMANDS = {
    "EXIT": exit_shell,
    "HELP": help_shell,
    "HASH": hash_val,
    "DECODE": decode,
    "ENCODE": encode,
}


def execute(command: str, arguments: list[str]) -> None:
    if command in COMMANDS:
        COMMANDS[command](arguments)


def main() -> None:
    print(DOC)
    while True:
        command, arguments = shell_input()
        execute(command, arguments)


if __name__ == "__main__":
    main()
