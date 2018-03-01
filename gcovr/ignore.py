# -*- coding:utf-8 -*-

# This file is part of gcovr <http://gcovr.com/>.
#
# Copyright 2018 the gcovr authors
# This software is distributed under the BSD license.

import os
import re
import sys

#
# Global cache of ignore rules for directories
#
ignore_cache = {}


#
# Check all paths relative root_dir (including ..) for .gcovrignore files
#
def ignore_file(filename, options):
    if os.path.isabs(filename):
        # Only allow absolute paths if they are subdirs to root dir
        if not filename.startswith(options.root_dir):
            return False
        filename = os.path.relpath(filename, options.root_dir)

    (dir_, name) = os.path.split(filename)
    while True:
        rules = load_ignore_rules(dir_, options)
        if any(rule.match(filename) for rule in rules):
            return True
        if not dir_:
            break
        (dir_, part) = os.path.split(dir_)
        name = os.path.join(part, name)

    return False


#
# Load ignore rules from cache if available otherwise try to load from file
# if .gcovrignore exists in the directory
#
def load_ignore_rules(base, options):
    path = os.path.realpath(os.path.join(options.root_dir, base))
    try:
        return ignore_cache[path]
    except KeyError:
        pass
    file_ = os.path.join(path, '.gcovrignore')
    rules = []
    if os.path.isfile(file_):
        with open(file_) as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                if not line or line[0] == '#':
                    continue
                if os.name == 'nt':
                    rules.append(re.compile(re.escape(base + "\\") + line))
                else:
                    rules.append(re.compile(os.path.join(base, line)))
        if options.verbose:
            sys.stdout.write(
                "Loaded %d rules from %s...\n" % (len(rules), file_)
            )
    ignore_cache[path] = rules
    return rules
