from setuptools import setup, find_packages

setup(name='CGTasks',
      version='1.1.6',
      author='Vsevolod Hermaniuk & artandfi (Artem Fisunenko)',
      url='https://github.com/OGKG/CGTasks',
      packages=find_packages(exclude=['CGTasks.tests']),
      install_requires = [
        'MarkLib',
        'CGLib'
      ],
      zip_safe=False)