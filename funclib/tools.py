import glob
import os
import pathlib
import subprocess
import uuid

from colorama import Fore, Style
from prettytable import PrettyTable

from funclib.stack import GlobalConst as gc

import psutil


def print_table(data, log):
	"""
	创建并打印一个表格
	:param log:
	:param data: 表格数据，可以是字典或列表，每个键值对是表格的一行
	:return: None
	"""
	# 创建一个PrettyTable对象
	table = PrettyTable()
	# 检查数据类型
	try:
		if isinstance(data, dict):
			# 设置列名
			table.field_names = list(data.keys())

			# 添加数据
			table.add_row(list(data.values()))
		elif isinstance(data, list):
			# 设置列名
			table.field_names = list(data[0].keys())

			# 添加数据
			for row in data:
				table.add_row(list(row.values()))
		else:
			log.console("Unsupported data type for print_table. Please provide a dictionary or a list.")
	except IndexError:
		log.console("No data to print.")
		return
	# 打印表格
	print(Fore.GREEN + str(table) + Style.RESET_ALL)


def get_all_func_in_class(cls):
	# 获取类的所有方法和属性
	methods_and_attributes = dir(cls)

	# 过滤出所有的方法
	methods = [item for item in methods_and_attributes if callable(getattr(cls, item))]
	for method in methods:
		print(method)


def is_file_open(file_path):
	for proc in psutil.process_iter():
		try:
			for item in proc.open_files():
				if file_path == item.path:
					return True
		except Exception:
			pass
	return False


def check_if_process_running(process_name):
	# 检测线程是否在运行
	for proc in psutil.process_iter():
		try:
			# 检测线程名是否存在
			if process_name.lower() in proc.name().lower():
				return True
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return False


def clear_logs():
	# 使用glob模块获取所有文件
	files = glob.glob(os.path.join(str(pathlib.Path(__file__).parent.absolute().parent / 'resource' / 'logs'), '*'))
	for f in files:
		# 使用os模块删除文件
		os.remove(f)


def choose_url(urls):
	for url in urls:
		print(f"{url}")
	return urls[int(input("请输入序号:")) - 1]


def run_cmd(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	return stdout.decode(), stderr.decode()


def aria2c_download(url, proxy=gc.update_proxy, connections=5, dir=gc.MAA_RES_PATH):
	if proxy is None:
		cmd = f"{gc.downloader} -x {connections} --dir={dir} {url}"
	else:
		cmd = (f"set http_proxy={proxy} "
			   f"& set https_proxy={proxy} "
			   f"& {gc.downloader} -x {connections} --dir={dir} {url}")
	print(cmd)
	stdout, stderr = run_cmd(cmd)
	return stdout, stderr


def generate_uuid(phone_number):
	"""
	根据指定的手机号码生成特定的UUID
	:param phone_number: 手机号码
	:return: UUID
	"""
	return uuid.uuid5(uuid.NAMESPACE_DNS, phone_number)


def print_dict(d):
	for key, value in d.items():
		print(f"{key}: {value}")
