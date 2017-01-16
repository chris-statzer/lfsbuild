import yaml
import logging
import os
import glob
import string

import download
import config

log = logging.getLogger('TASK')

tasks = {}

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
        log.info('Running task: <<( {} )>>'.format(self.name))

        # check deps
        if 'deps' in self.data:
            for dep in self.data['deps']:
                tasks[dep].run()

        # Download the package if we dont already have it
        url = self.data['src_uri']
        md5 = self.data['md5']
        filename = url[url.rfind('/')+1:]
        if download.download(url, md5) is False:
            return False

        # extract the package to the src directory
        tar_flags = ''
        if url[-2:] == 'gz':
            tar_flags = 'xzf'
        elif url[-2:] == 'xz':
            tar_flags = 'xJf'
        elif url[-3:] == 'bz2':
            tar_flags = 'xjf'
        extract_cmd = 'tar {} {}/{} -C {}'.format(tar_flags, config.CACHE_PATH, filename, config.SOURCE_PATH)
        log.info('Extracting {} to {}'.format(filename, config.BUILD_PATH))
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
        
        # process actions 
        if self.action == 'build':
            # configure
            configure_args = string.Template(self.config_opts).safe_substitute(config.CONFIGURE_VARS)
            # custom configure command
            custom_configure = 'configure'
            if 'custom_configure_command' in self.data:
                custom_configure = self.data['custom_configure_command']
            # configure ENV vars
            config_env_vars = ''
            if 'config_env_vars' in self.data:
                config_env_vars = string.Template(self.data['config_env_vars']).safe_substitute(config.CONFIGURE_VARS)
            configure_cmd = '{} ../../{}/{} {}'.format(config_env_vars, self.src_path, custom_configure, configure_args)
            log.info('Compiling {} with following options: {}'.format(self.name, configure_cmd))
            os.system(configure_cmd)
            
            # check for premake_commands
            if 'premake_commands' in self.data:
                for pmc in self.data['premake_commands']:
                    log.info('Running premake command: \n\r{}'.format(pmc))
                    os.system(pmc)
            
            # make
            log.info('Running make on {}...'.format(self.name))
            os.system('make {}'.format(config.MAKE_OPTS))

            # make install
            log.info('Installing {}....'.format(self.name))
            # check for preinstall_commands
            if 'preinstall_commands' in self.data:
                for pic in self.data['preinstall_commands']:
                    log.info('Running preinstall command: \n\r{}'.format(pic))
                    os.system(pic)
            os.system('make install')
        
        elif self.action == 'custom_commands':
            for cc in self.data['commands']:
                os.system(cc)
        os.chdir(config.ROOT_PATH)

    @property
    def name(self):
        return self.data['name']

    @property
    def src_path(self):
        return '{}/{}'.format(config.SOURCE_PATH, self.data['dir_name'])

    @property
    def build_path(self):
        return '{}/{}'.format(config.BUILD_PATH, self.name)

    @property
    def config_opts(self):
        return self.data['config_opts']

    @property
    def action(self):
        try:
            action = self.data['action']
        except KeyError:
            return 'none'
        return action


def load_tasks(path=config.TASK_PATH):
    num_tasks = 0
    task_file_list = glob.glob('{}/*.yaml'.format(config.TASK_PATH))
    for f in task_file_list:
        t = Task(f)
        tasks[t.name] = t
        num_tasks += 1
    log.info('Loaded {} tasks...'.format(num_tasks))
    return tasks
