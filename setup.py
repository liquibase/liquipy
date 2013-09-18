#!/usr/bin/python

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

with open('README-pypi.rst', 'r') as inp:
  sdict = {
    'long_description' : inp.read()
  }

execfile('liquipy/version.py', {}, sdict)

sdict.update({
  'name' : 'liquipy',
  'description' : 'Python client for CEPT API',
  'url': 'http://github.com/groksolutions/liquipy',
  'download_url' : 'https://pypi.python.org/packages/source/g/liquipy/liquipy-%s.tar.gz' % sdict['version'],
  'author' : 'Matthew Taylor',
  'author_email' : 'matt@groksolutions.com',
  'keywords' : ['sql', 'migrations', 'liquibase'],
  'license' : 'MIT',
  'install_requires': [
    'PyYAML',
    'nose'],
  'test_suite': 'tests.unit',
  'packages' : ['liquipy'],
  'data_files': [('externals', ['externals/liquibase.jar', 'externals/mysql-connector-java-5.1.17-bin.jar'])],
  'classifiers' : [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python']
})

setup(**sdict)