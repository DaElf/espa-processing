#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
import logging
from configparser import ConfigParser

from . import settings as settings
from . import utilities as util
from . import config_utils as config
from .logging_tools import EspaLogging
from . import processor as processor
from . import transfer as transfer
from .cli import archive_log_s3
from .cli import archive_log_files
from .cli import copy_log_file
from .cli import export_environment_variables

from .espa_worker import validate_order
from .espa_worker import process_order


APP_NAME = 'ESPA-Processing-Worker'
VERSION = '2.23.0.1'


def main():
    """Read a JSON file with details about an order from
       an S3 bucket and process the order
    """

    if len(sys.argv) != 2:
        sys.stderr.write('Error: expected one argument, got {}'.format(len(sys.argv) - 1))
        sys.exit(1)
    order_id = sys.argv[1]
    s3_key = order_id + '/' + order_id + '.json'

    job_bucket = "jdc-test-dev"  # JDC debug
    if 'espaJobBucket' in os.environ:
        job_bucket = os.environ['espaJobBucket']
    if 'AWSRegion' in os.environ:
        s3 = boto3.resource('s3', region_name = os.environ['AWSRegion'])
    else:
        s3 = boto3.resource('s3')

    s3 = boto3.resource("s3").Bucket(job_bucket)
    try:
        json.load_s3 = lambda f: json.load(s3.Object(key=f).get()["Body"])
        order = json.load_s3(s3_key)
    except Exception as e:
        sys.stderr.write("Can't load JSON object from s3: {}".format(e))
        sys.exit(1)

    if not validate_order(order):
        sys.stderr.write('Invalid order')
        sys.exit(1)

    # JDC Debug
    print("Processing order " + order['orderid'])
    print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
    process_order(order)


if __name__ == '__main__':
    main()
