import pip
import os

path = os.path.abspath("sw")
assert os.path.exists(path)
pip.main(["install", "-r", "requirements.txt", "--no-index", "-f", "file://%s" % path])

