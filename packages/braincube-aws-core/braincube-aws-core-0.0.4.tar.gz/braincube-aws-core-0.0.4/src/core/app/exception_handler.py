from json import dumps
from http import HTTPStatus
from abc import ABC, abstractmethod


class ExceptionHandler(ABC):

    @abstractmethod
    def handle(self, error: Exception) -> tuple[HTTPStatus, str, dict]:
        raise NotImplementedError()


class BaseExceptionHandler(ExceptionHandler):
    def handle(self, error: Exception) -> tuple[HTTPStatus, str, dict]:
        print(f"error:: {error}")
        return HTTPStatus.BAD_REQUEST, dumps({"message": str(error)}), dict()
