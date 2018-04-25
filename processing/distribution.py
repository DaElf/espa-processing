
''' Provides methods for creating and distributing products '''


import os
import sys
import shutil
import glob
from time import sleep

import settings
import utilities
import sensor
import transfer


def package_product(immutability, source_directory, destination_directory,
                    product_name):
    '''
    Description:
      Package the contents of the source directory into a gzipped tarball
      located in the destination directory and generates a checksum file for
      it.

      The filename will be prefixed with the specified product name.

    Returns:
      product_full_path - The full path to the product including filename
      cksum_full_path - The full path to the check sum including filename
      cksum_value - The checksum value
    '''



    product_full_path = os.path.join(destination_directory, product_name)

    # Make sure the directory exists.
    utilities.create_directory(destination_directory)

    # Remove any pre-existing files
    # Grab the first part of the filename, which is not unique
    filename_parts = product_full_path.split('-')
    filename_parts[-1] = '*'  # Replace the last element of the list
    filename = '-'.join(filename_parts)  # Join with '-'

    # Name of the checksum to be created
    cksum_filename = '.'.join([product_name, settings.ESPA_CHECKSUM_EXTENSION])

    # Remove the file first just in-case this is a second run
    cmd = ' '.join(['rm', '-f', filename])
    output = ''
    try:
        output = utilities.execute_cmd(cmd)
    finally:
        if len(output) > 0:
            logging.info(output)

    # Change to the source directory
    current_directory = os.getcwd()
    os.chdir(source_directory)

    try:
        # Tar the files
        logging.info("Packaging completed product to %s.tar.gz"
                    % product_full_path)

        # Grab the files to tar and gzip
        product_files = glob.glob("*")

        # Execute tar with zipping, the full/path/*.tar.gz name is returned
        product_full_path = utilities.tar_files(product_full_path,
                                                product_files, gzip=True)

        # Change file permissions
        logging.info("Changing file permissions on %s to 0644"
                    % product_full_path)
        os.chmod(product_full_path, 0644)

        # Verify that the archive is good
        output = ''
        cmd = ' '.join(['tar', '-tf', product_full_path])
        try:
            output = utilities.execute_cmd(cmd)
        finally:
            if len(output) > 0:
                logging.info(output)

        # If it was good create a checksum file
        cksum_output = ''
        cmd = ' '.join([settings.ESPA_CHECKSUM_TOOL, product_full_path])
        try:
            cksum_output = utilities.execute_cmd(cmd)
        finally:
            if len(cksum_output) > 0:
                logging.info(cksum_output)

        # Get the base filename of the file that was checksum'd
        cksum_prod_filename = os.path.basename(product_full_path)

        logging.debug("Checksum file = %s" % cksum_filename)
        logging.debug("Checksum'd file = %s" % cksum_prod_filename)

        # Make sure they are strings
        cksum_values = cksum_output.split()
        cksum_value = "%s %s" % (str(cksum_values[0]),
                                 str(cksum_prod_filename))
        logging.info("Generating cksum: %s" % cksum_value)

        cksum_full_path = os.path.join(destination_directory, cksum_filename)

        try:
            with open(cksum_full_path, 'wb+') as cksum_fd:
                cksum_fd.write(cksum_value)
        except Exception:
            logging.exception('Error building checksum file')
            raise

    finally:
        # Change back to the previous directory
        os.chdir(current_directory)

    return (product_full_path, cksum_full_path, cksum_value)


def distribute_product_remote(immutability, product_name, source_path,
                              packaging_path, cache_path, parms):



    opts = parms['options']

    env = Environment()

    # Determine the remote hostname to use
    destination_host = utilities.get_cache_hostname(env.get_cache_host_list())

    # Deliver the product files
    # Attempt X times sleeping between each attempt
    sleep_seconds = settings.DEFAULT_SLEEP_SECONDS
    max_number_of_attempts = settings.MAX_DISTRIBUTION_ATTEMPTS
    max_package_attempts = settings.MAX_PACKAGING_ATTEMPTS
    max_delivery_attempts = settings.MAX_DELIVERY_ATTEMPTS

    attempt = 0
    product_file = 'ERROR'
    cksum_file = 'ERROR'
    while True:
        try:
            # Package the product files
            # Attempt X times sleeping between each sub_attempt
            sub_attempt = 0
            while True:
                try:
                    (product_full_path, cksum_full_path,
                     local_cksum_value) = package_product(immutability,
                                                          source_path,
                                                          packaging_path,
                                                          product_name)
                except Exception:
                    logging.exception("An exception occurred processing %s"
                                     % product_name)
                    if sub_attempt < max_package_attempts:
                        sleep(sleep_seconds)  # sleep before trying again
                        sub_attempt += 1
                        continue
                    else:
                        raise
                break

            # Distribute the product
            # Attempt X times sleeping between each sub_attempt
            sub_attempt = 0
            while True:
                try:
                    (remote_cksum_value, product_file, cksum_file) = \
                        transfer_product(immutability, destination_host,
                                         cache_path,
                                         opts['destination_username'],
                                         opts['destination_pw'],
                                         product_full_path, cksum_full_path)
                except Exception:
                    logging.exception("An exception occurred processing %s"
                                     % product_name)
                    if sub_attempt < max_delivery_attempts:
                        sleep(sleep_seconds)  # sleep before trying again
                        sub_attempt += 1
                        continue
                    else:
                        raise
                break

            # Checksum validation
            if local_cksum_value.split()[0] != remote_cksum_value.split()[0]:
                raise ESPAException("Failed checksum validation between"
                                    " %s and %s:%s"
                                    % (product_full_path,
                                       destination_host,
                                       product_file))

            # Always log where we placed the files
            logging.info("Delivered product to %s at location %s"
                        " and cksum location %s" % (destination_host,
                                                    product_file, cksum_file))
        except Exception:
            if attempt < max_number_of_attempts:
                sleep(sleep_seconds)  # sleep before trying again
                attempt += 1
                # adjust for next set
                sleep_seconds = int(sleep_seconds * 1.5)
                continue
            else:
                raise
        break

    return (product_file, cksum_file)


def distribute_product_local(immutability, product_name, source_path,
                             packaging_path):



    # Deliver the product files
    # Attempt X times sleeping between each attempt
    sleep_seconds = settings.DEFAULT_SLEEP_SECONDS
    max_number_of_attempts = settings.MAX_DISTRIBUTION_ATTEMPTS
    max_package_attempts = settings.MAX_PACKAGING_ATTEMPTS

    attempt = 0
    product_file = 'ERROR'
    cksum_file = 'ERROR'

    while True:
        try:
            # Package the product files to the online cache location
            # Attempt X times sleeping between each sub_attempt
            sub_attempt = 0
            while True:
                try:
                    (product_file, cksum_file,
                     local_cksum_value) = package_product(immutability,
                                                          source_path,
                                                          packaging_path,
                                                          product_name)

                    # Change the attributes on the files so that we can't
                    # remove them
                    if immutability:
                        cmd = ' '.join(['sudo', 'chattr', '+i', product_file,
                                        cksum_file])
                        output = utilities.execute_cmd(cmd)
                        if len(output) > 0:
                            logging.info(output)

                except Exception:
                    logging.exception("An exception occurred processing %s"
                                     % product_name)
                    if sub_attempt < max_package_attempts:
                        sleep(sleep_seconds)  # sleep before trying again
                        sub_attempt += 1
                        continue
                    else:
                        raise
                break

            # Always log where we placed the files
            logging.info("Delivered product to location %s"
                        " and checksum location %s" % (product_file,
                                                       cksum_file))
        except Exception:
            if attempt < max_number_of_attempts:
                sleep(sleep_seconds)  # sleep before trying again
                attempt += 1
                # adjust for next set
                sleep_seconds = int(sleep_seconds * 1.5)
                continue
            else:
                raise
        break

    return (product_file, cksum_file)


def distribute_product(immutability, product_name, source_path,
                       packaging_path, parms):
    '''
    Description:
        Determines if the distribution method is set to local or remote and
        calls the correct distribution method.

    Returns:
      product_file - The full path to the product either on the local system
                     or the remote destination.
      cksum_value - The check sum value of the product.

    Args:
        immutability - Wether or not to set the immutability flag on the
                       product files
        product_name - The name of the product.
        source_path - The full path to of directory containing the data to
                      package and distribute.
        package_dir - The full path on the local system for where the packaged
                      product should be placed under.
        parms - All the user and system defined parameters.
    '''

    env = Environment()

    distribution_method = env.get_distribution_method()

    # The file paths to the distributed product and checksum files
    product_file = 'ERROR'
    cksum_file = 'ERROR'

    if distribution_method == DISTRIBUTION_METHOD_LOCAL:
        # Use the local cache path
        cache_path = os.path.join(settings.ESPA_LOCAL_CACHE_DIRECTORY,
                                  parms['orderid'])

        # Override if we are doing bridge processing
        if parms['bridge_mode']:
            sensor_info = sensor.info(parms['product_id'])
            cache_path = os.path.join(settings.ESPA_LOCAL_CACHE_DIRECTORY,
                                      str(sensor_info.date_acquired.year),
                                      str(sensor_info.path).lstrip('0'),
                                      str(sensor_info.row).lstrip('0'))

        # Adjust the packaging_path to use the cache
        package_path = os.path.join(packaging_path, cache_path)

        (product_file, cksum_file) = \
            distribute_product_local(immutability,
                                     product_name,
                                     source_path,
                                     package_path)

    else:  # remote
        # Use the remote cache path
        cache_path = os.path.join(settings.ESPA_REMOTE_CACHE_DIRECTORY,
                                  parms['orderid'])

        (product_file, cksum_file) = \
            distribute_product_remote(immutability,
                                      product_name,
                                      source_path,
                                      packaging_path,
                                      cache_path,
                                      parms)

    return (product_file, cksum_file)
