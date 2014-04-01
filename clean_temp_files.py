"""
deletes old files in your windows temp directory

requires win32api
"""


import win32api
import logging
import os.path
import time
import calendar
import shutil
import argparse
import sys
import collections

TYPE_FILE = 'TYPE_FILE'
TYPE_DIR = 'TYPE_DIR'

def gen_pruned_tree(predicate, root_path):
    for root, dirs, files in os.walk(root_path):
        for bag_name, bag in [(TYPE_DIR, dirs), (TYPE_FILE, files)]:
            indices = []
            for i, x in enumerate(bag):
                abs_x = os.path.join(root, x)
                if predicate(abs_x):
                    yield bag_name, abs_x
                    indices.append(i)
            remove_list_items_in_place(bag, indices)

def remove_list_items_in_place(a, indices):
    for i in indices:
        a[i] = None
    while None in a:
        a.remove(None)

TWO_WEEKS_IN_SECONDS = 60 * 60 * 24 * 7 * 2

def parse_args(args):
    p = argparse.ArgumentParser()
    p.add_argument('--temp-root', default=None, type=str, help='root of temp dir. defaults to win32api.GetTempPath().')
    p.add_argument('--actually-delete', default=False, action='store_true', help='ACTUALLY DELETE. ARE YOU SURE?')
    p.add_argument('--max-age', default=TWO_WEEKS_IN_SECONDS, type=int, help='max age, in seconds. defaults to 2 weeks.')
    p.add_argument('--log-level', default='INFO', type=str, help='log level')
    return p.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    logging.basicConfig(level=args.log_level)
    temp_root = args.temp_root
    if temp_root is None:
        temp_root = os.path.abspath(win32api.GetTempPath())

    current_time = calendar.timegm(time.gmtime())
    min_mtime = current_time - args.max_age

    logging.info('temp_root = %r' % (temp_root, ))
    logging.info('max_age = %r' % (args.max_age, ))
    logging.info('current_time = %r' % (current_time, ))
    logging.info('min_mtime = %r' % (min_mtime, ))
    logging.info('actually_delete = %r' % (args.actually_delete, ))

    def has_old_mtime(p):
        return os.path.getmtime(p) < min_mtime

    def noop(x):
        pass

    if args.actually_delete:
        handler_by_type = {TYPE_FILE : os.remove, TYPE_DIR : shutil.rmtree}
    else:
        handler_by_type = {TYPE_FILE:noop, TYPE_DIR:noop}

    stat_by_type = collections.defaultdict(lambda : 0)
    err_stat_by_type = collections.defaultdict(lambda : 0)

    for x_type, x in gen_pruned_tree(has_old_mtime, temp_root):
        x_mtime = os.path.getmtime(x)
        days_old = float(current_time - x_mtime) / (60 * 60 * 24)
        logging.debug('found %r of %r that is %.1f days old' % (x, x_type, days_old))

        try:
            handler_by_type[x_type](x)
            stat_by_type[x_type] += 1
        except Exception as e:
            logging.warn('error while processing %r %r: %r' % (x_type, x, e))
            err_stat_by_type[x_type] += 1

    if args.actually_delete:
        summary_template = 'deleted %r dir(s) and %r file(s)'
    else:
        summary_template = 'dry run - found %r dir(s) and %r file(s) to delete'

    logging.info(summary_template % (stat_by_type[TYPE_FILE], stat_by_type[TYPE_DIR]))

    if err_stat_by_type:
        logging.error('encountered errors processing %r dir(s) and %r file(s)' % (err_stat_by_type[TYPE_FILE], err_stat_by_type[TYPE_DIR]))

    sys.exit(bool(err_stat_by_type))

if __name__ == '__main__':
    main()

