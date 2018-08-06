# -*- coding: utf-8 -*-
"topcli configuration module."

import os
import pickle

home = os.path.expanduser("~")
configdir = os.path.join(home, ".topcli")
configfile = os.path.join(configdir, "config")

# created a config directory
if not os.path.exists(configdir):
    os.mkdir(configdir)

if not os.path.exists(configfile):
    with open(configfile, 'w') as f:
        cfg = {}
        cfg['installed_tasks'] = {}
        pickle.dump(cfg, f)

with open(configfile, 'r') as f:
    config = pickle.load(f)

del home
del configdir
del configfile
