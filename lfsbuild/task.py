import json
import logging
import os

import download

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
        if self.type == 'download':
            self.download()
        else:
            log.error('Unsupported task type: {}'.format(self.type))
            return

    def download(self):
        urls = self.data['urls']
        for t in urls:
            file_type = t['type']
            url = t['url']
            md5 = t['md5']
            download.download(file_type, url, md5)
    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']
