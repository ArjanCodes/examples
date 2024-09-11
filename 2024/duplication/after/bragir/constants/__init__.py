# Constants for file operations

# List of files to be ignored during processing
BLACKLISTED_FILES = [".DS_Store"]

# Maximum number of tokens for transcription
TOKEN_LIMIT = 1500

# Bitrates in kbps for different audio file formats
BITRATES_KBPS = {
    "mp3": [128, 192, 256, 320],
    "mp4": [96, 128, 160, 192, 256, 320],
    "mpeg": [1000, 1500, 3000, 4000, 10000],
    "mpga": [96, 128, 160, 192, 256, 320],
    "m4a": [128, 160, 192, 256, 320],
    "wav": [1410, 2820],
    "webm": [500, 1000, 1500, 3000, 4000, 10000],
}

# Duration in seconds for a 25MB file with the highest possible kbps for different audio file formats
DURATION_SECONDS_25MB = {
    "mp3": 640.0,
    "mp4": 640.4,
    "mpeg": 2.5,
    "mpga": 2.5,
    "m4a": 320.0,
    "wav": 8.0,
    "webm": 2.5,
}
