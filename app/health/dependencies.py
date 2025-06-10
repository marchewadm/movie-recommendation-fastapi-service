from typing import Annotated

from fastapi import Depends

from .controller import HealthController


HealthControllerDependency = Annotated[HealthController, Depends()]
