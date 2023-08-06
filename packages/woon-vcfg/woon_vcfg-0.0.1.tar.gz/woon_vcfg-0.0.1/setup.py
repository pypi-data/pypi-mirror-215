from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='woon_vcfg',
  version='0.0.1',
  author='MrWoon',
  author_email='vladpika51@gmail.com',
  description='Module for .vfg configs type',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://woonworld.fun',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='vcfg vconfig config',
  project_urls={
    'Homepage': 'https://woonworld.fun',
    'Documentation': 'https://github.com/MrWoonWorldT1/vconfig/issues/1',
  },
  python_requires='>=3.7'
)