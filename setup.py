#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
        'yaml',
        'nose'],
    'test_suite': 'tests.unit',
    'packages' : ['liquipy'],
    'classifiers' : [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
})

setup(**sdict)