#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
import logging


import settings as settings
import utilities as util
import config_utils as config
from logging_tools import EspaLogging
import processor as processor
import transfer as transfer
from cli import archive_log_s3 
from cli import archive_log_files
from cli import copy_log_file
from cli import export_environment_variables


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
    EspaLogging.configure_base_logger(filename=cli_log_filename(order),
                                          level=logging.INFO)

    # Configure the processing logger for this request
    EspaLogging.configure(settings.PROCESSING_LOGGER,
                          order=order['orderid'],
                          product=order['product_id'],
                          debug=order['options']['debug'])
    # Get a logger
    logger = EspaLogging.get_logger('base')

    return logger


def clear_environment_variables(cfg):
    """Clear the configuration environment variables

    Args:
        cfg <ConfigParser>: Configuration
    """

    for key, value in cfg.items('processing'):
        del os.environ['key.upper()']


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


def validate_order(order):
    """Validate the order

    Check that required elements are in the order

    Args:
        order <dict>: the order to be validated
    """

    # Check for required arguments
    try:
        order_id = order['orderid']
        scene = order['scene']
        product_id = order['product_id']
        product_type = ['product_type']
        download_url= ['download_url']
        espa_api= ['espa_api']
        bridge_mode= ['bridge_mode']
        options = ['options']
    except KeyError as e:
        print("Error in order: [{}] not present".format(str(e)))
        return False

    return True


def process_order(order):
    """Process the order

    Args:
        order <dict>: the order to be processed
    """

    current_directory = os.getcwd()
    logger = cli_log_setup(order)

    order_id = order['orderid']
    try:
        logger.info('*** Begin ESPA Processing on host [{}] ***'
                    .format(socket.gethostname()))
        logger.info('Order ID [{}]'.format(order_id))

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
            os.chdir(current_directory)
            clear_environment_variables(proc_cfg)

    except Exception as e:
        print(e)
        logger.exception('*** Errors during processing ***')

    if not order['bridge_mode']:
        archive_log_files(order, proc_cfg, proc_status)

    if order['dist_method'] is not None and order['dist_method'] == 's3':
        archive_log_s3(order=order, base_log=cli_log_filename(order))

    if logger is not None:
        logger.info('*** ESPA Processing Complete ***')
        EspaLogging.shutdown()

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
        print("Starting to listen", len(message_list))
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

        if not validate_order(order):
            continue

        print json.dumps(order, sort_keys=True, indent=4, separators=(',', ': '))
        process_order(order)


if __name__ == '__main__':
    main()
