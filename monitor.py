import time
from datetime import datetime

import psutil

from config import ALERT_THRESHOLD, WEIGHTS
from db import is_whitelisted, log_event
from scoring import score_process


def format_time(create_time):
    if create_time > 0:
        return datetime.fromtimestamp(create_time).strftime("%H:%M:%S")
    return "--:--:--"


def monitor_once(seen):
    current = set()
    items = []

    for proc in psutil.process_iter(["pid", "name", "create_time", "exe"]):
        try:
            info = proc.info
            pid = int(info.get("pid", -1))
            create_time = float(info.get("create_time", 0.0))
        except (psutil.AccessDenied, psutil.NoSuchProcess, TypeError, ValueError):
            continue

        current.add((pid, create_time))
        items.append((create_time, proc))

    items.sort(key=lambda item: item[0])

    for create_time, proc in items:
        try:
            info = proc.info
            pid = int(info.get("pid", -1))
            create_time = float(info.get("create_time", 0.0))
        except (psutil.AccessDenied, psutil.NoSuchProcess, TypeError, ValueError):
            continue

        if (pid, create_time) in seen:
            continue

        name = str(info.get("name", "unknown") or "unknown")

        exe = ""
        try:
            exe = proc.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

        started = format_time(create_time)
        print("[NEW]", started, pid, name, exe)

        if is_whitelisted(name):
            print("[WHITELISTED]", started, pid, name)
            continue

        result = score_process(exe, name)
        score = result[0]
        reasons = result[1]

        if score >= ALERT_THRESHOLD:
            for rule in reasons:
                weight = WEIGHTS.get(rule, 0)
                print("[SUSPECT]", started, pid, name, score, rule)
                log_event(pid, name, exe, rule, weight, score)

    return current


def monitor_loop(sleep_interval=2.0):
    seen = set()

    while True:
        seen = monitor_once(seen)
        time.sleep(sleep_interval)