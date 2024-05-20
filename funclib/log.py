import logging
from colorama import Fore, Style
from funclib.stack import GlobalConst as gc


class ColoredFormatter(logging.Formatter):
	"""
	自定义日志输出格式
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def format(self, record):
		record.name = Fore.CYAN + record.name + Style.RESET_ALL
		record.levelname = Fore.MAGENTA + record.levelname + Style.RESET_ALL
		if record.levelno == logging.DEBUG:
			record.msg = Fore.BLUE + record.msg + Style.RESET_ALL
		elif record.levelno == logging.INFO:
			record.msg = Fore.GREEN + record.msg + Style.RESET_ALL
		elif record.levelno == logging.WARNING:
			record.msg = Fore.YELLOW + record.msg + Style.RESET_ALL
		elif record.levelno == logging.ERROR:
			record.msg = Fore.RED + record.msg + Style.RESET_ALL
		return super().format(record)


class logger:
	def __init__(self, name, is_console=gc.is_console, level=logging.DEBUG):
		# 创建一个logger
		self.__logger = logging.getLogger(name)
		self.__logger.setLevel(level)  # 设置日志级别为DEBUG

		log_path = gc.LOG_PATH + name + '.log'
		# 创建一个handler，用于写入日志文件
		self.__file_handler = logging.FileHandler(log_path)
		self.__file_handler.setLevel(level)

		# 再创建一个handler，用于输出到控制台
		self.__console_handler = logging.StreamHandler()
		self.__console_handler.setLevel(level)

		# 定义handler的输出格式
		file_formatter = logging.Formatter('%(asctime)s - %(name)s[%(levelname)s]%(message)s')
		self.__file_handler.setFormatter(file_formatter)

		console_formatter = ColoredFormatter('%(name)s[%(levelname)s]%(message)s')
		self.__console_handler.setFormatter(console_formatter)

		# 给logger添加handler
		self.__logger.addHandler(self.__file_handler)
		if is_console:
			self.__logger.addHandler(self.__console_handler)
		else:
			pass

	def debug(self, message):
		self.__logger.debug(str(message))

	def info(self, message):
		self.__logger.info(str(message))

	def warning(self, message):
		self.__logger.warning(str(message))

	def error(self, message):
		self.__logger.error(str(message))

	def critical(self, message):
		self.__logger.critical(str(message))

	def console(self, message):
		self.__logger.removeHandler(self.__file_handler)
		self.info(str(message))
		self.__logger.addHandler(self.__file_handler)

	def file(self, message):
		self.__logger.removeHandler(self.__console_handler)
		self.info(str(message))
		self.__logger.addHandler(self.__console_handler)
