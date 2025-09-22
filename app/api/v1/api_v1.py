from fastapi import APIRouter

from .movie_recommender.router import router as movie_recommender_router


router = APIRouter(prefix="/v1", tags=["API v1"])

router.include_router(movie_recommender_router)
