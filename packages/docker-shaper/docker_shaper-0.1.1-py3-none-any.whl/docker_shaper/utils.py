#!/usr/bin/env python3

"""Common stuff shared among modules"""

import asyncio
import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from pathlib import Path
from typing import cast

from asyncinotify import Event, Inotify, Mask


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.utils")


def watchdog(
    afunc: Callable
) -> Callable:
    """Watch for async functions to throw an unhandled exception"""

    @wraps(afunc)
    async def run(*args: object, **kwargs: object) -> object:
        """Run wrapped function and handle exceptions"""
        try:
            return await afunc(*args, **kwargs)
        except asyncio.CancelledError:
            log().info("Task cancelled: `%s`", afunc.__name__)
        except KeyboardInterrupt:
            log().info("KeyboardInterrupt in `%s`", afunc.__name__)
        except Exception:  # pylint: disable=broad-except
            log().exception("Exception in `%s`:", afunc.__name__)
            asyncio.get_event_loop().stop()
        return None

    return run


@watchdog
async def watch_changes(
    path: Path,
    callback: Callable,
    *,
    queue: asyncio.Queue = asyncio.Queue(),
    mask: Mask = Mask.CLOSE_WRITE | Mask.MOVED_TO | Mask.CREATE,
    postpone: bool = False,
    timeout: float = 2,
) -> None:
    """Controllable, timed filesystem watcher"""

    # pylint: disable=too-many-locals

    async def fuse_fn(queue: asyncio.Queue[str], timeout: float) -> None:
        await asyncio.sleep(timeout)
        await queue.put("timeout")

    def task(name: str) -> asyncio.Task[str | Event]:
        """Creates a task from a name identifying a data source to read from"""
        return asyncio.create_task(
            cast(asyncio.Queue[str] | Inotify, {"inotify": inotify, "mqueue": queue}[name]).get(),
            name=name,
        )

    with Inotify() as inotify:
        inotify.add_watch(path, mask)
        fuse = None
        changed_files = set()
        tasks = set(map(task, ("inotify", "mqueue")))

        while True:
            done, tasks = await asyncio.wait(
                fs=tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for event in done:
                event_type, event_value = event.get_name(), event.result()
                tasks.add(task(event_type))
                if event_type == "inotify":
                    assert isinstance(event_value, Event)
                    if event_value.path:
                        changed_files.add(event_value.path)
                    if postpone and fuse:
                        fuse.cancel()
                        del fuse
                        fuse = None
                    if not fuse:
                        fuse = asyncio.create_task(fuse_fn(queue, timeout))
                elif event_type == "mqueue":
                    if event_value == "timeout":
                        del fuse
                        fuse = None
                        callback(changed_files)
                        changed_files.clear()
