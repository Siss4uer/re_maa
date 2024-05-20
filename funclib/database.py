import datetime
import os
import sqlite3
from sqlite3 import Error
from funclib.stack import GlobalConst as gc
from funclib.log import logger

"""
数据库操作类
创建实例后自动链接数据库
functions:
	__init__(db_file) -> None: 初始化数据库链接
	__del__() -> None: 关闭数据库链接
	add(data) -> None: 添加数据
	syntax() -> int: 更新Syntax值
	delete(id) -> None: 删除数据
	retrieve_data(id_key) -> list: 获取数据
	update(id, data) -> bool: 更新数据
"""


class SqliteDB:
	def __init__(self, db_file=None):
		if db_file is None:
			db_file = gc.Database_Path
		self.__db_file = db_file
		self.__logger = logger('SqliteDB')
		self.table_key = list(gc.database_header.keys())
		if not os.path.exists(db_file):
			try:
				conn = sqlite3.connect(db_file)
				cursor = conn.cursor()
				for table in gc.database_header.keys():
					columns = ', '.join([f"'{column}' TEXT" for column in gc.database_header[table]])
					if table == 'user_data':
						sql = f"CREATE TABLE {table} ({columns}, PRIMARY KEY(Syntax))"
					else:
						sql = f"CREATE TABLE {table} ({columns})"
					cursor.execute(sql)
				conn.commit()
				self.__logger.file(f'Database {db_file} created with default tables.')
			except Error as e:
				self.__logger.warning(f'Error: {e}')
			finally:
				if conn:
					conn.close()
		else:
			conn = sqlite3.connect(db_file)
			cursor = conn.cursor()
			for table in gc.database_header.keys():
				cursor.execute(f"PRAGMA table_info({table})")
				columns_in_db = [column[1] for column in cursor.fetchall()]
				if set(columns_in_db) != set(gc.database_header[table]):
					self.__logger.warning(f"Table {table} does not match the schema defined in gc.default_headers.")
					conn.close()
					exit(1)
			conn.close()
		self.__conn = sqlite3.connect(db_file)
	# self.__syntax = self.syntax()

	def add(self, data):
		"""
		添加数据
		:param data:
		:return:
		"""
		cursor = self.__conn.cursor()

		# 获取当前最大的 Syntax 值
		cursor.execute("SELECT MAX(Syntax) FROM user_data")
		max_syntax = cursor.fetchone()[0]
		new_syntax = max_syntax + 1 if max_syntax is not None else 1

		# 添加 Syntax 到 data
		data['Syntax'] = new_syntax
		# 添加 status 到 data
		data['status'] = gc.default_value_user_data['status']
		# 添加 last_run 到 data
		data['last_run'] = gc.default_value_user_data['last_run']
		# 添加 uuid 到 data
		data['uuid'] = gc.hash_string(data['id'])

		# Capitalize client
		if 'client' in data:
			data['client'] = data['client'].capitalize()

		# Convert arrays in 'data' to strings and booleans to 'True'/'False' strings
		for key, value in data.items():
			if isinstance(value, list):
				data[key] = '@'.join(value)
			elif isinstance(value, bool):
				data[key] = 'True' if value else 'False'

		# Insert into user_data table
		user_data_columns = ', '.join([f"'{key}'" for key in data.keys()])
		user_data_placeholders = ', '.join(['?' for _ in data])
		user_data_sql = f"INSERT INTO user_data ({user_data_columns}) VALUES ({user_data_placeholders})"
		user_data_values = tuple(data.values())
		cursor.execute(user_data_sql, user_data_values)
		self.__conn.commit()
		self.__logger.file(f'Data with Syntax {new_syntax} inserted into user_data')

		# Check if uuid exists in user_scheme
		cursor.execute("SELECT uuid FROM user_scheme WHERE uuid = ?", (data['uuid'],))
		uuid_exists = cursor.fetchone() is not None

		# If uuid does not exist in user_scheme, insert a default row
		if not uuid_exists:
			default_scheme_items = dict(gc.default_scheme.items())
			# Convert arrays in 'default_scheme_items' to strings
			for key, value in default_scheme_items.items():
				if isinstance(value, list):
					default_scheme_items[key] = '@'.join(value)
			default_scheme_items['uuid'] = data['uuid']
			scheme_columns = ', '.join([f"'{key}'" for key in default_scheme_items.keys()])
			scheme_placeholders = ', '.join(['?' for _ in default_scheme_items])
			scheme_sql = f"INSERT INTO user_scheme ({scheme_columns}) VALUES ({scheme_placeholders})"
			scheme_values = tuple(default_scheme_items.values())
			cursor.execute(scheme_sql, scheme_values)
			self.__conn.commit()
			self.__logger.file(f'Default scheme data with uuid {data["uuid"]} inserted into user_scheme')

	def delete(self, id):
		"""
		删除数据
		:param id:
		:return:
		"""
		# 生成uuid
		uuid = gc.hash_string(id)
		# 在user_data表中删除数据
		sql = f"DELETE FROM user_data WHERE uuid = ?"
		self.__conn.cursor().execute(sql, (uuid,))
		self.__conn.commit()
		self.__logger.file(f'Data {uuid} deleted from user_data')
		sql = f"DELETE FROM user_scheme WHERE uuid = ?"
		self.__conn.cursor().execute(sql, (uuid,))
		self.__conn.commit()
		self.__logger.file(f'Data {uuid} deleted from user_scheme')

	def retrieve_data(self, id_key=None):
		"""
		获取数据
		:param id_key:
		:return:
		"""
		cursor = self.__conn.cursor()
		cursor.execute("PRAGMA table_info(user_data)")
		user_data_columns = [column[1] for column in cursor.fetchall()]
		cursor.execute("PRAGMA table_info(user_scheme)")
		user_scheme_columns = [column[1] for column in cursor.fetchall()]

		if id_key is not None:
			uuid = gc.hash_string(id_key)
			cursor.execute(
				f"SELECT * FROM user_data JOIN user_scheme ON user_data.uuid = user_scheme.uuid WHERE user_data.uuid = ? ORDER BY Syntax",
				(uuid,))
		elif id_key is True:
			cursor.execute(
				"SELECT * FROM user_data JOIN user_scheme ON user_data.uuid = user_scheme.uuid WHERE status = 'on' ORDER BY Syntax")
		elif id_key is False:
			cursor.execute(
				"SELECT * FROM user_data JOIN user_scheme ON user_data.uuid = user_scheme.uuid WHERE status = 'off' ORDER BY Syntax")
		else:
			cursor.execute(
				"SELECT * FROM user_data JOIN user_scheme ON user_data.uuid = user_scheme.uuid ORDER BY Syntax")

		rows = [dict(zip(user_data_columns + user_scheme_columns, row)) for row in cursor.fetchall()]

		result = []
		for row in rows:
			# Convert strings back to arrays and booleans
			for key, value in row.items():
				if isinstance(value, str):
					if '@' in value:
						row[key] = value.split('@')
					elif value == 'True':
						row[key] = True
					elif value == 'False':
						row[key] = False
			result.append(row)
		return result

	def generate_default_scheme(self):
		"""
		为user_data中的所有数据生成对应的默认user_scheme数据
		:return: None
		"""
		cursor = self.__conn.cursor()

		# 获取user_data表中的所有uuid
		cursor.execute("SELECT uuid FROM user_data")
		uuids_in_user_data = [row[0] for row in cursor.fetchall()]

		# 获取user_scheme表中的所有uuid
		cursor.execute("SELECT uuid FROM user_scheme")
		uuids_in_user_scheme = [row[0] for row in cursor.fetchall()]

		# 找出在user_data表中但不在user_scheme表中的uuid
		uuids_to_insert = set(uuids_in_user_data) - set(uuids_in_user_scheme)

		# 对于每一个需要插入的uuid，插入一行默认数据到user_scheme表中
		for uuid in uuids_to_insert:
			default_scheme_items = dict(gc.default_scheme.items())
			# Convert arrays in 'default_scheme_items' to strings
			for key, value in default_scheme_items.items():
				if isinstance(value, list):
					default_scheme_items[key] = '@'.join(value)
			default_scheme_items['uuid'] = uuid
			scheme_columns = ', '.join([f"'{key}'" for key in default_scheme_items.keys()])
			scheme_placeholders = ', '.join(['?' for _ in default_scheme_items])
			scheme_sql = f"INSERT INTO user_scheme ({scheme_columns}) VALUES ({scheme_placeholders})"
			scheme_values = tuple(default_scheme_items.values())
			cursor.execute(scheme_sql, scheme_values)

		self.__conn.commit()
		self.__logger.file(f"Default scheme data inserted for {len(uuids_to_insert)} users")

	def update(self, id, data):
		"""
		更新数据
		:param id:
		:param data:
		:return:
		"""
		# 生成uuid
		uuid = gc.hash_string(id)

		# 获取数据库中的表结构
		cursor = self.__conn.cursor()
		cursor.execute("PRAGMA table_info(user_data)")
		user_data_columns = [column[1] for column in cursor.fetchall()]
		cursor.execute("PRAGMA table_info(user_scheme)")
		user_scheme_columns = [column[1] for column in cursor.fetchall()]

		# 检查每个键值对
		for key, value in data.items():
			# 不允许用户操作'Syntax'或'uuid'
			if key in ['Syntax', 'uuid']:
				continue

			# 检查列名是否存在
			if key not in user_data_columns and key not in user_scheme_columns:
				return False

			# 如果值是一个数组，将其拼接为以@作为分隔符的字符串
			if isinstance(value, list):
				value = '@'.join(value)

			# 确定要更新的表
			table = 'user_data' if key in user_data_columns else 'user_scheme'
			print(f"table: {table}")
			# 更新数据库中的相应记录
			sql = f"UPDATE {table} SET '{key}' = ? WHERE uuid = ?"
			self.__conn.cursor().execute(sql, (value, uuid))
			self.__conn.commit()
			self.__logger.file(f"Data {uuid} updated in {table}")

		return True

	def toggle_status(self, id):
		"""
		切换指定id的status状态
		:param id: 要切换状态的数据行的id，或者'all'来切换所有用户的状态
		:return: None
		"""
		cursor = self.__conn.cursor()

		# 判断是否需要对所有用户进行操作
		if id.lower() == 'all':
			ids = [row[0] for row in cursor.execute("SELECT id FROM user_data").fetchall()]
		else:
			ids = [id]

		for id in ids:
			# 生成uuid
			uuid = gc.hash_string(id)

			# 获取当前的status状态
			cursor.execute("SELECT status FROM user_data WHERE uuid = ?", (uuid,))
			current_status = cursor.fetchone()[0]

			# 切换status状态
			if current_status.lower() == 'enabled':
				new_status = 'disabled'
			elif current_status.lower() == 'disabled':
				new_status = 'enabled'
			else:
				new_status = 'enabled'
				self.__logger.warning(f"Unknown status value '{current_status}' for user {id}, setting to 'enabled'")

			# 更新数据库中的status状态
			cursor.execute("UPDATE user_data SET status = ? WHERE uuid = ?", (new_status, uuid))
			self.__logger.info(f"Data {id} updated in user_data, status set to {new_status}")
		self.__conn.commit()

	def toggle_last_run(self, id, flag):
		"""
		切换指定id的last_run状态
		:param id: 要切换状态的数据行的id
		:param flag: 标记状态，1为marked，0为unmarked
		:return: None
		"""
		cursor = self.__conn.cursor()

		# 判断是否需要对所有用户进行操作
		if id.lower() == 'all':
			ids = [row[0] for row in cursor.execute("SELECT id FROM user_data").fetchall()]
		else:
			ids = [id]

		# 切换last_run状态
		if flag == 1:
			new_status = 'marked'
			last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		elif flag == 0:
			new_status = 'unmarked'
			last_run_time = None
		else:
			new_status = 'unmarked'
			last_run_time = None
			self.__logger.warning(f"Unknown flag value '{flag}' for user {id}, setting to 'unmarked'")

		for id in ids:
			# 生成uuid
			uuid = gc.hash_string(id)
			# 更新数据库中的last_run状态
			cursor.execute("UPDATE user_data SET last_run = ?, last_run_time = ? WHERE uuid = ?",
						   (new_status, last_run_time, uuid))
			self.__logger.info(
				f"Data {id} updated in user_data, last_run set to {new_status}, last_run_time set to {last_run_time}")
		self.__conn.commit()
