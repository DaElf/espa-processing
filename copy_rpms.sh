#!/bin/sh
set -x

find ./*/RPMS/x86_64 -name \*.rpm -exec rsync -aP {}  $HOME/CentOS/7/local/x86_64/RPMS/ \;
createrepo $HOME/CentOS/7/local/x86_64/
