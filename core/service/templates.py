from abc import ABC, abstractmethod
from typing import Optional


class AbstractSessionContext(ABC):
    db: Optional

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    def add(self):
        raise NotImplementedError

    @abstractmethod
    def exec(self):
        raise NotImplementedError


class AbstractCRUD(ABC):

    db: AbstractSessionContext

    def __init__(self, db):
        self.db = db

    @abstractmethod
    def get_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError


class AbstractService(ABC):

    crud_controller: AbstractCRUD

    def __init__(self, crud_controller):
        self.crud_controller = crud_controller

    @abstractmethod
    def get_list_of_items(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_item(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_item(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update_item(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, *args, **kwargs):
        raise NotImplementedError
