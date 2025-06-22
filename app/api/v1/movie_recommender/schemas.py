from typing import Annotated

from pydantic import BaseModel, Field, field_validator, field_serializer


ALLOWED_GENRES = [
    "action",
    "adventure",
    "animation",
    "children's",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "fantasy",
    "film-noir",
    "horror",
    "musical",
    "mystery",
    "romance",
    "sci-fi",
    "thriller",
    "war",
    "western",
]


class GetRecommendationsQuery(BaseModel):
    """Model for validating movie recommendation query parameters."""

    model_config = {"extra": "forbid"}

    tmdb_id: Annotated[int, Field(ge=1)]
    limit: Annotated[int, Field(validate_default=True, default=10, ge=1, le=20)]
    min_rating_count: Annotated[
        int,
        Field(validate_default=True, default=50, ge=1),
    ]
    tags: set[str] | None = None
    genres: set[str] | None = None

    @field_validator("genres")  # noqa
    @classmethod
    def validate_genres(cls, genres: set[str]):
        for genre in genres:
            if genre not in ALLOWED_GENRES:
                raise ValueError(f"Genre must be one of: {', '.join(ALLOWED_GENRES)}.")

        return genres


class Recommendation(BaseModel):
    """Model representing a single movie recommendation."""

    tmdb_id: Annotated[int, Field(ge=1, serialization_alias="tmdbId")]
    similarity_score: Annotated[float, Field(serialization_alias="similarityScore")]

    @field_serializer("similarity_score", when_used="json")
    def serialize_float_5_digits(self, similarity_score: float):
        return round(similarity_score, 5)


class GetRecommendationsResponse(BaseModel):
    """Response model containing movie recommendations."""

    recommendations: list[Recommendation]
