#! /usr/bin/env python


from .cli import *
import boto3
import random

PROC_CFG_FILENAME = 'processing.conf'

def main():
    """Configures an order from the command line input and calls the
       processing code using the order
    """

    args = parse_command_line()
    proc_cfg = config.retrieve_cfg(PROC_CFG_FILENAME)

    proc_cfg = override_config(args, proc_cfg)

    try:
        # Extra command line validation
        if args.pixel_size is not None and args.pixel_size_units is None:
            raise CliError('Must specify --pixel-size-units if specifying'
                           ' --pixel-size')

        export_environment_variables(proc_cfg)

        template = load_template(filename=TEMPLATE_FILENAME)

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
        response = queue.send_message(MessageBody=json.dumps(order), MessageGroupId="ESPA", MessageDeduplicationId=str(random.getrandbits(128)))

        print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))

    except Exception as e:
	print(e)
        sys.stderr.write('Error(s) during job submission\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
