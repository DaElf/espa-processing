#!/usr/bin/sh
set -x
set -e

REPOS="\
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



for repo in $REPOS_NOT; do
#    mkdir -p $repo/SOURCES $repo/SPECS
    #    (cd $repo/SPECS; rpmdev-newspec $repo)
    (cd $repo; \
     git clone https://github.com/USGS-EROS/$repo;
     cd $repo;
      git archive --format=tar.gz -o ../SOURCES/$repo.tar.gz --prefix=$repo-1.0/ master)

done

for repo in $REPOS; do
    (cd $repo; \
     rpmbuild --define "_topdir $(pwd)" -bs SPECS/$repo.spec; \
     sudo mock --no-clean --old-chroot --configdir=$(pwd)/../mock_config -r my-epel-7-x86_64 --resultdir $(pwd)/mock_result SRPMS/*.src.rpm)
     ./copy_rpms.sh
done

for repo in $REPOS_NOT; do
    git submodule add https://github.com/USGS-EROS/$repo
done

#     sudo mock --no-clean  --old-chroot  -r my-epel-7-x86_64 SRPMS/espa-product-formatter-1.0-1.el7.centos.src.rpm

#(cd espa-product-formatter; git archive --format=tar.gz -o ../SOURCES/espa-product-formatter.tar.gz --prefix=espa-product-formatter-1.0/ master)
