from setuptools import setup


setup(
    name='zeke',
    version='0.2.2',
    author='Yodle',
    author_email='mdrago@yodle.com',
    url='https://github.com/yodle/zeke',
    description='A command-line tool for Zookeeper that is a pleasure to use',
    packages=['zeke'],
    entry_points={
        'console_scripts': [
            'zeke = zeke.zeke:main'
        ]
    },
    tests_require=['mock'],
    install_requires=['kazoo', 'dnspython'],
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
**Zeke is a command-line tool for Zookeeper that is a pleasure to use.**
"""
)
