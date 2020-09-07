import json
import logging
import os
import shutil
import subprocess
import time
from zipfile import ZipFile
from multiprocessing import Process

import requests

from os import sys, path

from jose import jws

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # fix imports
from client.tuf_client import update_conf

INFO_FILE = "device_info.json"
INSTALLED_REQUIREMENTS_FILE = "installed_requirements.json"
LOG_FILE = "log/main.log"
LOOP_WAIT_TIME = 20
TERMINATE_WAIT_TIME = 20
KEY = '97OhFFgOHNFHMiQ6wuqFfGn7atS0mtm1BLFlu7vsRTHlgP6FgUUp3b7_ETuzi5lsyqavKNko-TNOzbJ8UCViCg'


def remove_app_from_config(old_app):
    with open(INFO_FILE) as json_file:
        device_info = json.load(json_file)
        device_info["applications"].remove(old_app)

    with open(INFO_FILE, 'w') as outfile:
        json.dump(device_info, outfile)

    return device_info["applications"]


# returns installed app even if app is null
def add_app_to_config(new_app):
    with open(INFO_FILE) as json_file:
        device_info = json.load(json_file)
        if new_app is not None:
            device_info["applications"].append(new_app)
        with open(INFO_FILE, 'w') as outfile:
            json.dump(device_info, outfile)
    return device_info["applications"]


def load_application_config():
    logging.info("loading device info:")
    new_apps = []
    old_apps = []

    with open(INFO_FILE) as json_file:
        device_info = json.load(json_file)
        device_config = download_and_verify("/rest/stage1/devices/")
        if not device_config:
            logging.error("Connection to Rest Server failed")
            return None, None, None

    inst_apps = device_info["applications"]
    configured_apps = device_config["applications"]
    for conf_app in configured_apps:
        to_install = True
        for installed in inst_apps:
            if conf_app["id"] == installed["id"] and conf_app["version"] == installed["version"]:
                to_install = False
        if to_install:
            new_apps.append(conf_app)

    for installed in inst_apps:
        to_uninstall = True
        for app in configured_apps:
            if app["id"] == installed["id"] and app["version"] == installed["version"]:
                to_uninstall = False
        if to_uninstall:
            old_apps.append(installed)

    logging.info("Success: Config: device: %s , user %s ", device_info["uuid"], device_info["user"])

    return device_config["host"], new_apps, old_apps


def bash(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, check=True, executable="/bin/bash")


def _importer(name, root_package=False, relative_globals=None, level=0):
    """ We only import modules, functions can be looked up on the module.
    Usage:

    from foo.bar import baz
    >>> baz = importer('foo.bar.baz')

    import foo.bar.baz
    >>> foo = importer('foo.bar.baz', root_package=True)
    >>> foo.bar.baz

    from .. import baz (level = number of dots)
    >>> baz = importer('baz', relative_globals=globals(), level=2)
    """
    return __import__(name, locals=None,  # locals has no use
                      globals=relative_globals,
                      fromlist=[] if root_package else [None],
                      level=level)


def start_app(file):
    try:
        import_statement = '{}.main'.format(file)
        app = _importer(import_statement, root_package=True)
        p = Process(target=app.main.run, args=())
        p.start()
    except:
        logging.error("Error Starting " + file)
        return
    return p


def configure_logs() -> None:
    if not os.path.isfile(LOG_FILE):
        os.mknod(LOG_FILE)
    # noinspection PyArgumentList
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=LOG_FILE,
        filemode="w",
        format="{asctime} - {levelname:8}: {message}",
        level=logging.INFO,
        style="{"
    )
    logging.info("App loader started.")


def install_new_app(app, host_repo):
    update_available = False
    logging.info("installing app id: %s", app['id'])
    base_filename = "App" + str(app["id"]) + "V_" + str(
        app["version"])
    archive_filename = base_filename + ".zip"
    logging.info("Update: %s at %s", archive_filename, host_repo),
    try:
        update_available = update_conf(archive_filename, host_repo)
    except Exception as e:
        logging.error("Cant download %s at %s", archive_filename, host_repo)
        raise e
    logging.info("Download done")
    if update_available:
        logging.info("new version App %s : %s", app["id"], app["version"])
        archive_path = "tufclient/tuftargets/"
        full_archive_filename = os.path.join(os.getcwd(), archive_path, archive_filename)
        with ZipFile(full_archive_filename, 'r') as zip:
            # printing all the contents of the zip file
            zip.printdir()
            # extracting all the files
            logging.info('ZIP:Extracting all the files now...')
            zip.extractall()
            logging.info('ZIP:Done!')
            with open(os.path.join(os.getcwd(), base_filename, "metadata.json")) as metadata:
                data = json.load(metadata)
                install_requirements(data)
            os.remove(full_archive_filename)
    else:
        raise FileNotFoundError
    return base_filename


def install_requirements(metadata):
    with open(INSTALLED_REQUIREMENTS_FILE) as json_file:
        installed = json.load(json_file)
    for req in metadata['apt']:
        if req in installed['apt']:
            installed['apt'][req].append(metadata['app_name'])
        else:
            bash.call('apt-get install ' + req)
            installed['apt'][req] = [metadata['app_name']]
    for req in metadata['pip']:
        if req in installed['pip']:
            installed['pip'][req].append(metadata['app_name'])
        else:
            bash.call(['pip', 'install', '-y', req])
            installed['pip'][req] = [metadata['app_name']]
    with open(INSTALLED_REQUIREMENTS_FILE, 'w') as outfile:
        json.dump(installed, outfile)
    return


def uninstall_requirements(metadata):
    with open(INSTALLED_REQUIREMENTS_FILE) as json_file:
        installed = json.load(json_file)
    for req in metadata['apt']:
        installed['apt'][req].remove(metadata['app_name'])
        if not installed['apt'][req]:
            del installed['apt'][req]
            bash.call('apt-get remove ' + req)

    for req in metadata['pip']:
        installed['pip'][req].remove(metadata['app_name'])
        if not installed['pip'][req]:
            del installed['pip'][req]
            subprocess.call(['pip', 'install', '-y', req])
    with open(INSTALLED_REQUIREMENTS_FILE, 'w') as outfile:
        json.dump(installed, outfile)
    return


def load_app_config(url, targetfile):
    logging.info("App Configuration from: " + url)
    data = download_and_verify(url)
    if data:
        with open(targetfile, 'w') as outfile:
            json.dump(data, outfile)


def download_and_verify(url):
    with open(INFO_FILE) as json_file:
        device_info = json.load(json_file)
    url = device_info["host"] + url
    logging.info("Starting Download from: " + url)
    resp = requests.get(url + str(device_info["uuid"]), auth=(device_info["user"], device_info["password"]))
    try:
        data = jws.verify(resp.json(), KEY, algorithms=['HS512'])
    except:
        logging.error("Wrong signature")
        return
    data = data.decode('ASCII')
    data = json.loads(data)
    return data


if __name__ == "__main__":
    running_apps = {}
    configure_logs()
    logging.info("Started main loop")
    while 1:
        host, to_install, to_uninstall = load_application_config()
        if host is None:
            time.sleep(LOOP_WAIT_TIME)
            continue
        for app in to_install:
            try:
                app_name = install_new_app(app, host)
                add_app_to_config(app)
            except:
                logging.error("Error downloading %s", app["name"])
        installed_apps = add_app_to_config(None)
        logging.info("All apps updated")
        for app in installed_apps:
            app_dir = "App" + str(app["id"]) + "V_" + str(app["version"])
            metadatafile = os.path.join(os.getcwd(), app_dir, "metadata.json")
            with open(metadatafile) as metadatawrapper:
                metadata = json.load(metadatawrapper)
                load_app_config(metadata["config_url"], app_dir + "/config.json")
                logging.info("starting app %s", app["id"])
            if app["id"] not in running_apps:
                process = start_app("App" + str(app["id"]) + "V_" + str(
                    app["version"]))
            if process is not None:
                running_apps[app["id"]] = process

            logging.info("all apps started")
            for app in to_uninstall:
                try:
                    logging.info("killing app %s", app["id"])
                    process = running_apps[app["id"]]
                    process.terminate()
                    time.sleep(1)  # the process can restore the initial state
                    app_dir = "App" + str(app["id"]) + "V_" + str(app["version"])
                    with open(os.path.join(os.getcwd(), app_dir, "metadata.json")) as metadatafile:
                        metadata = json.load(metadatafile)
                        uninstall_requirements(metadata)
                    shutil.rmtree(app_dir, ignore_errors=True)
                    del running_apps[app["id"]]
                    remove_app_from_config(app)

                except Exception as e:
                    logging.error(e)
        logging.info("all apps uninstalled")
        time.sleep(LOOP_WAIT_TIME)
