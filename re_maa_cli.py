import cmd
import sys
from typing import IO
import argparse

import re_maa


class Re_maa_Shell(cmd.Cmd):
	intro = 'W. Type help or ? to list commands.\n'
	prompt = 're_maa$ '

	def __init__(self, completekey: str = "tab", stdin: IO[str] | None = None, stdout: IO[str] | None = None):
		super().__init__(completekey, stdin, stdout)
		self.re_maa_handler = None

	def do_init(self, arg):
		"""Initialize re_maa."""
		parser = argparse.ArgumentParser()
		parser.add_argument('-boot', action='store_true')
		parser.add_argument('-db', action='store_true')
		args = parser.parse_args(arg.split())

		if args.boot:
			self.re_maa_handler = re_maa.ReMaa(Emulator=True, Core=True, Adb=True, DB=True)
		elif args.db:
			self.re_maa_handler = re_maa.ReMaa(Emulator=False, Core=True, Adb=False, DB=True)
		else:
			print("Invalid argument. Please use -boot or -db.")

	def do_trigger(self, arg):
		"""Trigger re_maa."""
		self.re_maa_handler.trigger()

	def do_add(self, arg):
		"""Add a new user """
		parser = argparse.ArgumentParser()
		parser.add_argument('-id', type=str, required=True)
		parser.add_argument('-phone', type=str, required=True)
		parser.add_argument('-client', type=str, required=True)
		args = parser.parse_args(arg.split())
		self.re_maa_handler.add_user(args.id, args.phone, args.client)

	# add -id self -phone 15230270267 -client official
	def do_show(self, arg):
		"""Show all users"""
		parser = argparse.ArgumentParser()
		parser.add_argument('-id', type=str, required=False)
		args = parser.parse_args(arg.split())
		if args.id:
			self.re_maa_handler.show_data(args.id)
		else:
			self.re_maa_handler.show_data()

	def do_switch(self, arg):
		"""switch user status"""

		parser = argparse.ArgumentParser()
		parser.add_argument('-id', type=str, required=True)
		parser.add_argument('-status', type=str, required=False)
		args = parser.parse_args(arg.split())
		self.re_maa_handler.switch_user_status(args.id, args.status)

	def do_exit(self, arg):
		"""Exit re_maa."""
		return True

	def do_delete(self, arg):
		"""Delete a user"""
		parser = argparse.ArgumentParser()
		parser.add_argument('-id', type=str, required=True)
		args = parser.parse_args(arg.split())
		print(f"你确定要删除用户{args.id}吗？")
		confirm = input("Y/N:")
		if confirm.lower() == "y":
			self.re_maa_handler.delete_user(args.id)
		else:
			print("取消删除")


if __name__ == '__main__':
	# re_maa.__init(Emulator=True, Core=True, Adb=True, DB=True)
	# for i, arg in enumerate(sys.argv):
	# 	print(f"Argument {i}: {arg}")
	Re_maa_Shell().cmdloop()
