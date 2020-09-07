import datetime
import os
import shutil

import securesystemslib
import tuf.formats
import tuf.log
import tuf.repository_tool as repo_tool
from tuf.scripts.repo import import_privatekey_from_file

PROG_NAME = 'repo.py'

REPO_DIR = 'tufrepo'
CLIENT_DIR = 'tufclient'
KEYSTORE_DIR = '../tufkeystore'

ROOT_KEY_NAME = 'root_key'
TARGETS_KEY_NAME = 'targets_key'
SNAPSHOT_KEY_NAME = 'snapshot_key'
TIMESTAMP_KEY_NAME = 'timestamp_key'
PW = 'pw'

STAGED_METADATA_DIR = '/tufrepo/metadata.staged'
METADATA_DIR = '/tufrepo/metadata'

# The supported keytype strings (as they appear in metadata) are listed here
# because they won't necessarily match the key types supported by
# securesystemslib.
SUPPORTED_KEY_TYPES = ('ed25519', 'ecdsa-sha2-nistp256', 'rsa')


def add_conf(configuration_file):
    """
     <Purpose>
       Adds a file to the repo and generates all the necessary metadata
     <Arguments>
       configuration_file:
         The file to eb added to the directory.
     <Exceptions>

     <Side Effects>
       None.
     <Returns>
       None.
     """
    repo_targets_path = os.path.join(os.getcwd(), 'tufrepo', 'targets')
    print(repo_targets_path)
    repository = repo_tool.load_repository(os.path.join(os.getcwd(), REPO_DIR))

    # Copy the configuration to the repo directory and add them to the targets metadata
    # Code to which does the same as add_target_to_repo
    securesystemslib.util.ensure_parent_dir(
        os.path.join(repo_targets_path, configuration_file))
    shutil.copy(configuration_file, os.path.join(repo_targets_path, configuration_file))

    roleinfo = tuf.roledb.get_roleinfo(
        'targets', repository_name=repository._repository_name)

    # It is assumed we have a delegated role, and that the caller has made
    # sure to reject top-level roles specified with --role.
    if configuration_file not in roleinfo['paths']:
        # logger.debug('Adding new target: ' + repr(target_path))
        roleinfo['paths'].update({configuration_file: {}})

    else:
        # logger.debug('Replacing target: ' + repr(target_path))
        roleinfo['paths'].update({configuration_file: {}})

    tuf.roledb.update_roleinfo('targets', roleinfo,
                               mark_role_as_dirty=True, repository_name=repository._repository_name)

    consistent_snapshot = tuf.roledb.get_roleinfo('root',
                                                  repository._repository_name)['consistent_snapshot']

    # Load the top-level, non-root, keys to make a new release.
    targets_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR, 'targets_key'),
        PW)
    repository.targets.load_signing_key(targets_private)

    # make relaese
    snapshot_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR, SNAPSHOT_KEY_NAME),
        PW)
    timestamp_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR,
                     TIMESTAMP_KEY_NAME), PW)

    repository.snapshot.load_signing_key(snapshot_private)
    repository.timestamp.load_signing_key(timestamp_private)
    #TODO in Produktion auf Vernüniftige werte setzten
    repository.targets.expiration = datetime.datetime(2080, 10, 28, 12, 8)
    repository.snapshot.expiration = datetime.datetime(2080, 10, 28, 12, 8)
    repository.timestamp.expiration = datetime.datetime(2080, 10, 28, 12, 8)

    repository.writeall(consistent_snapshot=consistent_snapshot)
    write_to_live_repo()


def write_to_live_repo():
    staged_meta_directory = os.path.join(
        REPO_DIR, STAGED_METADATA_DIR)
    live_meta_directory = os.path.join(
        REPO_DIR, METADATA_DIR)
    staged_meta_directory = os.getcwd() + staged_meta_directory
    live_meta_directory = os.getcwd() + live_meta_directory

    shutil.rmtree(live_meta_directory, ignore_errors=True)
    shutil.copytree(staged_meta_directory, live_meta_directory)


def delete_conf(file):
    repository = repo_tool.load_repository(os.path.join(os.getcwd(), REPO_DIR))

    # NOTE: The following approach of using tuf.roledb to update the target TODO
    # files will be modified in the future when the repository tool's API is
    # refactored.
    roleinfo = tuf.roledb.get_roleinfo(
        'targets', repository._repository_name)

    del roleinfo['paths'][file]

    tuf.roledb.update_roleinfo(
        'targets', roleinfo, mark_role_as_dirty=True,
        repository_name=repository._repository_name)

    targets_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR, TARGETS_KEY_NAME),
        PW)
    repository.targets.load_signing_key(targets_private)

    # Load the top-level keys for Snapshot and Timestamp to make a new release.
    snapshot_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR, SNAPSHOT_KEY_NAME),
        PW)
    timestamp_private = import_privatekey_from_file(
        os.path.join(os.getcwd(), KEYSTORE_DIR,
                     TIMESTAMP_KEY_NAME), PW)

    repository.snapshot.load_signing_key(snapshot_private)
    repository.timestamp.load_signing_key(timestamp_private)

    consistent_snapshot = tuf.roledb.get_roleinfo('root',
                                                  repository._repository_name)['consistent_snapshot']
    repository.writeall(consistent_snapshot=consistent_snapshot)
    write_to_live_repo()


# Move staged metadata directory to "live" metadata directory.
if __name__ == '__main__':
    delete_conf("App1V_1.zip")
    #delete_conf('App9V_2.zip')
    add_conf("App1V_1.zip")

