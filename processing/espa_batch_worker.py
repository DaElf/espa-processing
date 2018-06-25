#! /usr/bin/env python


import os
import sys
import string
import json
import boto3

from espa_worker import validate_order
from espa_worker import process_order


APP_NAME = 'ESPA-Processing-Batch-Worker'
VERSION = '2.23.0.1'


def parse_s3_url(url):
    """Parse an S3 URL

    Args:
        url <string>: A URL in the form s3://<bucket>/<key>

    Returns:
        (bucket, key) (<string>, <string>): A tuple with the S3 bucket and key
    """

    u_list = string.split(url, '/')

    if len(u_list) < 4 or \
            u_list[0] != 's3:' or \
            u_list[1] != '':
        sys.stderr.write("Error: Badly formed URL: {}\n".format(url))
        return(None, None)

    return(u_list[2], string.join(u_list[3:], '/'))


def main():
    """Read a JSON file with details about an order from
       an S3 bucket and process the order

        Command line parameter:
            URL <str>: A URL in the form s3://<bucket>/<key>
    """

    if len(sys.argv) != 2:
        sys.stderr.write('Error: expected one argument, got {}\n'.format(len(sys.argv) - 1))
        sys.exit(1)

    (job_bucket, s3_key) = parse_s3_url(sys.argv[1])
    if job_bucket is None:
        sys.stderr.write('Error: invalid URL {}\n'.format(sys.argv[1]))
        sys.exit(1)

    if 'AWSRegion' in os.environ:
        s3 = boto3.resource('s3', region_name = os.environ['AWSRegion'])
    else:
        s3 = boto3.resource('s3')

    s3 = boto3.resource('s3').Bucket(job_bucket)
    try:
        json.load_s3 = lambda f: json.load(s3.Object(key=f).get()['Body'])
        order = json.load_s3(s3_key)
    except Exception as e:
        sys.stderr.write("Error: Can't load S3 JSON object: {}\n".format(e))
        sys.exit(1)

    if not validate_order(order):
        sys.stderr.write('Error: Invalid order\n')
        sys.exit(1)

    # JDC Debug
    print('Processing order ' + order['orderid'])
    print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
    process_order(order)


if __name__ == '__main__':
    main()
