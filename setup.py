from setuptools import setup

setup(
   name='chnangelog-generator',
   version='0.1.3',
   description='A module that generates changelogs with git. It uses conventional commits (https://www.conventionalcommits.org) and tags.',
   keywords='changelog conventional commit git',
   author='Lennart Suwe',
   author_email='lennsa999@gmx.de',
   packages=['changelog'],
   install_requires=[
     "Click==7.0",
     "GitPython==3.0.3",
     "requests==2.22.0",
   ],
   entry_points={"console_scripts": ["changelog = changelog.__main__:generator"]}
)
