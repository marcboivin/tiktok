from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='tiktok',
      version=version,
      description="TikTak CLI",
      long_description="""\
Program for accessing TikTak through the command-line""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gregory Eric Sanderson',
      author_email='gzou2000@gmail.com',
      url='http://github.com/gelendir/tiktok',
      license='GPL3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data = {
        'tiktok' : ['config/defaults.cfg'],
      },
      zip_safe=True,
      install_requires=[
          'restkit>=3.2.1'
      ],
      entry_points={
          'console_scripts': [
              'tiktok = tiktok.cli:main',
          ]
      }
      )
