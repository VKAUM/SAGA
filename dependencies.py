import subprocess

# List of dependencies (excluding built-in modules)
dependencies = [
    "SpeechRecognition",
    "pyaudio",
    "numpy",
    "pymongo",
    "Pillow",  # Pillow instead of PIL
    "mediapipe"
]

# Install the dependencies using pip
def install_dependencies():
    for dep in dependencies:
        try:
            subprocess.check_call(['pip', 'install', dep])
            print(f"Successfully installed {dep}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {dep}")

    # Install OpenCV separately
    try:
        subprocess.check_call(['pip', 'install', 'opencv-python'])
        print("Successfully installed OpenCV (cv2)")
    except subprocess.CalledProcessError:
        print("Failed to install OpenCV (cv2)")

if __name__ == "__main__":
    install_dependencies()
