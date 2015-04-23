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
$ cat dumpfile.zk
["/each/line/must/be/a/valid", "2-element"]
["/json/list/of/key/value/pairs", "thanks"]

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

#### Handling non-UTF-8 data
Zookeeper [requires that all keys be a subset of UTF-8](https://zookeeper.apache.org/doc/trunk/zookeeperProgrammers.html#ch_zkDataModel),
so Zeke does not handle non-UTF-8 keys either.  However, zookeeper values can be any arbitrary data.  Zeke uses UTF-8
when reading/writing data.  To be able to use UTF-8, Zeke will encode any non-UTF-8 data with base64.  To indicate that
a value is encoded with base64 zeke will prepend the output with "base64:".  For example, if zeke comes across a value
with a single byte of B7, which is invalid UTF-8, Zeke will output "base64:tw==".  Likewise, if Zeke is given a value
that begins with "base64:" it will strip off that label, decode the remainder of the string with base64, and use the
result when setting the value in zookeeper.


### Why?
Zeke was written to replace our old script zkconfig.py.  Zeke is an improvement over zkconfig in the following ways:

- Zeke has a sane command-line UI, zkconfig's interface was crazy
- Zeke works with python2 and python3, zkconfig only worked with python2
- Zeke works on Mac OSX, zkconfig did not (at the very least it was difficult to get installed properly)
- Zeke uses the kazoo python library for zookeeper, zkconfig used python-zookeeper which has been end-of-lifed
- Zeke installs like a proper python package, zkconfig was a single-file script that had to be copied around
- Zeke writes and reads json, zkconfig wrote stringified python lists and parsed them using eval
- Zeke has unit tests, zkconfig did not
- Zeke is obviously a better name than zkconfig

I started writing zeke after writing the following line to get a value out of zookeeper with zkconfig:

```sh
graphite_host=`/opt/zkconfig/zkconfig.py -g /dev/null -d -p /com/yodle/conf/tech/metrics/graphite-host 2> /dev/null | grep graphite-host | grep -v -e server-specific -e '#' | sed -e "s/.*graphite-host', '//" -e "s/'.*//"`
```

### Todo

- zkconfig had the ability to purge a branch from zookeeper, zeke lacks this support
- zkconfig had the ability to prepend a path to the node names while loading a file.  I'm not sure that we ever used this feature, but zeke doesn't have it.
- zkconfig logged all of its actions to a place in /natpal/logs.  I don't like the idea of hard-coding a log location like this, and I'm not sure that we have ever looked at the zkconfig logs anyway.
- zkconfig can load files that were created by zeke, but due to the strict quoting rules of json (only double-quotes are valid), zeke can not load files that were created by zkconfig
