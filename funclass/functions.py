"""Performs Stack Overflow 2022 survey analysis using functional programming."""

import csv
from collections import Counter
from typing import Optional, Union


def cumulative_count(column_name: str, field_sep=None) -> Counter:
    """Cumulative count of anwswers for specific column in Stack Overflow survey."""

    print(f"--- Analysing frequencies of {column_name} --- ")

    with open("data/survey_results_public.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        counter = Counter()
        for line in csv_reader:
            if field_sep:
                splited_line = line[column_name].split(field_sep)
                for element in splited_line:
                    counter[element] += 1
            else:
                counter[line[column_name]] += 1
    return counter


def sum_total_respondents(counter: Counter):
    """Calculate the total respondents including the absent ones."""

    # In Python 3.10 there is the counter.total() method that simplify a lot the next line!
    return sum(counter[element] for element in counter)


def show_frequencies(counter: Counter):
    """Prints the absolute and relative frequency for each possible answer, including NA answers."""

    total_respondents = sum_total_respondents(counter)

    for possibility, freq in counter.most_common():
        print(
            f"{possibility: <36} -> {freq: <5} |",
            f"{round(freq /  total_respondents * 100, 2)}%",
        )
    print("\n")


def show_all_answers(counter: Counter):
    """Prints all answered possibilities for a question in survey, including NA answers."""

    print("The possible answers found within the dataset are:")
    print(f"{';'.join(list(counter))}\n")


def analyze_frequencies(column_name: str, field_sep: Optional[Union[str, None]] = None):
    """Process the entire frequency analyzis on a column."""

    target = cumulative_count(column_name=column_name, field_sep=field_sep)
    show_all_answers(target)
    show_frequencies(target)


def main() -> None:
    """Analyse remote work and languages answers."""
    analyze_frequencies(column_name="RemoteWork")
    analyze_frequencies(column_name="LanguageHaveWorkedWith", field_sep=";")


if __name__ == "__main__":
    main()
