import sys
from setuptools import setup


if sys.version_info >= (3,):
    dnspython = "dnspython3"
else:
    dnspython = "dnspython"

setup(
    name='zeke',
    version='0.2.1',
    author='Yodle',
    author_email='mdrago@yodle.com',
    url='https://git.yodle.com/projects/TOOL/repos/zeke/browse',
    description='Mess around with zookeeper',
    packages=['zeke'],
    entry_points={
        'console_scripts': [
            'zeke = zeke.zeke:main'
        ]
    },
    tests_require=['mock'],
    install_requires=['kazoo', dnspython],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ],
    long_description="""
**Zeke lets you mess around with zookeeper**
"""
)
