# coding=utf-8
from typing import List


class GenymotionDeviceModel(object):
    """
    Genymotion Device Model

    Args:
        object (_type_): _description_
    """

    status: bool = False  # is open or not

    device_serial: str = ""  # the device adb serial

    uuid: str = ""  # the uuid device name

    device_name: str = ""  # the device name

    def __init__(self,
                 status: bool,
                 device_serial: str,
                 uuid: str,
                 device_name: str) -> None:
        self.status = status
        self.device_serial = device_serial
        self.uuid = uuid
        self.device_name = device_name

    @staticmethod
    def str_to_model(line: str) -> object:
        """Convert line string to model

        Args:
            line (str): _description_

        Returns:
            object: _description_
        """
        device_dict: List[str] = list(map(lambda item: item.strip(), line.split("|")))
        status: bool = device_dict[0] == 'On'
        adb_serial: str = device_dict[1]
        uuid: str = device_dict[2]
        device_name: str = device_dict[3]
        return GenymotionDeviceModel(
            status=status,
            device_serial=adb_serial,
            uuid=uuid,
            device_name=device_name
        )
