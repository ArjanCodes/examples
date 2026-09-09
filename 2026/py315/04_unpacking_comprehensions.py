"""PEP 798: flatten iterables and merge mappings directly in a comprehension."""


def main() -> None:
    weekly_scores = [[8, 9], [10], [7, 8]]
    all_scores = [*scores for scores in weekly_scores]

    feature_flags = [
        {"dark_mode": False, "beta_search": True},
        {"dark_mode": True, "new_editor": True},
    ]
    merged_flags = {**flags for flags in feature_flags}

    print(f"flattened scores: {all_scores}")
    print(f"merged flags: {merged_flags}")


if __name__ == "__main__":
    main()
