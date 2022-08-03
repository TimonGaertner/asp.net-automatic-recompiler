import os
import time
import signal
import subprocess
import atexit

class AutomaticRecompile():
    last_saved = 0
    dotnet = None
    def exit_dotnet(this):
        if this.dotnet is not None:
            os.killpg(os.getpgid(this.dotnet.pid), signal.SIGTERM)
    def check_last_save_and_run(this):
        for root, subdirs, files in os.walk(os.getcwd()):
            for i in files:
                if i.endswith(".cs"):
                    file_path=os.path.join(root,i)
                    saved=os.path.getmtime(file_path)
                    if saved > this.last_saved:
                        print("recompiling")
                        this.last_saved = saved
                        this.exit_dotnet()
                        this.dotnet = subprocess.Popen("dotnet run", shell=True, preexec_fn=os.setsid) 
                        return
recompilation = AutomaticRecompile()

atexit.register(recompilation.exit_dotnet)
while True:
    recompilation.check_last_save_and_run()
    time.sleep(1)

