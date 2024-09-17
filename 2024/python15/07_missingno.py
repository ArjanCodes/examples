import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd


def main():
    # Create a larger sample dataframe with missing data
    data = {
        "name": [
            "Alice",
            "Bob",
            "Charlie",
            "David",
            "Eve",
            "Frank",
            "Grace",
            "Helen",
            "Ivy",
            "Jack",
        ],
        "age": [25, 35, np.nan, 22, 40, np.nan, 33, 29, np.nan, 45],
        "score": [85, 90, np.nan, 95, 88, 76, np.nan, 80, 92, np.nan],
        "height": [165, 180, 175, np.nan, 168, 177, np.nan, 162, 170, 178],
        "weight": [70, np.nan, 68, 75, 72, 80, np.nan, 64, 70, 85],
    }
    df = pd.DataFrame(data)

    # Visualize missing data in a larger dataset
    msno.matrix(df)
    plt.show()


if __name__ == "__main__":
    main()
