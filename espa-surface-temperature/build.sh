#!/usr/bin/sh
set -x
set -e

rm ./SRPMS/*.src.rpm
if [ ! -f SOURCES/espa-surface-temperature.tar.gz ]; then
(cd ../../espa-surface-temperature; \
	 git  archive --format=tar.gz \
	-o ../espa-rpmbuild/espa-surface-temperature/SOURCES/espa-surface-temperature.tar.gz  \
	--prefix=espa-surface-temperature-1.1.1/ master)
fi
rpmbuild --define "_topdir $(pwd)" -bs SPECS/*.spec
sudo mock --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm

