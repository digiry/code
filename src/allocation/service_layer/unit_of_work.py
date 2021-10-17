import abc

from allocation import config

from allocation.adapters import repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    # 저자들이 더 고민해본 Context manager 구문으로 암묵적 commit, rollback 처리.
    # 하지만 명시적 commit을 더 선호한다.
    # def __exit__(self, exn_type, exn_value, traceback):
    #     if exn_type is None:
    #         self.commit()
    #     else:
    #         self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
