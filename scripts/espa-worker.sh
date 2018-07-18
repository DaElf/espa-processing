#!/bin/sh -x

sudo chmod 777 /jobtmp
my_dir=$(mktemp -p /jobtmp -d -t espa-worker.XXXXXX) || exit 1
chown espa $my_dir

sudo -E -u espa -s <<EOF
set -x
env

aws s3 cp s3://a.out/espa-processing.conf $my_dir/processing.conf
export ESPA_CONFIG_PATH=$my_dir
gpg --import ./gpg-tools/USGS_private.gpg || true
(cd $my_dir; time espa-batch-worker $1)

EOF

ret=$?
echo "Exit now" $ret
exit $ret
