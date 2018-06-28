#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
import random
from argparse import ArgumentParser


import settings
import utilities as util
import config_utils as config
import cli as cli


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
    parser.add_argument('--queue',
                          action='store',
                          type=str,
                          dest='job_queue',
                          default=None,
                          help='Queue to submit job')

    return parser.parse_args()


def submit_SQS_job(args, order):

    sqs_queue_name = None
    if args.job_queue is not None:
        sqs_queue_name = args.job_queue
    elif 'SQSQueue' in os.environ:
           sqs_queue_name = os.environ['SQSQueue']
    else:
        sys.stderr.write("Error: queue name not set\n" +
                "       Must use --queue or set SQSQueue\n")
        sys.exit(1)

    if 'AWSRegion' in os.environ:
        sqs = boto3.resource('sqs', region_name = os.environ['AWSRegion'])
    else:
        sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
    response = queue.send_message(MessageBody=json.dumps(order),
            MessageGroupId = 'ESPA',
            MessageDeduplicationId = str(random.getrandbits(128)))


def submit_batch_job(args, order):
    """Submit a job to the batch queue

    Create a directory with the order ID in the job bucket.  Put
    a file with the JSON-encoded order in the directory.  Submit
    a job to the queue with a parameter specifying the location
    of the order file.

    Args:
        order <dict>: Dictionary with the job parameters
    """

    job_definition = 'ESPA_ProcessJob'  # JDC Debug
    job_bucket = 'jdc-test-dev'  # JDC debug
    queue_name = 'ESPA_ProcessJobQueueNOT'  # JDC Debug

    if args.job_queue is not None:
        queue_name = args.job_queue
    elif 'BatchQueue' in os.environ:
        queue_name = os.environ['BatchQueue']
    else:
        sys.stderr.write("Error: queue name not set\n" +
                "       Must use --queue or set BatchQueue\n")
        sys.exit(1)


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
    s3_url = 's3://' + job_bucket + '/' + s3_key

    s3obj = s3.Object(job_bucket, s3_key)
    order_str = json.dumps(order)
    s3obj.put(Body = order_str)

    client = boto3.client('batch')
#    print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
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
           parameters = {'order_url': s3_url})


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

        if "ESPA_PROCESS_TEMPLATE" in os.environ:
            template = cli.load_template(filename=os.environ["ESPA_PROCESS_TEMPLATE"])
        else:
            template = cli.load_template(filename=TEMPLATE_FILENAME)

        order = cli.update_template(args=args, template=template)
        order['proc_cfg'] = proc_cfg.items('processing')

        if batch_mode:
            submit_batch_job(args,order)
        else:
            submit_SQS_job(args,order)

    except Exception as e:
        sys.stderr.write('Error: {}\n'.format(e))
        raise
        sys.exit(1)


if __name__ == '__main__':
    main()
