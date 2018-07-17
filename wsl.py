import asyncio
import json
from datetime import date, time, datetime
from types import FunctionType
from typing import Dict

import websockets as ws


class Endpoint:
    def __init__(self, path, socket, methods):
        self.path = path
        self.socket = socket
        self.methods = methods
        self.init()

    def init(self):
        pass

    def shutdown(self):
        pass

    async def send(self, obj):
        data = json.dumps(obj, default=self._serialize)
        try:
            await self.socket.send(data)
        except Exception:
            await self.close()

    def _serialize(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, date):
            serial = obj.isoformat()
            return serial

        if isinstance(obj, time):
            serial = obj.isoformat()
            return serial

        if isinstance(obj, datetime):
            serial = obj.isoformat
            return serial

        try:
            return obj.__dict__
        finally:
            print(obj)
            return ""

    async def handle(self):
        try:
            async for message in self.socket:
                data = json.loads(message)
                if "method" in data:
                    if data["method"] in self.methods:
                        method_dict = self.methods[data["method"]]
                        if all(k if k in data else False for k in method_dict["required"]):
                            method = method_dict["callable"]
                            await method(self, data)
                        else:
                            await self.send({"Error": "Missing required arguments"})
                    else:
                        await self.send({"Error": "Unknown method given."})
                else:
                    await self.send({"Error": "No method given."})
        finally:
            await self.close()

    async def close(self):
        await self.socket.close()
        self.shutdown()
        print("Client disconnected from {0} .".format(self.path))


class WebSocketServer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.endpoints: Dict[str, Endpoint.__class__] = {}
        self.methods: Dict[str, FunctionType] = {}

    def start(self):
        asyncio.get_event_loop().run_until_complete(
            ws.serve(self.handle_request, self.ip, self.port))
        asyncio.get_event_loop().run_forever()

    async def handle_request(self, socket, path):
        if path in self.endpoints:
            endpoint = self.endpoints[path]
            print("Accepting request on known path: {0}".format(path))
            if endpoint is not None:
                consumer = endpoint(path, socket, self.methods[endpoint.__qualname__])
                await consumer.handle()
            else:
                print("Invalid endpoint")
        else:
            print("Unknown path: {0}".format(path))
        socket.close()

    def _create_endpoint_if_not_exists(self, path):
        if path not in self.endpoints:
            self.endpoints[path] = None

    def endpoint(self, path):
        def handler(clazz: Endpoint.__class__):
            if issubclass(clazz, Endpoint):
                self._create_endpoint_if_not_exists(path)
                self.endpoints[path] = clazz
                self._create_methods_if_not_exists(clazz)
                print("Adding path {0} with endpoint {1}".format(path, clazz.__name__))
            else:
                print("Not adding path {0} with endpoint {1}. Reason: No endpoint.".format(path, clazz.__name__))
        return handler

    def _create_methods_if_not_exists(self, clazz):
        if clazz not in self.methods:
            self.methods[clazz] = {}

    def method(self, *argv):
        def handler(func: FunctionType):
            clazz = func.__qualname__.rsplit('.', 1)[0]
            self._create_methods_if_not_exists(clazz)
            self.methods[clazz][func.__name__] = {"callable": func, "required": argv}
        return handler

