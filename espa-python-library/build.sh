#!/usr/bin/sh
set -x
set -e

rm -rf mock_result
rm -f SRPMS/*.src.rpm
REPOS="espa-python-library"
branch="master"

if [ ! -f SOURCES/$REPOS.tar.gz ]; then
    for repo in $REPOS; do
	(cd ../../$repo && \
	 git  archive --format=tar.gz \
	      -o ../espa-rpmbuild/$repo/SOURCES/$repo.tar.gz  \
	      --prefix=$repo/ $branch)
    done
fi

for repo in $REPOS; do
    my_dist=$(cd ../../$repo; git describe --long --tags | awk -F'-g' '{print "g"$2}')
    rpmbuild --define "_topdir $(pwd)" --define "dist $my_dist" -bs SPECS/$repo.spec
    sudo mock --old-chroot  --configdir=$(pwd)/../mock_config --define "dist $my_dist" \
	 -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*${my_dist}*.src.rpm

    root=/efs
    rm -f $root/CentOS/7/local/x86_64/RPMS/${repo}*
    mkdir -p $root/CentOS/7/local/x86_64/
    find ./ -name \*.x86_64.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \;
    createrepo $root/CentOS/7/local/x86_64/
done
