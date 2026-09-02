from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

DATABASE_URL = (
    "postgresql+psycopg://"
    "job_tracker:job_tracker@localhost:5432/job_tracker"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

def get_db():
    with SessionLocal() as session:
        yield session

if __name__ == "__main__":
    from sqlalchemy import text

    with engine.connect() as connection:
        result = connection.execute(
            text(
                "select current_database(), current_user"
            )
        )

        print(result.one())