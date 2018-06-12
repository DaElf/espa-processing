#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3


import espa_processing.settings as settings
import espa_processing.utilities as util
import espa_processing.config_utils as config
from espa_processing.logging_tools import EspaLogging
import espa_processing.processor as processor
import espa_processing.transfer as transfer


APP_NAME = 'ESPA-Processing-Worker'
VERSION = '2.23.0.1'


def cli_log_filename(order):
    """Specifies the log filename

    Args:
        order <dict>: order parameters
    """

    orderid = "undef"
    product_id = "undef"

    if order['orderid'] is not None:
        orderid = order['orderid']
    if order['product_id'] is not None:
        product_id = order['product_id']
    return 'cli-{}-{}.log'.format(orderid, product_id)


def cli_log_setup(order):

    # Configure the base logger for this request
    EspaLogging.configure_base_logger(filename=cli_log_filename(order))
    # Configure the processing logger for this request
    EspaLogging.configure(settings.PROCESSING_LOGGER,
                          order=order['orderid'],
                          product=order['product_id'],
                          debug=order['options']['debug'])
    # Get a logger
    logger = EspaLogging.get_logger('base')

    return logger


def export_environment_variables(cfg):
    """Export the configuration to environment variables

    Supporting applications require them to be in the environmant

    Args:
        cfg <ConfigParser>: Configuration
    """

    for key, value in cfg.items('processing'):
        os.environ[key.upper()] = value


def override_config(order, proc_cfg):
    """Override configuration with command line values

    Args:
        order <dict>: Order parameters
        proc_cfg <ConfigParser>: Configuration

    Returns:
        <ConfigParser>: Configuration updated (not a copy)
    """

    # Just pretending to be immutable, can't deepcopy ConfigParser
    cfg = proc_cfg

    if order['work_dir'] is not None:
        cfg.set('processing', 'espa_work_dir', order['work_dir'])

    if order['dist_method'] is not None:
        cfg.set('processing', 'espa_distribution_method', order['dist_method'])

    if order['dist_dir'] is not None:
        cfg.set('processing', 'espa_distribution_dir', order['dist_dir'])

    return cfg


def copy_log_file(log_name, destination_path, proc_status):
    """Copy the log file

    Args:
        log_name <str>: Relative path to the log file
        destination_path <str>: Location to copy the log file
        proc_status <bool>: True = Success, False = Error

    Note: proc_status is passed in to allow for the modification of the
          archive filename for the log.  It is meant to mean that processing
          of the scene was successful(True) or not(False).  Allowing users to
          more easily find scenes with failures when looking in the archive
          log directory.
    """

    abs_log_path = os.path.abspath(log_name)
    if proc_status:
        base_log_name = 'success-{}'.format(os.path.basename(log_name))
    else:
        base_log_name = 'error-{}'.format(os.path.basename(log_name))

    # Determine full destination
    destination_file = os.path.join(destination_path, base_log_name)

    # Copy it
    shutil.copyfile(abs_log_path, destination_file)


def archive_log_files(order, proc_cfg, proc_status):
    """Archive the log files for the current execution

    Args:
        order <dict>: Command line arguments
        proc_cfg <ConfigParser>: Configuration
        proc_status <bool>: True = Success, False = Error
    """

    base_log = cli_log_filename(order)
    proc_log = EspaLogging.get_filename(settings.PROCESSING_LOGGER)
    dist_path = proc_cfg.get('processing', 'espa_log_archive')
    destination_path = os.path.join(dist_path, order['orderid'])

    # Create the archive path
    util.create_directory(destination_path)

    # Copy them
    copy_log_file(base_log, destination_path, proc_status)
    copy_log_file(proc_log, destination_path, proc_status)

    # Remove the source versions
    if os.path.exists(base_log):
        os.unlink(base_log)

    if os.path.exists(proc_log):
        os.unlink(proc_log)


def process_order(order):
    """Process the order

    Args:
        order <dict>: the order to be processed
    """

    current_directory = os.getcwd()
    logger = cli_log_setup(order)

    try:
        order_id = order['orderid']
        logger.info('*** Begin ESPA Processing on host [{}] ***'
                    .format(socket.gethostname()))
        logger.info('Order ID [{}]'.format(order_id))
        logger.info(str(order))

        proc_cfg = config.retrieve_cfg(PROC_CFG_FILENAME)
        proc_cfg = override_config(order, proc_cfg)
        export_environment_variables(proc_cfg)

        # Retrieve all of the required auxiliary data.
        if "S3URL" in os.environ:
            if transfer.retrieve_aux_data(order_id) != 0:
                raise CliException('Failed to retrieve auxiliary data.')

        # Change to the processing directory
        os.chdir(proc_cfg.get('processing', 'espa_work_dir'))

        try:
            # All processors are implemented in the processor module
            pp = processor.get_instance(proc_cfg, order)
            (destination_product_file, destination_cksum_file) = pp.process()
        finally:
            # Change back to the previous directory
            os.chdir(current_directory)

    except Exception as e:
        print(e)
        logger.exception('*** Errors during processing ***')

    if logger is not None:
        logger.info('*** ESPA Processing Complete ***')
        EspaLogging.shutdown()

    if not order['bridge_mode']:
        archive_log_files(order, proc_cfg, proc_status)


def get_message_from_sqs():
    """Read a message from the SQS queue

    Returns:
        message <list>: A list of messages that were read
    """

    queue = sqs.get_queue_by_name(QueueName=sqsqueue_name)
    message = queue.receive_messages(WaitTimeSeconds=20,
            MaxNumberOfMessages=1)
    return(message)


PROC_CFG_FILENAME = 'processing.conf'
try:
    sqsqueue_name = os.environ['SQSBatchQueue']
except KeyError as e:
    print("Error: environment variable SQSBatchQueue not defined")
    exit(1)

try:
    aws_region = os.environ['AWSRegion']
except KeyError:
    sqs = boto3.resource('sqs')
else:
    sqs = boto3.resource('sqs', region_name=aws_region)


def main():
    """Get a JSON file with details about an order from
       the SQS queue and process the order
    """

    while True:
        message_list = get_message_from_sqs()
        if len(message_list) == 0:
            continue
        message = message_list[0]

        try:
            order = json.loads(message.body)
            # JDC Debug
            print("Got order " + order['orderid'])
        except Exception as e:
            print(str(e) + " message " + order)
            continue
        finally:
            message.delete()

        process_order(order)


if __name__ == '__main__':
    main()
