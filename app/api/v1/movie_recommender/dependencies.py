from typing import Annotated

from fastapi import Depends

from .controller import MovieRecommenderController


MovieRecommenderControllerDependency = Annotated[MovieRecommenderController, Depends()]
