import os
from pathlib import Path

import pandas as pd


def get_filepath(filename: str, subfolder: str = "data"):
    return Path(os.environ["PYTEST_CURRENT_TEST"]).parent / subfolder / filename


def infer_iso_datetime(values: pd.Series) -> pd.Series:
    try:
        converted_values = pd.to_datetime(values)
    except (ValueError, TypeError):
        # if not possible to parse as datetime, return original values
        return values
    try:
        values_isoformat = converted_values.apply(pd.Timestamp.isoformat)
    except TypeError:
        return values
    if not (values_isoformat == values).all():
        # if original values is not in ISO 8601 format, return original values
        return values
    return converted_values


def infer_iso_timedelta(values: pd.Series) -> pd.Series:
    try:
        converted_values = pd.to_timedelta(values)
    except (ValueError, TypeError):
        # if not possible to parse as time delta, return original values
        return values
    try:
        values_isoformat = converted_values.apply(pd.Timedelta.isoformat)
    except TypeError:
        return values
    if not (values_isoformat == values).all():
        # if original values is not in ISO 8601 format, return original values
        return values
    return converted_values


def make_df(data: list[str]):
    pd.DataFrame.from_records(data)


def read_df(
    filename: str,
    subfolder: str = "data",
) -> pd.DataFrame:
    """
    Read pandas DataFrame from test data.
    Datetimes and timedeltas are inferred automatically.

    Args:
        filename (str): CSV file with test data
        subfolder (str, optional): Subfolder relative to test being
            run currently (taken from  the environment variable PYTEST_CURRENT_TEST),
            from where to read the test data. Defaults to "data".
    """
    filepath = get_filepath(filename, subfolder)
    df = pd.read_csv(
        filepath,
        parse_dates=True,
        infer_datetime_format=True,
        keep_default_na=False,
        na_values=["nan"],
    )

    # try converting ISO 8601 strings to pd.Timestamp and pd.Timedelta
    df = df.apply(infer_iso_datetime)
    df = df.apply(infer_iso_timedelta)

    return df
