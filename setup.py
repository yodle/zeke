from setuptools import setup

setup(
    name='zeke',
    version='0.0.1',
    author='Yodle',
    author_email='noreply@yodle.com',
    url='http://git.yodle.com/markdrago/zeke',
    description='Mess around with zookeeper',
    packages=['zeke'],
    entry_points={
        'console_scripts': [
            'zeke = zeke.zeke:main'
        ]
    },
    tests_require=['mock'],
    install_requires=['kazoo'],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX',
        'Development Status :: 4 - `eta',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ],
    long_description="""
**Zeke lets you mess around with zookeeper**
"""
)
