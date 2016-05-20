# Zeke

Zeke is a command-line tool for Zookeeper that is a pleasure to use.

### Installation
```sh
$ sudo pip install zeke
```

### Usage
#### Get the value of a node
```sh
$ zeke -g /path/to/node
node value
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

#### Delete a node from zookeeper (only works on nodes without children)
```sh
$ zeke --delete /path/to/delete
```

#### Purge a branch of zookeeper (recursively delete all nodes) [USE WITH CAUTION]
```sh
$ zeke --purge /path/to/purge
```

#### Discover Zookeeper via DNS
The commands get, set, dump, load, delete, and purge all default to using the zookeeper they discover via DNS.  Zeke looks for SRV records for `_zookeeper._tcp` and that DNS lookup will be combined with any DNS search paths that are defined on the system.  This makes it fairly easy to use this autodiscovery mechanism in separate environments.  By using --discover you can get the location of the discovered zookeeper nodes.

```sh
$ zeke --discover
zk1.prod.company.com:2181
zk2.prod.company.com:2181
zk3.prod.company.com:2181
```

#### Specify the location of zookeeper
It is possible to override the DNS discovery mechanism by specifying the location of zookeeper with -a.  This can be added to all other commands (get, set, dump, load, delete, purge).

```sh
$ zeke -a localhost:2181 -d /path/to/dump > dumpfile.zk
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
Why create zeke when zkCli.sh exists?

- Zeke is a joy to use on the command-line and in scripts where zkCli.sh feels out of place and awkward
- Zeke supports dumping and loading full trees of zookeeper
- Zeke supports autodiscovery of zookeeper nodes via DNS


Zeke was originally written to replace one of our old scripts called zkconfig.py.  Zeke is an improvement over zkconfig in the following ways:

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
graphite_host=`/opt/zkconfig/zkconfig.py -g /dev/null -d -p /com/company/conf/tech/metrics/graphite-host 2> /dev/null | grep graphite-host | grep -v -e server-specific -e '#' | sed -e "s/.*graphite-host', '//" -e "s/'.*//"`
```
