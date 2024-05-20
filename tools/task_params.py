from funclib.log import logger


class task:
	def __init__(self, task_name: str, task_params):
		self.task_name = task_name
		self.task_params = task_params


class task_chains:

	def __init__(self):
		self.logger = logger('ReMaa')
		self.task_chain = []

	# def append_task_StartUp(self, client=None, phone_number=None, start_game_enabled=False):
	#
	# 	if phone_number is not None:
	# 		account_name: object = phone_number[:3] + '****' + phone_number[7:]
	# 	else:
	# 		account_name = None
	#
	# 	tasks = task("StartUp", {
	# 		"enable": True,
	# 		"client_type": client,
	# 		"start_game_enabled": start_game_enabled,
	# 		"account_name": account_name
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_CloseDown(self):
	# 	tasks = task("CloseDown", {
	# 		"enable": True
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Fight(self, level_name, medicine=0, expiring_medicine=0, stone=0, client_type=None):
	# 	tasks = task("Fight", {
	#
	# 		"enable": True,  # 是否启用本任务，可选，默认为 true
	# 		"stage": level_name,  # 关卡名，可选，默认为空，识别当前/上次的关卡。不支持运行中设置
	# 		# 支持全部主线关卡，如 "1-7"、"S3-2"等
	# 		# 可在关卡结尾输入Normal/Hard表示需要切换标准与磨难难度
	# 		# 剿灭作战，必须输入 "Annihilation"
	# 		# 当期 SS 活动 后三关，必须输入完整关卡编号
	# 		"medicine": medicine,  # 最大使用理智药数量，可选，默认 0
	# 		"expiring_medicine": expiring_medicine,  # 最大使用 48 小时内过期理智药数量，可选，默认 0
	# 		"stone": stone,  # 最大吃石头数量，可选，默认 0
	# 		"client_type": client_type,  # 客户端版本，可选，默认为空。用于游戏崩溃时重启并连回去继续刷，若为空则不启用该功能
	# 		# 选项："Official" | "Bilibili" | "txwy" | "YoStarEN" | "YoStarJP" | "YoStarKR"
	#
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Recruit(self):
	# 	tasks = task("Recruit", {
	#
	# 		"enable": True  # 是否启用本任务，可选，默认为 true
	#
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Infrast(self):
	# 	tasks = task("Infrast", {
	#
	# 		"enable": True  # 是否启用本任务，可选，默认为 true
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Mall(self):
	# 	tasks = task("Mall", {
	#
	# 		"enable": True,  # 是否启用本任务，可选，默认为 true
	# 		"shopping": True
	#
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Award(self):
	# 	tasks = task("Award", {
	#
	# 		"enable": True,  # 是否启用本任务，可选，默认为 true
	# 		"award": True,  # 领取每日/每周任务奖励，默认为 true
	# 		"mail": True,  # 领取所有邮件奖励，默认为 false
	# 		# "recruit": bool,           # 领取限定池子赠送的每日免费单抽，默认为 false
	# 		# "orundum": bool,          # 领取幸运墙的合成玉奖励，默认为 false
	# 		# "mining": bool,            # 领取限时开采许可的合成玉奖励，默认为 false
	# 		"specialaccess": True  # 领取五周年赠送的月卡奖励，默认为 false
	#
	# 	})
	# 	self.task_chain.append(tasks)
	#
	# def append_task_Roguelike(self):
	# 	pass
	#
	# def append_task_OperBox(self):
	# 	pass
	#
	# def append_task_Copilot(self):
	# 	pass
	#
	# def __len__(self):
	# 	return len(self.task_chain)
	#
	# def show_task_chain(self):
	# 	return self.task_chain
	#
	# def clear_task_chain(self):
	# 	self.task_chain.clear()
	#
	# def chain_in(self,asst):
	# 	for tasks in self.task_chain:
	# 		asst.append_task(tasks.task_name, tasks.task_params)
