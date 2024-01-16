import re


def split_into_sentences(text: str) -> list[str]:
    # Regular expression to match sentence endings
    pattern = r"(?<=[.!?])\s+"
    sentences = re.split(pattern, text)
    return sentences


def concatenate_sentences(sentences: list[str], limit: int) -> list[str]:
    concatenated_sentences: list[str] = []
    tmp: list[str] = []
    tot_length: int = 0
    for sentence in sentences:
        tmp.append(sentence)
        tot_length += len(sentence)
        if tot_length >= limit:
            extra_sentence = tmp.pop()
            text = "".join(tmp)
            concatenated_sentences.append(text)
            tmp=[extra_sentence]

    return concatenated_sentences


def split_query_into_parts(query: str, limit: int) -> list[str]:
    sentences = split_into_sentences(query)

    return concatenate_sentences(sentences, limit)
