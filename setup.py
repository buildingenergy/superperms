"""
:copyright: (c) 2014 Building Energy Inc
:license: see LICENSE for details.
"""
from setuptools import setup, find_packages

setup(
    name='superperms',
    version='0.2.3',
    description='Flexible Permissions for Django.',
    long_description=open('README.md').read(),
    author='Gavin McQuillan',
    author_email='gavin.mcquillan@buildingenergy.com',
    url='http://github.com/buildingenergy/superperms',
    license='Apache2',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.md']},
    install_requires=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
