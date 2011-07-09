"""
recursively set file access permissions for win32

file access permissions are replaced, allowing everyone all access

only tested on windows 7 ultimate N

edit the root path in main() to specify the target

based on Tim Golden's incredibly helpful example here:
    http://timgolden.me.uk/python/win32_how_do_i/add-security-to-a-file.html
"""

import os
import win32api
import win32security
import ntsecuritycon as con

def fix_access(file_name, acc_name):
    """
    replace access permissions for file with FILE_ALL_ACCESS for acc_name
    """
    print 'fixing access for "%s"' % file_name
    sd = win32security.GetFileSecurity(file_name, win32security.DACL_SECURITY_INFORMATION)
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, acc_name)
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    hresult = win32security.SetFileSecurity(file_name, win32security.DACL_SECURITY_INFORMATION, sd)

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

def main():
    root = 'D:\\cygwin_packages' # change this ...
    fix_access_subtree(root, get_acc_name('Everyone'))

if __name__ == '__main__':
    main()
