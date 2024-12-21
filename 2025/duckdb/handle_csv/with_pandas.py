import pandas as pd


# Create a sample DataFrame
def main() -> None:
    # Read data from CSV file

    df = pd.read_csv("data/employees.csv")

    # Filter the DataFrame
    filtered_df = df[df["salary"] > 125000][["name", "job_title", "salary"]].head(3)

    print("3 records with a high salary per year:")
    print(filtered_df)


if __name__ == "__main__":
    main()
