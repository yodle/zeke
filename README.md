# Zeke

Zeke is a simple command-line client for interacting with Zookeeper.

### Installation
```sh
$ sudo pip install git+https://git.yodle.com/scm/tool/zeke.git 
```

### Usage
#### Get the value of a node
```sh
$ zeke -g /com/yodle/conf/tech/metrics/graphite-host
dev-graphite.nyc.dev.yodle.com
```

#### Set the value of a node
```sh
$ zeke -s /path/to/node "node value"
```

#### Dump a tree of zookeeper out to a file
```sh
$ zeke -d /path/to/dump > dumpfile.zk
```

#### Load a file with node/value pairs in to zookeeper
```sh
$ zeke -l < dumpfile.zk
```

#### Discover Zookeeper via DNS
The commands get, set, dump, and load default to using the zookeeper they discover via DNS.  By using --discover you can get the location of the discovered zookeeper nodes.
```sh
$ zeke --discover
dev-zk1.dev.yodle.com:2181
dev-zk3.dev.yodle.com:2181
dev-zk2.dev.yodle.com:2181
```

#### Specify the location of zookeeper
It is possible to override the DNS discovery mechanism by specifying the location of zookeeper with -a.  This can be added to get, set, dump, and load.
```sh
$ zeke -a localhost:2181 -d /com/yodle/conf/tech > dumpfile.zk
```

### Why?
Zeke was written to replace our old script zkconfig.py.  Zeke is an improvement over zkconfig in the following ways:
- Zeke has a sane command-line UI, zkconfig's interface was crazy
- Zeke works with python2 and python3, zkconfig only worked with python2
- Zeke works on Mac OSX, zkconfig did not (at the very least it was difficult to get installed properly)
- Zeke uses the kazoo python library for zookeeper, zkconfig used python-zookeeper which has been end-of-lifed
- Zeke installs like a proper python package, zkconfig was a single-file script that had to be copied around
- Zeke writes and reads json, zkconfig wrote stringified python lists and parsed them using eval
- Zeke has unit tests, zkconfig did not

