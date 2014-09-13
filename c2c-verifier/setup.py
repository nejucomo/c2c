#! /usr/bin/env python

import os, sys, subprocess
from setuptools import setup, find_packages, Command


PACKAGENAME = 'c2c-verifier'
INSTALL_REQUIRES = [
    'pyOpenSSL >= 0.14',
    'zbase32 >= 1.1.5',
    ]


def main(args = sys.argv[1:]):
    setup(
        name=PACKAGENAME,
        description='c2c verifier - Connect to Certificate verification callback for pyOpenSSL.',
        url='https://github.com/nejucomo/c2c',
        license='GPLv3',
        version='0.1.dev0',
        author='Nathan Wilcox',
        author_email='nejucomo@gmail.com',

        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,

        cmdclass={
            'test': TestWithCoverageAndTrialInAVirtualEnvCommand,
            },
        )


class VirtualEnvCommandBase (Command):
    """A base command class for setup subcommands to be run within a virtual env."""

    TestToolRequirements = [] # Subclasses should override this with tools they require.

    user_options = [
    ]

    def __init__(self, dist):
        Command.__init__(self, dist)
        join = os.path.join

        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.importname = PACKAGENAME.replace('-', '_')
        self.pymod = join(self.basedir, self.importname)
        self.testdir = join(self.basedir, 'build', 'test')
        self.venvdir = join(self.testdir, 'venv')

        self.bindir = os.path.join(self.venvdir, 'bin')
        self.trial = os.path.join(self.bindir, 'trial')
        self.pip = os.path.join(self.bindir, 'pip')
        self.coverage = os.path.join(self.bindir, 'coverage')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self._initialize_virtualenv()
        self._install_testing_tools()

        # Coverage and trial dump things into cwd, so cd:
        os.chdir(self.testdir)

        self.run_within_virtualenv()

    def _initialize_virtualenv(self):
        run('virtualenv', '--no-site-packages', self.venvdir)

    def _install_testing_tools(self):
        reqspath = os.path.join(self.testdir, 'test-tool-requirements.txt')

        with file(reqspath, 'w') as f:
            for req in INSTALL_REQUIRES + self.TestToolRequirements:
                f.write(req + '\n')

        run(self.pip, 'install', '--use-mirrors', '--requirement', reqspath)


class TestWithCoverageAndTrialInAVirtualEnvCommand (VirtualEnvCommandBase):
    """Run unit tests with coverage analysis and reporting in a virtualenv.

    Note: A design goal of this is that all generated files (except for
    .pyc files) will appear under ./build so that .gitignore can contain
    only ./build and *.pyc, and a clean operation is merely 'rm -r ./build'.
    """

    description = __doc__

    # Internal settings:
    TestToolRequirements = [
        'coverage == 3.7.1',
        'twisted >= 14.0',
        ]

    def run_within_virtualenv(self):
        self._update_python_path()
        try:
            run(self.coverage, 'run', '--branch', '--source', self.pymod, self.trial, self.importname)
        finally:
            run(self.coverage, 'html')

    def _update_python_path(self):
        if 'PYTHONPATH' in os.environ:
            os.environ['PYTHONPATH'] = '{0}:{1}'.format(self.basedir, os.environ['PYTHONPATH'])
        else:
            os.environ['PYTHONPATH'] = self.basedir


def run(*args):
    print 'Running: {0!r}'.format(args)
    try:
        subprocess.check_call(args, shell=False)
    except subprocess.CalledProcessError, e:
        print 'Process exited with {0!r} exit status.'.format(e.returncode)
        raise




if __name__ == '__main__':
    main()
