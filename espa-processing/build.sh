#!/usr/bin/sh
set -x
set -e

rm -rf mock_result
rm SRPMS/*.src.rpm
REPOS="espa-processing"
if [ ! -f SOURCES/espa-processing.tar.gz ]; then
    for repo in $REPOS; do
	(cd ../../$repo && \
	 git  archive --format=tar.gz \
	      -o ../espa-rpmbuild/$repo/SOURCES/$repo.tar.gz  \
	      --prefix=$repo/ cloud-master)
    done
fi

my_dist=$(cd ../../espa-processing; git describe | awk -F'-g' '{print "g"$2}')
rpmbuild --define "_topdir $(pwd)" --define "dist $my_dist" -bs SPECS/*.spec
sudo mock --old-chroot  --configdir=$(pwd)/../mock_config --define "dist $my_dist" \
     -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm

