from subprocess import check_output, CalledProcessError, check_call
import glob
import sys
import os
import tempfile

def distribute_sum_directory(path='.', product_name='sum'):

    sum_list = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            sum_list.append(os.path.join(path, name))

    sum_file = product_name + '.sha256'
    try:
    # sha 256 sum all the files
        print("Including sha56 sum off all files")
        cmd = ["sha256sum"] + sum_list
        print ("my cmd ", cmd)
        fout=open(sum_file, 'w')
        check_call(cmd, stdout=fout)
    except IOError as e:
        print("I/O error on '%s': %s" % (e.filename, e.strerror))
        raise
    except CalledProcessError as e:
        print("sha256sum failed: %s" % (str(e)))
        raise
    except OSError as e:
        print("failed to run 'sha256sum': %s" % (str(e)))
        raise
        
    try:
        #tempdir = tempfile.mkdtemp()
        #check_output(['gpg','--homedir',tempdir,'--import','USGS_private.asc'])
        #check_output(['gpg','--homedir',tempdir,'--detach-sig','--armor','sum.sha256'])
        check_output(['gpg', '--yes', '--sign', '--armor', sum_file])
    except IOError as e:
        print("I/O error on '%s': %s" % (e.filename, e.strerror))
    except CalledProcessError as e:
        print("gpg failed: %s" % (str(e)))
    except OSError as e:
        print("failed to run 'gpg': %s" % (str(e)))
