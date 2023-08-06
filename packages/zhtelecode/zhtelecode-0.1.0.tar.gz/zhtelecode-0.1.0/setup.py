#!/usr/bin/env python

from setuptools import setup

import zhtelecode

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(name='zhtelecode',
      version=zhtelecode.__version__,
      description='Convert between Chinese Telegraph Codes and Unicode Chinese characters.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=zhtelecode.__author__,
      url='https://github.com/charlessimpson/zhtelecode/',
      py_modules=['zhtelecode'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      license='MIT License',
      platforms=['any'],
      python_requires='>=3.6',
      )
