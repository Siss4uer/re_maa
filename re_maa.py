import json
import os
import time
import urllib
import pprint

from urllib import request
from colorama import Fore, Style

from funclib.log import logger
from funclib.core import Asst
from funclib.database import SqliteDB
from funclib.emulator import Bluestacks
from funclib import tools
from funclib.stack import GlobalConst as gc

log = logger('ReMaa')
core = logger('MaaCore')


@Asst.CallBackType
def callback_details(msg, details, arg):
	"""
	自定义回调函数
	:param msg: 消息
	:param details: 详细信息
	:param arg: 附加参数
	:return: None
	"""
	# 打印消息
	core.info(f"{msg} - {details} - {arg}")


@Asst.CallBackType
def callback_file(msg, details, arg):
	"""
	自定义回调函数
	:param msg: 消息
	:param details: 详细信息
	:param arg: 附加参数
	:return: None
	"""
	# 打印消息
	core.file(f"{msg} - {details} - {arg}")


@Asst.CallBackType
def callback_filter(msg, details, arg):
	"""
	自定义回调函数
	:param msg: 消息
	:param details: 详细信息
	:param arg: 附加参数
	:return: None
	"""
	details = json.loads(details.decode('utf-8'))
	if msg == 0:
		core.info(f"[内部错误]")
	elif msg == 1:
		core.info(f"[初始化失败]@{details['what']}-{details['why']}-{details['details']}")
	elif msg == 2:
		core.info(f"[连接相关信息]@{details['uuid']}-{details['what']}")
	elif msg == 3:
		core.info(f"[任务完成]@{details['uuid']}-{details['finished_tasks']}")
	elif msg == 4:
		core.info(
			f"[外部异步调用信息]@{details['uuid']}-{details['what']}-{details['async_call_id']}-{details['cost']}")
	elif msg == 10000:
		core.info(f"[任务链执行/识别错误]@")
		pass
	elif msg == 10001:
		core.info(f"[任务链开始]@{details['uuid']}-{details['taskchain']}-{details['taskid']}")
		pass
	elif msg == 10002:
		core.info(f"[任务链完成]@{details['uuid']}-{details['taskchain']}-{details['taskid']}")
		pass
	elif msg == 10003:
		core.info(f"[任务链额外信息]@")
		pass
	elif msg == 10004:
		core.info(f"[任务链手动停止]@")
		pass
	elif msg == 20000:
		core.info(f"[原子任务执行/识别错误]@{details['uuid']}-{details['subtask']}-{details['taskid']}")
		pass
	elif msg == 20001:
		if details['subtask'] == 'ProcessTask':
			pass
		core.info(f"[原子任务开始]@{details['uuid']}-{details['subtask']}-{details['taskid']}")
		pass
	elif msg == 20002:
		if details['subtask'] == 'ProcessTask':
			pass
		core.info(f"[原子任务完成]@{details['uuid']}-{details['subtask']}-{details['taskid']}")
		pass
	elif msg == 20003:
		core.info(f"[原子任务额外信息]@")  # maa工具输出位置
		pass
	elif msg == 20004:
		core.info(f"[原子任务手动停止]@")
		pass
	else:
		pass


class ReMaa:

	def __init__(self, Core=True, Emulator=False, Adb=False, DB=True):
		self.CORE, self.EMULATOR, self.ADB, self.db = None, None, None, None
		if Emulator:
			self.EMULATOR = self.__emulator_boot()
		if Core:
			self.CORE = self.__core_init()
			if Adb:
				self.ADB = self.__adb_connect(self.CORE)
		if DB:
			self.db = SqliteDB(gc.Database_Path)

	@staticmethod
	def __core_init():
		temp = None
		if gc.is_update_ota:
			# 更新游戏索引
			dir_path = os.path.dirname(gc.ota_tasks_path)
			os.makedirs(dir_path, exist_ok=True)
			with open(gc.ota_tasks_path, 'w', encoding='utf-8') as f:
				with urllib.request.urlopen(gc.ota_tasks_url) as u:
					f.write(u.read().decode('utf-8'))
			# 加载MAACORE
			Asst.load(path=gc.MAA_RES_PATH, incremental_path=gc.incremental_path)
		else:
			Asst.load(path=gc.MAA_RES_PATH)
		if gc.callback_type == "details":
			temp = Asst(callback=callback_details)
		elif gc.callback_type == "filter":
			temp = Asst(callback=callback_filter)
		if temp is not None:

			# 设置额外配置
			# 触控方案配置
			temp.set_instance_option(gc.InstanceOptionType.touch_type, gc.touch_type)
			# 暂停下干员
			# self.__asst.set_instance_option(gc.InstanceOptionType.deployment_with_pause, gc.deployment_with_pause)

			return temp
		else:
			return None

	@staticmethod
	def __adb_connect(asst: Asst):
		if asst is None:
			return False
		# ADB连接
		if asst.connect(gc.ADB_PATH[0], gc.ADB_PATH[1]):
			log.info('连接成功')
			return asst
		else:
			log.info('连接失败')
			return False

	@staticmethod
	def input_(msg):
		return input(Fore.GREEN + msg + Style.RESET_ALL)

	@staticmethod
	def __emulator_boot():
		if tools.check_if_process_running(gc.EMULATOR[0].split('\\')[-1]):
			log.info('模拟器已启动')
			return True
		else:
			# 启动模拟器。
			log.info(f'正在启动模拟器，默认等待时间{gc.EMULATOR[1]}s')
			return Bluestacks.launch_emulator_win(gc.EMULATOR[0], gc.EMULATOR[1])

	def add_user(self, id, phone_number, client):
		"""

		:param id:
		:param phone_number:
		:param client:
		:return:
		"""
		return self.db.add({
			"id": id,
			"phone_number": phone_number,
			"client": client
		})

	def delete_user(self, id):
		"""

		:param id:
		:return:
		"""
		return self.db.delete(id)

	def show_data(self, ID=None):
		if ID:
			tools.print_table(self.db.retrieve_data(ID), log)
		else:
			tools.print_table(self.db.retrieve_data(), log)

	def switch_user_status(self, id, status=None):
		if status == "enabled":
			self.db.toggle_status(id, 1)
		elif status == "disabled":
			self.db.toggle_status(id, 0)
		elif status == "1":
			self.db.toggle_status(id, 1)
		elif status == "0":
			self.db.toggle_status(id, 0)
		else:
			self.db.toggle_status(id)

	def trigger(self):
		tools.print_table(self.db.retrieve_data(), log)
		user_list = self.db.retrieve_data()
		for user in user_list:
			if user['status'] == "disabled":  # 跳过禁用用户
				continue
			if user['last_run'] == "marked":  # 跳过标记用户
				continue
			for target_task in user['task_chain']:
				if target_task not in gc.task_chain:
					continue
				if target_task == 'CloseDown':
					self.CORE.append_task(target_task, {
						"enable": True
					})
				elif target_task == 'StartUp':
					if user['client'] == "Official":
						account_name = str(user['phone_number'])[:3] + '****' + str(user['phone_number'])[7:]
					else:
						account_name = None
					self.CORE.append_task(target_task, {
						"enable": True,
						"client_type": user['client'],
						"start_game_enabled": True,
						"account_name": account_name
					})
				elif target_task == 'Recruit':
					self.CORE.append_task(target_task, {
						"enable": True,
						"select": [4],
						"confirm": [3, 4],
						"times": 4
					})
				elif target_task == 'Infrast':
					self.CORE.append_task(target_task, {
						"enable": True,
						"facility": user['facility'],
						"drones": user['drones']
					})
				elif target_task == 'Fight':
					self.CORE.append_task(target_task, {
						"enable": True,
						"stage": user['stage'],
						"medicine": int(user['medicine']),
						"expiring_medicine": int(user['expiring_medicine']),
						"stone": int(user['stone']),
						"client_type": user['client']
					})
				elif target_task == 'Mall':
					self.CORE.append_task(target_task, {
						"enable": True,
						"shopping": True,
						"buy_first": user['buy_first'],
						"blacklist": user['black_list']
					})
				elif target_task == 'Award':
					self.CORE.append_task(target_task, {
						"enable": True,
						"award": bool(user['award']),
						"mail": bool(user['mail']),
						"recruit": bool(user['recruit']),
						"orundum": bool(user['orundum']),
						"mining": bool(user['mining']),
						"specialaccess": bool(user['specialaccess'])
					})
				else:
					pass
			self.CORE.start()
			try:
				while self.CORE.running():
					time.sleep(0)
				self.CORE.stop()
				self.db.toggle_last_run(user['id'], 1)
			except KeyboardInterrupt:
				self.CORE.stop()
				log.warning('任务已停止')
				pass
