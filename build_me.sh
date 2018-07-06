#!/usr/bin/sh
set -x
set -e

root=/devel/$USER

pushd $root;
python -m SimpleHTTPServer 9000 &
pid=$! ;  echo "simple server pid $pid"
popd

sigint()
{
   echo "signal INT received, script ending"
   kill $pid
   exit 0
}

trap 'sigint'  INT

process_repos () {
for repo in $1; do
    my_dist=$(cd ../$repo; git describe --long --tags | awk -F'-g' '{print "g"$2}')
    (cd ../$repo && \
	 git  archive --format=tar.gz \
	      -o ../espa-rpmbuild/$repo/SOURCES/$repo.tar.gz  \
	      --prefix=$repo/ master)
    (cd $repo; \
     rm -f SRPMS/*.src.rpm; sudo rm -rf mock_result;  \
     rpmbuild --define "_topdir $(pwd)" --define "dist $my_dist" -bs SPECS/$repo.spec \
	 && sudo mock $old_chroot --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --define "dist $my_dist" \
		 --resultdir $(pwd)/mock_result SRPMS/*${my_dist}*.src.rpm \
	 && rm -f $root/CentOS/7/local/x86_64/RPMS/${repo}* \
	 && find ./ -name \*.x86_64.rpm -exec rsync -aP {} $root/CentOS/7/local/x86_64/RPMS/ \; \
	 && createrepo $root/CentOS/7/local/x86_64 \
     )
done
}

REPOS="\
	geotiff \
	hdf4 \
	HDF-EOS \
	gdal"

# for building inside a docker container
#old_chroot="--no-clean --old-chroot" 
old_chroot=""

#pushd ../../ips-all/ips_rpmbuild/
#process_repos "$REPOS"
#popd

REPOS="\
     espa-product-formatter \
     espa-cloud-masking \
     espa-python-library \
     espa-l2qa-tools \
     espa-spectral-indices \
     espa-surface-water-extent \
     espa-surface-reflectance \
     espa-surface-temperature \
     espa-elevation \
     espa-reprojection \
     espa-plotting"

#espa-processing

process_repos "$REPOS"

kill $pid
exit
