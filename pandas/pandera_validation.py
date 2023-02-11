from datetime import datetime
from pathlib import Path

import pandera as pa
from pandera.errors import SchemaError

import pandas as pd


def read_airports_dataset(path: Path, filename: str) -> pd.DataFrame:
    """Read the Netherlands airport dataset csv file as a pandas dataframe."""
    airports = pd.read_csv(path / filename)
    return airports


def remove_metadata_information(path: Path, filename: str) -> pd.DataFrame:
    """Read the Netherlands airport dataset csv file as a pandas dataframe."""
    df_out = pd.read_csv(path / filename, skiprows=2)
    return df_out


def main() -> None:
    dataset_path = Path().absolute() / "datasets"
    filename = "netherlands_airports.csv"

    airports_wrong_type_infer = read_airports_dataset(dataset_path, filename)

    print(airports_wrong_type_infer.info())

    airports_raw = remove_metadata_information(dataset_path, filename)
    airports_raw.columns = airports_wrong_type_infer.columns
    print(airports_raw.info())

    schema = pa.DataFrameSchema(
        columns={
            "id": pa.Column(int),
            "ident": pa.Column("string", coerce=True),
            "type": pa.Column("string", coerce=True),
            "name": pa.Column("string", coerce=True),
            "latitude_deg": pa.Column(float, nullable=True),
            "longitude_deg": pa.Column(float, nullable=True),
            "elevation_ft": pa.Column(float, nullable=True),
            "continent": pa.Column("string", coerce=True),
            "iso_country": pa.Column("string", coerce=True),
            "iso_region": pa.Column("string", coerce=True),
            "municipality": pa.Column("string", coerce=True, nullable=True),
            "scheduled_service": pa.Column(bool, coerce=True),
            "gps_code": pa.Column("string", coerce=True, nullable=True),
            "iata_code": pa.Column("string", coerce=True, nullable=True),
            "local_code": pa.Column("string", coerce=True, nullable=True),
            "home_link": pa.Column("string", coerce=True, nullable=True),
            "wikipedia_link": pa.Column("string", coerce=True, nullable=True),
            "keywords": pa.Column("string", coerce=True, nullable=True),
            "score": pa.Column("string", coerce=True, nullable=True),
            "last_updated": pa.Column(datetime, coerce=True),
        }
    )

    try:
        schema.validate(airports_wrong_type_infer)
    except SchemaError:
        print("The validations on airports_wrong_type_infer failed.")

    try:
        schema.validate(airports_raw)
    except SchemaError:
        print("The validations on airports_raw failed.")


if __name__ == "__main__":
    main()
