#!/usr/bin/env python3

"""Functionality that might change during runtime
"""
import logging
import re
from contextlib import suppress
from datetime import datetime
from subprocess import CalledProcessError
from typing import MutableMapping, Optional

from docker_shaper.utils import process_output


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.dynamic")


def short_id(docker_id: str) -> str:
    """Return the 10-digit variant of a long docker ID
    >>> short_id("sha256:abcdefghijklmnop")
    'abcdefghij'
    """
    assert docker_id.startswith("sha256:")
    return docker_id[7:17]


def event_from(line: str):
    """Reads a line from event log and turns it into a tuple containing the data"""
    match = re.match(r"^(.*) \((.*)\)$", line)
    assert match, f"line did not match the expected format: {line!r}"
    cmd, params = match.groups()
    timestamp, object_type, operator, *cmd, uid = cmd.split(" ")
    assert len(timestamp) == 35
    assert (operator in {"exec_create:", "exec_start:", "health_status:"}) == bool(
        cmd
    ), f"{operator=} {cmd=} {line=}"
    assert object_type in {
        "container",
        "network",
        "image",
        "volume",
        "builder",
    }, f"{object_type}"
    assert operator in {
        "create",
        "destroy",
        "attach",
        "connect",
        "disconnect",
        "start",
        "die",
        "pull",
        "push",
        "tag",
        "save",
        "delete",
        "untag",
        "prune",
        "commit",
        "unpause",
        "resize",
        "exec_die",
        "exec_create:",
        "exec_start:",
        "health_status:",
        "mount",
        "unmount",
        "archive-path",
        "rename",
        "kill",
        "stop",
        "top",
        "pause",
    }, f"{operator}"
    assert len(uid) == 64 or (object_type, operator) in {
        ("image", "pull"),
        ("image", "push"),
        ("image", "tag"),
        ("image", "untag"),
        ("image", "save"),
        ("image", "delete"),
        ("image", "prune"),
        ("volume", "prune"),
        ("container", "prune"),
        ("network", "prune"),
        ("builder", "prune"),
    }, f"{len(uid)=} {(object_type, operator)}"
    return (
        int(
            datetime.strptime(
                f"{timestamp[:26]}{timestamp[-6:]}", "%Y-%m-%dT%H:%M:%S.%f%z"
            ).timestamp()
        ),
        object_type,
        operator,
        cmd,
        uid,
        dict(p.split("=") for p in params.split(", ")),
    )


def id_from(name: str) -> Optional[str]:
    """Looks up name using `docker inspect` and returns a 12 digit Docker ID"""
    with suppress(CalledProcessError):
        log().debug("resolve %s", name)
        return short_id(
            name
            if name.startswith("sha256:")
            else process_output(f"docker inspect --format='{{{{.Id}}}}' {name}")
        )
    return None


def lookup_id(ids: MutableMapping[str, Optional[str]], name: str) -> Optional[str]:
    """Looks up a given @name in @ids and resolves it first if not yet given"""
    if name not in ids:
        ids[name] = id_from(name)
    return ids[name]


def handle_docker_event_line(global_state, line):
    """Read a `docker events` line and maintain the last-used information"""
    #    print("||", line)
    ids = {}

    tstamp, object_type, operator, _cmd, _uid, params = event_from(line)
    if not object_type == "container" or operator == "prune":
        return
    log().debug("handle docker event %s", (tstamp, _uid[:12], operator, params["image"]))
    if not (referenced_image_id := lookup_id(ids, params["image"])):
        return

    print(tstamp, object_type, operator, _cmd, _uid, params)
    return

    GLOBALS["EVENT_HORIZON"] = min(GLOBALS["EVENT_HORIZON"], tstamp)
    referenced[referenced_image_id] = max(
        referenced.setdefault(referenced_image_id, tstamp), tstamp
    )
