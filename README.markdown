`win32_chowntree`
=================

usage
-----

    C:\>python win32_chowntree.py --help
    usage: win32_chowntree.py [-h] [-u USERNAME] DIR

    recursively enable all permissions for files in target_dir

    positional arguments:
      DIR                   target directory

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --user_account_name USERNAME
                            account name. Default is "Everyone".

`clean_temp_files`
==================

deletes old temp files from your temp directory.


    C:\foo> python clean_temp_files.py --help
    usage: clean_temp_files.py [-h] [--temp-root TEMP_ROOT] [--actually-delete]
                               [--max-age MAX_AGE] [--log-level LOG_LEVEL]

    optional arguments:
      -h, --help            show this help message and exit
      --temp-root TEMP_ROOT
                            root of temp dir. defaults to win32api.GetTempPath().
      --actually-delete     ACTUALLY DELETE. ARE YOU SURE?
      --max-age MAX_AGE     max age, in seconds. defaults to 2 weeks.
      --log-level LOG_LEVEL
                            log level

alternate approaches include:

1.  http://windows.microsoft.com/en-us/windows7/schedule-disk-cleanup-to-run-regularly -- *which opens a dialog*
2.  http://www.howtogeek.com/howto/10705/how-to-schedule-disk-cleanup-in-windows-7-vista/ -- *which uses registry settings, and breaks under windows 7 sometimes in ways the author of the article does not understand*
