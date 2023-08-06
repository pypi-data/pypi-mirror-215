from setuptools import setup, find_packages

setup(
    name='datascrub',
    version='1.0.1',
    author=['Samuel Shine', 'Alex Benjamin'],
    author_email='samuelshine112003@gmail.com',
    description='A Python package for cleaning and preprocessing data in pandas DataFrames',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/samuelshine/cleanmydata',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'pandas',
        'numpy',
        'charset_normalizer',
        'fuzzywuzzy',
        'scipy',
        'emoji',
        'googletrans',
    ],
)
