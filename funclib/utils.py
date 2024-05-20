from typing import Union, Dict, List, Any, Type
from enum import Enum, IntEnum, unique, auto

# 定义一个类型别名，可以表示任何JSON类型的数据
JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


# 定义一个枚举类，表示实例选项类型
class InstanceOptionType(IntEnum):
	touch_type = 2
	deployment_with_pause = 3


# 定义一个唯一的枚举类，表示回调消息类型
@unique
class Message(Enum):
	"""
    回调消息

    请参考 docs/回调消息.md
    """
	InternalError = 0

	InitFailed = auto()

	ConnectionInfo = auto()

	AllTasksCompleted = auto()

	TaskChainError = 10000

	TaskChainStart = auto()

	TaskChainCompleted = auto()

	TaskChainExtraInfo = auto()

	TaskChainStopped = auto()

	SubTaskError = 20000

	SubTaskStart = auto()

	SubTaskCompleted = auto()

	SubTaskExtraInfo = auto()

	SubTaskStopped = auto()


# 定义一个唯一的枚举类，表示目标版本类型
@unique
class Version(Enum):
	"""
    目标版本
    """
	Nightly = auto()

	Beta = auto()

	Stable = auto()
