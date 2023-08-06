from pyzipper import ZipFile

file = ZipFile("./test/flag.zip")
file.extractall("./test", pwd=b"123")