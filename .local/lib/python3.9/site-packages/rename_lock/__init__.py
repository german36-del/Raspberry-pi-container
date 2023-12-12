
# Easy file exclusive locking tool [rename_lock]

import os
import sys
import fies
import time
import random
from sout import sout

# 16進数の全文字列
all_16 = list("0123456789abcdef")

# ランダムな16進数の文字列の生成
def gen_rand_16(digits = 64):
	return "".join([
		random.choice(all_16)	# 16進数の全文字列
		for _ in range(digits)
	])

# 名称変更後のファイル名を生成
def gen_post_filename(filename):
	post_filename = "%s_%s.locked"%(
		filename,
		gen_rand_16(digits = 64)	# ランダムな16進数の文字列の生成
	)
	return post_filename

# path.existsは嘘をつくことがあるので、本当に存在するかを確かめる
def strong_ensure(filename):
	if os.path.exists(filename) is False: return False
	try:
		with open(filename, "br") as f:
			pass
	except:
		return False
	return True

# 名称変更のトライアルループ
def rename_loop(filename, post_filename, retry_interval):
	while True:
		"""
			【！】注意【！】
			ここの実装は非常に違和感があるかもしれないが、これで正しい。
			特にwindows環境では、os.rename()は
			「変更できていないのにエラーを吐かない」「変更できているのにエラーを吐く」など、あらゆる可能性があるため、
			成否に関して全く信用することができない。このため、成否の判定はstrong_ensure()関数に完全に任せる実装となっている。
		"""
		try:
			# 変更の試行
			os.rename(filename, post_filename)
		except:
			pass
		# path.existsは嘘をつくことがあるので、本当に存在するかを確かめる
		if strong_ensure(post_filename) is True:
			# 成功時
			return True
		time.sleep(retry_interval)

# ロックオブジェクト
class RLockObj:
	# 初期化処理
	def __init__(self, org_filename, post_filename):
		# 変更後ファイル名
		self.filename = post_filename
		# 元のファイル名
		self.org_filename = org_filename
	# ロック解除
	def unlock(self):
		# 名称変更によるロック解除
		os.rename(self.filename, self.org_filename)
	# with構文突入時
	def __enter__(self):
		return self	# 自身を返す (with構文の簡易的な使い方)
	# with構文脱出時
	def __exit__(self, ex_type, ex_value, trace):
		# ロック解除
		self.unlock()

# ロックオブジェクト生成
def rename_lock(filename, retry_interval = 0.0001):
	# 名称変更後のファイル名を生成
	post_filename = gen_post_filename(filename)
	# 名称変更のトライアルループ
	rename_loop(filename, post_filename, retry_interval)
	# ロックオブジェクト
	rlock = RLockObj(filename, post_filename)
	return rlock

# 呼び出しの準備
sys.modules[__name__] = rename_lock	# モジュールオブジェクトとrename_lock関数を同一視
