from setuptools import setup

setup(
   name='chnangelog-generator',
   version='0.1.3',
   description='A module that generates changelogs with git. It uses conventional commits (https://www.conventionalcommits.org) and tags.',
   keywords='changelog conventional commit git',
   author='Lennart Suwe',
   author_email='lennsa999@gmx.de',
   packages=['chnangelog-generator'],
   install_requires=['bar', 'greek'], #external packages as dependencies
)
