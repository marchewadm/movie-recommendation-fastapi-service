from typing import Annotated

from fastapi import APIRouter, Query, Request, status

from .schemas import GetRecommendationsQuery, GetRecommendationsResponse
from .dependencies import MovieRecommenderControllerDependency


router = APIRouter(prefix="/movies", tags=["Recommender"])


@router.get(
    "/recommend",
    response_model=GetRecommendationsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_recommendations(
    request: Request,
    query: Annotated[GetRecommendationsQuery, Query()],
    movie_recommender_controller: MovieRecommenderControllerDependency,
):
    """Get movie recommendations based on specified criteria."""

    response = await movie_recommender_controller.recommend(
        query, request.app.state.recommendation_model
    )

    return response
