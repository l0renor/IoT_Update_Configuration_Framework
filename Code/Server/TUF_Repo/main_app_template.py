import signal
import subprocess
import sys

CONFIG_FILE = 'config.json'



def handler(signum, frame):
    #Code hier wird vor dem Deinstallieren der App ausgefürt.
    #Eventuell vorgenommene Änderungen am System sollten hier Rückgängig gemacht werden.
    sys.exit()


def run():
    signal.signal(signal.SIGTERM, handler)
    #Registriert Handler für das Desinstallieren.
    #App-Code hier.------------------------------------------------



## bash ------------------------------------------------------------
class CallError(Exception):
    pass


def _call(cmd: str) -> str:
    try:
        output: str = subprocess.run(
            cmd,
            shell=True,
            check=True,
            executable="/bin/bash"
        ).stdout
        return output
    except subprocess.CalledProcessError as e:
        raise CallError(e.stderr)





if __name__ == "__main__":
    run()
