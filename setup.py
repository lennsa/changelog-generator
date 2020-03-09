from setuptools import setup

setup(
   name='changelog-generator',
   version='0.1.6',
   description='A module that generates changelogs with git. It uses conventional commits (https://www.conventionalcommits.org) and tags.',
   keywords='changelog conventional commit git',
   author='Lennart Suwe',
   author_email='lennsa999@gmx.de',
   packages=['changelog'],
   install_requires=[
     "Click==7.0",
     "GitPython==3.1.0",
     "requests==2.22.0",
   ],
   entry_points={"console_scripts": ["pychangelog = changelog.changelog_generator:generator"]}
)
