import subprocess

subprocess.run(["raspivid", "-o", "test.h264", "-t", "30000"])
