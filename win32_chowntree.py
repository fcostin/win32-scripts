"""
recursively set file access permissions for win32

file access permissions are replaced, allowing everyone all access

only tested on windows 7 ultimate N

based on Tim Golden's incredibly helpful example here:
    http://timgolden.me.uk/python/win32_how_do_i/add-security-to-a-file.html
"""

import sys
import os
import win32security
import ntsecuritycon as con
import argparse
import logging


def fix_access(file_name, acc_name):
    """
    replace access permissions for file with FILE_ALL_ACCESS for acc_name
    """
    logging.info('fixing access for "%s"' % file_name)
    sd = win32security.GetFileSecurity(file_name, win32security.DACL_SECURITY_INFORMATION)
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, acc_name)
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(file_name, win32security.DACL_SECURITY_INFORMATION, sd)

def fix_access_subtree(root, acc_name):
    """
    recursively replace access permissions from root path using os.path.walk
    """
    def f(_, dirname, file_names):
        for file_name in file_names:
            path = os.path.join(dirname, file_name)
            fix_access(path, acc_name)
    os.path.walk(root, f, None)

def get_acc_name(name):
    acc_name, _, _ = win32security.LookupAccountName('', name)
    return acc_name

def parse_args(args):
    p = argparse.ArgumentParser(description='recursively enable all permissions for files in target_dir')
    p.add_argument('root', metavar='DIR', help='target directory')
    p.add_argument('-u', '--user_account_name', metavar='USERNAME', dest='account_name', default='Everyone', help='account name. Default is "Everyone".')
    return p.parse_args()

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s')

def main(argv=None):
    setup_logging()
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    fix_access_subtree(args.root, get_acc_name(args.account_name))

if __name__ == '__main__':
    main()

