from dataclasses import dataclass, field
from enum import Enum


class VacancyStatus(Enum):
    NEW = 'new'
    APPLIED = 'applied'
    INTERVIEW = 'interview'
    REJECTED = 'rejected'

@dataclass
class Vacancy:
    company: str
    title: str
    salary: int | None
    status: VacancyStatus
    technologies: list[str] = field(default_factory=list)