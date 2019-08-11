from pathlib import Path
import subprocess

path = Path(__file__).resolve().parent / "video.py"
print(str(path))
subprocess.run(["python3", str(path)])
