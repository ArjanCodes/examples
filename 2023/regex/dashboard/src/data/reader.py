import pandas as pd

def load_json(file_path: str) -> pd.DataFrame:
    """
    Reads a JSON file and creates a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - pd.DataFrame: The DataFrame created from the JSON file.
    """
    try:
        # Read the JSON file into a DataFrame
        df = pd.read_json(file_path)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
