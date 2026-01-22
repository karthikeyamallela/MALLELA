import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder


def preprocess_data(df, label_column=None):
    """
    Flexible preprocessing for IDS datasets
    Supports NSL-KDD and other formats
    
    Args:
        df: DataFrame with features and labels
        label_column: Column index/name for labels (default: last column)
    """

    # Determine label column
    if label_column is None:
        label_column = df.shape[1] - 1  # Default to last column (NSL-KDD format)
    
    # Extract features and labels
    if isinstance(label_column, (int, np.integer)):
        # Column index
        X = df.iloc[:, :label_column].copy()
        y = df.iloc[:, label_column].copy()
    else:
        # Column name
        X = df.drop(columns=[label_column]).copy()
        y = df[label_column].copy()

    # Binary classification: normal vs attack
    y = y.apply(lambda x: 0 if str(x).lower() == "normal" else 1)

    # Encode categorical columns
    categorical_cols = X.select_dtypes(include=["object"]).columns

    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y.values

