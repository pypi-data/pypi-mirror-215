#!/usr/bin/env python
from setuptools import setup

with open('README.md', 'r') as fh:
    long_desc = fh.read()

setup(name='as-mongodb',
      version='1.4.1',
      description='Singer.io tap for extracting data from MongoDB - Datazip compatible',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author='Wise',
      url='https://github.com/datazip/as-mongodb',
      classifiers=[
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      py_modules=['as_mongodb'],
      install_requires=[
          'pipelinewise-singer-python==1.*',
          'pymongo==4.3.*',
          'tzlocal==2.1.*',
          'terminaltables==3.1.*',
          'dnspython==2.1.*',
      ],
      extras_require={
          'dev': [
              'pylint==2.12',
              'ipdb==0.13.*'
          ],
          'test': [
              'pytest==6.2.5',
              'pytest-cov==3.0.0'
          ]
      },
      entry_points='''
          [console_scripts]
          as-mongodb=as_mongodb:main
      ''',
      packages=['as_mongodb', 'as_mongodb.sync_strategies'],
)
