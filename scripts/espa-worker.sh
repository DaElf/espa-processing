#!/bin/sh -x

sudo chmod 777 /jobtmp
my_dir="/jobtmp/$HOSTNAME"
cd $my_dir

sudo -E -u espa -s <<EOF
set -x
env

gpg --import ./gpg-tools/USGS_private.gpg || true
(cd $my_dir; time espa-batch-worker $1)

EOF

ret=$?
echo "Exit now" $ret
exit $ret
