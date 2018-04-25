''' Generate the products the system is capable of producing.
'''

import datetime
import logging

import cfg
import sensor
import schema
import staging
import providers
import distribution


def distribute_product(product_name, destination, output_dir, parms=None):
    """Packaging and distribution of the product
    """
    try:
        return distribution.distribute_product(destination, product_name,
                                               output_dir, parms)
    except Exception:
        logging.exception('An exception occurred delivering the product')
        raise


def stage_input_data(product_id, download_urls, untar=True):
    """Stages the input data required for the processor
    """
    try:
        return stage_input_data(product_id, download_urls, untar=True)
    except Exception:
        logging.exception('An exception occurred stagging the product')
        raise


def get_product_name(input_name, fmt_str):
    """Build the product name from the product information and current time
    """
    return fmt_str.format(prefix=str(sensor.info(input_name).product_prefix),
                          timestamp=datetime.datetime.utcnow())


def get_product_bucket(parms, fmt_str):
    """Build the product name from the product information and current time
    """
    return fmt_str.format(**parms)


# ===========================================================================
def process(cfg, parms):
    """ Product processing state flow management and fulfilment

    Args:
        cfg (dict): environmental configuration
        parms (dict): processing request options

    Returns:
        dict: execution status, resources used, and metadata
    """

    # Verify work request schema
    parms = schema.load(parms)

    # Build the product name
    product_name = get_product_name(parms['input_name'],
                                    cfg.get('output_filename_fmt'))

    # Initialize the processing directory.
    directories = staging.initialize_processing_directory(cfg.get('work_dir'))

    # Stage the required input data
    staging.stage_input_data(download_urls=parms['input_urls'],
                             staging=directories.get('stage'),
                             destination=directories.get('work'),
                             unpack=cfg.get('unpack_formats'),
                             remove_staged=cfg.get('keep_intermediate','').lower() != 'false')

    logging.warning(providers.sequence(parms['products'][0], product_id=parms['input_name']))

    # Remove science products and intermediate data not requested
    cleanup_work_dir()

    # Customize products
    customize_products()

    # Generate statistics products
    generate_statistics()

    # Reformat product
    reformat_products()

    # [[ Formatting-Resource Snapshot ]]
    snapshot_resources()

    # Package and deliver product
    destination_product, destination_cksum = distribute_product()

    # Remove the product directory
    # Free disk space to be nice to the whole system.
    remove_product_directory()

    return {"resources": None, "logs": None, "metadata": None, "results": None}
