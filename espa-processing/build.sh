#!/usr/bin/sh
set -x
set -e

if [ ! -f SOURCES/espa-processing.tar.gz ]; then
(cd ../../espa-processing; \
	 git  archive --format=tar.gz \
	-o ../espa-rpmbuild/espa-processing/SOURCES/espa-processing.tar.gz  \
	--prefix=espa-processing-1.0/ ceph)
fi
rpmbuild --define "_topdir $(pwd)" -bs SPECS/espa-processing.spec
sudo mock --old-chroot  --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm

