import os
import logging

log = logging.getLogger("DOWN")


def download(file_type, url, md5):
    # log.info('downloading {} of type {}'.format(url, file_type))
    filename = url[url.rfind('/')+1:]
    if os.path.isfile('cache/{}'.format(filename)):
        log.info('{} exists. Checking md5'.format(filename))
        cache_md5 = os.popen('md5 -q cache/{}'.format(filename)).read().rstrip()
        if cache_md5 == md5:
            log.info('Good md5 using the cached file.')
        else:
            log.error('File {} is bad!'.format(filename))
            return False
    else:
        log.info('Fetching {}...'.format(url))
        return_code = os.system('wget -P ./cache {}'.format(url))
        if return_code != 0:
            log.error('Error downloading {}'.format(url))
            os.system('rm cache/{}'.format(filename))
            return False
        else:
            return True
