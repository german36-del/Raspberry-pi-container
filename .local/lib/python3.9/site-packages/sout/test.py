
# 巨大オブジェクトのデバッグ表示 [sout]
# 【動作確認 / 使用例】

import sys
from ezpip import load_develop
# 巨大オブジェクトのデバッグ表示 [sout]
sout = load_develop("sout", "../", develop_flag = True)

large_obj = [{j:"foo" for j in range(i+2)}
	for i in range(1000)]
sout.sout(large_obj)

# json_stockとの連結テスト

import json_stock as jst
jst_db = jst.JsonStock("test_db")

jst_db["test_table"]["test_key"] = "value"

sout.sout(jst_db["test_table"])
