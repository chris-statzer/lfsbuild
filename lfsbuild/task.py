import json
import logging
import os

import download
import config

log = logging.getLogger('TASK')

class Task(object):
    """docstring for Task."""
    def __init__(self, filename):
        super(Task, self).__init__()
        self.filename = filename
        self.data = None
        with open(filename, 'r') as json_file:
            self.data = json.loads(json_file.read())
        # print self.data

    def run(self):
        log.info('Running task: << {} >>'.format(self.name))
        urls = self.data['urls']
        for t in urls:
            file_type = t['type']
            url = t['url']
            md5 = t['md5']
            filename = url[url.rfind('/')+1:]
            download.download(file_type, url, md5)
            if file_type == 'src':
                tar_flags = ''
                if url[-2:] == 'gz':
                    tar_flags = 'xzf'
                elif url[-2:] == 'xz':
                    tar_flags = 'xJf'
                extract_cmd = 'tar {} {}/{} -C {}'.format(tar_flags, config.CACHE_PATH, filename, config.SOURCE_PATH)
                print extract_cmd
    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']
