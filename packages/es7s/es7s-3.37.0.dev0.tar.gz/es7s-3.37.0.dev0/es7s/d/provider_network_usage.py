# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import typing as t
from collections import deque
from enum import unique

import psutil
import pytermor as pt
from psutil._common import snetio

from es7s.shared.dto import NetworkUsageInfo
from ._base import DataProvider


@unique
class UsageType(str, pt.ExtendedEnum):
    UPLOAD = enum.auto()
    DOWNLOAD = enum.auto()


class NetworkUsageProvider(DataProvider[NetworkUsageInfo]):
    def __init__(self):
        super().__init__("network-usage", "network-usage", 2.0)
        self._data_queue: t.Dict[UsageType, deque[int]] = {
            k: deque(maxlen=5) for k in UsageType.dict().keys()
        }
        self._interface = "wlp0s20f3"  # @TEMP

    def _reset(self):
        return NetworkUsageInfo()

    def _collect(self) -> NetworkUsageInfo:
        counters : snetio = psutil.net_io_counters(pernic=True).get(self._interface)
        self._data_queue.get(UsageType.UPLOAD).append(counters.bytes_sent)
        self._data_queue.get(UsageType.DOWNLOAD).append(counters.bytes_recv)
       # self._data_queue(.)
        return NetworkUsageInfo()
