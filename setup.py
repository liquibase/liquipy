#!/usr/bin/python

try:
  from setuptools import setup, Command
except ImportError:
  from distutils.core import setup, Command

class PyTest(Command):
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    import subprocess
    errno = subprocess.call(['py.test'])
    raise SystemExit(errno)

sdict = {}

execfile('liquipy/version.py', {}, sdict)

sdict.update({
  'name' : 'liquipy',
  'description' :
    'a Python wrapper for Liquibase (see http://www.liquibase.org/)',
  'url': 'http://github.com/groksolutions/liquipy',
  'download_url' :
    'https://pypi.python.org/packages/source/g/liquipy/liquipy-%s.tar.gz' % (
      sdict['version'],),
  'author' : 'Matthew Taylor',
  'author_email' : 'matt@groksolutions.com',
  'keywords' : ['sql', 'migrations', 'liquibase'],
  'license' : 'Apache',
  'install_requires': [
    'mock',
    'PyYAML',
    'pytest',
    'unittest2'],
  'test_suite': 'tests.unit',
  'packages' : ['liquipy'],
  'package_data':
    {'liquipy' : ['externals/liquibase.jar',
                  'externals/mysql-connector-java-5.1.17-bin.jar']},
  'classifiers' : [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python'],
  'zip_safe' : False,
  'cmdclass' : {'test': PyTest},
})

setup(**sdict)
