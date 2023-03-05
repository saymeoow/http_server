import asyncio
import json
import python_http_parser as http_parser
from argparse import ArgumentParser
from datetime import date
from contextlib import asynccontextmanager
from functools import partial
from asrv.web.root import urls


def get_args():
    parser = ArgumentParser(
        prog='This is a server (c) {}\n'.format(date.today().year))
    parser.add_argument('-port', '--port', type=int, default=9001, help='Port')
    parser.add_argument('--host', default='localhost', help='Host')
    return parser.parse_known_args()


kn_args, ot_args = get_args()


async def start(app):
    print('Start Only')


async def stop_1(app):
    con = app.connection
    print(con)
    print('Stop_1 Only')


async def stop_2(app):
    con = app.connection
    print(con)
    print('Stop_2 Only')


async def start_stop_1(app):
    print('start_stop_1 run')
    yield
    print('start_stop_1 end')


async def start_stop_2(app):
    print('start_stop_2 run')
    yield
    print('start_stop_2 end')


class Controller(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('#' * 100)
        print(data.decode('utf-8').__repr__())
        req = http_parser.parse(data)
        print(json.dumps(dict(req), indent=4))
        for url in urls.urlpatterns:
            if url[0] == req['req_uri']:
                res = url[1](req)
                self.transport.write(res)
        self.transport.close()


class Server:
    on_start = []
    on_stop = []
    on_start_stop = []
    _bg_gen = []

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    @asynccontextmanager
    async def serve(self, factory):
        for cd in set(self.on_start):
            await cd(self)
        for gcb in set(self.on_start_stop):
            it = gcb(self).__aiter__()
            await it.__anext__()
            self._bg_gen.append(it)
        try:
            yield await factory()
        finally:
            print('\r')
            for it in self._bg_gen[::-1]:
                try:
                    await it.__anext__()
                except StopAsyncIteration:
                    ...
            for cb in self.on_stop:
                await cb(self)
            print('Server was stopped')
            
    async def start(self):
        loop = asyncio.get_running_loop()
        _server = partial(
            loop.create_server,
            lambda: Controller(),
            host=kn_args.host,
            port=kn_args.port,
        )
        async with self.serve(_server) as srv:
            await srv.serve_forever()


def run():
    srv = Server()
    srv.on_start = [start]
    srv.on_stop.extend([stop_1, stop_2])
    srv.on_start_stop.append(start_stop_1)
    srv.on_start_stop.append(start_stop_2)
    srv['connection'] = {}

    try:
        asyncio.run(srv.start())
    except KeyboardInterrupt:
        print('Stop application')
