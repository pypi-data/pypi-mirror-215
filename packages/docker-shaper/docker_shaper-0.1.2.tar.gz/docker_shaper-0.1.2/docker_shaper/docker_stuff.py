#!/usr/bin/env python3

import asyncio
import functools
import logging

from aiodocker import Docker, DockerError
from aiodocker.containers import *
from quart import Quart, render_template, request, websocket

from docker_shaper.utils import watchdog


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.docker_stuff")


@watchdog
async def watch_container(container, containers):
    name = "unknown"
    try:
        containers[container.id]["container"] = container
        containers[container.id]["short_id"] = (short_id := container.id[:12])
        containers[container.id]["show"] = await container.show()
        containers[container.id]["name"] = (name := containers[container.id]["show"]["Name"][1:])
        log().info(">> new container: %s %s", short_id, name)
        async for stats in container.stats():
            containers[container.id]["last_stats"] = containers[container.id].get("stats", {})
            containers[container.id]["stats"] = stats
            containers[container.id]["show"] = await container.show()
    except DockerError as exc:
        log().error("DockerError: %s", exc)
    finally:
        log().info("<< container terminated: %s %s", short_id, name)
        del containers[container.id]


@watchdog
async def watch_containers(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            log().info("crawl containers..")
            for container in await docker.containers.list(all=True):
                if container.id not in global_state.containers:
                    global_state.containers[container.id] = {}
                    asyncio.ensure_future(watch_container(container, global_state.containers))

            await asyncio.sleep(global_state.intervals["container_update"])
    finally:
        await docker.close()


@watchdog
async def watch_images(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            log().info("crawl images..")
            for image in await docker.images.list(all=True):
                log().debug(image)
                if image["Id"] not in global_state.images:
                    global_state.images[image["Id"]] = {}
            #                    asyncio.ensure_future(watch_container(container, registered))

            await asyncio.sleep(global_state.intervals["image_update"])
    finally:
        await docker.close()
