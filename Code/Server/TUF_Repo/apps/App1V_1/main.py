import json
import logging
import os
import signal
import subprocess
import sys
import time
CONFIG_FILE = 'config.json'



def handler(signum, frame):
    logging.critical("uninstall iptables firewall")
    _call('iptables -F\n')  # delete all firewall configurations
    sys.exit()


def run():
    signal.signal(signal.SIGTERM, handler)
    configure_logs()
    while 1:
        execute_config()
        time.sleep(20)




def execute_config():
    """Loads a iptables configuration from config.json and executes it."""
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir,'config.json')) as json_file:
        data = json.load(json_file)
        data = data["ip_rule_set"]
        _call('echo \"firewall App running\"\n')
        _call('iptables -F\n')
        _call('iptables -X\n')
        for date in data:
            command = "iptables -A {} ".format(date['chain'])
            if date['packet_type'] != "all":
                command += "-p {} ".format(date['packet_type'])

            if date['destination_port'] > 0:
                command += "--dport {} ".format(date['destination_port'])
            command += "-j {}\n".format(date['action'])
            try:
                _call(command) #/bin/bash call
            except subprocess.CalledProcessError as error:
                logging.error("Error applying firewall rule.".format(error.stderr))


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


def configure_logs() -> None:
    script_dir = os.path.dirname(__file__)
    if not os.path.isfile(os.path.join(script_dir, "firewall.log")):
        os.mknod(os.path.join(script_dir, "firewall.log"))
    # noinspection PyArgumentList
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=os.path.join(script_dir, "firewall.log"),
        # filemode="w",
        format="{asctime} - {levelname:8}: {message}",
        level=logging.INFO,
        style="{"
    )
    logging.info("IPTables Firewall started.")


if __name__ == "__main__":
    run("")
