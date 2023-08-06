from typing import TYPE_CHECKING, Union, Optional

from .._definition import BaseSurfaceDefinition
from ..._surfaces._swaption_surface_request_item import SwaptionSurfaceRequestItem
from ....._content_type import ContentType

if TYPE_CHECKING:
    from . import SwaptionSurfaceDefinition, SwaptionCalculationParams
    from ..._surfaces._surface_types import SurfaceLayout
    from ....._types import ExtendedParams, OptStr


class Definition(BaseSurfaceDefinition):
    """
    Create a Swaption data Definition object.

    Parameters
    ----------
    instrument_type : DEPRECATED
        This attribute doesn't use anymore.
    surface_layout : SurfaceLayout
        See details in SurfaceLayout class
    surface_parameters : SwaptionCalculationParams
        See details in SwaptionCalculationParams class
    underlying_definition : dict or EtiSurfaceDefinition
       Dict or EtiSurfaceDefinition object. See details in EtiSurfaceDefinition class
       Example:
            {"fxCrossCode": "EURUSD"}
    surface_tag : str, optional
        A user defined string to describe the volatility surface
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    get_data(session=session, on_response=on_response, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> from refinitiv.data.content.ipa.surfaces import swaption
    >>> definition = swaption.Definition(
    ...     underlying_definition=swaption.SwaptionSurfaceDefinition(
    ...         instrument_code="USD",
    ...         discounting_type=swaption.DiscountingType.OIS_DISCOUNTING
    ...     ),
    ...     surface_tag="USD_Strike__Tenor_",
    ...     surface_layout=swaption.SurfaceLayout(
    ...         format=swaption.Format.MATRIX
    ...     ),
    ...     surface_parameters=swaption.SwaptionCalculationParams(
    ...         x_axis=swaption.Axis.TENOR,
    ...         y_axis=swaption.Axis.STRIKE,
    ...         calculation_date="2020-03-20"
    ...     )
    >>> )
    """

    def __init__(
        self,
        instrument_type=None,
        surface_layout: "SurfaceLayout" = None,
        surface_parameters: Optional["SwaptionCalculationParams"] = None,
        underlying_definition: Union[dict, "SwaptionSurfaceDefinition"] = None,
        surface_tag: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = SwaptionSurfaceRequestItem(
            instrument_type=instrument_type,
            surface_layout=surface_layout,
            surface_parameters=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES_SWAPTION,
            universe=request_item,
            extended_params=extended_params,
        )
