from fastapi import Depends

from app.shared.type_definitions import TrainedModel

from .schemas import GetRecommendationsQuery, GetRecommendationsResponse, Recommendation
from .service import MovieRecommenderService


class MovieRecommenderController:
    """Handles incoming requests for movie recommendations.

    Attributes:
        movie_recommender_service (MovieRecommenderService):
            An instance of "MovieRecommenderService".
    """

    def __init__(
        self,
        movie_recommender_service: MovieRecommenderService = Depends(
            MovieRecommenderService
        ),
    ) -> None:
        """Initialize MovieRecommenderController with MovieRecommenderService instance.

        Args:
            movie_recommender_service (MovieRecommenderService):
                An instance of "MovieRecommenderService".

        Returns:
            None
        """

        self.movie_recommender_service = movie_recommender_service

    async def recommend(
        self, query: GetRecommendationsQuery, ml_model: TrainedModel
    ) -> GetRecommendationsResponse:
        """Generates movie recommendations based on the provided query.

        Args:
            query (GetRecommendationsQuery):
                An object containing the query parameters for recommendations,
                including "tmdb_id", "tags", "genres", "limit", and "min_rating_count".
            ml_model (TrainedModel):
                The preloaded machine learning model, injected via FastAPI's
                lifespan context.

        Returns:
            GetRecommendationsResponse:
                A Pydantic model containing a list of "Recommendation" objects,
                each representing a recommended movie with its TMDB ID and
                similarity score.
        """

        recommendations = await self.movie_recommender_service.recommend(
            query.tmdb_id,
            ml_model,
            query.tags,
            query.genres,
            query.limit,
            query.min_rating_count,
        )

        return GetRecommendationsResponse(
            recommendations=[Recommendation(**rec) for rec in recommendations]
        )
