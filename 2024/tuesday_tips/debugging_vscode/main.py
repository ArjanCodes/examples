def calculate_average(scores: list[int]):
    return sum(scores) / len(scores)

def process_author_scores(author_name: str, scores: list[int]):
    average_score = calculate_average(scores)
    print(f"Average score for {author_name} is {average_score}")
    return average_score

def main() -> None:
    authors_scores = {
        "George Orwell": [85, 90, 88, 92],
        "Arjan": [92, 94, 88, 90],
        "Jane Austen": [88, 91, 85, 87]
    }

    for author, scores in authors_scores.items():
        process_author_scores(author, scores)

if __name__ == "__main__":
    main()
