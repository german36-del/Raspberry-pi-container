
# developバージョンのツールを読み込み [ezpip]

import sys
import importlib
# 開発用ディレクトリの名前の始まり方のルール [config.py]
from .config import develop_header

# developバージョンの読み込みconfirmメッセージの表示
def show_confirm_message(develop_tool_name):
	# input("developバージョンのツール(%s)を読み込みます ([Enter]キーで続行...)"%develop_tool_name)
	input("Load the develop version of the tool (%s) ([Enter] key to continue...)"%develop_tool_name)

# developバージョンのツールを読み込み [ezpip]
def load_develop(
	tool_name,	# モジュール名
	tool_path,	# モジュールが存在するパス
	develop_flag = True,	# developバージョンを読み込むか (False指定でpipリリースバージョンを読み込み)
	confirm = True	# developバージョンを読み込んでいる旨の警告を表示するか
):
	# モジュール名のチェック
	if tool_name[:len(develop_header)] == develop_header:
		raise Exception("[ezpip error] load_develop()関数のtool_nameは「_develop_」が付かない、公開版の名前で指定してください")
	# 開発版 / 本番切り替え
	if develop_flag is True:
		develop_tool_name = develop_header + tool_name
		if confirm is True: show_confirm_message(develop_tool_name)	# developバージョンの読み込みconfirmメッセージの表示
		sys.path.append(tool_path)
		tool = importlib.import_module(develop_tool_name)
	else:
		tool = importlib.import_module(tool_name)
	return tool
