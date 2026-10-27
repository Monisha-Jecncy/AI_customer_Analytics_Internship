"""
Data ingestion + cleaning.
Handles CSV/Excel upload, missing values, type coercion, and feature selection.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_dataset(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV or Excel file into a DataFrame."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Unsupported file type. Upload a CSV or Excel file.")


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Clean a raw dataframe and return (clean_df, report).
    - drops fully-empty columns
    - fills numeric NaNs with median, categorical with mode
    - removes duplicate rows
    """
    report = {}
    original_shape = df.shape

    df = df.dropna(axis=1, how="all")
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()

    numeric_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(exclude=np.number).columns

    filled = 0
    for col in numeric_cols:
        n = int(df[col].isna().sum())
        if n:
            df[col] = df[col].fillna(df[col].median())
            filled += n
    for col in cat_cols:
        n = int(df[col].isna().sum())
        if n and not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
            filled += n

    report = {
        "original_rows": original_shape[0],
        "original_cols": original_shape[1],
        "final_rows": df.shape[0],
        "final_cols": df.shape[1],
        "duplicates_removed": duplicates,
        "values_filled": filled,
        "numeric_features": list(numeric_cols),
    }
    return df.reset_index(drop=True), report


def scale_features(df: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    """Standardise the chosen numeric features for clustering."""
    scaler = StandardScaler()
    return scaler.fit_transform(df[feature_cols])
