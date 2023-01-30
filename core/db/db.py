from core.service.templates import AbstractSessionContext
from sqlalchemy.orm import Session


class PostgresDB(AbstractSessionContext):
    db: Session

    def __init__(self, db):
        self.db = db

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def add(self, arg):
        self.db.add(arg)

    def exec(self):
        return self.db
