import os
import logging

log = logging.getLogger('CONF')


ROOT_PATH = '/home/daspork/werk/lfsbuild'
TASK_PATH = 'tasks'
CACHE_PATH = 'cache'
SOURCE_PATH = 'src'
PATCH_PATH = 'patch'
BUILD_PATH = 'build'
MAKE_OPTS = '-j 4'

CONFIGURE_VARS = {
    'LFS': '/mnt/lfs',
    'LFS_TGT': 'x86_64-lfs-linux-gnu'}

# check paths and make them if needed
paths = [CACHE_PATH,
         SOURCE_PATH,
         PATCH_PATH,
         BUILD_PATH]
for p in paths:
    if not os.path.isdir(p):
        log.info('Creating missing path: {}'.format(p))
        os.mkdir(p)
