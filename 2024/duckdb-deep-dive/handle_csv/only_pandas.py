import pandas as pd


# Create a sample DataFrame
def main() -> None:
    # Read data from CSV file

    df = pd.read_csv("data/employees.csv")

    # Filter the DataFrame
    filtered_df = df[df["salary"] > 2000][["name", "position", "salary"]].head(3)

    print("Top 3 records with the highest salary per year:")
    print(filtered_df)


if __name__ == "__main__":
    main()
