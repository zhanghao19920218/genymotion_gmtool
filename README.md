# Genymotion Gmtool for Python

> Usage: `free version`
>
> 1. get devices from genymotion
> 2. start devices from genymotion
> 3. stop device from genymotion

## Usage

> Get devices from genymotion
>
> 1. Status contains three (running, off, all)

```python
def get_list_devices_running(status: GenyStatus = GenyStatus.ALL) -> List[GenymotionDeviceModel]
```

> Start device from genymotion
>
> Param:`device_name`:  the name of device

```python
def start_device_name(device_name: str) -> int
"""
:param device_name: the device name , must confirm if it's online
:return return 0 means start successfully, -1 means not
"""
```

> Stop device from genymotion
>
> Param: `device_name`

```python
def stop_device_name(device_name: str) -> int
"""
:param device_name: the device name , must confirm if it's online
:return return 0 means stop successfully, -1 means not
"""
```

