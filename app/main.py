import os
import pickle

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.api import router as api_router
from .core.config import settings
from .shared.type_definitions import TrainedModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to manage the lifespan of the application.

    Handles the loading and unloading of the
    machine learning recommendation model for the application.

    Args:
        app (FastAPI):
            The FastAPI application instance.

    Yields:
        None
    """

    with open(
        os.path.join(str(settings.MODELS_DIR), settings.TRAINED_PKL_FILE), "rb"
    ) as f:
        ml_model: TrainedModel = pickle.load(f)

    app.state.recommendation_model = ml_model  # noqa

    yield

    app.state.recommendation_model.clear()  # noqa


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
