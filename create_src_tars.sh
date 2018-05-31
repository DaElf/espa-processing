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

for repo in $REPOS_NOT; do
    git submodule add https://github.com/USGS-EROS/$repo
done

