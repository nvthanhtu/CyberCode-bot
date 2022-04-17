import subprocess
import sys

required = ["numpy", "PIL", "opencv-python"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
def main():
    for package in required:
        install(package)
    
if __name__ == "__main__":
    main()