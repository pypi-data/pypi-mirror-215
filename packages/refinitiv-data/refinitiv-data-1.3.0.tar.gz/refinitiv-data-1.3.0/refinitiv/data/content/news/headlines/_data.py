import abc
from dataclasses import dataclass, fields
from typing import Optional, List

import pandas as pd
from humps import decamelize
from pandas.core.tools.datetimes import DatetimeScalar

from .. import Urgency
from .._tools import get_headlines
from ..._content_data import Data
from ...._tools import get_from_path
from ...._types import OptInt


@dataclass
class NewsHeadlinesData(Data):
    _headlines: Optional[List["HeadlineRDP"]] = None
    _limit: "OptInt" = None

    @abc.abstractmethod
    def _build_headlines(self, raw: dict, limit: int) -> List["HeadlineRDP"]:
        # override this
        pass

    @property
    def headlines(self) -> List["HeadlineRDP"]:
        if self._headlines is None:
            self._headlines = self._build_headlines(self.raw, self._limit)

        return self._headlines


@dataclass
class NewsHeadlinesRDPData(NewsHeadlinesData):
    def _build_headlines(self, raw: dict, limit: int) -> List["HeadlineRDP"]:
        return get_headlines(raw, headline_rdp_from_dict, limit)


@dataclass
class NewsHeadlinesUDFData(NewsHeadlinesData):
    def _build_headlines(self, raw: dict, limit: int) -> List["HeadlineUDF"]:
        return get_headlines(raw, headline_udf_from_dict, limit)


@dataclass
class HeadlineRDP:
    title: str
    creator: str
    source: List[dict]
    language: List[dict]
    item_codes: List[str]
    urgency: Urgency
    first_created: "DatetimeScalar"
    version_created: "DatetimeScalar"
    story_id: str


def headline_rdp_from_dict(datum: dict) -> HeadlineRDP:
    subject = get_from_path(datum, "newsItem.contentMeta.subject")
    item_codes = [item.get("_qcode") for item in subject]

    urgency = get_from_path(datum, "newsItem.contentMeta.urgency.$")
    urgency = Urgency(urgency)

    first_created = get_from_path(datum, "newsItem.itemMeta.firstCreated.$")
    first_created = pd.to_datetime(first_created)

    version_created = get_from_path(datum, "newsItem.itemMeta.versionCreated.$")
    version_created = pd.to_datetime(version_created)

    headline = HeadlineRDP(
        title=get_from_path(datum, "newsItem.itemMeta.title.0.$"),
        creator=get_from_path(datum, "newsItem.contentMeta.creator.0._qcode"),
        source=get_from_path(datum, "newsItem.contentMeta.infoSource"),
        language=get_from_path(datum, "newsItem.contentMeta.language"),
        item_codes=item_codes,
        urgency=urgency,
        first_created=first_created,
        version_created=version_created,
        story_id=datum["storyId"],
    )
    return headline


@dataclass
class HeadlineUDF:
    display_direction: str
    document_type: str
    first_created: "DatetimeScalar"
    is_alert: bool
    language: str
    report_code: str
    source_name: str
    story_id: str
    text: str
    version_created: "DatetimeScalar"


def headline_udf_from_dict(datum: dict) -> HeadlineUDF:
    keys = [field.name for field in fields(HeadlineUDF)]
    kwargs = decamelize(datum)
    kwargs = {k: v for k, v in kwargs.items() if k in keys}
    kwargs["first_created"] = pd.to_datetime(kwargs["first_created"])
    kwargs["version_created"] = pd.to_datetime(kwargs["version_created"])
    headline = HeadlineUDF(**kwargs)
    return headline
