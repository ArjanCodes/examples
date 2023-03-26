import csv
from collections import Counter


def cumulative_count(column_name: str, field_sep: str | None = None) -> Counter[str]:
    print(f"--- Analysing frequencies of {column_name} --- ")

    with open("data/survey_results_public.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        counter = Counter()
        for line in csv_reader:
            if field_sep:
                splitted_line = line[column_name].split(field_sep)
                for element in splitted_line:
                    counter[element] += 1
            else:
                counter[line[column_name]] += 1
    return counter


def show_frequencies(counter: Counter[str]) -> None:
    for possibility, freq in counter.most_common():
        print(
            f"{possibility: <36} -> {freq: <5} |",
            f"{round(freq /  counter.total() * 100, 2)}%",
        )
    print("\n")


def show_all_answers(counter: Counter[str]) -> None:
    print("The possible answers found within the dataset are:")
    print(f"{';'.join(list(counter))}\n")


def analyze_frequencies(column_name: str, field_sep: str | None = None) -> None:
    target = cumulative_count(column_name=column_name, field_sep=field_sep)
    show_all_answers(target)
    show_frequencies(target)


def main() -> None:
    analyze_frequencies(column_name="RemoteWork")
    analyze_frequencies(column_name="LanguageHaveWorkedWith", field_sep=";")


if __name__ == "__main__":
    main()
