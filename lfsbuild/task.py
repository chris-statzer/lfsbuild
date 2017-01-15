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

        # Download the package if we dont already have it
        if download.download(url, md5) is False:
            return False

        # extract the package to the src directory
        tar_flags = ''
        if url[-2:] == 'gz':
            tar_flags = 'xzf'
        elif url[-2:] == 'xz':
            tar_flags = 'xJf'
        extract_cmd = 'tar {} {}/{} -C {}'.format(tar_flags, config.CACHE_PATH, filename, config.SOURCE_PATH)
        log.info('Extracting {} to {}'.format(filename, config.SOURCE_PATH))
        return_code = os.system(extract_cmd)
        if return_code != 0:
            log.error('Error extracting {}'.format(filename))
            return False

        # delete old build directory if it exists
        if os.path.isdir(self.build_path):
            os.system('rm -rf {}'.format(self.build_path))

        # now create the build path and change to it
        os.system('mkdir {}'.format(self.build_path))
        os.chdir(self.build_path)

        os.system('../../{}/configure'.format(self.src_path))
        os.system('make')
    @property
    def name(self):
        return self.data['name']

    @property
    def src_path(self):
        return '{}/{}'.format(config.SOURCE_PATH, self.data['dir_name'])

    @property
    def build_path(self):
        return '{}/{}'.format(config.BUILD_PATH, self.name)


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
