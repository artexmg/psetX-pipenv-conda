import tempfile

fp = tempfile.TemporaryFile()
fp.write(b"Jello!")

fp.seek(0)
fp.read()

f = tempfile.NamedTemporaryFile(delete=False)
f.name