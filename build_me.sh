#!/usr/bin/sh
set -x
set -e

pushd /efs;
python -m SimpleHTTPServer 9000 &
pid=$! ;  echo "simple server pid $pid"
popd

process_repos () {
for repo in $1; do
    (cd $repo; \
     rpmbuild --define "_topdir $(pwd)" -bs SPECS/*.spec \
     && sudo mock $old_chroot --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm \
     && find ./ -name \*.x86_64.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \; \
     && createrepo $root/CentOS/7/local/x86_64 \
     )
done
}

REPOS_no="\
	geotiff \
	hdf4 \
	HDF-EOS \
	gdal"

REPOS="\
	geotiff"

# for building inside a docker container
#old_chroot="--no-clean --old-chroot" 
old_chroot=""
root=/efs

pushd ../../ips-all/ips_rpmbuild/
process_repos "$REPOS"
popd

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
     espa-plotting \
     espa-processing"

process_repos "$REPOS"
kill $pid
exit
