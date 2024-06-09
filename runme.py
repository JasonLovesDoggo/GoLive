from sample_project.app import app
import subprocess
import platform

system = platform.system()
if system == "Windows":
    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    subprocess.call("start chrome --allow-file-access-from-file")

else:
    try:
        subprocess.call("pkill chrome")
        subprocess.call("google-chrome --allow-file-access-from-file")
    except FileNotFoundError:
        # subprocess.call("apt-get update && apt-get install procps -y")
        pass  # It's a server


if __name__ == "__main__":
    import webbrowser
    webbrowser.open_new_tab("http://localhost:5000/")
    app.run(port=5000)
