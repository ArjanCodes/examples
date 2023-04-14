import csv
from collections import Counter
from csv import DictReader
from pathlib import Path

ROOT = Path().absolute()
DATA = ROOT / "data"

FILENAME = "survey_results_public.csv"


def cumulative_count(
    column_name: str, file: DictReader, field_sep: str | None = None
) -> Counter[str]:
    print(f"--- Analysing frequencies of {column_name} --- ")
    counter = Counter()
    for line in file:
        if field_sep:
            splitted_line = line[column_name].split(field_sep)
            for element in splitted_line:
                counter[element] += 1
        else:
            counter[line[column_name]] += 1
    del counter[column_name]
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


def analyze_frequencies(
    column_name: str, file: DictReader, field_sep: str | None = None
) -> None:
    target = cumulative_count(column_name=column_name, file=file, field_sep=field_sep)
    show_all_answers(target)
    show_frequencies(target)


def main() -> None:
    with open(DATA / FILENAME, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        analyze_frequencies(column_name="RemoteWork", file=csv_reader)

        # the analysis should run again starting from the first line, not from header.
        csv_file.seek(1)

        analyze_frequencies(
            column_name="LanguageHaveWorkedWith", file=csv_reader, field_sep=";"
        )


if __name__ == "__main__":
    main()
