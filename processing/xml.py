""" Utilities to operate on provided ESPA XML metadata """

import os

from espa import Metadata


def remove_band_from_xml(self, band):
    """Remove the band from disk and from the XML
    """

    img_filename = str(band.file_name)
    hdr_filename = img_filename.replace('.img', '.hdr')

    # Remove the files
    if os.path.exists(img_filename):
        os.unlink(img_filename)
    if os.path.exists(hdr_filename):
        os.unlink(hdr_filename)

    # Remove the element
    parent = band.getparent()
    parent.remove(band)


def remove_products_from_xml(self):
    """Remove the specified products from the XML file

    The file is read into memory, processed, and written back out with out
    the specified products.
    """
    # Create and load the metadata object
    espa_metadata = Metadata(xml_filename=self._xml_filename)

    # Search for and remove the items
    for band in espa_metadata.xml_object.bands.band:
        if band.attrib['product'] in products_to_remove:
            # Business logic to always keep the radsat_qa band if bt,
            # or toa, or sr output was chosen
            if (band.attrib['name'] == '' and
                    (options['include_sr'] or options['include_sr_toa'] or
                        options['include_sr_thermal'])):
                continue
            else:
                self.remove_band_from_xml(band)

    # Validate the XML
    espa_metadata.validate()

    # Write it to the XML file
    espa_metadata.write(xml_filename=self._xml_filename)
