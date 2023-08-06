#!/usr/bin/env python3

import asyncio
import functools
import json
import logging
import os
import sys
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from typing import MutableMapping

import yaml
from quart import Quart, render_template, request, websocket

from docker_shaper import dynamic
from docker_shaper.docker_stuff import watch_container, watch_containers, watch_images
from docker_shaper.utils import read_process_output, watchdog


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.server")


@dataclass
class GlobalState:
    intervals: MutableMapping[str, float]
    ids: MutableMapping[str, object]
    images: MutableMapping[str, object]
    containers: MutableMapping[str, object]

    def __init__(self):
        self.intervals = {
            "state": 2,
            "image_stats": 2,
            "image_update": 2,
            "container_update": 2,
        }
        self.ids = {}
        self.images = {}
        self.containers = {}

        self.counter = 0

    def dump(self):
        print(self.intervals)
        print(f"counter: {self.counter}")
        print(f"images: {len(self.images)}")
        print(f"containers: {len(self.containers)}")


def label_filter(label_values):
    return ",".join(
        w.replace("artifacts.lan.tribe29.com:4000", "A")
        for key, l in label_values.items()
        if key
        in (
            "org.tribe29.base_image",
            "org.tribe29.cmk_branch",
            "org.tribe29.cmk_edition_short",
            "org.tribe29.cmk_hash",
            "org.tribe29.cmk_version",
        )
        for w in l.split()
        if not (w.startswith("sha256") or len(w) == 64)
    )


def jobname_from(binds):
    candidates = [
        d.replace("/home/jenkins/workspace/", "").replace("/checkout", "")
        for b in binds or []
        for d in (b.split(":")[0],)
        if "workspace" in d
    ]
    if not len(candidates) == len(set(candidates)):
        print(binds)
    return candidates and candidates[0] or "--"


def cpu_perc(cpu_stats, last_cpu_stats):
    if not (
        cpu_stats
        and "system_cpu_usage" in cpu_stats
        and last_cpu_stats
        and "system_cpu_usage" in last_cpu_stats
    ):
        return 0
    return (
        (cpu_stats["cpu_usage"]["total_usage"] - last_cpu_stats["cpu_usage"]["total_usage"])
        / (cpu_stats["system_cpu_usage"] - last_cpu_stats["system_cpu_usage"])
        * cpu_stats["online_cpus"]
    )


def timestamp_from(string):
    with suppress(ValueError):
        return datetime.strptime(string[:26], "%Y-%m-%dT%H:%M:%S.%f")
    return None


@watchdog
async def print_stats(registered):
    hostname = open("/etc/hostname").read().strip()
    while True:
        stats = [
            {
                "short_id": cnt["short_id"],
                "name": cnt["name"],
                "usage": mem_stats.get("usage", 0),
                "cmd": " ".join(cnt["show"]["Config"]["Cmd"]),
                "job": jobname_from(
                    cnt["show"]["HostConfig"]["Binds"]
                    or list(cnt["show"]["Config"]["Volumes"] or [])
                ),
                "cpu": cpu_perc(cpu_stats, last_cpu_stats),
                "created_at": timestamp_from(cnt["show"]["Created"]),
                "started_at": timestamp_from(cnt["show"]["State"]["StartedAt"]),
                "status": cnt["show"]["State"]["Status"],
                "hints": label_filter(cnt["show"]["Config"]["Labels"]),
                "pid": int(cnt["show"]["State"]["Pid"]),
                "container": cnt["container"],
            }
            for cnt, mem_stats, cpu_stats, last_cpu_stats in (
                (
                    c,
                    c["stats"].get("memory_stats", {}),
                    c["stats"]["cpu_stats"],
                    c["last_stats"].get("cpu_stats"),
                )
                for c in registered.values()
                if c.keys() > {"short_id", "name", "stats"}
            )
        ]

        os.system("clear")
        print(f"=[ {hostname} ]======================================")
        print(
            f"{'ID':<12}  {'NAME':<25}"
            f" {'PID':>9}"
            f" {'CPU':>9}"
            f" {'MEM':>9}"
            f" {'UP':>9}"
            f" {'STATE':>9}"
            f" {'JOB':<60}"
            f" {'HINTS'}"
        )
        now = datetime.now()
        for s in sorted(stats, key=lambda e: e["pid"]):
            tds = int((now - (s["started_at"] or s["created_at"])).total_seconds())
            col_td = "\033[1m\033[91m" if tds // 3600 > 5 else ""
            dur_str = f"{tds//86400:2d}d+{tds//3600%24:02d}:{tds//60%60:02d}"
            col_mem = "\033[1m\033[91m" if s["usage"] >> 30 > 2 else ""
            mem_str = f"{(s['usage']>>20)}MiB"
            col_cpu = "\033[1m\033[91m" if s["cpu"] > 2 else ""
            container_is_critical = (
                (s["started_at"] and tds // 3600 > 5)
                or s["status"] == "exited"
                or not s["started_at"]
            )
            col_cpu = "\033[1m\033[91m" if s["cpu"] > 2 else ""
            print(
                f"{s['short_id']:<12}  {s['name']:<25}"
                f" {s['pid']:>9}"
                f" {col_cpu}{int(s['cpu'] * 100):>8}%\033[0m"
                f" {col_mem}{mem_str:>9}\033[0m"
                f" {col_td}{dur_str}\033[0m"
                f" {s['status']:>9}"
                f" {s['job']:<60}"
                f" {s['hints']}"
            )
            # if (
            #    (s["started_at"] and tds // 3600 > 5)
            #    or s["status"] == "exited"
            #    or not s["started_at"]
            # ):
            #    log(f"remove {s['short_id']}")
            #    await s["container"].delete(force=True)
        print(
            f"{'TOTAL':<12}  {len(stats):<25}"
            f" {'':>9}"
            f" {int(sum(s['cpu'] for s in stats)*1000) / 10:>8}%\033[0m"
            f" {int(sum(s['usage'] for s in stats) / (1<<30)*10) / 10:>6}GiB\033[0m"
            f" {''}"
            f" {'':>9}"
            f" {'':<60}"
            f" {''}"
        )
        await asyncio.sleepp(global_state.intervals["container_stats"])


@watchdog
async def print_state(global_state):
    while True:
        global_state.counter += 1
        global_state.dump()
        await asyncio.sleep(global_state.intervals["state"])


def no_serve():
    global_state = GlobalState()
    with suppress(KeyboardInterrupt, BrokenPipeError):
        # asyncio.ensure_future(print_stats(registered))
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(
            read_process_output(
                "docker events",
                lambda *args: getattr(dynamic, "handle_docker_event_line")(None, *args),
            )
        )
        asyncio.get_event_loop().run_forever()


def serve():
    """"""
    app = Quart(__name__)
    global_state = GlobalState()

    @app.route("/shutdown")  # , methods=['POST'])
    def shutdown():
        app.terminator.set()
        return "Server shutting down..."

    @watchdog
    async def self_destroy():
        await app.terminator.wait()
        print("BOOM")
        app.shutdown()
        asyncio.get_event_loop().stop()
        print("!!!!")

    @app.route("/", methods=["GET", "POST"])
    async def hello_world():
        return await render_template(
            "result.html",
            result={
                "foo": 23,
                "bar": 42,
            },
        )

    @app.before_serving
    async def create_db_pool():
        asyncio.ensure_future(self_destroy())
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(
            read_process_output(
                "docker events",
                lambda *args: getattr(dynamic, "handle_docker_event_line")(None, *args),
            )
        )

    app.terminator = asyncio.Event()
    app.run(
        host="0.0.0.0",
        port=5432,
        debug=False,
        use_reloader=False,
        loop=asyncio.get_event_loop(),
    )
