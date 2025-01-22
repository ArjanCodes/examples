# Bragir
![Authors](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/themes/2149113237/settings_images/4adb13d-824c-454-a5c-72b2c6f06e1_Arjan_Codes_-_FInal_Files.png)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Description

The bragir CLI is a command-line application built using Click. Its primary purpose is to handle and generate SubRip Subtitle (SRT) files using ChatGPT and Whisper from Openai.

## Features

- **Translation:** Translate the content of SRT files from one language to another using ChatGPT.
- **Transcription:** Trancribe the content of video and audio files from one language to another using Whisper.
- **Batch Processing:** Process a single file, multiple files, or an entire directory, providing flexibility and efficiency.
- **Easy-to-Use Interface:** Utilize a user-friendly command-line interface powered by Click, making translation tasks straightforward.

## Table of Contents

- [Bragir](#bragir)
  - [Description](#description)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [As a package](#as-a-package)
    - [Brew](#brew)
    - [OpenAI](#openai)
    - [Bragir](#bragir-1)
- [Usage](#usage)
    - [Examples](#examples)
- [Contributing](#contributing)
- [Commit Message Structure](#commit-message-structure)
  - [Example Commit Messages](#example-commit-messages)
- [License](#license)

## Installation

In order to use the full potential of Bragir, FFmpeg is needed to be installed on the system and you need to obtain an Openai key.

### As a package
```zsh
pip install bragir
```

### Brew
**NOTE:** Currently bragir is not available on the homebrew-core repo, so you will need to tap our custom [ArjanCodes repo](https://github.com/ArjanCodes/homebrew-core)

```zsh
brew tap arjancodes/core
```

Then, you can run the following command:

```zsh
brew update && brew install bragir
```

### OpenAI

Currently, this tool relise on OpenAIs API. That means that an OpenAI api-key is crucial. See the following resource of [how to get an OpenAI api-key](https://platform.openai.com/docs/quickstart?context=python)

### Bragir
Use pip to install Bragir
```bash
pip install bragir
```

Check if installation is complete

```
bragir --version
```
If a version is displayed, then Bragir is installed correctly.


# Usage

Bragir comes with two commands, transcribe and translate. Transcribe will always generate an file with extension `.srt`. The translate command has only been tested with SRT-files, however other files would work. However, Bragir is not intended to translate other file types  

In order to use bragir, the api key can be loaded into the session or saved in the config.ini file (Default at `~/.bragir/cli/config.ini`).

Load Openai key as an enviroment variable into current session
```
export OPENAI_KEY=<VALUE>
```

### Examples
Translate a single file to one language:

```
bragir translate <FILE_PATH> --language French
```

Translate one file to multiple languages:

```
bragir translate <FILE_PATH> --language French --language German
```

Translate files in a directory to multiple languages:

```
bragir translate <DIRECTORY_PATH> --language French --language German
```

Transcribe file:

```
bragir transcribe <FILE_PATH>
```

Transcribe files in a directory:

```
bragir transcribe <DIRECTORY_PATH>
```

# Contributing
If you want to contribute to this project, please use the following steps:

1. Fork the project.
2. Create a new branch (git checkout -b feature/awesome-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/awesome-feature).
5. Open a pull request.

# Commit Message Structure

This projects aims to follow the [Conventional Commits](https*://www.conventionalcommits.org/en/v1.0.0/#summary) guidelines.

When writing commit messages, use one of the following categories to clearly describe the purpose of your commit:

- **feat** / **feature**: ✨  Introducing new features
- **fix** / **bugfix**: 🐛  Addressing bug fixes
- **perf**: 🚀  Enhancing performance
- **refactor**: 🔄  Refactoring code - **Not displayed in CHANGELOG**
- **test** / **tests**: ✅  Adding or updating tests - **Not displayed in CHANGELOG**
- **build** / **ci**: 🛠️  Build system or CI/CD updates - **Not displayed in CHANGELOG**
- **doc** / **docs**: 📚  Documentation changes - **Not displayed in CHANGELOG**
- **style**: 🎨  Code style or formatting changes - **Not displayed in CHANGELOG**
- **chore**: 🔧  Miscellaneous chores
- **other**: 🌟  Other significant changes

## Example Commit Messages

- `feat: Add cool new feature`
- `fix: Resolve unexpected behavior with translation`

# License
This project is licensed under the MIT License.