import yaml
import logging
import os
import glob


import download
import config

log = logging.getLogger('TASK')

class Task(object):
    """docstring for Task."""
    def __init__(self, filename):
        super(Task, self).__init__()
        self.filename = filename
        self.data = None
        with open(filename, 'r') as yaml_file:
            self.data = yaml.load(yaml_file.read())
        # print self.data

    def run(self):
        log.info('Running task: << {} >>'.format(self.name))
        url = self.data['src_uri']
        md5 = self.data['md5']
        filename = url[url.rfind('/')+1:]

        if download.download(url, md5) is True:
            tar_flags = ''
            if url[-2:] == 'gz':
                tar_flags = 'xzf'
            elif url[-2:] == 'xz':
                tar_flags = 'xJf'
            extract_cmd = 'tar {} {}/{} -C {}'.format(tar_flags, config.CACHE_PATH, filename, config.SOURCE_PATH)
            log.info('Extracting {} to {}'.format(filename, config.SOURCE_PATH))
            return_code = os.system(extract_cmd)
    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']


def load_tasks(path=config.TASK_PATH):
    tasks = {}
    num_tasks = 0
    task_file_list = glob.glob('{}/*.yaml'.format(config.TASK_PATH))
    for f in task_file_list:
        t = Task(f)
        tasks[t.name] = t
        num_tasks += 1
    log.info('Loaded {} tasks...'.format(num_tasks))
    return tasks
