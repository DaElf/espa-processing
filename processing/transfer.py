
''' Routines for transfering files hosted from different protocols '''

import os
import shutil
import ftplib
import urllib2
import random
import logging
import time

import requests

import settings
import utilities
import staging


def http_transfer_file(remote_url, destination_file,
                       username=None, password=None, timeout=300):
    ''' Chunk HTTP transfer a file from a server URI to local filesystem

    Args:
        remote_url (str): server resource identification/location
        destination_file (str): full path to local file
        username (str): authentication credentials for remote server
        password (str): authentication credentials for remote server
        timeout (int): seconds to wait for server response

    Returns:
        str: path to destination file
    '''
    if not os.path.isdir(destination_file) and os.path.exists(destination_file):
        logging.warning('Already exists: %s \n' % destination_file)
        return

    auth = (username, password) if all((username, password)) else None
    head = requests.head(remote_url, auth=auth, timeout=timeout,
                         verify=False, allow_redirects=True)
    head.raise_for_status()

    logging.info('>>> HEADERS %s', head.headers)
    if os.path.isdir(destination_file):
        if 'Content-Disposition' in head.headers:
            filename = head.headers['Content-Disposition'].split('filename=')[-1]
        else:
            filename = os.path.basename(remote_url)
        destination_file = os.path.join(destination_file, filename)

    file_size = None
    if 'Content-Length' in head.headers:
        file_size = int(head.headers['Content-Length'])

    tmp_file = destination_file + '.part'
    bytes_recv = 0
    if os.path.exists(tmp_file):
        bytes_recv = os.path.getsize(tmp_file)

    logging.info("Downloading %s to %s", remote_url, destination_file)
    resume_header = {'Range': 'bytes=%d-' % bytes_recv}
    sock = requests.get(remote_url, headers=resume_header, stream=True, auth=auth,
                        timeout=timeout, verify=False, allow_redirects=True)

    start = time.time()
    f = open(tmp_file, 'ab')
    bytes_in_mb = 1024*1024
    for block in sock.iter_content(chunk_size=bytes_in_mb):
        if block:
            f.write(block)
            bytes_recv += len(block)
    f.close()
    ns = time.time() - start
    mb = bytes_recv/float(bytes_in_mb)
    logging.info("%s (%3.2f (MB) in %3.2f (s), or  %3.2f (MB/s))", destination_file, mb, ns, mb/ns)

    if bytes_recv >= file_size:
        os.rename(tmp_file, destination_file)
    return destination_file


def local_transfer_file(source_file, destination_file, remove_original=False):
    """ Copy data from source to destination, unpackaging first if needed

    Args:
        source_file (str): path location of local file to copy
        destination_file (str): path to folder or final filename
        remove_original (bool): flag to remove the original file

    Returns:
        str: path to destination file
    """
    logging.debug('Copy file %s to %s', source_file, destination_file)
    if os.path.isdir(destination_file):
        destination_file = os.path.join(destination_file,
                                        os.path.basename(source_file))
    shutil.copyfile(source_file, destination_file)
    if remove_original:
        logging.debug('Remove source file %s', source_file)
        os.unlink(source_file)
    return destination_file


def download_file_url(download_url, destination_file=None, username=None, password=None):
    ''' Using a URL download the specified file to the destination

    Args:
        download_url (str): server resource identification/location
        destination_file (str): full path to local file
        username (str): authentication credentials for remote server
        password (str): authentication credentials for remote server

    Returns:
        str: path to destination file
    '''
    protocol_type = download_url.split("://")[0]
    logging.debug('#### PROTOCOL: %s', protocol_type)
    if protocol_type in ('http', 'https'):
        return http_transfer_file(download_url, destination_file)
    elif protocol_type in ('file', ):
        source_file = download_url.replace('file://', '')
        logging.debug('#### source_file: %s', source_file)
        return local_transfer_file(source_file, destination_file, remove_original=False)
