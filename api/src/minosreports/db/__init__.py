from collections.abc import Callable, Generator
from typing import Any

from sqlalchemy import SelectBase, create_engine, func, select
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import sessionmaker

from minosreports.context import Context
context = Context.get(fallback_to_class=True)

Session = sessionmaker(bind=create_engine(url=context.database_url, echo=False))

def dbsession(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to create an SQLAlchemy ORM session object and wrap the function
    inside the session. A `session` argument is automatically set. Commit is
    automatically performed when the function finish (and before returning to
    the caller). Should any exception arise, rollback of the transaction is also
    automatic.
    """

    def inner(*args: Any, **kwargs: Any) -> Any:
        with Session.begin() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return inner


def gen_dbsession() -> Generator[OrmSession, None, None]:
    """FastAPI's Depends() compatible helper to provide a began DB Session"""
    with Session.begin() as session:
        yield session


def dbsession_manual(func):
    """Decorator to create an SQLAlchemy ORM session object and wrap the function
    inside the session. A `session` argument is automatically set. Transaction must
    be managed by the developer (e.g. perform a commit / rollback).
    """

    def inner(*args, **kwargs):
        with Session() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return inner


def count_from_stmt(session: OrmSession, stmt: SelectBase) -> int:
    """Count all records returned by any statement `stmt` passed as parameter"""
    return session.execute(
        select(func.count()).select_from(stmt.subquery())
    ).scalar_one()
