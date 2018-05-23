#!/bin/sh
set -x

find ./ -name \*.x86_64.rpm -exec rsync -aP {}  $HOME/CentOS/7/local/x86_64/RPMS/ \;
createrepo $HOME/CentOS/7/local/x86_64/
