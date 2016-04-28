"""
setup module for 2016_awpug_pypiserver
"""

from setuptools import setup, find_packages


long_description = ("A project used to show the potential for packaging and "
                    "distributing one's own packages via pypiserver.")

setup(
    name='awpug_sample_package',
    version='1.0.0',
    description='AWPUG Demonstration Package',
    long_description=long_description,
    url='https://www.github.com/mplanchard/2016_awpug_pypiserver',
    author='Matthew Planchard',
    author_email='msplanchard@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
    keywords='awpug sample package test_code',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts':
            ['awpug = awpug_sample_package:greet_awpug']
    }
)
