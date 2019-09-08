import sys
import os
import subprocess

scripts = os.path.dirname(sys.executable)
pyuic = os.path.join(scripts, "pyuic5.exe")

if not os.path.exists("ui"):
    os.mkdir("ui")
if not os.path.exists("src"):
    os.mkdir("src")

uis = os.listdir("./ui")
for ui in uis:
    inFile = os.path.join("ui", ui)
    outFile = os.path.join("src", ui).replace(".ui", ".py")
    subprocess.run([pyuic, "-x", inFile, "-o", outFile], capture_output=True)
