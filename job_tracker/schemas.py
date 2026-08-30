from pydantic import BaseModel, Field, field_validator
from job_tracker.models import VacancyStatus

class VacancyResponse(BaseModel):
    company: str
    title: str
    salary: int | None
    status: VacancyStatus
    technologies: list[str]

class VacancyCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    salary: int | None = Field(default=None, gt=0)
    technologies: list[str] = Field(default_factory=list)

    @field_validator("company", "title")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value

class VacancyStatusUpdate(BaseModel):
    status: VacancyStatus