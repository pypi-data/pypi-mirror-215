#!/usr/bin/env python3

import asyncio
from quart import Quart, render_template, request, websocket
from docker_shaper.utils import watchdog


app = Quart(__name__)

@watchdog
async def watch_containers():
    while True:
        print("WDx")
        await asyncio.sleep(5)


@app.route("/shutdown")  # , methods=['POST'])
def shutdown():
    app.terminator.set()
    return "Server shutting down..."


@app.route("/", methods=["GET", "POST"])
async def hello_world():
    return await render_template(
        "result.html",
        result={
            "foo": 23,
            "bar": 42,
        },
    )


@watchdog
async def self_destroy():
    await app.terminator.wait()
    print("BOOM")
    app.shutdown()
    asyncio.get_event_loop().stop()
    print("!!!!")


@app.before_serving
async def create_db_pool():
    asyncio.ensure_future(self_destroy())
    asyncio.ensure_future(watch_containers())


def serve():
    app.terminator = asyncio.Event()
    app.run(
        host="0.0.0.0",
        port=5432,
        # debug=True,
        loop=asyncio.get_event_loop()
    )
