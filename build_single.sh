#!/bin/sh
set -x
set -e

if [ ! -z "$1" ]; then
    repo=$1
else
    echo "No repo set"
    exit 1
fi

rpmbuild_home=espa-rpmbuild

pushd $repo
sudo rm -rf ./mock_result
rm -f ./SRPMS/*.src.rpm
if [ -d ./SOURCES ]; then
	rm -f ./SOURCES/$repo.tar.gz
else
	mkdir ./SOURCES
fi

if [ ! -z "$2" ]; then
    branch="$2"
else
    branch="master"
fi

if [ ! -f "SOURCES/$repo.tar.gz" ]; then
    (cd ../../$repo && \
	 git  archive --format=tar.gz \
	      -o ../$rpmbuild_home/$repo/SOURCES/$repo.tar.gz  \
	      --prefix=$repo/ $branch)
fi

old_chroot="--old-chroot"
old_chroot=

my_dist=".$(cd ../../$repo; git describe --long --tags | awk -F'-g' '{print "g"$2}')"
if [ -z "$my_dist" ]; then
    my_dist=".eros"
fi

rpmbuild --define "_topdir $(pwd)" \
         --define "dist $my_dist" \
         -bs SPECS/*$repo.spec
sudo mock $old_chroot \
     --no-clean \
     --verbose \
     --configdir=$(pwd)/../mock_config \
     --define "dist $my_dist" \
     -r my-epel-7-x86_64 \
     --resultdir=$(pwd)/mock_result \
     SRPMS/*${my_dist}*.src.rpm

exit 0
# Do not need to stash stuff
root=/devel/$USER
mkdir -p $root/CentOS/7/local/x86_64/
rm -f $root/CentOS/7/local/x86_64/RPMS/${repo}*
find ./ -name \*.x86_64.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \;
find ./ -name \*.noarch.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \;
createrepo $root/CentOS/7/local/x86_64/
