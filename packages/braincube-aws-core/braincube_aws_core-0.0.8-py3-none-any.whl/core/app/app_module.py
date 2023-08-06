import os
import time
from json import dumps
from inspect import signature
from typing import get_args, get_origin

from .data import *
from .app_processor import AppProcessor
from .http_exception_handler import HttpExceptionHandler, BaseHttpExceptionHandler

from ..utils.convert import JSONEncoder
from ..utils.data import import_modules, import_directories
from ..di.data import qualifier_to_data
from ..di.injector import init_config, provide


class AppModule:
    """AWS lambda application main entry point.
    :param processors: AWS event resources.
    :param ex_handler: APIGateway global exception handler.
    :param modules: Modules to force import.
    :param directories: Directories to force import.
    """

    def __init__(self,
                 processors: list[AppProcessor] = None,
                 ex_handler: HttpExceptionHandler = BaseHttpExceptionHandler(),
                 modules: list[str] = None,
                 directories: list[str] = None):

        self._exception_handler = ex_handler

        # import files

        mods = modules.copy() if modules else (
            os.environ["IMPORT_MODULES"].split(",") if "IMPORT_MODULES" in os.environ else None)
        if mods:
            import_modules(mods)

        root = os.environ["ROOT_DIRECTORY"] if "ROOT_DIRECTORY" in os.environ else "/var/task/"
        dirs = directories.copy() if directories else (
            os.environ["IMPORT_DIRECTORIES"].split(",") if "IMPORT_DIRECTORIES" in os.environ else None)
        if dirs:
            import_directories(root, dirs)

        init_config()

        # events definition

        self._handlers = dict()

        if not processors:
            return

        for proc in processors:
            for event_alias, (func, qualifier) in proc.handlers.items():
                dependencies = list()
                payload_type: type | None = None
                data = qualifier_to_data(qualifier) if qualifier else dict()
                for key, value in signature(func).parameters.items():
                    origin = get_origin(value.annotation)
                    cls = origin if origin else value.annotation
                    if cls is proc.data_type:
                        args = get_args(value.annotation)
                        payload_type = args[0] if len(args) > 0 else dict
                        continue
                    dependencies.append((cls, data.get(key)))
                if not payload_type:
                    raise Exception(f"{str(proc.data_type)} param is not provided.")
                self._handlers[event_alias] = Handler(func, payload_type, dependencies)

    async def serve(self, event: dict, context):

        if "httpMethod" in event:
            return await self._serve_http(event, context)

        if "triggerSource" in event:
            event_type = EventType.cognito
        elif event.get("Records") and event["Records"]["eventSource"] == "aws:sqs":
            event_type = EventType.sqs
        else:
            event_type = None

        if event_type:
            return await self._serve_event(event_type, event, context)

        raise Exception("Handler not found.")

    async def _serve_event(self, event_type: EventType, event: dict, context):

        cognito_unique_key = f"{EventType.cognito.value}::{event['triggerSource']}"
        key = str(event_type.value) \
            if event_type is not EventType.cognito or (cognito_unique_key not in self._handlers) \
            else cognito_unique_key

        trigger = self._handlers.get(key)
        if not trigger:
            raise ValueError(f"unknown event: {key}")

        params = [
            *[await provide(c, n) for c, n in trigger.dependencies],
            convert_to_event_payload(trigger.payload_type, event, context)
        ]

        result = await trigger.func(*params)

        return result.dict(by_alias=True) if isinstance(result, BaseModel) else result

    async def _serve_http(self, event: dict, context):

        try:
            start = time.time()

            route = self._handlers[f"{event['resource']}::{event['httpMethod']}"]
            if not route:
                raise ValueError(f"unknown route, resource: {event['resource']} method: {event['httpMethod']}")

            params = [
                *[await provide(c, n) for c, n in route.dependencies],
                convert_to_http_request(route.payload_type, event, context)
            ]
            response: HTTPResponse = await route.func(*params)

            status_code = response.status
            body = dumps(response.body, cls=JSONEncoder) if response.body else response.body

            headers = {**http_headers.copy(), "X-Process-Time": int((time.time() - start) * 1000)}
            if response.headers:
                headers.update(response.headers)

        except Exception as error:
            status_code, body, headers = self._exception_handler.handle(error)

        return {
            "body": body,
            "headers": headers,
            "statusCode": status_code
        }
