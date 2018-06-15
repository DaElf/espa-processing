#!/usr/bin/sh
set -x
set -e

REPOS="\
     espa-cloud-masking \
     espa-product-formatter \
     espa-python-library \
     espa-l2qa-tools \
     espa-spectral-indices \
     espa-surface-water-extent \
     espa-surface-reflectance \
     espa-surface-temperature \
     espa-elevation \
     espa-reprojection \
     espa-plotting"

#     espa-processing

for repo in $REPOS; do
    (cd ../$repo; \
     git  archive --format=tar.gz \
	  -o ../espa-rpmbuild/$repo/SOURCES/$repo.tar.gz  \
	  --prefix=$repo/ master)
done

