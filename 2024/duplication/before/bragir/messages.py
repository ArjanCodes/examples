from bragir.languages import Languages, to_output

PROMPT_HELP = {
    "file": "Path to file",
    "api_key": "Enter valid openai api key",
    "directory": "Enter one directory that contains the files that is going to be translated",
    "language": f"Enter one or more languages {to_output(Languages)}",
    "file_path": "Path to a .srt file in your system",
    "output_path": "Path to where the file should be stored in your system"
}


ACTIONS = {
    "translating": "Translating to following language/languages: {lanugages}",
}
