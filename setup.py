from setuptools import setup

setup(
    name='scooper',
    version='0.0.1',
    author='Yodle',
    author_email='noreply@yodle.com',
    url='http://git.yodle.com/markdrago/scooper',
    description='Get values out of zookeeper',
    packages=['scooper'],
    entry_points={
        'console_scripts': [
            'scooper = scooper.scooper:main'
        ]
    },
    install_requires=['kazoo', 'dnspython'],
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
**Scooper gets values out of zookeeper.**
"""
)
