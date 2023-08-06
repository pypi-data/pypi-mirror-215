import os
import time
import json
from functools import reduce
from inspect import signature
from dataclasses import dataclass
from typing import get_args, get_origin

from .app_event import AppEvent
from .app_controller import AppController
from .exception_handler import ExceptionHandler, BaseExceptionHandler
from .data import HTTPRequest, HTTPResponse, http_event_to_request, EventType
from ..utils.convert import JSONEncoder
from ..utils.data import import_modules, import_directories
from ..di.data import qualifier_to_data
from ..di.injector import init_config, provide


@dataclass()
class _Route:
    func: callable
    request_type: type | None
    dependencies: list[tuple[type, str | None]]


@dataclass()
class _Trigger:
    func: callable
    dependencies: list[tuple[type, str | None]]


class AppModule:
    """AWS lambda application main entry point.
    :param controllers: Application controllers.
    :param modules: Modules to force import.
    :param directories: Directories to force import.
    """

    def __init__(self, controllers: list[AppController] = None,
                 events: list[AppEvent] = None,
                 ex_handler: ExceptionHandler = BaseExceptionHandler(),
                 modules: list[str] = None,
                 directories: list[str] = None):

        self._exception_handler = ex_handler

        # import files

        if modules:
            import_modules(modules)
        elif os.environ.get("IMPORT_MODULES"):
            import_modules(os.environ["IMPORT_MODULES"].split(","))

        root = os.environ["ROOT_DIRECTORY"] if os.environ.get("ROOT_DIRECTORY") else "/var/task/"

        if directories:
            import_directories(root, directories)
        elif os.environ.get("IMPORT_DIRECTORIES"):
            import_directories(root, os.environ["IMPORT_DIRECTORIES"].split(","))

        init_config()

        # events definition

        if events:
            self._triggers = reduce(lambda a, b: {**a, **b}, [e.triggers.copy() for e in events])

            for event_type, (handler, qualifier) in self._triggers.items():
                dependencies = list()
                data = qualifier_to_data(qualifier) if qualifier else dict()

                for key, value in signature(handler).parameters.items():
                    origin = get_origin(value.annotation)
                    cls = origin if origin else value.annotation
                    if cls is dict:
                        continue
                    dependencies.append((cls, data.get(key)))

                self._triggers[event_type] = _Trigger(handler, dependencies)
        else:
            self._triggers = dict()

        # controllers definition

        if controllers:
            self._routes = reduce(lambda a, b: {**a, **b}, [c.routes.copy() for c in controllers])

            for resource, methods in self._routes.items():
                for method, (handler, qualifier) in methods.items():

                    dependencies = list()
                    request_type: type | None = None
                    data = qualifier_to_data(qualifier) if qualifier else dict()

                    for key, value in signature(handler).parameters.items():
                        origin = get_origin(value.annotation)
                        cls = origin if origin else value.annotation
                        if cls is HTTPRequest:
                            args = get_args(value.annotation)
                            request_type = args[0] if len(args) > 0 else dict
                            continue
                        dependencies.append((cls, data.get(key)))

                    if not request_type:
                        raise Exception("HTTPRequest param is not provided.")
                    self._routes[resource][method] = _Route(handler, request_type, dependencies)
        else:
            self._routes = dict()

    async def serve(self, event: dict, context):

        handler = None

        for key, value in {
            "httpMethod": self._serve_http,
            "triggerSource": self._serve_cognito
        }.items():
            if key in event:
                handler = value
                break

        if event.get("Records") and event["Records"]["eventSource"] == "aws:sqs":
            handler = self._serve_sqs

        if not handler:
            raise Exception("Handler not found.")

        return await handler(event, context)

    async def _serve_cognito(self, event: dict, context) -> dict:

        cognito_key = str(EventType.cognito.value)
        combination_key = f"{cognito_key}::{event['triggerSource']}"

        trigger = self._triggers.get(combination_key if combination_key in self._triggers else cognito_key)
        if not trigger:
            raise ValueError(f"unknown event: {cognito_key} source: {event.get('triggerSource')}")

        params = [await provide(cls, name) for cls, name in trigger.dependencies]
        params.append(event)

        return await trigger.func(*params)

    async def _serve_sqs(self, event: dict, context) -> dict:
        # TODO: implement
        pass

    async def _serve_http(self, event: dict, context) -> dict:

        try:
            start = time.time()

            route = self._routes[event["resource"]][event["httpMethod"]]
            if not route:
                raise ValueError(f"unknown route, resource: {event.get('resource')} method: {event.get('httpMethod')}")

            params = [await provide(cls, name) for cls, name in route.dependencies]
            params.append(http_event_to_request(route.request_type, event, context))

            response: HTTPResponse = await route.func(*params)

            status_code = response.status
            body = json.dumps(response.body, cls=JSONEncoder) if response.body else response.body
            headers = response.headers if response.headers else dict()
            headers["X-Process-Time"] = int((time.time() - start) * 1000)

        except Exception as error:
            status_code, body, headers = self._exception_handler.handle(error)

        return {
            "statusCode": status_code,
            "body": body,
            "headers": headers
        }
