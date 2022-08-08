# coding=utf-8
import os
import time
from multiprocessing import Event
from subprocess import run, CompletedProcess, PIPE
from typing import List
from geny_gmtool.genymotion_model import GenymotionDeviceModel
from enum import Enum
from geny_gmtool.g_error import GmtoolError, GmtoolErrorType
from geny_gmtool.thread_timer import ThreadTimer
import platform


def is_windows() -> bool:
    """
    Check the system is windows or not
    Returns:

    """
    if platform.system().lower() == 'windows':
        return True
    else:
        return False


class GenyStatus(Enum):
    """
    Show Geny status enumeration

    Args:
        Enum (_type_): _description_
    """
    RUNNING = 1

    OFF = 2

    ALL = 3


def get_list_devices_running(status: GenyStatus = GenyStatus.ALL) -> List[GenymotionDeviceModel]:
    """
    get the genymotion devices that online
    """
    command_list: List[str] = ['gmtool', 'admin', 'list']
    if status == GenyStatus.RUNNING:
        command_list.append('--running')
    elif status == GenyStatus.OFF:
        command_list.append('--off')
    result: CompletedProcess[bytes] = run(command_list,
                                          stdout=PIPE)
    ret: str = result.stdout.decode(encoding='utf-8')
    device_strs: List[str] = ret.split("\n")
    devices: List[GenymotionDeviceModel] = []
    for index, device_str in enumerate(device_strs):
        if index > 1 and index != (len(device_strs) - 1):
            tmp_model: GenymotionDeviceModel = GenymotionDeviceModel.str_to_model(line=device_str)
            devices.append(tmp_model)
    return devices


def start_device_name(device_name: str) -> int:
    """
    open a device,
    Args:
        device_name (str): the device name you have given
    Returns:
        -1 means stop failure
        0 means stop successfully
    """
    ret: int = -1
    devices: List[GenymotionDeviceModel] = get_list_devices_running(
        status=GenyStatus.ALL)
    device_names: List[str] = list(map(lambda item: item.device_name, devices))
    if device_name not in device_names:
        raise GmtoolError(error_type=GmtoolErrorType.NotFoundDevice)
    online_devices: List[GenymotionDeviceModel] = list(filter(lambda item: item.status, devices))
    online_dev_names: List[str] = list(
        map(lambda item: item.device_name, online_devices))
    if device_name in online_dev_names:
        return ret
    else:
        command_list: List[str] = ['gmtool', 'admin', 'start', device_name]
        if is_windows():
            os.system(f'gmtool admin start "{device_name}"')
            time.sleep(10)
        else:
            result: CompletedProcess[bytes] = run(command_list,
                                                  shell=False,
                                                  stdout=PIPE,
                                                  timeout=None)
            str_result: str = result.stdout.decode(encoding='utf-8')
            if "not found" in str_result:
                raise GmtoolError(error_type=GmtoolErrorType.NotFoundDevice)
            elif "already started" in str_result:
                return -1
        # check the status in ten seconds
        ret = loop_check_device_status(device_name=device_name)
    return ret


def stop_device_name(device_name: str) -> int:
    """
    Stop the device
    Args:
        device_name:

    Returns:
        -1 means stop failure
        0 means stop successfully
    """
    ret = -1
    devices: List[GenymotionDeviceModel] = get_list_devices_running(
        status=GenyStatus.ALL)
    device_names: List[str] = list(map(lambda item: item.device_name, devices))
    if device_name not in device_names:
        raise GmtoolError(error_type=GmtoolErrorType.NotFoundDevice)
    is_online: bool = check_is_on_line(device_name=device_name)
    if not is_online:
        return ret
    else:
        command_list: List[str] = ['gmtool', 'admin', 'stop', device_name]
        result: CompletedProcess[bytes] = run(command_list,
                                              stdout=PIPE)
        _: str = result.stdout.decode(encoding='utf-8')
        # check the status in ten seconds
        ret = loop_check_device_status(device_name=device_name, is_online=False)
        return ret


def check_is_on_line(device_name: str,
                     is_online: bool = True) -> bool:
    """Check device is online

    Args:
        device_name (str): _description_
        is_online: whether is online checked

    Returns:
        bool: _description_
    """
    devices: List[GenymotionDeviceModel] = get_list_devices_running(
        status=GenyStatus.ALL)
    online_devices: List[GenymotionDeviceModel] = list(
        filter(lambda item: item.status if is_online else not item.status, devices))
    online_dev_names: List[str] = list(
        map(lambda item: item.device_name, online_devices))
    if device_name in online_dev_names:
        return True
    else:
        return False


def loop_check_device_status(device_name: str,
                             time_interval: int = 10,
                             is_online: bool = True) -> int:
    """
    Loop check the status
    Args:
        device_name:
        time_interval:
        is_online: is online or not

    Returns:

    """
    stopFlag = Event()
    thread = ThreadTimer(event=stopFlag,
                         duration=1,
                         time_interval=time_interval,
                         function=check_is_on_line,
                         args=(device_name, is_online))
    thread.start()
    tmp_timer: int = time_interval
    while tmp_timer >= 0:
        time.sleep(1)
        tmp_timer = tmp_timer - 1
        status = thread.is_open
        if status:
            return 0
        else:
            continue
    return -1
