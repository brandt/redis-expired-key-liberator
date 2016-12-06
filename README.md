# redis-expired-key-liberator

A simple script that reads through a given RDB file and performs a GET on every expired key it finds.  This prompts Redis to garbage collect that item.

This was built as a workaround for a situation where the [Redis lazy garbage collection algorithm][] was not freeing memory fast enough.


## Requirements

Install dependencies with:

     pip install rdbtools
     pip install redis

It expects the standard Redis unix domain socket to be available to perform the GET requests.


## Supported Types

Currently, not all types are supported.  That's mainly because my use case didn't require anything more than the basics.  Support for other types can probably be added without too much difficulty.


## Author

- J. Brandt Buckley <brandt@runlevel1.com> 


[Redis lazy garbage collection algorithm]: https://redis.io/commands/expire#how-redis-expires-keys
