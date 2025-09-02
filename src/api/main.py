from enum import Enum, IntEnum, StrEnum
from typing import Annotated
from urllib.parse import quote, urlencode

from fastapi import FastAPI
from pydantic import AliasChoices, BaseModel, Field, PlainSerializer

app = FastAPI()


class ExperienceLevel(IntEnum):
    """Standard codes for the LinkedIn Jobs experience level filter."""

    internship = 1
    entry = 2
    associate = 3
    mid_senior = 4
    director = 5
    executive = 6


class JobType(StrEnum):
    """Standard codes for the LinkedIn Jobs job type filter."""

    full_time = 'F'
    part_time = 'P'
    contract = 'C'
    temporary = 'T'
    internship = 'I'
    volunteer = 'V'


class WorkplaceSetup(IntEnum):
    """Standard codes for the LinkedIn Jobs workplace setup filter."""

    onsite = 1
    hybrid = 2
    remote = 3


class SortBy(StrEnum):
    """Standard codes for the LinkedIn Jobs sort order options."""

    newest = 'DD'
    relevance = 'R'


def join_list(values: list[int | str | Enum]) -> str | None:
    """Serialize a list of values or enums as a comma-separated string."""
    return (
        ','.join(str(x.value) if isinstance(x, Enum) else str(x) for x in values)
        if values
        else None
    )


def bool_lower(flag: bool | None) -> str | None:  # noqa: FBT001
    """Serialize a boolean as `'true'` or `'false'`."""
    return None if flag is None else ('true' if flag else 'false')


def f_TPR(seconds: int | None) -> str | None:  # noqa: N802
    """Serialize a time range as LinkedIn's `'r{seconds}'` format."""
    return None if seconds is None else f'r{seconds}'


class BuildRequest(BaseModel):
    """LinkedIn Jobs search filters."""

    actively_hiring: Annotated[
        bool | None,
        Field(
            serialization_alias='f_AL',
            description='Return only jobs at companies marked as actively hiring.',
        ),
        PlainSerializer(bool_lower, return_type=str | None),
    ] = None

    extra_locations: Annotated[
        list[int] | None,
        Field(serialization_alias='f_PP', description='Multiple custom location IDs.'),
        PlainSerializer(join_list, return_type=str | None),
    ] = None

    spell_correction: Annotated[
        bool | None,
        Field(
            serialization_alias='spellCorrectionEnabled',
            description='Enable or disable LinkedIn spell correction.',
        ),
        PlainSerializer(bool_lower, return_type=str | None),
    ] = None

    time_range: Annotated[
        int | None,
        Field(ge=0, serialization_alias='f_TPR', description='Time range in seconds.'),
        PlainSerializer(f_TPR, return_type=str | None),
    ] = None

    distance: Annotated[
        int | None,
        Field(
            ge=0, description='Search radius in miles (used with point locations like postcodes).'
        ),
    ] = None

    keywords: Annotated[str | None, Field(description='Search keywords.')] = None

    geo_id: Annotated[
        int | None,
        Field(
            serialization_alias='geoId',
            validation_alias=AliasChoices('geoId', 'geo_id'),
            description='Geographic location ID.',
        ),
    ] = None

    experience_levels: Annotated[
        list[ExperienceLevel] | None,
        Field(serialization_alias='f_E', description='Filter by experience level.'),
        PlainSerializer(join_list, return_type=str | None),
    ] = None

    job_functions: Annotated[
        list[str] | None,
        Field(serialization_alias='f_F', description='Filter by job function.'),
        PlainSerializer(join_list, return_type=str | None),
    ] = None

    job_types: Annotated[
        list[JobType] | None,
        Field(serialization_alias='f_JT', description='Filter by job type.'),
        PlainSerializer(join_list, return_type=str | None),
    ] = None

    easy_apply: Annotated[
        bool | None,
        Field(serialization_alias='f_EA', description='Return only jobs with Easy Apply.'),
        PlainSerializer(bool_lower, return_type=str | None),
    ] = None

    verified_jobs: Annotated[
        bool | None,
        Field(serialization_alias='f_VJ', description='Return only jobs marked as verified.'),
        PlainSerializer(bool_lower, return_type=str | None),
    ] = None

    network_jobs: Annotated[
        bool | None,
        Field(
            serialization_alias='f_JIYN', description='Return only jobs where you have connections.'
        ),
        PlainSerializer(bool_lower, return_type=str | None),
    ] = None

    workplace_setups: Annotated[
        list[WorkplaceSetup] | None,
        Field(serialization_alias='f_WT', description='Filter by workplace setup.'),
        PlainSerializer(join_list, return_type=str | None),
    ] = None

    sort_by: Annotated[
        SortBy | None, Field(serialization_alias='sortBy', description='Set result ordering.')
    ] = None


@app.post('/build')
async def build(req: BuildRequest) -> dict[str, str]:
    """Generate a custom LinkedIn job search URL."""
    base_url = 'https://www.linkedin.com/jobs/search'
    params = req.model_dump(by_alias=True, exclude_none=True)
    query = urlencode(params, quote_via=quote)
    return {'url': f'{base_url}?{query}' if query else base_url}
