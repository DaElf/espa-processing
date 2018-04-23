''' Generate the products the system is capable of producing.
'''

import os
import shutil
import logging

import settings
import utilities
import sensor
import landsat_metadata
import staging
import transfer
import distribution


def remove_product_directory(self):
    """Remove the product directory
    """

    options = self._parms['options']

    # We don't care about this failing, we just want to attempt to free
    # disk space to be nice to the whole system.  If this processing
    # request failed due to a processing issue.  Otherwise, with
    # successfull processing, hadoop cleans up after itself.
    if self._product_dir is not None and not options['keep_directory']:
        shutil.rmtree(self._product_dir, ignore_errors=True)


def distribute_product(self):
    """Does both the packaging and distribution of the product using
        the distribution module
    """

    product_name = self.get_product_name()

    # Deliver the product files
    product_file = 'ERROR'
    cksum_file = 'ERROR'
    try:
        immutability = self._cfg.getboolean('processing',
                                            'immutable_distribution')

        (product_file, cksum_file) = \
            distribution.distribute_product(immutability,
                                            product_name,
                                            self._work_dir,
                                            self._output_dir,
                                            self._parms)
    except Exception:
        self._logger.exception('An exception occurred delivering'
                                ' the product')
        raise

    self._logger.info('*** Product Delivery Complete ***')

    # Let the caller know where we put these on the destination system
    return (product_file, cksum_file)


def reformat_products(self):
    """Reformat the customized products if required for the processor
    """

    # Nothing to do if the user did not specify anything to build
    if not self._build_products:
        return

    options = self._parms['options']

    # Convert to the user requested output format or leave it in ESPA ENVI
    # We do all of our processing using ESPA ENVI format so it can be
    # hard-coded here
    product_formatting.reformat(self._xml_filename, self._work_dir,
                                'envi', options['output_format'])

def stage_input_data(self):
    """Stages the input data required for the processor
    """

    product_id = self._parms['product_id']
    download_url = self._parms['download_url']

    file_name = ''.join([product_id,
                            settings.LANDSAT_INPUT_FILENAME_EXTENSION])
    staged_file = os.path.join(self._stage_dir, file_name)

    # Download the source data
    transfer.download_file_url(download_url, staged_file)

    # Un-tar the input data to the work directory
    staging.untar_data(staged_file, self._work_dir)
    os.unlink(staged_file)

    #----<<<<<<<
    product_id = self._parms['product_id']
    download_url = self._parms['download_url']

    file_name = ''.join([product_id,
                            settings.MODIS_INPUT_FILENAME_EXTENSION])
    staged_file = os.path.join(self._stage_dir, file_name)

    # Download the source data
    transfer.download_file_url(download_url, staged_file)

    self._hdf_filename = os.path.basename(staged_file)
    work_file = os.path.join(self._work_dir, self._hdf_filename)

    # Copy the staged data to the work directory
    shutil.copyfile(staged_file, work_file)
    os.unlink(staged_file)


def get_product_name(product_id):
    """Build the product name from the product information and current
        time
    """
    ts = datetime.datetime.today()

    # Extract stuff from the product information
    product_prefix = sensor.info(product_id).product_prefix

    product_name = ('{0}-SC{1}{2}{3}{4}{5}{6}'
                    .format(product_prefix,
                            str(ts.year).zfill(4),
                            str(ts.month).zfill(2),
                            str(ts.day).zfill(2),
                            str(ts.hour).zfill(2),
                            str(ts.minute).zfill(2),
                            str(ts.second).zfill(2)))
    return product_name


# ===========================================================================
def process(cfg, parms):
    """ TODO: what is this doing?
    """

    # Logs the order parameters that can be passed to the mapper for this
    # processor
    log_order_parameters()

    # Translate product identification
    input_info = sensor.info(parms['product_id'])

    # Build the product name
    product_name = get_product_name(input_info)

    # Create the product directory name
    product_dirname = '-'.join([str(order_id), str(product_id)])

    # Initialize the processing directory.
    initialize_processing_directory()

    # Stage the required input data
    stage_input_data()

    # Create the combinded stats and plots
    process_stats()

    # Remove science products and intermediate data not requested
    cleanup_work_dir()

    # Customize products
    customize_products()

    # Generate statistics products
    generate_statistics()

    # Distribute statistics
    distribute_statistics()

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
