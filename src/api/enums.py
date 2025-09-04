from enum import IntEnum, StrEnum


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
