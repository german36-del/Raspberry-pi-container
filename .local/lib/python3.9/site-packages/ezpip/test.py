
import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
# 公開用パッケージの作成 [ezpip]
import _develop_ezpip as ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_dummy_module/", version = "1.0.*") as p:
	# 本番ではここにsetup()などを記載
	sout(p.version)
	sout(p.packages)
	sout(p.long_description)
	input("press [Enter] to continue>")
