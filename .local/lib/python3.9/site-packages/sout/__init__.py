
# 巨大オブジェクトのデバッグ表示 [sout]

import sys
import json

indent_str = "  "

# コンテナ的な型の表示
def container_stringify(
	iter_target,	# イテレート対象
	element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
	brackets,	# 括弧
	indent_depth,	 # インデント深さ
	element_limit,	# 省略の度合い
	one_line	# 1行で表示
):
	# インデント文字列準備
	if one_line is True:
		idt0, idt1 = "", ""
	else:
		idt0, idt1 = indent_str*indent_depth, indent_str*(indent_depth+1)
	if element_limit is None: element_limit = len(iter_target)
	bra, ket = brackets
	show_ls = []
	show_ls.append(bra)
	for i,e in enumerate(iter_target):
		if i >= element_limit:
			show_ls.append(idt1 + "... (all_n = %d)"%len(iter_target))
			break
		# カンマ (最終要素の場合はカンマなし)
		if i == len(iter_target) - 1:
			comma_str = ""
		else:
			comma_str = ", " if one_line is True else ","
		# 追記
		show_ls.append(idt1 + element_str_func(e) + comma_str)
	show_ls.append(idt0 + ket)
	if one_line is True:
		show_str = "".join(show_ls)
	else:
		show_str = "\n".join(show_ls)
	return show_str

# 再帰的に可視化につかうオブジェクトを作る
def gen_show_str(data, element_limit, indent_depth, one_line_limit = 40):
	# 1行で表示できるかを試す (複数行指定の場合でも)
	if one_line_limit is not None:
		# 強制的に1行で表示してみる
		one_line_str = gen_show_str(data, element_limit, indent_depth, one_line_limit = None)
		if len(one_line_str) <= one_line_limit: return one_line_str
	# 型ごとに分岐
	if type(data) == type({}):
		# 辞書の場合
		def element_str_func(key):
			return "%s: %s"%(
				gen_show_str(key, element_limit, indent_depth+1, one_line_limit),	# キー
				gen_show_str(data[key], element_limit, indent_depth+1, one_line_limit)	# 値
			)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["{", "}"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	elif type(data) == type([]):
		# リストの場合
		def element_str_func(elem):
			return gen_show_str(elem, element_limit, indent_depth+1, one_line_limit)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["[", "]"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	elif type(data) == type(()):
		# タプルの場合
		def element_str_func(elem):
			return gen_show_str(elem, element_limit, indent_depth+1, one_line_limit)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["(", ")"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	elif type(data) == type({1,2}):
		# 集合の場合
		def element_str_func(elem):
			return gen_show_str(elem, element_limit, indent_depth+1, one_line_limit)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["{", "}"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	elif type(data) == type(""):
		# 文字列の場合
		if one_line_limit is None:
			limit_len = 1000
		else:
			limit_len = one_line_limit
		if len(data) > limit_len:
			show_data = data[:limit_len] + " ... (len = %d)"%len(data)
		else:
			show_data = data
		show_str = json.dumps(show_data, ensure_ascii = False)
	elif data.__class__.__name__ == "Table":
		# json-stockのtableの場合
		def element_str_func(key):
			return "%s: %s"%(
				gen_show_str(key, element_limit, indent_depth+1, one_line_limit),	# キー
				gen_show_str(data[key], element_limit, indent_depth+1, one_line_limit)	# 値
			)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["<json-stock Table {", "}>"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	elif data.__class__.__name__ == "JsonStock":
		# json-stockのdbの場合
		def element_str_func(key):
			return "%s: %s"%(
				gen_show_str(key, element_limit, indent_depth+1, one_line_limit),	# キー
				gen_show_str(data[key], element_limit, indent_depth+1, one_line_limit)	# 値
			)
		# コンテナ的な型の表示
		show_str = container_stringify(
			data,	# イテレート対象
			element_str_func,	# 要素の可視化 (引数はイテレートして出てくるもの)
			["<json-stock DB {", "}>"],	# 括弧
			indent_depth,	 # インデント深さ
			element_limit,	# 省略の度合い
			one_line = (one_line_limit is None)	# 1行で表示
		)
	else:
		show_str = str(data)
	return show_str

# 巨大オブジェクトのデバッグ表示(文字列化のみ) [sout]
def souts(
	data,	# 表示すべきデータ
	element_limit = 5	# 省略の度合い (None指定で全表示)
):
	# 再帰的に可視化につかうオブジェクトを作る
	show_str = gen_show_str(
		data,
		element_limit,
		indent_depth = 0,
		one_line_limit = 40
	)
	return show_str

# 巨大オブジェクトのデバッグ表示 [sout]
def sout(
	data,	# 表示すべきデータ
	element_limit = 5	# 省略の度合い (None指定で全表示)
):
	# 巨大オブジェクトのデバッグ表示(文字列化のみ) [sout]
	show_str = souts(data, element_limit)
	print(show_str)
