import datetime
import re
from collections.abc import Iterator
from enum import Enum
from re import Pattern
from typing import Self

from citation_docket import (
    CITATION_OPTIONS,
    ShortDocketCategory,
    extract_docket_from_data,
    extract_dockets,
)
from citation_report import Report
from pydantic import BaseModel, ConfigDict, Field


class Citation(BaseModel):
    """
    A Philippine Supreme Court `Citation` includes fields sourced from:

    1. `Docket` - as defined in [citation-docket](https://github.com/justmars/citation-docket) - includes:
        1. _category_,
        2. _serial number_, and
        3. _date_.
    2. `Report` - as defined in [citation-report](https://github.com/justmars/citation-report) - includes:
        1. _volume number_,
        2. _identifying acronym of the reporter/publisher_,
        3. _page of the reported volume_.

    It is typical to see a `Docket` combined with a `Report`:

    > _Bagong Alyansang Makabayan v. Zamora, G.R. Nos. 138570, 138572, 138587, 138680, 138698, October 10, 2000, 342 SCRA 449_

    Taken together (and using _Bagong Alyansang Makabayan_ as an example) the text above can be extracted into fields:

    Example | Field | Type | Description
    --:|:--:|:--|--:
    GR | `docket_category` | optional (`ShortDocketCategory`) | See shorthand
    138570 |`docket_serial` | optional (str) | See serialized identifier
    datetime.date(2000, 10, 10) | `docket_date` | optional (date) | When docket serial issued
    GR 138570, Oct. 10, 2000 | `docket` | optional (str) | Combined `docket_category` `docket_serial` `docket_date`
    None | `phil` | optional (str) | combined `volume` Phil. `page`
    342 SCRA 449 | `scra` | optional (str) | combined `volume` SCRA `page`
    None | `offg` | optional (str) | combined `volume` O.G. `page`
    """  # noqa: E501

    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)
    docket_category: ShortDocketCategory | None = Field(
        None,
        title="Docket Category",
        description="Common categories of PH Supreme Court decisions.",
    )
    docket_serial: str | None = Field(
        None,
        title="Docket Serial Number",
        description="Serialized identifier of docket category.",
    )
    docket_date: datetime.date | None = Field(
        None,
        title="Docket Date",
        description="Distinguishes same category and serial decisions by issuance.",
    )
    docket: str | None = Field(
        None,
        title="Docket Reference",
        description="Clean parts: category, a single serial id, and date.",
    )
    phil: str | None = Field(
        None,
        title="Philippine Reports",
        description="Combine `volume` Phil. `page` from `citation-report`.",
    )
    scra: str | None = Field(
        None,
        title="Supreme Court Reports Annotated",
        description="Combine `volume` SCRA `page` from `citation-report`.",
    )
    offg: str | None = Field(
        None,
        title="Official Gazette",
        description="Combine `volume` O.G. `page` from `citation-report`.",
    )

    @property
    def is_statute(self) -> bool:
        """This flag is a special rule to determine whether a combination of category
        and serial number would qualify the citation instance as a statutory pattern
        rather than a decision pattern."""
        if self.docket_category:
            if self.docket_category == ShortDocketCategory.BM:
                if bm_text := self.docket_serial:
                    if CitationBasedStatutes.BAR.pattern.search(bm_text):
                        return True
        return False

    @classmethod
    def extract_citation_from_data(cls, data: dict) -> Self:
        """Direct creation of Citation object based on a specific data dict.

        Examples:
            >>> data = {"date_prom": "1985-04-24", "docket": "General Register L-63915, April 24, 1985", "orig_idx": "GR No. L-63915", "phil": "220 Phil. 422", "scra": "136 SCRA 27", "offg": None}
            >>> Citation.extract_citation_from_data(data).model_dump()
            {'docket_category': <ShortDocketCategory.GR: 'GR'>, 'docket_serial': 'L-63915', 'docket_date': datetime.date(1985, 4, 24), 'docket': 'GR L-63915, Apr. 24, 1985', 'phil': '220 Phil. 422', 'scra': '136 SCRA 27', 'offg': None}

        Args:
            data (dict): See originally scraped `details.yaml` converted to dict

        Returns:
            Citation: A citation object
        """  # noqa: E501
        docket_data = {}
        if cite := extract_docket_from_data(data):  # Set docket, if present.
            docket_data = dict(
                docket=str(cite),  # see Docket __str__
                docket_category=ShortDocketCategory(cite.short_category),
                docket_serial=cite.serial_text,
                docket_date=cite.docket_date,
            )
        return Citation(
            **docket_data,  # type: ignore
            phil=Report.extract_from_dict(data, "phil"),
            scra=Report.extract_from_dict(data, "scra"),
            offg=Report.extract_from_dict(data, "offg"),
        )

    @classmethod
    def extract_citations(cls, text: str) -> Iterator[Self]:
        """Combine `Docket`s (which have `Reports`), and filtered `Report` models,
        if they exist.

        Examples:
            >>> text = "<em>Gatchalian Promotions Talent Pool, Inc. v. Atty. Naldoza</em>, 374 Phil 1, 10-11 (1999), citing: <em>In re Almacen</em>, 31 SCRA 562, 600 (1970).; People v. Umayam, G.R. No. 147033, April 30, 2003; <i>Bagong Alyansang Makabayan v. Zamora,</i> G.R. Nos. 138570, 138572, 138587, 138680, 138698, October 10, 2000, 342 SCRA 449; Villegas <em>v.</em> Subido, G.R. No. 31711, Sept. 30, 1971, 41 SCRA 190;"
            >>> results = [c.model_dump(exclude_none=True) for c in Citation.extract_citations(text)]
            >>> len(results)
            5

        Yields:
            Iterator[Self]: Matching Citations found in the text.
        """  # noqa: E501
        from .helpers import filtered_reports

        def extract_report(obj):
            if isinstance(obj, Report):
                return cls(
                    docket=None,
                    docket_category=None,
                    docket_serial=None,
                    docket_date=None,
                    phil=obj.phil,
                    scra=obj.scra,
                    offg=obj.offg,
                )

        def extract_docket(obj):
            if isinstance(obj, CITATION_OPTIONS) and obj.ids:
                return cls(
                    docket=str(obj),  # see Docket __str__
                    docket_category=ShortDocketCategory(obj.short_category),
                    docket_serial=obj.serial_text,
                    docket_date=obj.docket_date,
                    phil=obj.phil,
                    scra=obj.scra,
                    offg=obj.offg,
                )

        if dockets := list(extract_dockets(text)):
            if reports := list(Report.extract_report(text)):
                if undocketed := filtered_reports(text, dockets, reports):
                    for docket in dockets:
                        if obj := extract_docket(docket):
                            if not obj.is_statute:
                                yield obj
                    for report in undocketed:
                        if obj := extract_report(report):
                            yield obj
                else:
                    for docket in dockets:
                        if obj := extract_docket(docket):
                            if not obj.is_statute:
                                yield obj
                    for report in reports:
                        if obj := extract_report(report):
                            yield obj
            else:
                for docket in dockets:
                    if obj := extract_docket(docket):
                        if not obj.is_statute:
                            yield obj
        else:
            if reports := list(Report.extract_report(text)):
                for report in reports:
                    if obj := extract_report(report):
                        yield obj

    @classmethod
    def extract_citation(cls, text: str) -> Self | None:
        """Thin wrapper around `cls.extract_citations()`.

        Examples:
            >>> sample = "Gatchalian Promotions Talent Pool, Inc. v. Atty. Naldoza, 374 Phil 1, 10-11 (1999)"
            >>> Citation.extract_citation(sample).model_dump(exclude_none=True)
            {'phil': '374 Phil 1'}

        Args:
            text (str): Text to look for Citations

        Returns:
            Self | None: First matching Citation found in the text.
        """  # noqa: E501
        try:
            return next(cls.extract_citations(text))
        except StopIteration:
            return None


class CitationBasedStatutes(Enum):
    BAR = [
        803,
        1922,
        1645,
        850,
        287,
        1132,
        1755,
        1960,
        209,
        1153,
        411,
        356,
    ]
    ADMIN = [
        r"(?:\d{1,2}-){3}SC\b",
        r"99-10-05-0\b",
    ]

    @property
    def regex(self) -> str:
        return r"(?:" + "|".join(str(i) for i in self.value) + r")"

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex)
