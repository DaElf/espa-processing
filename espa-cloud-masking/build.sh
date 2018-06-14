#!/usr/bin/sh
set -x
set -e

if [ ! -f SOURCES/espa-cloud-masking.tar.gz ]; then
(cd ../../espa-cloud-masking; \
	 git  archive --format=tar.gz \
	-o ../espa-rpmbuild/espa-cloud-masking/SOURCES/espa-cloud-masking.tar.gz  \
	--prefix=espa-cloud-masking-1.0/ master)
fi
rpmbuild --define "_topdir $(pwd)" -bs SPECS/*.spec
sudo mock --old-chroot  --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm

