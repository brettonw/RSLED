#! /usr/bin/env python3

import logging
import threading

from typing import NamedTuple
from time import time, sleep
from datetime import datetime

from zeroconf import (Zeroconf, IPVersion, ServiceBrowser, ServiceListener)
from const import _SVC_PROTOCOL_HTTP, ZEROCONF


def timestamp() -> int:
    return int(time() * 1000)


class DiscoveryAction(NamedTuple):
    action: str
    service_name: str
    timestamp: int = timestamp()

    def report(self):
        date = datetime.fromtimestamp(self.timestamp / 1000.0)
        print()
        print(f"{date} - {self.action} ({self.service_name[:-(len(_SVC_PROTOCOL_HTTP) + 1)]})")


class DiscoveryHandler(ServiceListener):
    @staticmethod
    def _report_device(zc: Zeroconf, discovery_action: DiscoveryAction):
        info = zc.get_service_info(_SVC_PROTOCOL_HTTP, discovery_action.service_name)

        # check to see if this is a reefLED
        isReefLED = False
        if (info is not None) and (info.properties is not None) and (len(info.properties.keys()) > 0):
            for key, value in info.properties.items():
                if value is not None:
                    if (key.decode("utf-8") == "hw_model") and (value.decode("utf-8").startswith("RSLED")):
                        isReefLED = True

        if isReefLED:
            discovery_action.report()
            addresses = info.parsed_scoped_addresses()
            port = f":{info.port}" if int(info.port) != 80 else ""
            print("  address" + ("es" if len(addresses) > 1 else "") + ": " +
                  ", ".join([f"{address}{port}" for address in addresses]))
            host: str = info.server[:-1] if info.server.endswith(".") else info.server
            host = (host[:-6] if host.endswith(".local") else host).lower()
            print(f"  host: {host}")
            if (info.properties is not None) and (len(info.properties.keys()) > 0):
                preface = "  properties:\n    "
                for key, value in info.properties.items():
                    if value is not None:
                        print(f"{preface}{key.decode("utf-8")}: {value.decode("utf-8") if isinstance(value, bytes) else value}")
                        preface = "    "
        else:
            #print("  no info")
            pass

    def __init__(self):
        # shared work queue and a synchronizing primitive for it
        self.work_queue: list[DiscoveryAction] = []
        self.work_queue_lock = threading.Lock()

    def enqueue(self, discovery_action: DiscoveryAction):
        with self.work_queue_lock:
            self.work_queue.append(discovery_action)

    def dequeue(self) -> DiscoveryAction | None:
        with self.work_queue_lock:
            return self.work_queue.pop() if len(self.work_queue) > 0 else None

    def perform(self, zc: Zeroconf):
        discovery_action = self.dequeue()
        while discovery_action is not None:
            if (discovery_action.action == "add") or (discovery_action.action == "update"):
                self._report_device(zc, discovery_action)
            discovery_action = self.dequeue()

    def add_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("add", service_name))

    def update_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("update", service_name))

    def remove_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("remove", service_name))

    def browse(self):
        zc = Zeroconf(ip_version=IPVersion.V4Only)
        logging.getLogger(ZEROCONF).setLevel(logging.DEBUG)
        ServiceBrowser(zc, _SVC_PROTOCOL_HTTP, self)
        print(f"\nbrowsing for {_SVC_PROTOCOL_HTTP} services (press [ctrl-c] to stop)...")
        try:
            while True:
                self.perform(zc)
                sleep(1)
        except KeyboardInterrupt:
            print("stopping...")
        finally:
            zc.close()


DiscoveryHandler().browse()
