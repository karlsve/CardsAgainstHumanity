import asyncio
import json
import sqlite3 as sql
from types import FunctionType
from typing import Dict

import websockets as ws


class GameServer(object):
    def __init__(self, dbname, ip, port):
        self.ip = ip
        self.port = port
        self.endpoints: Dict[str, Endpoint.__class__] = {}
        self.methods = {}
        self.db = sql.connect("{0}.db".format(dbname))

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


class Endpoint:
    def __init__(self, path, socket, methods):
        self.path = path
        self.socket = socket
        self.methods = methods
        self.init()

    def init(self):
        pass

    async def send(self, obj):
        js = json.dumps(obj)
        print(js)
        await self.socket.send(js)

    async def handle(self):
        try:
            async for message in self.socket:
                gm = json.loads(message)
                if "method" in gm:
                    if gm["method"] in self.methods:
                        methoddict = self.methods[gm["method"]]
                        if all(k if k in gm else False for k in methoddict["required"]):
                            method = methoddict["callable"]
                            await method(self, gm)
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
        print("Connection to {0} disconnected.".format(self.path))
