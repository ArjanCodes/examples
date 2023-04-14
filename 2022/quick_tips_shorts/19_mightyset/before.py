POSITIVE_WORDS = [
    "awesome",
    "great",
    "super",
    "fun",
    "entertaining",
    "cool",
    "adventurous",
    "nice",
]

NEGATIVE_WORDS = [
    "boring",
    "annoying",
    "useless",
    "bad",
    "terrible",
    "gross",
    "stupid",
    "hate",
]


def detect_positive(review: str) -> bool:
    words = review.split()
    count_positive = 0
    count_negative = 0
    for word in words:
        if word in POSITIVE_WORDS:
            count_positive += 1
        if word in NEGATIVE_WORDS:
            count_negative += 1
    return count_positive >= count_negative


def main():
    good_review = "This movie is awesome!"
    print(detect_positive(good_review))
    bad_review = "I hate this movie"
    print(detect_positive(bad_review))


if __name__ == "__main__":
    main()
