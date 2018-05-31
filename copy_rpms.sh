#!/bin/sh
set -x

root=/efs

mkdir -p $root/CentOS/7/local/x86_64/
find ./ -name \*.x86_64.rpm -exec rsync -aP {}  $root/CentOS/7/local/x86_64/RPMS/ \;
createrepo $root/CentOS/7/local/x86_64/
