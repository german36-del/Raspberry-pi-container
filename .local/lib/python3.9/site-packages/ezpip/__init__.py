
import os
import sys
import fies
import shutil
from sout import sout
from pathlib import Path
# 開発用ディレクトリの名前の始まり方のルール [config.py]
from .parts.config import develop_header
# developバージョンのツールを読み込み [ezpip]
from .parts.load_develop import load_develop

# version_historyのファイルをロード
def load_version_history(filename):
	# 存在しない場合ファイルを作る
	if os.path.exists(filename) is False:
		fies[filename, "json"] = []
	# 読み込み
	version_history = fies[filename]
	return version_history

# ワイルドカード指定に該当するものの一覧を取得
def wild_search(data_ls, query):
	head, tail = query.split("*")
	wild_ls = []
	for e in data_ls:
		if len(e) < len(query)-1: continue
		if e.startswith(head) is False: continue
		if e.endswith(tail) is False: continue
		wild_ls.append(e[len(head):len(e)-len(tail)])
	return wild_ls

# 渡された処理がエラーを起こすかを判断
def judge_error(func):
	try:
		func()
		return False
	except:
		return True

# ワイルドカード指定に該当する「次の」のインデックスを取得
def get_new_idx(version_history, version):
	# ワイルドカード指定に該当するものの一覧を取得
	wild_ls = wild_search(version_history, version)
	# int化 (int化できないものは飛ばす)
	int_wild_ls = [int(e) for e in wild_ls
		if judge_error(lambda: int(e)) is False]
	# 履歴なき場合は0を返す
	if len(int_wild_ls) == 0: return 0
	# 最大のidxの次のidxを返す
	new_idx = max(int_wild_ls) + 1
	return new_idx

# 最新versionを自動的に決める
def gen_latest_version(version):
	filename = "__ezpip_version_history__.json"
	# verison未指定の場合
	if version is None: return None
	# ワイルドカード指定あり / なし 分岐
	if "*" in version:
		# ワイルドカードが「ちょうど1つ」かを確認
		if len(version.split("*"))-1 != 1: raise Exception("[ezpip error] ワイルドカード「*」の指定はちょうど1つである必要があります。")
		# ワイルドカード指定がある場合
		version_history = load_version_history(filename)	# version_historyのファイルをロード
		new_idx = get_new_idx(version_history, version)	# ワイルドカード指定に該当する「次の」のインデックスを取得
		new_version = version.replace("*", str(new_idx))
	else:
		# ワイルドカード指定がない場合
		new_version = version
	fies[filename] = fies[filename] + [new_version]	# 追記
	return new_version

# パスの末尾部分を分離
def div_path_tail(arg_path):
	# しっぽの取得
	raw_path = Path(arg_path)
	abs_path = raw_path.resolve()
	tail = abs_path.parts[-1]
	# しっぽ以外の取得
	no_tail_path = os.path.abspath(arg_path + "/../")
	return no_tail_path, tail

# develop_dirの名前の規則と存在の確認 (問題がある場合は落とす)
def check_develop_dir(develop_dir):
	# develop_dirのパスの末尾部分を取得
	_, develop_name = div_path_tail(develop_dir)	# パスの末尾部分を分離
	# develop_dirのディレクトリ名のチェック
	if develop_name[:len(develop_header)] != develop_header:
		raise Exception("[ezpip error] develop_dirは「%s」で始まる文字列である必要があります"%develop_header)
	# ディレクトリの存在チェック
	if os.path.exists(develop_dir) is False:
		raise Exception("[ezpip error] develop_dirが存在しません (%s)"%develop_dir)

# 公開用パッケージ名を生成
def gen_publish_name(develop_dir):
	# develop_dirのパスの末尾部分を取得
	_, develop_name = div_path_tail(develop_dir)	# パスの末尾部分を分離
	# 公開用パッケージ名を生成
	publish_name = develop_name[len(develop_header):]
	return publish_name

# 公開用ディレクトリがすでに存在しないかをチェック (存在する場合は落とす)
def check_no_pd(publish_dir):
	if os.path.exists(publish_dir) is True:
		raise Exception("[ezpip error] 公開用ディレクトリ(%s)がすでに存在します。ezpipを使用するためには、このディレクトリが存在しない必要があります。"%os.path.abspath(publish_dir))

# 再帰的にディレクトリを走査してファイルを列挙
def listup_files(root_dir):
	ret_ls = []
	for temp_dir, in_dir_ls, files in os.walk(root_dir):
		# ファイルを列挙
		ret_ls += ["%s/%s"%(temp_dir, s) for s in files]
	return ret_ls

# packagesの列挙
def listup_packages(publish_dir):
	# 再帰的にディレクトリを走査してファイルを列挙
	package_ls = listup_files(publish_dir)
	raw_package_ls = []
	for file in package_ls:
		# python形式のもの以外を除く
		if file[-3:] != ".py": continue
		# 相対パスを求める
		no_tail_python, _ = div_path_tail(file)	# パスの末尾部分を分離
		package_dir = os.path.relpath(no_tail_python, publish_dir+"/../")
		# 追記
		raw_package_ls.append(package_dir)
	# 重複の除去
	packages = list(set(raw_package_ls))
	return packages

	# こんなかんじ: ["ezRL", "ezRL/parts/catcher_game", "ezRL/parts/DQN_Agent", "ezRL/parts/normal_cnn", "ezRL/parts/"]

# ディレクトリが存在する場合は消す
def del_dir(arg_dir):
	if os.path.exists(arg_dir) is True:
		shutil.rmtree(arg_dir)

# long_description(README.md)の取得
def get_long_description(md_path):
	# ファイルの存在確認
	if os.path.exists(md_path) is False:
		raise Exception("[ezpip error] long_description属性に参照する場合は、(%s)を設置する必要があります。"%os.path.abspath(md_path))
	# README.mdの内容の取得
	with open(md_path, "r", encoding = "utf-8") as f:
		long_description = f.read()
	return long_description

# パッケージ情報にアクセスするインターフェース (with構文内)
class _EzpipPackageResult:
	# 初期化処理
	def __init__(self, cleanup_proc, publish_name, packages, root_dir, version):
		self.cleanup_proc = cleanup_proc
		self.publish_name = publish_name
		self._packages = packages
		self._root_dir = root_dir
		self._version = version
	# with突入時の処理 (with構文のas節内に代入される)
	def __enter__(self):
		return self
	# with脱出時の処理
	def __exit__(self, exception_type, exception_value, traceback):
		# 公開後の後片付け
		self.cleanup_proc()
	def __getattr__(self, attr_name):
		if attr_name == "packages":
			return self._packages
		elif attr_name == "long_description":
			# long_description(README.md)の取得
			return get_long_description(md_path = self._root_dir + "/README.md")
		elif attr_name == "version":
			if self._version is None: raise Exception("[ezpip error] version が指定されていません。")
			return self._version
		else:
			raise Exception("[ezpip error] AttributeError: this object has no attribute '%s'"%attr_name)
	# 文字列化(その1)
	def __str__(self):
		return "<_EzpipPackageResult package_name=%s>"%self.publish_name
	# 文字列化(その2)
	def __repr__(self):
		return str(self)

# 公開用パッケージの作成 [ezpip]
def packager(develop_dir, version = None):
	# 最新versionを自動的に決める
	new_version = gen_latest_version(version)
	# develop_dirの名前の規則と存在の確認 (問題がある場合は落とす)
	check_develop_dir(develop_dir)
	# 公開用パッケージ名を生成
	publish_name = gen_publish_name(develop_dir)
	# 公開用ディレクトリ
	publish_dir = "%s/../%s"%(develop_dir, publish_name)
	# 公開用ディレクトリがすでに存在しないかをチェック (存在する場合は落とす)
	check_no_pd(publish_dir)
	# ディレクトリごとコピー (develop_dirの存在確認はすでに完了している)
	shutil.copytree(develop_dir, publish_dir)
	# 公開後の後片付け
	def cleanup_proc():
		del_dir(publish_dir)
	# packagesの列挙
	packages = listup_packages(publish_dir)
	return _EzpipPackageResult(cleanup_proc, publish_name, packages, root_dir = publish_dir + "/../", version = new_version)
