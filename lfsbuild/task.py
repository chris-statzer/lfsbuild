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
        if os.path.isfile('{}/installed/{}'.format(config.DB_PATH, self.name)):
            log.info('{} is already installed skipping!'.format(self.name))
            return True

        # check deps
        if 'deps' in self.data:
            for dep in self.data['deps']:
                tasks[dep].run()

        # Download the package if we dont already have it
        if 'src_uri' in self.data:
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
            self.run_command(extract_cmd)

        # delete old build directory if it exists
        if os.path.isdir(self.build_path):
            self.run_command('rm -rf {}'.format(self.build_path))

        # now create the build path and change to it
        self.run_command('mkdir {}'.format(self.build_path))
        os.chdir(self.build_path)

        # process actions
        if self.action == 'build':
            # configure
            # check for preconfigure_commands
            self.run_command_list('preconfigure_commands')

            # custom configure command
            custom_configure = 'configure'
            if 'custom_configure_command' in self.data:
                custom_configure = self.data['custom_configure_command']

            # configure ENV vars
            config_env_vars = ''
            if 'config_env_vars' in self.data:
                config_env_vars = self.data['config_env_vars']

            # Format and run configure
            configure_cmd = '{} ../../{}/{} {}'.format(config_env_vars, self.src_path, custom_configure, self.config_opts)
            log.info('Compiling {} with following options: {}'.format(self.name, configure_cmd))
            self.run_command(configure_cmd)

            # check for postconfigure_commands
            self.run_command_list('postconfigure_commands')

            # make
            # check for premake_commands
            self.run_command_list('premake_commands')

            # format and run make
            log.info('Running make on {}...'.format(self.name))
            custom_make_command = 'make {}'.format(config.MAKE_OPTS)
            if 'custom_make_command' in self.data:
                custom_make_command = self.data['custom_make_command']
            self.run_command(custom_make_command)

            # check for postmake_commands
            self.run_command_list('postmake_commands')

            # make install
            log.info('Installing {}....'.format(self.name))

            # check for preinstall_commands
            self.run_command_list('preinstall_commands')

            # Run make install
            custom_install_command = 'make install'
            if 'custom_install_command' in self.data:
                custom_install_command = self.data['custom_install_command']
            self.run_command(custom_install_command)

            # check for post_install_commands
            self.run_command_list('postinstall_commands')

        elif self.action == 'custom_commands':
            self.run_command_list('commands')

        # clean up and change the directory back to root
        os.chdir(config.ROOT_PATH)
        # mark package as installed
        if self.action != 'meta':
            log.info('Marking {} as installed...'.format(self.name))
            self.run_command('touch {}/installed/{}'.format(config.DB_PATH, self.name))

    def run_command(self, cmd):
        return_code = os.system(cmd)
        if return_code != 0:
            log.error('Nonzero return from command: {}'.format(cmd))
            exit()

    def run_command_list(self, list_name):
        if list_name in self.data:
            for cmd in self.data[list_name]:
                log.info('Running {} command: \n\r{}'.format(list_name, cmd))
                self.run_command(cmd)
        else:
            log.info('No {} to run for {}'.format(list_name, self.name))

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
        if 'config_opts' in self.data:
            return self.data['config_opts']
        else:
            ''

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
