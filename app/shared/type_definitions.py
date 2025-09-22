from typing import TypedDict

from numpy import ndarray
from pandas import DataFrame, Series


class TrainedModel(TypedDict):
    """A TypedDict to define the structure of the trained recommendation model.

    Attributes:
        movies_df (DataFrame):
            The DataFrame containing movie metadata.
        cosine_sim (ndarray):
            The cosine similarity matrix.
        tmdb_id_to_index (Series):
            A mapping from TMDB ID to DataFrame index.
    """

    movies_df: DataFrame
    cosine_sim: ndarray
    tmdb_id_to_index: Series
