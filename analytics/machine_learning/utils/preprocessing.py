from typing import List, Optional

import pandas as pd
from sklearn.preprocessing import (
    OneHotEncoder,
    MinMaxScaler
)


def perform_one_hot_encoding(
    df: pd.DataFrame,
    encoder: OneHotEncoder,
    fit: bool = False,
    categorical_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Given a dataframe with categorical columns this function will return a new dataframe
    that will replace these columns with the one hot encoding ones and will leave the rest
    of the columns unchanged.
    params:
    - fit -> If fit is True then fit_transform is called , otherwise only transform
    - categorical_columns -> A list with the names of the categorical columns we want to
    transform. If not given then columns with type category are used
    """

    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include='category').columns.tolist()

    if fit: 
        encoded_df = pd.DataFrame(encoder.fit_transform(df[categorical_columns]).toarray(), columns=encoder.get_feature_names_out())
    else:
        encoded_df = pd.DataFrame(encoder.transform(df[categorical_columns]).toarray(), columns=encoder.get_feature_names_out())

    #merge one-hot encoded columns back with original DataFrame
    final_df = df.join(encoded_df)

    # Drop original categorical columns
    final_df.drop(categorical_columns, axis=1, inplace=True)

    return final_df.reset_index(drop=True)


def perform_min_max_scaling(
    df: pd.DataFrame,
    min_max_scaler: MinMaxScaler,
    fit: bool = False,
    columns_to_scale: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Given a dataframe with numerical columns this function will return a new dataframe
    that will perform min max scaling on these columns and will leave the rest
    of the columns unchanged.
    params:
    - fit -> If fit is True then fit_transform is called , otherwise only transform
    - columns_to_scale -> A list with the names of the numerical columns we want to
    transform. If not given then columns with type float64 are used
    """

    if columns_to_scale is None:
        columns_to_scale = df.select_dtypes(include='float64').columns.tolist()

    scaled_df = df.copy()
    # Scale the specified columns
    if fit:
        scaled_df[columns_to_scale] = min_max_scaler.fit_transform(df[columns_to_scale])
    else:
        scaled_df[columns_to_scale] = min_max_scaler.transform(df[columns_to_scale])

    return scaled_df