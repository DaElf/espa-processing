#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
import random
from argparse import ArgumentParser


from . import settings
from . import utilities as util
from . import config_utils as config
from . import cli as cli


def parse_command_line():
    """Parse the command line

    Override def parse_command_line() from cli.py
    to add a --batch switch.

    Returns:
        <parser>: Command line parser
    """

    parser = cli.build_command_line_parser()

    parser.add_argument('--batch',
                          action='store_true',
                          dest='batch_mode',
                          default=False,
                          help='Queue job for batch processing')

    return parser.parse_args()


def submit_SQS_job(order):

    try:
        sqs_queue_name = os.environ['SQSBatchQueue']
    except Exception as e:
        print('Environment variable {} not set'.format(e))
        raise

    try:
        aws_region = os.environ['AWSRegion']
    except KeyError:
        sqs = boto3.resource('sqs')
    else:
        sqs = boto3.resource('sqs', region_name=aws_region)

    queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
    response = queue.send_message(MessageBody=json.dumps(order),
            MessageGroupId = 'ESPA',
            MessageDeduplicationId = str(random.getrandbits(128)))


def submit_batch_job(order):
    """Submit a job to the batch queue

    Create a directory with the order ID in the job bucket.  Put
    a file with the JSON-encoded order in the directory.  Submit
    a job to the queue with a parameter specifying the location
    of the order file.

    Args:
        order <dict>: Dictionary with the job parameters
    """

    job_definition = 'JobDefinition-2e3ad758b69ada8'  # JDC Debug
    job_bucket = 'jdc-test-dev'  # JDC debug
    queue_name = 'JobQueue-55396c72757b39d'  # JDC Debug

    if 'BatchQueue' in os.environ:
        queue_name = os.environ['BatchQueue']
    if 'espaJobBucket' in os.environ:
        job_bucket = os.environ['espaJobBucket']
    if 'JobDefinition' in os.environ:
        job_definition = os.environ['JobDefinition']

    try:
        aws_region = os.environ['AWSRegion']
    except KeyError:
        s3 = boto3.resource('s3')
    else:
        s3 = boto3.resource('s3', region_name=aws_region)

    order_id = order['orderid']
    s3_key = order_id + '/' + order_id + '.json'

    s3obj = s3.Object(job_bucket, s3_key)
    order_str = json.dumps(order)
    s3obj.put(Body = order_str)

    client = boto3.client('batch')
    print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
    client.submit_job(
            jobName = order['orderid'],
            jobQueue = queue_name,
            jobDefinition = job_definition,
#           containerOverrides = {  # JDC XXX -- dow we need this?
#               "vcpus":2,
#               "memory":2000,
#               "environment": [
#                   {"name": "sourceBucket", "value": bucketName},
#                   {"name": "destBucket", "value": destBucket},
#                   {"name": "sceneToProcess", "value": keyName}
#               ]
#           },
           parameters = {'order': s3_key})


def main():
    """Configures an order from the command line input and submits the
       order to the SQS queue specified in SQSBatchQueue
    """

    args = parse_command_line()
    batch_mode = args.batch_mode

    proc_cfg = config.retrieve_cfg(cli.PROC_CFG_FILENAME)

    proc_cfg = cli.override_config(args, proc_cfg)

    try:
        # Extra command line validation
        if args.pixel_size is not None and args.pixel_size_units is None:
            raise CliError('Must specify --pixel-size-units if specifying'
                           ' --pixel-size')

        template = cli.load_template(filename=cli.TEMPLATE_FILENAME)

        order = cli.update_template(args=args, template=template)
        order['proc_cfg'] = proc_cfg.items('processing')

        if batch_mode:
            submit_batch_job(order)
        else:
            submit_SQS_job(order)

    except Exception as e:
        sys.stderr.write('Error: {}\n'.format(e))
        raise
        sys.exit(1)


if __name__ == '__main__':
    main()

