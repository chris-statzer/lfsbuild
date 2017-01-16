import os
import logging

import config

log = logging.getLogger("DOWN")


def download(url, md5):
    # log.info('downloading {} of type {}'.format(url, file_type))
    filename = url[url.rfind('/')+1:]
    if os.path.isfile('{}/{}'.format(config.CACHE_PATH, filename)):
        log.info('{} exists. Checking md5'.format(filename))
        cache_md5 = os.popen('md5sum {}/{}'.format(config.CACHE_PATH, filename)).read().split(' ')[0].rstrip()
        if cache_md5 == md5:
            log.info('Good md5 using the cached file.')
            return True
        else:
            log.error('File {} is bad!'.format(filename))
            return False
    else:
        log.info('Fetching {}...'.format(url))
        return_code = os.system('wget -P {} {}'.format(config.CACHE_PATH, url))
        if return_code != 0:
            log.error('Error downloading {}'.format(url))
            os.system('rm {}/{}'.format(config.CACHE_PATH, filename))
            return False
        else:
            return True
