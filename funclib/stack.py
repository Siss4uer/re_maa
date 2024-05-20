import hashlib
import os

from .utils import Version, InstanceOptionType


class GlobalConst:
	# 数据库表头
	database_header = {
		"user_data": ["Syntax", "phone_number", "id", "remain", "status", "client", "password", "last_run",
					  "last_run_time",
					  "game_id", "uuid", "scheme_uuid"],
		"user_scheme": ["uuid", "task_chain", "stage", "is_Annihilation", "medicine", "expiring_medicine", "stone",
						'facility', 'drones',
						"buy_first", "black_list",
						"mining", "orundum", "award", "mail", "recruit", "specialaccess",
						"OperatorBox",
						"scheme_uuid"],
		"time_scheme": ["Trigger", "time", "status"]

	}
	default_value_user_data = {
		"status": "enabled",
		"last_run": "unmarked",
	}
	default_scheme = {
		"task_chain": ['CloseDown', 'StartUp', 'Recruit', 'Infrast', 'Fight', 'Mall', 'Award'],
		"stage": "LS-6",
		"is_Annihilation": None,
		"medicine": 0,
		"expiring_medicine": 2,
		"stone": 0,
		"facility": ["Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"],
		"drones": "Money",
		"buy_first": ['招聘许可', '龙门币'],
		"black_list": ['家具', '碳'],
		"mining": False,
		"orundum": False,
		"award": True,
		"mail": True,
		"recruit": False,
		"specialaccess": True,
		"OperatorBox": None,
		"scheme_uuid": None
	}
	task_chain = ['CloseDown', 'StartUp', 'Recruit', 'Infrast', 'Fight', 'Mall', 'Award']
	default_task_params = {
		"CloseDown": {
			"enable": True
		},
		"StartUp": {
			"enable": True,
			"client_type": None,
			"start_game_enabled": False,
			"account_name": None
		},
		"Recruit": {
			'select': [4],
			'confirm': [3, 4],
			'times': 4
		},
		"Infrast": {
			'facility': [
				"Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"
			],
			'drones': "Money"
		},
		"Fight": {
			"enable": True,  # 是否启用本任务，可选，默认为 true
			"stage": None,
			"medicine": 0,
			"expiring_medicine": 0,
			"stone": 0,
			"client_type": None

		},
		"Mall": {
			"shopping": True,
			"buy_first": ['招聘许可', '龙门币'],
			"blacklist": ['家具', '碳'],
		},
		"Award": {
			"enable": True,  # 是否启用本任务，可选，默认为 true
			"award": True,  # 领取每日/每周任务奖励，默认为 true
			"mail": True,  # 领取所有邮件奖励，默认为 false
			"recruit": False,  # 领取限定池子赠送的每日免费单抽，默认为 false
			"orundum": False,  # 领取幸运墙的合成玉奖励，默认为 false
			"mining": False,  # 领取限时开采许可的合成玉奖励，默认为 false
			"specialaccess": True  # 领取五周年赠送的月卡奖励，默认为 false
		}
	}

	# RE_MAA设置
	project_path = os.getcwd()
	LOG_PATH = project_path + "\\resource\\logs\\"
	MAA_RES_PATH = project_path + "\\resource\\maa_res\\"  # MAACore.dll路径
	EMULATOR = ["C:\Program Files\BlueStacks_nxt\HD-Player.exe", 20]  # 模拟器路径
	ADB_PATH = ["C:\Program Files\BlueStacks_nxt\HD-Adb.exe", "127.0.0.1:5555"]  # ADB路径
	Database_Path = project_path + "\\resource\\data\\data.db"
	is_update = False
	is_update_ota = False
	is_console = True
	callback_type = "filter"  # "details" or "filter
	# MaaCore设置
	ota_tasks_url = 'https://ota.maa.plus/MaaAssistantArknights/api/resource/tasks.json'
	ota_tasks_path = os.path.join(MAA_RES_PATH, 'cache', 'resource', 'tasks.json')
	incremental_path = os.path.join(MAA_RES_PATH, 'cache')
	touch_type = 'maatouch'
	deployment_with_pause = '1'
	maa_version = Version.Nightly
	InstanceOptionType = InstanceOptionType
	update_proxy = "http://127.0.0.1:7890"
	downloader = project_path + "\\tools\\aria2c.exe"

	@staticmethod
	def hash_string(input_string):
		sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
		return sha_signature

	@staticmethod
	def verify(input_string, signature):
		return hashlib.sha256(input_string.encode()).hexdigest() == signature
