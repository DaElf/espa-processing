#! /usr/bin/env python


import os
import sys
import shutil
import socket
import json
import boto3
from argparse import ArgumentParser


import settings
import utilities as util
import config_utils as config
import cli as cli


def update_template(args, template):

    order = cli.update_template(args, template)

    order['dist_dir'] = args.dist_dir
    order['dist_method'] = args.dist_method
    order['work_dir'] = args.work_dir

    return order

def main():
    """Configures an order from the command line input and calls the
       processing code using the order
    """

    args = cli.parse_command_line()
    proc_cfg = config.retrieve_cfg(cli.PROC_CFG_FILENAME)

    proc_cfg = cli.override_config(args, proc_cfg)

    try:
        # Extra command line validation
        if args.pixel_size is not None and args.pixel_size_units is None:
            raise CliError('Must specify --pixel-size-units if specifying'
                           ' --pixel-size')

        cli.export_environment_variables(proc_cfg)

        template = cli.load_template(filename=cli.TEMPLATE_FILENAME)

        order = update_template(args=args, template=template)

        try:
            sqs_queue_name = os.environ['SQSBatchQueue']
        except Exception as e:
            print(e)
            raise

        try:
            aws_region = os.environ['AWSRegion']
        except KeyError:
            sqs = boto3.resource('sqs')
        else:
            sqs = boto3.resource('sqs', region_name=aws_region)

        queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
        response = queue.send_message(MessageBody=json.dumps(order))

    except Exception as e:
        print(e)
        sys.stderr.write('Error(s) during job submission\n')
        sys.exit(1)


if __name__ == '__main__':
    main()

