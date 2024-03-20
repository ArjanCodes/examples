import pandas as pd


def load_json(file_path: str) -> pd.DataFrame:
    """
    Reads a JSON file and creates a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - pd.DataFrame: The DataFrame created from the JSON file.

    Raises:
    - ValueError: If the JSON file has formatting issues.
    - FileNotFoundError: If the JSON file is not found at the specified path.
    """
    try:
        # Read the JSON file into a DataFrame
        print(file_path)
        df = pd.read_json(file_path)
        return df
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        raise
    except FileNotFoundError as fnfe:
        print(f"FileNotFoundError occurred: {fnfe}")
        raise
