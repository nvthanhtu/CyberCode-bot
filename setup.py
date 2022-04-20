import subprocess
import sys

required = ["numpy", "Pillow", "opencv-python", "pywin32"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
def main():
    for package in required:
        install(package)
    
if __name__ == "__main__":
    main()
