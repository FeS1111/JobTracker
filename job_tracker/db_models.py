from sqlalchemy import Enum as SQLEnum, Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from job_tracker.database import Base
from job_tracker.models import VacancyStatus


vacancy_technologies = Table(
    "vacancy_technology",
    Base.metadata,

    Column(
        "vacancy_id",
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "technology_id",
        ForeignKey("technologies.id", ondelete="CASCADE"),
        primary_key=True,
    )
)


class VacancyORM(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    salary: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    status: Mapped[VacancyStatus] = mapped_column(
        SQLEnum(VacancyStatus,
            name='vacancy_status',
            values_callable=lambda enum:[
              status.value for status in enum
            ],
        ),
        nullable=False
    )

    technologies: Mapped[list["TechnologyORM"]] = relationship(
        secondary=vacancy_technologies,
        back_populates="vacancies",
    )

    def __repr__(self) -> str:
        return (
            f"VacancyORM("
            f"id={self.id}, "
            f"company='{self.company}', "
            f"title='{self.title}', "
            f"salary={self.salary}, "
            f"status={self.status}"
            f")"
        )


class TechnologyORM(Base):
    __tablename__ = 'technologies'

    id: Mapped[int]  = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    vacancies: Mapped[list[VacancyORM]] = relationship(
        secondary=vacancy_technologies,
        back_populates="technologies",
    )

    def __repr__(self) -> str:
        return (
            f"TechnologyORM("
            f"id={self.id}, "
            f"name='{self.name}', "
            f")"
        )