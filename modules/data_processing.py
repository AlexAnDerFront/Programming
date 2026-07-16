"""
Pandas transformations. Keep XML parsing and sqlite I/O out of here —
this module should only take a DataFrame in and return a DataFrame out,
which makes it easy to unit test.
"""
import pandas as pd


def records_to_dataframe(records: list[dict]) -> pd.DataFrame:
    """Turn a list of dicts (from xml_parser) into a DataFrame."""
    return pd.DataFrame.from_records(records)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Example cleaning steps — adjust to your actual schema.
    """
    if df.empty:
        return df

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # Example type coercion (only runs if the columns exist)
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")

    # Drop rows that ended up fully empty after coercion
    df = df.dropna(how="all")

    return df.reset_index(drop=True)