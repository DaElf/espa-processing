#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
import random
import string
from argparse import ArgumentParser


import settings
import utilities as util
import config_utils as config
import cli as cli


def parse_command_line():
    """Parse the command line

    Override def parse_command_line() from cli.py
    to add job submission arguments.

    Returns:
        <parser>: Command line parser
    """

    parser = cli.build_command_line_parser()

    submit = parser.add_argument_group('job submission specifics')
    submit.add_argument('--batch-command',
                          action='store',
                          type=str,
                          dest='batch_cmd',
                          default=None,
                          help='Command to run in batch container (developer convenience)')
    submit.add_argument('--job-bucket',
                          action='store',
                          type=str,
                          dest='job_bucket',
                          default=None,
                          help='S3 bucket to hold job information')
    submit.add_argument('--job-definition',
                          action='store',
                          type=str,
                          dest='job_definition',
                          default=None,
                          help='Job definition name for batch job')
    submit.add_argument('--no-submit',
                          action='store_true',
                          dest='no_submit',
                          default=False,
                          help="Don't submit job, just print S3 URL of job order file (default: False)")
    submit.add_argument('--s3-job-prefix',
                          action='store',
                          type=str,
                          dest='s3_job_prefix',
                          default=None,
                          help='S3 job file prefix')
    submit.add_argument('--queue',
                          action='store',
                          type=str,
                          dest='job_queue',
                          default=None,
                          help='Queue to submit job')

    return parser.parse_args()


def submit_job(args, order):
    """Submit a job to the batch queue

    Create a directory with the order ID in the job bucket.  Put
    a file with the JSON-encoded order in the directory.  Submit
    a job to the queue with a parameter specifying the location
    of the order file.  The JSON-encoded order and the
    processing.conf file are copied to the job bucket.

    Args:
        order <dict>: Dictionary with the job parameters
    """

    if not args.no_submit:
        if args.job_queue is not None:
            queue_name = args.job_queue
        elif 'espaQueue' in os.environ:
            queue_name = os.environ['espaQueue']
        else:
            sys.stderr.write("Error: queue name not set\n" +
                    "       Must use --queue or set espaQueue\n")
            sys.exit(1)

    if args.job_definition is not None:
        job_definition = args.job_definition
    elif 'espaJobDefinition' in os.environ:
        job_definition = os.environ['espaJobDefinition']
    else:
        sys.stderr.write("Error: job definition not set\n" +
                "       Must use --job-definition or set espaJobDefinition\n")
        sys.exit(1)

    if args.job_bucket is not None:
        job_bucket = args.job_bucket
    elif 'espaJobBucket' in os.environ:
        job_bucket = os.environ['espaJobBucket']
    else:
        sys.stderr.write("Error: job bucket not set\n" +
                "       Must use --job-bucket or set espaJobBucket\n")
        sys.exit(1)

    if 'AWSRegion' in os.environ:
        s3 = boto3.resource('s3', region_name=os.environ['AWSRegion'])
    else:
        s3 = boto3.resource('s3')

    proc_cfg_file = config.get_cfg_file_path(cli.PROC_CFG_FILENAME)
    if proc_cfg_file is None:
        sys.stderr.write("Error: no processing.conf file\n")
        sys.exit(1)
    elif not os.path.isfile(proc_cfg_file):
        sys.stderr.write("Error: can't find file {}\n".format(proc_cfg_file))
        sys.exit(1)

    order_id = order['orderid']
    if args.s3_job_prefix is not None:
        s3_prefix = args.s3_job_prefix + '/' + order_id
    else:
        s3_prefix = order_id

    s3_key = s3_prefix + '/' + order_id + '.json'
    s3_url = 's3://' + job_bucket + '/' + s3_key

    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=job_bucket, Body=json.dumps(order), Key=s3_key)

    s3_key = s3_prefix + '/' + proc_cfg_file.split('/')[-1]
    s3_client.upload_file(proc_cfg_file, job_bucket, s3_key)

    # JDC Debug
#   print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
    if args.batch_cmd is not None:
        batch_cmd = args.batch_cmd
    else:
        batch_cmd = 'espa-worker.sh'

    if args.no_submit:
        print(s3_url)
    else:
        client = boto3.client('batch')
        client.submit_job(
                jobName = order['orderid'],
                jobQueue = queue_name,
                jobDefinition = job_definition,
                parameters = {'order_url': s3_url},
                containerOverrides = {
                    'command': [batch_cmd, 'Ref::order_url']
                })

        # JDC Debug
        print("Submitted job {} to queue {}".format(
                order['orderid'], queue_name))


def main():
    """Configures an order from the command line input and submits the
       order to the SQS queue specified in SQSBatchQueue
    """

    args = parse_command_line()
    if args.order_id.lower() == 'random':
        args.order_id = ''.join(random.choice(string.ascii_lowercase) \
                for _ in range(4)) + '-00001'

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
            template = cli.load_template(filename=cli.TEMPLATE_FILENAME)

        order = cli.update_template(args=args, template=template)
        if args.batch_cmd is not None:
            order['batch_cmd'] = args.batch_cmd
        order['proc_cfg'] = proc_cfg.items('processing')

        submit_job(args,order)

    except Exception as e:
        sys.stderr.write('Error: {}\n'.format(e))
        raise
        sys.exit(1)


if __name__ == '__main__':
    main()
