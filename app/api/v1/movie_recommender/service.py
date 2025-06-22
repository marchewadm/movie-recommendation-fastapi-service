import numpy as np
import pandas as pd

from app.shared.type_definitions import TrainedModel


class MovieRecommenderService:
    """Service for generating movie recommendations."""

    @staticmethod
    async def _read_data_from_model(
        model: TrainedModel,
    ) -> tuple[pd.DataFrame, np.ndarray, pd.Series]:
        """Extracts key data components from the loaded trained model.

        Args:
            model (TrainedModel):
                The loaded trained recommendation model as a TypedDict.

        Returns:
            tuple[pd.DataFrame, np.ndarray, pd.Series]:
                The extracted key data components from the loaded model:
                - pd.DataFrame: The DataFrame of movie metadata.
                - np.ndarray: The cosine similarity matrix.
                - pd.Series: The mapping from TMDB ID to DataFrame index.
        """

        movies_df = model["movies_df"]
        cosine_sim = model["cosine_sim"]
        tmdb_id_to_index = model["tmdb_id_to_index"]

        return movies_df, cosine_sim, tmdb_id_to_index

    @staticmethod
    async def _find_movie_recommendations(
        tmdb_id: int,
        movie_index_map: pd.Series,
        movies_dataframe: pd.DataFrame,
        similarity_matrix: np.ndarray,
        n_recommendations: int = 10,
        target_genres: list[str] = None,
        target_tags: list[str] = None,
        min_rating_count: int = 50,
    ) -> pd.DataFrame:
        """Recommends movies similar to the given movie based on cosine similarity.

        The function uses a precomputed cosine similarity matrix to find movies most
        similar to the one specified by `tmdb_id`. Results can be filtered by genre,
        tag, and minimum number of ratings.

        Args:
            tmdb_id (int):
                The TMDB ID of the movie to find recommendations for.
            movie_index_map (pd.Series):
                A mapping from tmdbId to the corresponding row index in the similarity
                matrix and movies DataFrame.
            movies_dataframe (pd.DataFrame):
                The DataFrame containing movie metadata, such as title, genres, tags,
                average ratings, and rating count.
            similarity_matrix (np.ndarray):
                Matrix of cosine similarity scores between movies.
            n_recommendations (int):
                Number of recommendations to return.
                Defaults to 10.
            target_genres (list[str] | None):
                List of genres to filter recommendations by. If provided, only movies
                that share at least one of the specified genres will be returned.
            target_tags (list[str] | None):
                List of tags to filter recommendations by. If provided, only movies
                that share at least one of the specified tags will be returned.
            min_rating_count (int):
                Minimum number of ratings a recommended movie must have. This helps
                filter out obscure movies with unreliable averages.
                Defaults to 50.

        Returns:
            pd.DataFrame:
                A DataFrame containing recommended movies.
        """

        if tmdb_id not in movie_index_map:
            raise ValueError(f"Movie ID {tmdb_id} not found in the dataset.")

        recommendations = []

        target_genres_lower = (
            [genre.strip().lower() for genre in target_genres] if target_genres else []
        )
        target_tags_lower = (
            [tag.strip().lower() for tag in target_tags] if target_tags else []
        )

        movie_index = movie_index_map[tmdb_id]

        similarity_scores = list(enumerate(similarity_matrix[movie_index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[
            1:
        ]  # Remove the first row, as it always is the movie provided by the user.

        for similar_movie_index, similarity_score in similarity_scores:
            movie = movies_dataframe.iloc[similar_movie_index].copy()

            genres = (
                [genre.strip().lower() for genre in movie["genres"].split("|") if genre]
                if pd.notna(movie["genres"])
                else []
            )

            tags = (
                [tag.strip().lower() for tag in movie["tags"].split() if tag]
                if pd.notna(movie["tags"])
                else []
            )

            if target_genres_lower and not any(
                genre in genres for genre in target_genres_lower
            ):
                continue
            if target_tags_lower and not any(tag in tags for tag in target_tags_lower):
                continue
            if movie["ratingCount"] < min_rating_count:
                continue

            movie["similarityScore"] = similarity_score
            recommendations.append(movie)

            if len(recommendations) >= n_recommendations:
                break

        if not recommendations:
            raise LookupError(f"No recommendations found for movie ID {tmdb_id}.")

        recommendations_df = pd.DataFrame(recommendations).sort_values(
            by=["similarityScore", "averageRating"], ascending=[False, False]
        )

        return recommendations_df

    @staticmethod
    async def _transform_recommendations(
        recommendations_df: pd.DataFrame,
    ) -> list[dict[str, int | float]]:
        """Transforms the recommendations DataFrame into a list of dictionaries.

        Args:
            recommendations_df (pd.DataFrame):
                The DataFrame containing the raw movie recommendations.

        Returns:
            list[dict[str, int | float]]:
                A list of dictionaries, each representing a recommended movie with
                "tmdb_id" (int) and "similarity_score" (float).
        """

        columns_to_display = ["tmdbId", "similarityScore"]

        recommendations_df_copy: pd.DataFrame = recommendations_df[
            columns_to_display
        ].copy()

        recommendations_df_copy = recommendations_df_copy.rename(
            columns={"tmdbId": "tmdb_id", "similarityScore": "similarity_score"}
        )

        recommendations: list[dict[str, int | float]] = recommendations_df_copy.to_dict(
            orient="records"
        )

        return recommendations

    async def recommend(
        self,
        tmdb_id: int,
        ml_model: TrainedModel,
        tags: list[str] | None = None,
        genres: list[str] | None = None,
        limit: int = 10,
        min_rating_count: int = 50,
    ) -> list[dict[str, int | float]]:
        """Generates movie recommendations based on a given TMDB ID and filters.

        Args:
            tmdb_id (int):
                The TMDB ID of the movie to find recommendations for.
            ml_model (TrainedModel):
                The preloaded trained machine learning model containing all
                necessary components for recommendation generation.
            tags (list[str] | None):
                List of tags to filter recommendations by. If provided, only movies
                that share at least one of the specified tags will be returned.
            genres (list[str] | None):
                List of genres to filter recommendations by. If provided, only movies
                that share at least one of the specified genres will be returned.
            limit (int):
                The maximum number of recommendations to return.
                Defaults to 10.
            min_rating_count (int):
                The minimum number of ratings a recommended movie must have.
                Defaults to 50.

        Returns:
            list[dict[str, int | float]]:
                A list of dictionaries, each representing a recommended movie with
                "tmdb_id" (int) and "similarity_score" (float).
        """

        movies_df, cosine_sim, tmdb_id_to_index = await self._read_data_from_model(
            ml_model
        )

        recommendations_df = await self._find_movie_recommendations(
            tmdb_id,
            tmdb_id_to_index,
            movies_df,
            cosine_sim,
            limit,
            genres,
            tags,
            min_rating_count,
        )

        recommendations = await self._transform_recommendations(recommendations_df)

        return recommendations
