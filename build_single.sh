#!/bin/sh
set -x
set -e

if [ ! -z "$1" ]; then
    repo=$1
else
    echo "No repo set"
    exit 1
fi

root=/devel/$USER

pushd $repo
sudo rm -rf ./mock_result
rm -f ./SRPMS/*.src.rpm
rm -f ./SOURCES/$repo.tar.gz

if [ ! -z "$2" ]; then
    branch="$2"
else
    branch="master"
fi

if [ ! -f SOURCES/$repo.tar.gz ]; then
    for repo in $repo; do
	(cd ../../$repo && \
	 git  archive --format=tar.gz \
	      -o ../espa-rpmbuild/$repo/SOURCES/$repo.tar.gz  \
	      --prefix=$repo/ $branch)
    done
fi

my_dist=$(cd ../../$repo; git describe --long --tags | awk -F'-g' '{print ".g"$2}')
rpmbuild --define "_topdir $(pwd)" --define "dist $my_dist" -bs SPECS/*$repo.spec
sudo mock --verbose \
     --configdir=$(pwd)/../mock_config \
     --define "dist $my_dist" \
     -r my-epel-7-x86_64 \
     --resultdir=$(pwd)/mock_result \
     SRPMS/*${my_dist}*.src.rpm

mkdir -p $root/CentOS/7/local/x86_64/
rm -f $root/CentOS/7/local/x86_64/RPMS/${repo}*
find ./ -name \*.x86_64.rpm -o -name \*.noarch.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \;
createrepo $root/CentOS/7/local/x86_64/
