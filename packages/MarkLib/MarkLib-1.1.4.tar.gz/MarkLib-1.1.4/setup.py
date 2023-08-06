from setuptools import setup, find_packages

setup(name='MarkLib',
      version='1.1.4',
      description='',
      url='https://github.com/OGKG/PyMarkLib',
      author='Vsevolod Hermaniuk & artandfi (Artem Fisunenko)',
      license='MIT',
    #   packages=['MarkLib'],
      install_requires=[
          'pydantic',
      ],
      packages=find_packages(),
      zip_safe=False)