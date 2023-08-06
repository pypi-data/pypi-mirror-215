from typing import TYPE_CHECKING, Optional, Iterable

if TYPE_CHECKING:
    from ._fx_surface_parameters import FxSurfaceParameters
    from ._models import VolatilitySurfacePoint
    from ._models._surface_output import SurfaceLayout
    from .._enums import Format


SurfaceParameters = Optional["FxSurfaceParameters"]
SurfaceLayout = Optional["SurfaceLayout"]
OptFormat = Optional["Format"]
OptVolatilitySurfacePoints = Optional[Iterable["VolatilitySurfacePoint"]]
