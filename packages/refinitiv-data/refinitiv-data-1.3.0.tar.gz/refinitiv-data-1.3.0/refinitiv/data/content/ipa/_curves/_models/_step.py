# coding: utf8
from ..._object_definition import ObjectDefinition
from ....._types import OptDateTime


class Step(ObjectDefinition):
    """
    Parameters
    ----------
    effective_date : str or date or datetime or timedelta, optional

    meeting_date : str or date or datetime or timedelta, optional

    """

    def __init__(
        self,
        effective_date: "OptDateTime" = None,
        meeting_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.effective_date = effective_date
        self.meeting_date = meeting_date

    @property
    def effective_date(self):
        """
        :return: str
        """
        return self._get_parameter("effectiveDate")

    @effective_date.setter
    def effective_date(self, value):
        self._set_date_parameter("effectiveDate", value)

    @property
    def meeting_date(self):
        """
        :return: str
        """
        return self._get_parameter("meetingDate")

    @meeting_date.setter
    def meeting_date(self, value):
        self._set_date_parameter("meetingDate", value)
