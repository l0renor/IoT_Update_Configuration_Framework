import logging
import tuf
import tuf.client.updater
import tuf.settings


def update_conf(filename, host):
    """
         <Purpose>
           Downloads the FILENAME file from the localhost http server
         <Arguments>

         <Exceptions>

         <Side Effects>
           None.
         <Returns>
           None.
         """
    # conf = cc.load_conf(os.path.join(os.getcwd(),'Configuration/conf.json'))
    # Set the local repositories directory containing all of the metadata files.
    tuf.settings.repositories_directory = 'tufclient'

    # Set the repository mirrors.  This dictionary is needed by the Updater
    # class of updater.py.getupdates.pygetupdates.py
    repository_mirrors = {'mirror': {'url_prefix': host,
                                     'metadata_path': 'metadata', 'targets_path': 'targets',
                                     'confined_target_dirs': ['']}}

    # Create the repository object using the repository name 'repository'
    # and the repository mirrors defined above.
    updater = tuf.client.updater.Updater('tufrepo', repository_mirrors)

    # The local destination directory to save the target files.
    destination_directory = './tufclient/tuftargets'

    logging.info("TUF is updating...")
    # Refresh the repository's top-level roles...
    updater.refresh(unsafely_update_root_if_necessary=False)

    # ... and store the target information for the target file specified on the
    # command line, and determine which of these targets have been updated.
    target_fileinfo = []
    target_fileinfo.append(updater.get_one_valid_targetinfo(
        filename))

    updated_targets = updater.updated_targets(target_fileinfo, destination_directory)

    # Retrieve each of these updated targets and save them to the destination
    # directory.
    for target in updated_targets:
        try:
            updater.download_target(target, destination_directory)
            logging.info("TUF  updating  %s", target)

        except tuf.exceptions.DownloadError:
            logging.error("TUF update failed %s", target)

    # Remove any files from the destination directory that are no longer being
    # tracked.
    updater.remove_obsolete_targets(destination_directory)
    if len(updated_targets) > 0:
        return True
    return False


if __name__ == '__main__':
    print('looking for updates')
    if update_conf("App1V_1.zip", "https://dns-rpz.cs.hm.edu:8001"):
        print('found update\n installing update')
