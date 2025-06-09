from typing import Annotated

from fastapi import Depends

from app.controllers.health import HealthController


HealthControllerDependency = Annotated[HealthController, Depends()]
